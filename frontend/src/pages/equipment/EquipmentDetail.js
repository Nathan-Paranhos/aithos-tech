import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiArrowLeft, FiDownload, FiAlertTriangle, FiTool, FiClock, FiBarChart2, FiCalendar, FiThermometer, FiActivity } from 'react-icons/fi';
import { doc, getDoc, collection, query, where, orderBy, limit, getDocs } from 'firebase/firestore';
import { db } from '../../firebase';
import { useAuth } from '../../contexts/AuthContext';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Title, BarElement } from 'chart.js';
import { Doughnut, Line, Bar } from 'react-chartjs-2';

// Register ChartJS components
ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Title, BarElement);

function EquipmentDetail() {
  const { id } = useParams();
  const { currentUser } = useAuth();
  const [equipment, setEquipment] = useState(null);
  const [maintenanceHistory, setMaintenanceHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [operationalData, setOperationalData] = useState([]);

  useEffect(() => {
    const fetchEquipmentData = async () => {
      try {
        // In a real app, fetch from Firestore
        // const docRef = doc(db, 'equipments', id);
        // const docSnap = await getDoc(docRef);
        
        // if (docSnap.exists()) {
        //   setEquipment({ id: docSnap.id, ...docSnap.data() });
        // }

        // For demo purposes
        if (id === 'demo1' || !equipment) {
          setEquipment({
            id: 'demo1',
            nome: 'Motor WEG W22',
            modelo: 'WEG-W22-200CV',
            fabricante: 'WEG',
            tipo: 'Motor Elétrico Industrial',
            horas_uso: 16300,
            mtbf: 18000,
            ultima_falha: '2024-05-10',
            previsao_falha: '300h restantes',
            score_risco: '82%',
            acao_sugerida: 'Substituir rolamento traseiro',
            probabilidade_falha_5d: '63%',
            riskLevel: 'high',
            componentes_criticos: ['Rolamento dianteiro', 'Rolamento traseiro', 'Estator', 'Rotor', 'Sistema de refrigeração'],
            data_instalacao: '2022-03-15',
            localizacao: 'Linha de produção A - Setor 3',
            responsavel: 'Carlos Mendes',
            temperatura_atual: '78°C',
            vibracao_atual: '5.8 mm/s',
            ultima_manutencao: '2024-02-20',
          });

          // Sample maintenance history
          setMaintenanceHistory([
            {
              id: 'm1',
              data: '2024-02-20',
              tipo: 'Preventiva',
              descricao: 'Lubrificação dos rolamentos e verificação do sistema de refrigeração',
              tecnico: 'André Silva',
              custo: 'R$ 1.200,00'
            },
            {
              id: 'm2',
              data: '2023-11-05',
              tipo: 'Corretiva',
              descricao: 'Substituição do rolamento dianteiro após detecção de vibração anormal',
              tecnico: 'Roberto Almeida',
              custo: 'R$ 3.500,00'
            },
            {
              id: 'm3',
              data: '2023-08-12',
              tipo: 'Preventiva',
              descricao: 'Inspeção geral e limpeza do sistema de ventilação',
              tecnico: 'André Silva',
              custo: 'R$ 850,00'
            },
          ]);

          // Sample operational data for charts
          setOperationalData([
            { data: '2024-01', temperatura: 65, vibracao: 2.1, horas: 15200 },
            { data: '2024-02', temperatura: 68, vibracao: 2.3, horas: 15500 },
            { data: '2024-03', temperatura: 70, vibracao: 3.2, horas: 15800 },
            { data: '2024-04', temperatura: 72, vibracao: 4.1, horas: 16100 },
            { data: '2024-05', temperatura: 78, vibracao: 5.8, horas: 16300 },
          ]);
        }
      } catch (error) {
        console.error('Error fetching equipment details:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchEquipmentData();
  }, [id]);

  // Chart data for temperature trend
  const temperatureData = {
    labels: operationalData.map(item => item.data),
    datasets: [
      {
        label: 'Temperatura (°C)',
        data: operationalData.map(item => item.temperatura),
        borderColor: '#ef4444',
        backgroundColor: 'rgba(239, 68, 68, 0.2)',
        tension: 0.4,
        fill: true,
      },
    ],
  };

  // Chart data for vibration trend
  const vibrationData = {
    labels: operationalData.map(item => item.data),
    datasets: [
      {
        label: 'Vibração (mm/s)',
        data: operationalData.map(item => item.vibracao),
        borderColor: '#f59e0b',
        backgroundColor: 'rgba(245, 158, 11, 0.2)',
        tension: 0.4,
        fill: true,
      },
    ],
  };

  // Chart data for maintenance history
  const maintenanceData = {
    labels: ['Preventiva', 'Corretiva'],
    datasets: [
      {
        data: [
          maintenanceHistory.filter(m => m.tipo === 'Preventiva').length,
          maintenanceHistory.filter(m => m.tipo === 'Corretiva').length,
        ],
        backgroundColor: ['#22c55e', '#ef4444'],
        borderColor: ['#ffffff', '#ffffff'],
        borderWidth: 2,
      },
    ],
  };

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.5
      }
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  if (!equipment) {
    return (
      <div className="bg-white p-8 rounded-lg shadow-md border border-gray-100 hover:shadow-lg transition-all duration-300 text-center">
        <p className="text-gray-700 text-lg">Equipamento não encontrado.</p>
        <Link to="/equipment" className="text-primary-600 hover:text-primary-800 mt-4 inline-block transition-all duration-200 hover:underline">
          Voltar para lista de equipamentos
        </Link>
      </div>
    );
  }

  // Calculate risk color
  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'high':
        return 'text-danger-600';
      case 'medium':
        return 'text-warning-600';
      case 'low':
        return 'text-primary-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-6"
    >
      {/* Header with back button */}
      <div className="flex items-center">
        <Link to="/equipment" className="mr-4 p-2 rounded-full hover:bg-gray-200">
          <FiArrowLeft className="h-5 w-5 text-gray-600" />
        </Link>
        <h1 className="text-2xl font-bold text-gray-900">{equipment.nome}</h1>
        <div className={`ml-4 flex items-center ${getRiskColor(equipment.riskLevel)}`}>
          <FiAlertTriangle className="h-5 w-5 mr-1" />
          <span className="text-sm font-medium">Risco: {equipment.score_risco}</span>
        </div>
      </div>

      {/* Equipment Overview */}
      <motion.div variants={itemVariants} className="bg-white rounded-lg shadow-md border border-gray-100 hover:shadow-lg transition-all duration-300 overflow-hidden">
        <div className="p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Visão Geral</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div>
              <h3 className="text-sm font-medium text-gray-700">Informações Básicas</h3>
              <div className="mt-2 space-y-2">
                <p className="text-sm text-gray-700"><span className="font-medium">Modelo:</span> {equipment.modelo}</p>
                <p className="text-sm text-gray-700"><span className="font-medium">Fabricante:</span> {equipment.fabricante}</p>
                <p className="text-sm text-gray-700"><span className="font-medium">Tipo:</span> {equipment.tipo}</p>
                <p className="text-sm text-gray-700"><span className="font-medium">Instalação:</span> {equipment.data_instalacao}</p>
                <p className="text-sm text-gray-700"><span className="font-medium">Localização:</span> {equipment.localizacao}</p>
                <p className="text-sm text-gray-700"><span className="font-medium">Responsável:</span> {equipment.responsavel}</p>
              </div>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-700">Métricas Operacionais</h3>
              <div className="mt-2 space-y-2">
                <p className="text-sm text-gray-700"><span className="font-medium">Horas de Uso:</span> {equipment.horas_uso.toLocaleString()} h</p>
                <p className="text-sm text-gray-700"><span className="font-medium">MTBF:</span> {equipment.mtbf.toLocaleString()} h</p>
                <p className="text-sm text-gray-700"><span className="font-medium">Última Falha:</span> {equipment.ultima_falha}</p>
                <p className="text-sm text-gray-700"><span className="font-medium">Última Manutenção:</span> {equipment.ultima_manutencao}</p>
                <p className="text-sm text-gray-700"><span className="font-medium">Temperatura Atual:</span> {equipment.temperatura_atual}</p>
                <p className="text-sm text-gray-700"><span className="font-medium">Vibração Atual:</span> {equipment.vibracao_atual}</p>
              </div>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-700">Análise Preditiva</h3>
              <div className="mt-2 space-y-2">
                <p className="text-sm text-gray-700"><span className="font-medium">Score de Risco:</span> {equipment.score_risco}</p>
                <p className="text-sm text-gray-700"><span className="font-medium">Previsão de Falha:</span> {equipment.previsao_falha}</p>
                <p className="text-sm text-gray-700"><span className="font-medium">Prob. Falha (5 dias):</span> {equipment.probabilidade_falha_5d}</p>
                <p className="text-sm text-gray-700 font-medium text-danger-600">Ação Sugerida:</p>
                <p className="text-sm text-gray-700">{equipment.acao_sugerida || 'Nenhuma ação necessária no momento'}</p>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Temperature Trend */}
        <motion.div variants={itemVariants} className="bg-white rounded-lg shadow-md border border-gray-100 hover:shadow-lg transition-all duration-300 overflow-hidden">
          <div className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Tendência de Temperatura</h2>
            <div className="h-64">
              <Line 
                data={temperatureData} 
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: {
                      display: false,
                    },
                  },
                  scales: {
                    y: {
                      title: {
                        display: true,
                        text: 'Temperatura (°C)',
                      },
                    },
                  },
                }} 
              />
            </div>
          </div>
        </motion.div>

        {/* Vibration Trend */}
        <motion.div variants={itemVariants} className="bg-white rounded-lg shadow-md border border-gray-100 hover:shadow-lg transition-all duration-300 overflow-hidden">
          <div className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Tendência de Vibração</h2>
            <div className="h-64">
              <Line 
                data={vibrationData} 
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: {
                      display: false,
                    },
                  },
                  scales: {
                    y: {
                      title: {
                        display: true,
                        text: 'Vibração (mm/s)',
                      },
                    },
                  },
                }} 
              />
            </div>
          </div>
        </motion.div>
      </div>

      {/* Maintenance History */}
      <motion.div variants={itemVariants} className="bg-white rounded-lg shadow-md border border-gray-100 hover:shadow-lg transition-all duration-300 overflow-hidden">
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Histórico de Manutenção</h2>
            <button className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-white bg-burgundy hover:bg-burgundy-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-burgundy-500 shadow-sm hover:shadow-md transition-all duration-200">
              <FiDownload className="-ml-0.5 mr-1 h-4 w-4" />
              Exportar PDF
            </button>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            <div className="lg:col-span-3">
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Data</th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Tipo</th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Descrição</th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Técnico</th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Custo</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {maintenanceHistory.map((maintenance) => (
                      <tr key={maintenance.id}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{maintenance.data}</td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${maintenance.tipo === 'Preventiva' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                            {maintenance.tipo}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-700">{maintenance.descricao}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{maintenance.tecnico}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{maintenance.custo}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
            <div className="lg:col-span-1">
              <h3 className="text-sm font-medium text-gray-700 mb-2">Tipos de Manutenção</h3>
              <div className="h-48">
                <Doughnut 
                  data={maintenanceData} 
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        position: 'bottom',
                      },
                    },
                  }} 
                />
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Critical Components */}
      <motion.div variants={itemVariants} className="bg-white rounded-lg shadow-md border border-gray-100 hover:shadow-lg transition-all duration-300 overflow-hidden">
        <div className="p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Componentes Críticos</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {equipment.componentes_criticos.map((componente, index) => (
              <div key={index} className="border border-gray-200 rounded-md p-4">
                <h3 className="font-medium text-gray-700">{componente}</h3>
                <div className="mt-2 flex justify-between items-center">
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div 
                      className={`h-2.5 rounded-full ${index === 1 ? 'bg-danger-500' : index === 0 ? 'bg-warning-500' : 'bg-primary-500'}`} 
                      style={{ width: `${100 - (index * 15)}%` }}
                    ></div>
                  </div>
                  <span className="ml-2 text-xs font-medium text-gray-700">
                    {100 - (index * 15)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}

export default EquipmentDetail;