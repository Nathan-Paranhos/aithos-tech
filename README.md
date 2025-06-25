# AgroGuard - Plataforma de Manutenção Preditiva

AgroGuard é uma plataforma web inteligente para manutenção preditiva de equipamentos industriais, agrícolas e automotivos, desenvolvida pela Aithos Tech. A plataforma utiliza IA adaptativa para prever falhas em equipamentos, oferecendo dashboards personalizados por ativo e aprendendo continuamente com dados reais e fontes externas.

## Tecnologias Utilizadas

### Frontend
- React
- TailwindCSS
- Framer Motion

### Backend
- FastAPI
- Python (com foco em IA e APIs externas)
- Pydantic para validação de dados
- Firebase Admin SDK para autenticação e banco de dados
- Uvicorn como servidor ASGI

### Banco de Dados
- Firebase (Firestore e Storage)

### IA Preditiva
- Scikit-learn
- Pandas
- LightGBM
- Joblib

### Notificações
- WhatsApp (Twilio API)
- E-mail (EmailJS)

## Funcionalidades Principais

1. **Cadastro Inteligente de Equipamentos**
   - Consulta automática de fontes online confiáveis
   - Estimativa de tempo médio até falha (MTTF)
   - Ciclos de revisão recomendados

2. **Dashboard por Equipamento**
   - Status de risco (baixo/médio/alto)
   - Vida útil estimada de componentes
   - Gráficos de evolução de risco e uso
   - Histórico completo de falhas e manutenções

3. **Upload e Coleta de Dados Operacionais**
   - Formulários, CSV, Excel
   - Preparado para integração futura com sensores

4. **IA Aprendente e Adaptativa**
   - Random Forest + LightGBM + lógica de associação
   - Detecção de correlações ocultas entre falhas
   - Aprendizado com dados operacionais reais

5. **Relatórios Automatizados e Alertas Inteligentes**
   - Alertas por e-mail e WhatsApp
   - Relatórios em PDF

6. **Dashboard Administrativo**
   - Visão consolidada de todos os equipamentos
   - Filtros e gráficos de tendências

7. **Aprendizado Cruzado Entre Ativos**
   - Relação de falhas entre ativos semelhantes
   - Recalibração automática de estimativas

## Instalação e Configuração

### Instalação e Configuração

### Requisitos
- Node.js (v14+)
- Python (v3.8+)
- Firebase CLI
- Conta no Firebase

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

## Estrutura do Projeto

```
/
├── frontend/                # Aplicação React
│   ├── public/              # Arquivos públicos
│   └── src/                 # Código fonte
│       ├── assets/          # Recursos estáticos
│       ├── components/      # Componentes React
│       ├── pages/           # Páginas da aplicação
│       ├── services/        # Serviços e API
│       └── utils/           # Utilitários
│
└── backend/                 # API FastAPI
    ├── config/              # Configurações
    ├── models/              # Modelos de dados
    ├── routers/             # Rotas da API
    ├── services/            # Serviços de negócio
    └── models/ai/           # Modelos de IA treinados
```

## Licença
Proprietário - Aithos Tech