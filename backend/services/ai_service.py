from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import json
import numpy as np
import pandas as pd
import joblib
import os
import requests
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from lightgbm import LGBMRegressor, LGBMClassifier
from datetime import datetime, timedelta
from math import exp, log
from scipy.stats import weibull_min

from fastapi import HTTPException, status

from config import db


OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:8b")


# Definir um modelo de falha padrão para uso quando não houver dados suficientes
class DefaultFailureModel:
    def predict_proba(self, X):
        # Retorna uma probabilidade de 50% para não falha e 50% para falha
        return np.array([[0.5, 0.5]])

    def predict(self, X):
        # Retorna 0 (não falha) por padrão
        return np.array([0])



class AIService:
    # Diretório para armazenar modelos treinados
    MODELS_DIR = "./models/ai"

    @staticmethod
    async def _call_ollama_model(prompt: str) -> str:
        try:
            headers = {'Content-Type': 'application/json'}
            data = {
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(OLLAMA_API_URL, headers=headers, json=data)
            response.raise_for_status()  # Levanta um erro para status de resposta ruins (4xx ou 5xx)
            return response.json().get("response", "")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao chamar o modelo Ollama: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro de comunicação com o modelo de IA: {e}"
            )


    @staticmethod
    def _calculate_mtbf(failure_history: List[Dict[str, Any]], total_operational_time: float) -> float:
        """Calcula o Mean Time Between Failures (MTBF) em horas."""
        num_failures = len(failure_history)
        if num_failures == 0:
            return total_operational_time  # Se não houve falhas, MTBF é o tempo total de operação
        # MTBF = Tempo total de operação / Número de falhas
        return total_operational_time / num_failures

    @staticmethod
    def _calculate_failure_rate(mtbf: float) -> float:
        """Calcula a taxa de falha (lambda) a partir do MTBF."""
        if mtbf == 0:
            return float('inf')  # Taxa de falha infinita se MTBF for zero
        return 1 / mtbf

    @staticmethod
    def _weibull_probability(time: float, alpha: float, beta: float) -> float:
        """Calcula a probabilidade de falha usando a distribuição de Weibull."""
        if time < 0 or alpha <= 0 or beta <= 0:
            return 0.0
        return 1 - exp(-((time / alpha) ** beta))

    @staticmethod
    def _fit_weibull_parameters(failure_times: List[float]) -> Tuple[float, float]:
        """Estima os parâmetros alpha (escala) e beta (forma) da distribuição de Weibull.
        Requer pelo menos 2 pontos de falha para um ajuste razoável.
        """
        if len(failure_times) < 2:
            # Retorna valores padrão ou levanta um erro se não houver dados suficientes
            return 1000.0, 2.0  # Exemplo: alpha=1000h, beta=2 (desgaste)
        try:
            # Ajusta os parâmetros da distribuição de Weibull aos dados de tempo de falha
            # loc=0 é assumido para a distribuição de Weibull de 2 parâmetros
            shape, loc, scale = weibull_min.fit(failure_times, floc=0)
            return scale, shape
        except Exception as e:
            print(f"Erro ao ajustar Weibull: {e}")
            return 1000.0, 2.0

    @staticmethod
    def _calculate_risk_score(failure_probability: float, component_risk: List[Dict[str, Any]]) -> float:
        """Calcula um score de risco ponderado.
        Pode ser expandido para incluir outros fatores como criticidade do equipamento, custo de inatividade, etc.
        """
        base_risk = failure_probability * 100  # Converter para escala de 0-100
        component_risk_score = 0
        for comp in component_risk:
            if comp['risk_level'] == 'high':
                component_risk_score += 30
            elif comp['risk_level'] == 'medium':
                component_risk_score += 15
        
        # Exemplo de ponderação: 70% da probabilidade de falha, 30% do risco dos componentes
        total_risk_score = (base_risk * 0.7) + (min(component_risk_score, 100) * 0.3)
        return min(total_risk_score, 100.0)

    @staticmethod
    async def predict_equipment_failure(equipment_id: str, days_ahead: int = 30) -> Dict[str, Any]:
        """Prevê a probabilidade de falha de um equipamento nos próximos X dias"""
        try:
            equipment_doc = db.collection("equipment").document(equipment_id).get()
            if not equipment_doc.exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Equipamento não encontrado"
                )
            equipment_data = equipment_doc.to_dict()
            operational_data = equipment_data.get("operational_data", [])
            failure_history = equipment_data.get("failure_history", [])
            total_usage_hours = equipment_data.get("total_usage_hours", 0.0)

            # Calcular MTBF e Taxa de Falha
            mtbf = AIService._calculate_mtbf(failure_history, total_usage_hours)
            failure_rate = AIService._calculate_failure_rate(mtbf)

            # Preparar dados para previsão do modelo de ML
            if len(operational_data) < 5:
                # Dados insuficientes para previsão de ML, usar valores padrão ou baseados em MTBF
                failure_probability_ml = 0.5 # Valor padrão
                predicted_days_to_failure_ml = days_ahead
            else:
                features, _ = AIService._prepare_data(operational_data)
                model_path = os.path.join(AIService.MODELS_DIR, f"failure_model_{equipment_data.get('category', 'general')}.joblib")
                if os.path.exists(model_path):
                    model = joblib.load(model_path)
                else:
                    model = DefaultFailureModel() # Usar modelo padrão
                failure_probability_ml = model.predict_proba(features)[-1, 1] if hasattr(model, 'predict_proba') else 0.5
                predicted_days_to_failure_ml = max(1, int(days_ahead * (1 - failure_probability_ml)))

            # Calcular probabilidade de falha com Weibull
            weibull_prob = 0.0
            if len(failure_history) >= 2:
                # Extrair tempos de falha (assumindo que 'time_at_failure' é em horas de uso)
                failure_times = [f['time_at_failure'] for f in failure_history if 'time_at_failure' in f]
                if failure_times:
                    alpha, beta = AIService._fit_weibull_parameters(failure_times)
                    # Prever probabilidade de falha para o tempo atual + dias_ahead
                    # Convertendo dias_ahead para horas (assumindo 24h/dia de operação para simplificar)
                    future_time_hours = total_usage_hours + (days_ahead * 24)
                    weibull_prob = AIService._weibull_probability(future_time_hours, alpha, beta)

            # Combinar probabilidades (exemplo simples: média)
            # Pode ser mais sofisticado, como ponderar com base na confiança do modelo de ML
            combined_failure_probability = (failure_probability_ml + weibull_prob) / 2.0
            
            # Analisar componentes em risco
            components_at_risk = []
            for component in equipment_data.get("components", []):
                component_name = component.get("name", "Componente desconhecido")
                health = component.get("health_percentage", 100)
                current_usage = component.get("current_usage_hours", 0)
                estimated_lifetime = component.get("estimated_lifetime_hours", 10000)
                
                remaining_percentage = (estimated_lifetime - current_usage) / estimated_lifetime * 100
                if remaining_percentage < 30 or health < 50:
                    components_at_risk.append({
                        "name": component_name,
                        "health": health,
                        "remaining_life_percentage": remaining_percentage,
                        "risk_level": "high" if remaining_percentage < 15 or health < 30 else "medium"
                    })
            
            # Calcular Score de Risco
            risk_score = AIService._calculate_risk_score(combined_failure_probability, components_at_risk)

            # Estimar dias até falha (pode ser refinado com base na distribuição de Weibull)
            # Por simplicidade, ainda usando a previsão do ML ou uma média
            predicted_days_to_failure = max(1, int(days_ahead * (1 - combined_failure_probability)))

            # Gerar recomendação de ação e dias de falha com Ollama
            ollama_prompt = f"Baseado na probabilidade de falha de {combined_failure_probability:.2f} para o equipamento {equipment_data.get('name', 'desconhecido')} (ID: {equipment_id}), com MTBF de {mtbf:.2f} horas, taxa de falha de {failure_rate:.4f} e componentes em risco: {components_at_risk}, qual a previsão de dias para falha e qual a ação recomendada? Responda em formato JSON com 'predicted_failure_days' (inteiro) e 'recommended_action' (string)."
            ollama_response_text = await AIService._call_ollama_model(ollama_prompt)
            
            try:
                ollama_response = json.loads(ollama_response_text)
                predicted_failure_days_ai = ollama_response.get("predicted_failure_days", predicted_days_to_failure)
                recommended_action_ai = ollama_response.get("recommended_action", "Nenhuma ação específica recomendada pela IA.")
            except json.JSONDecodeError:
                print(f"Erro ao decodificar JSON do Ollama: {ollama_response_text}")
                predicted_failure_days_ai = predicted_days_to_failure
                recommended_action_ai = "Não foi possível obter recomendação detalhada da IA." # Fallback

            return {
                "failure_probability": combined_failure_probability,
                "confidence": 0.7,  # Pode ser ajustado com base na qualidade dos dados/modelo
                "predicted_days_to_failure": predicted_failure_days_ai,
                "recommended_action": recommended_action_ai,
                "components_at_risk": components_at_risk,
                "mtbf": mtbf,
                "failure_rate": failure_rate,
                "weibull_probability": weibull_prob,
                "risk_score": risk_score
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao prever falha do equipamento: {str(e)}"
            )
    
    @staticmethod
    async def recommend_maintenance_schedule(equipment_id: str) -> Dict[str, Any]:
        """Recomenda um cronograma de manutenção para o equipamento"""
        try:
            equipment_doc = db.collection("equipment").document(equipment_id).get()
            if not equipment_doc.exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Equipamento não encontrado"
                )
            equipment_data = equipment_doc.to_dict()
            
            maintenance_docs = db.collection("maintenance").where("equipment_id", "==", equipment_id).where("status", "==", "completed").stream()
            maintenance_history = []
            for doc in maintenance_docs:
                maintenance_data = doc.to_dict()
                maintenance_history.append(maintenance_data)
            
            if len(maintenance_history) >= 2:
                maintenance_history.sort(key=lambda x: x.get("completed_date", datetime.min))
                intervals = []
                for i in range(1, len(maintenance_history)):
                    prev_date = maintenance_history[i-1].get("completed_date")
                    curr_date = maintenance_history[i].get("completed_date")
                    if prev_date and curr_date:
                        delta = (curr_date - prev_date).days
                        intervals.append(delta)
                
                avg_interval = sum(intervals) / len(intervals) if intervals else 90
                
                if equipment_data.get("risk_level") == "high":
                    recommended_interval = max(7, avg_interval * 0.5)
                elif equipment_data.get("risk_level") == "medium":
                    recommended_interval = max(14, avg_interval * 0.7)
                else:
                    recommended_interval = avg_interval
            else:
                if equipment_data.get("risk_level") == "high":
                    recommended_interval = 30
                elif equipment_data.get("risk_level") == "medium":
                    recommended_interval = 60
                else:
                    recommended_interval = 90
            
            last_maintenance = equipment_data.get("last_maintenance_date")
            if last_maintenance:
                next_date = last_maintenance + timedelta(days=int(recommended_interval))
            else:
                next_date = datetime.utcnow() + timedelta(days=int(recommended_interval))
            
            recommendations = []
            if equipment_data.get("risk_level") == "high":
                recommendations.append("Realizar manutenção preventiva completa")
                recommendations.append("Verificar componentes críticos com prioridade")
            elif equipment_data.get("risk_level") == "medium":
                recommendations.append("Realizar inspeção detalhada")
                recommendations.append("Monitorar parâmetros operacionais com maior frequência")
            else:
                recommendations.append("Seguir cronograma de manutenção regular")
            
            for component in equipment_data.get("components", []):
                if component.get("health_percentage", 100) < 50:
                    recommendations.append(f"Substituir {component.get('name', 'componente')}")
                elif component.get("health_percentage", 100) < 70:
                    recommendations.append(f"Inspecionar {component.get('name', 'componente')}")
            
            return {
                "recommended_interval_days": int(recommended_interval),
                "next_maintenance_date": next_date,
                "maintenance_type": "preventive" if equipment_data.get("risk_level") != "high" else "corrective",
                "recommendations": recommendations,
                "priority": "high" if equipment_data.get("risk_level") == "high" else "medium" if equipment_data.get("risk_level") == "medium" else "low"
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao recomendar cronograma de manutenção: {str(e)}"
            )

    @staticmethod
    def _prepare_data(operational_data: List[Dict[str, Any]]) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepara os dados operacionais para o modelo de ML."""
        df = pd.DataFrame(operational_data)
        # Exemplo: converter timestamp para datetime e extrair features de tempo
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.dayofweek
        
        # Exemplo: selecionar features e target
        # Supondo que 'temperature', 'vibration', 'pressure' são features e 'failure_imminent' é o target
        features = df[['temperature', 'vibration', 'pressure']] # Adicione mais features conforme necessário
        target = pd.Series([0] * len(df)) # Target dummy, pois o modelo é para previsão de falha, não classificação direta aqui
        
        return features, target

    @staticmethod
    def _get_default_model():
        """Retorna um modelo padrão para previsão de falhas quando não há modelo treinado."""
        # Um modelo simples que sempre prevê uma probabilidade média
        class DefaultModel:
            def predict_proba(self, X):
                return np.array([[0.5, 0.5]]) # 50% de chance de falha
        return DefaultModel()


class DefaultFailureModel:
    """Um modelo de falha padrão para quando não há dados suficientes para treinar um modelo real."""
    def predict_proba(self, X):
        # Retorna uma probabilidade de 50% para 'não falha' e 50% para 'falha'
        return np.array([[0.5, 0.5]])

    def predict(self, X):
        # Retorna 0 (não falha) ou 1 (falha) com base na probabilidade
        return np.array([1 if self.predict_proba(X)[0, 1] > 0.5 else 0])

    @staticmethod
    async def analyze_operational_data(equipment_id: str) -> Dict[str, Any]:
        """Analisa dados operacionais para identificar padrões e anomalias"""
        try:
            equipment_doc = db.collection("equipment").document(equipment_id).get()
            if not equipment_doc.exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Equipamento não encontrado"
                )
            equipment_data = equipment_doc.to_dict()
            operational_data = equipment_data.get("operational_data", [])

            if not operational_data:
                return {
                    "message": "Nenhum dado operacional disponível para análise."
                }

            df = pd.DataFrame(operational_data)

            # Converter timestamp para datetime e definir como índice
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = df.set_index('timestamp')
                df = df.sort_index()

            analysis_results = {}

            # Análise Descritiva
            analysis_results['descriptive_statistics'] = df.describe().to_dict()

            # Detecção de Anomalias (Exemplo simples: IQR)
            anomalies = {}
            for column in ['temperature', 'vibration', 'pressure']:
                if column in df.columns:
                    Q1 = df[column].quantile(0.25)
                    Q3 = df[column].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    anomalous_data = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
                    if not anomalous_data.empty:
                        anomalies[column] = anomalous_data.to_dict(orient='records')
            analysis_results['anomalies'] = anomalies

            # Análise de Tendências (Exemplo: média móvel)
            trends = {}
            for column in ['temperature', 'vibration', 'pressure']:
                if column in df.columns:
                    trends[column] = df[column].rolling(window=5).mean().dropna().to_dict()
            analysis_results['trends'] = trends

            # Correlação de Pearson
            correlation_matrix = {}
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            if len(numeric_cols) > 1:
                correlation_matrix = df[numeric_cols].corr(method='pearson').to_dict()
            analysis_results['correlation_matrix'] = correlation_matrix

            return analysis_results

        except HTTPException:
            raise
        except Exception as e:


            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao analisar dados operacionais: {str(e)}"
            )
    
    @staticmethod
    async def train_custom_model(equipment_id: str, user_id: str) -> Dict[str, Any]:
        """Treina um modelo personalizado para um equipamento específico"""
        try:
            # Buscar dados do equipamento
            equipment_doc = db.collection("equipment").document(equipment_id).get()
            
            if not equipment_doc.exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Equipamento não encontrado"
                )
            
            equipment_data = equipment_doc.to_dict()
            
            # Verificar se o equipamento pertence ao usuário
            if equipment_data["user_id"] != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Acesso não autorizado a este equipamento"
                )
            
            operational_data = equipment_data.get("operational_data", [])
            
            # Verificar se há dados suficientes para treinamento
            if len(operational_data) < 10:
                return {
                    "success": False,
                    "message": "Dados insuficientes para treinamento do modelo. São necessários pelo menos 10 registros.",
                    "model_type": None,
                    "accuracy": None
                }
            
            # Preparar dados para treinamento
            features, target = AIService._prepare_data(operational_data, for_training=True)
            
            # Treinar modelo
            model = LGBMClassifier(n_estimators=100, random_state=42)
            model.fit(features, target)
            
            # Avaliar modelo (simplificado)
            accuracy = model.score(features, target)
            
            # Criar diretório para modelos se não existir
            os.makedirs(AIService.MODELS_DIR, exist_ok=True)
            
            # Salvar modelo
            category = equipment_data.get("category", "general")
            model_path = os.path.join(AIService.MODELS_DIR, f"failure_model_{category}_{equipment_id}.joblib")
            joblib.dump(model, model_path)
            
            return {
                "success": True,
                "message": "Modelo treinado com sucesso",
                "model_type": "LightGBM Classifier",
                "accuracy": accuracy
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao treinar modelo personalizado: {str(e)}"
            )
    
    @staticmethod
    def _prepare_data(operational_data: List[Dict[str, Any]], for_training: bool = False) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """Prepara dados operacionais para análise ou treinamento"""
        # Extrair features relevantes
        features_list = []
        for data in operational_data:
            features = [
                data.get("hours_used", 0),
                data.get("temperature", 0) or 0,
                data.get("vibration", 0) or 0,
                data.get("noise_level", 0) or 0,
                data.get("cycles", 0) or 0
            ]
            features_list.append(features)
        
        features_array = np.array(features_list)
        
        # Normalizar features
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features_array)
        
        # Para treinamento, criar target (simplificado)
        if for_training:
            # Simular target: 1 se temperatura > 80 ou vibração > 0.8, caso contrário 0
            target = np.array([
                1 if (data.get("temperature", 0) or 0) > 80 or (data.get("vibration", 0) or 0) > 0.8 else 0
                for data in operational_data
            ])
            return features_scaled, target
        
        return features_scaled, None
    
    @staticmethod
    def _get_default_model():
        """Retorna um modelo padrão pré-treinado"""
        # Criar modelo simples
        model = RandomForestClassifier(n_estimators=50, random_state=42)
        
        # Treinar com dados sintéticos simples
        X = np.random.rand(100, 5)
        y = np.random.randint(0, 2, 100)
        model.fit(X, y)
        
        return model
    
    @staticmethod
    def _analyze_trend(values: List[float]) -> str:
        """Analisa a tendência de uma série de valores"""
        if len(values) < 3:
            return "stable"
        
        # Calcular diferenças entre valores consecutivos
        diffs = [values[i] - values[i-1] for i in range(1, len(values))]
        
        # Contar diferenças positivas e negativas
        pos_count = sum(1 for d in diffs if d > 0)
        neg_count = sum(1 for d in diffs if d < 0)
        
        # Determinar tendência
        if pos_count > 0.7 * len(diffs):
            return "increasing"
        elif neg_count > 0.7 * len(diffs):
            return "decreasing"
        else:
            return "stable"