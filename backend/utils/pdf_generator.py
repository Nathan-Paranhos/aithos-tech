from typing import Dict, Any, List, Optional, Union
import os
import tempfile
from datetime import datetime
from fastapi import HTTPException, status
import jinja2
import pdfkit
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import base64
import io

# Configurar matplotlib para não usar interface gráfica
matplotlib.use('Agg')

# Configurar Jinja2 para carregar templates
template_loader = jinja2.FileSystemLoader(searchpath="./templates")
template_env = jinja2.Environment(loader=template_loader)

class PDFGenerator:
    """Classe para gerar arquivos PDF a partir de templates e dados"""
    
    @staticmethod
    def _figure_to_base64(fig):
        """Converte uma figura matplotlib para base64"""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close(fig)
        return img_str
    
    @staticmethod
    def generate_line_chart(data: List[Dict[str, Any]], x_key: str, y_key: str, title: str, 
                           x_label: str, y_label: str) -> str:
        """Gera um gráfico de linha e retorna como base64"""
        try:
            # Extrair dados
            x_values = [item[x_key] for item in data]
            y_values = [item[y_key] for item in data]
            
            # Criar figura
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x_values, y_values, marker='o', linestyle='-', color='#0074D9')
            
            # Configurar gráfico
            ax.set_title(title, fontsize=16)
            ax.set_xlabel(x_label, fontsize=12)
            ax.set_ylabel(y_label, fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Converter para base64
            return PDFGenerator._figure_to_base64(fig)
        except Exception as e:
            print(f"Erro ao gerar gráfico de linha: {str(e)}")
            return ""
    
    @staticmethod
    def generate_bar_chart(data: List[Dict[str, Any]], x_key: str, y_key: str, title: str, 
                          x_label: str, y_label: str) -> str:
        """Gera um gráfico de barras e retorna como base64"""
        try:
            # Extrair dados
            x_values = [item[x_key] for item in data]
            y_values = [item[y_key] for item in data]
            
            # Criar figura
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(x_values, y_values, color='#0074D9')
            
            # Adicionar valores acima das barras
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{height:.1f}', ha='center', va='bottom')
            
            # Configurar gráfico
            ax.set_title(title, fontsize=16)
            ax.set_xlabel(x_label, fontsize=12)
            ax.set_ylabel(y_label, fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.7, axis='y')
            
            # Converter para base64
            return PDFGenerator._figure_to_base64(fig)
        except Exception as e:
            print(f"Erro ao gerar gráfico de barras: {str(e)}")
            return ""
    
    @staticmethod
    def generate_pie_chart(data: List[Dict[str, Any]], label_key: str, value_key: str, 
                          title: str) -> str:
        """Gera um gráfico de pizza e retorna como base64"""
        try:
            # Extrair dados
            labels = [item[label_key] for item in data]
            values = [item[value_key] for item in data]
            
            # Criar figura
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, 
                   shadow=True, explode=[0.05] * len(labels),
                   colors=plt.cm.Paired(np.linspace(0, 1, len(labels))))
            
            # Configurar gráfico
            ax.set_title(title, fontsize=16)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            
            # Converter para base64
            return PDFGenerator._figure_to_base64(fig)
        except Exception as e:
            print(f"Erro ao gerar gráfico de pizza: {str(e)}")
            return ""
    
    @staticmethod
    async def generate_report_pdf(template_name: str, data: Dict[str, Any]) -> bytes:
        """Gera um PDF de relatório a partir de um template e dados"""
        try:
            # Carregar template
            template = template_env.get_template(f"{template_name}.html")
            
            # Adicionar data atual aos dados
            data['generated_at'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            # Renderizar HTML
            html_content = template.render(**data)
            
            # Configurar opções do pdfkit
            options = {
                'page-size': 'A4',
                'margin-top': '1.0cm',
                'margin-right': '1.0cm',
                'margin-bottom': '1.0cm',
                'margin-left': '1.0cm',
                'encoding': "UTF-8",
                'no-outline': None,
                'enable-local-file-access': None
            }
            
            # Gerar PDF
            pdf_content = pdfkit.from_string(html_content, False, options=options)
            
            return pdf_content
        except Exception as e:
            print(f"Erro ao gerar PDF: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao gerar PDF: {str(e)}"
            )
    
    @staticmethod
    async def generate_equipment_report(equipment_data: Dict[str, Any], 
                                      operational_data: List[Dict[str, Any]],
                                      maintenance_history: List[Dict[str, Any]],
                                      alerts: List[Dict[str, Any]]) -> bytes:
        """Gera um relatório PDF específico para equipamentos"""
        try:
            # Preparar dados para gráficos
            if operational_data:
                # Ordenar dados por data
                operational_data.sort(key=lambda x: x.get('timestamp', 0))
                
                # Gerar gráficos de desempenho
                performance_chart = PDFGenerator.generate_line_chart(
                    operational_data, 'timestamp_formatted', 'performance', 
                    'Desempenho ao Longo do Tempo', 'Data', 'Desempenho (%)')
                
                temperature_chart = PDFGenerator.generate_line_chart(
                    operational_data, 'timestamp_formatted', 'temperature', 
                    'Temperatura ao Longo do Tempo', 'Data', 'Temperatura (°C)')
                
                vibration_chart = PDFGenerator.generate_line_chart(
                    operational_data, 'timestamp_formatted', 'vibration', 
                    'Vibração ao Longo do Tempo', 'Data', 'Vibração (mm/s)')
            else:
                performance_chart = ""
                temperature_chart = ""
                vibration_chart = ""
            
            # Preparar dados para gráfico de manutenção
            if maintenance_history:
                maintenance_types = {}
                for maintenance in maintenance_history:
                    mtype = maintenance.get('maintenance_type', 'Não especificado')
                    maintenance_types[mtype] = maintenance_types.get(mtype, 0) + 1
                
                maintenance_data = [{'type': k, 'count': v} for k, v in maintenance_types.items()]
                maintenance_chart = PDFGenerator.generate_pie_chart(
                    maintenance_data, 'type', 'count', 'Distribuição de Tipos de Manutenção')
            else:
                maintenance_chart = ""
            
            # Preparar dados para gráfico de alertas
            if alerts:
                alert_severities = {}
                for alert in alerts:
                    severity = alert.get('severity', 'Não especificado')
                    alert_severities[severity] = alert_severities.get(severity, 0) + 1
                
                alert_data = [{'severity': k, 'count': v} for k, v in alert_severities.items()]
                alert_chart = PDFGenerator.generate_pie_chart(
                    alert_data, 'severity', 'count', 'Distribuição de Severidade de Alertas')
            else:
                alert_chart = ""
            
            # Compilar todos os dados
            report_data = {
                'equipment': equipment_data,
                'operational_data': operational_data,
                'maintenance_history': maintenance_history,
                'alerts': alerts,
                'charts': {
                    'performance': performance_chart,
                    'temperature': temperature_chart,
                    'vibration': vibration_chart,
                    'maintenance': maintenance_chart,
                    'alerts': alert_chart
                }
            }
            
            # Gerar PDF
            return await PDFGenerator.generate_report_pdf('equipment_report', report_data)
        except Exception as e:
            print(f"Erro ao gerar relatório de equipamento: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao gerar relatório de equipamento: {str(e)}"
            )

# Exportar instância para uso em outros módulos
pdf_generator = PDFGenerator()