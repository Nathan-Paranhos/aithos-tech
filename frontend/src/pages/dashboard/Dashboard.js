import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiPlus, FiAlertTriangle, FiCheckCircle, FiTruck, FiTool, FiCalendar } from 'react-icons/fi';
import { collection, query, where, getDocs, orderBy, limit } from 'firebase/firestore';
import { db } from '../../firebase';
import { useAuth } from '../../contexts/AuthContext';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Title } from 'chart.js';
import { Doughnut, Line } from 'react-chartjs-2';

// Register ChartJS components
ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Title);

const Dashboard = () => {
  const { currentUser } = useAuth();
  const [equipments, setEquipments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    total: 0,
    highRisk: 0,
    mediumRisk: 0,
    lowRisk: 0,
    needsMaintenance: 0
  });
  const [recentAlerts, setRecentAlerts] = useState([]);

  useEffect(() => {
    const fetchEquipments = async () => {
      try {
        const equipmentsQuery = query(
          collection(db, 'equipments'),
          where('userId', '==', currentUser.uid),
          orderBy('createdAt', 'desc')
        );

        const querySnapshot = await getDocs(equipmentsQuery);
        const equipmentsList = [];
        let highRisk = 0;
        let mediumRisk = 0;
        let lowRisk = 0;
        let needsMaintenance = 0;

        querySnapshot.forEach((doc) => {
          const equipment = { id: doc.id, ...doc.data() };
          equipmentsList.push(equipment);

          // Count by risk level
          if (equipment.riskLevel === 'high') highRisk++;
          else if (equipment.riskLevel === 'medium') mediumRisk++;
          else lowRisk++;

          // Count equipment needing maintenance
          if (equipment.needsMaintenance) needsMaintenance++;
        });

        setEquipments(equipmentsList);
        setStats({
          total: equipmentsList.length,
          highRisk,
          mediumRisk,
          lowRisk,
          needsMaintenance
        });

        // Fetch recent alerts
        const alertsQuery = query(
          collection(db, 'alerts'),
          where('userId', '==', currentUser.uid),
          orderBy('createdAt', 'desc'),
          limit(5)
        );

        const alertsSnapshot = await getDocs(alertsQuery);
        const alertsList = [];

        alertsSnapshot.forEach((doc) => {
          alertsList.push({ id: doc.id, ...doc.data() });
        });

        setRecentAlerts(alertsList);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    if (currentUser) {
      fetchEquipments();
    }
  }, [currentUser]);

  // For demo purposes, if no data is available
  useEffect(() => {
    if (!loading && equipments.length === 0) {
      // Sample data for demonstration
      setStats({
        total: 5,
        highRisk: 1,
        mediumRisk: 2,
        lowRisk: 2,
        needsMaintenance: 2
      });

      setRecentAlerts([
        {
          id: '1',
          equipmentId: 'demo1',
          equipmentName: 'Trator Agrícola',
          message: 'Risco ALTO de falha na bomba hidráulica. Previsão de falha em 4 dias.',
          severity: 'high',
          createdAt: new Date().toISOString(),
          component: 'Bomba Hidráulica'
        },
        {
          id: '2',
          equipmentId: 'demo2',
          equipmentName: 'Colheitadeira Agrícola',
          message: 'Risco MÉDIO de falha no sistema de refrigeração. Recomendamos inspeção.',
          severity: 'medium',
          createdAt: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
          component: 'Sistema de Refrigeração'
        },
        {
          id: '3',
          equipmentId: 'demo3',
          equipmentName: 'Pulverizador Jacto Uniport 3030',
          message: 'Manutenção preventiva recomendada para o sistema de bombeamento.',
          severity: 'low',
          createdAt: new Date(Date.now() - 172800000).toISOString(), // 2 days ago
          component: 'Sistema de Bombeamento'
        }
      ]);
    }
  }, [loading, equipments]);

  // Chart data
  const riskDistributionData = {
    labels: ['Alto Risco', 'Médio Risco', 'Baixo Risco'],
    datasets: [
      {
        data: [stats.highRisk, stats.mediumRisk, stats.lowRisk],
        backgroundColor: ['#ef4444', '#f59e0b', '#22c55e'],
        borderColor: ['#ffffff', '#ffffff', '#ffffff'],
        borderWidth: 2,
      },
    ],
  };

  // Line chart data for equipment health over time (mock data)
  const healthTrendData = {
    labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
    datasets: [
      {
        label: 'Saúde Média dos Equipamentos',
        data: [85, 82, 80, 75, 72, 70],
        borderColor: '#0ea5e9',
        backgroundColor: 'rgba(14, 165, 233, 0.2)',
        tension: 0.4,
        fill: true,
      },
    ],
  };

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

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-6"
    >
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <Link
          to="/equipment/add"
          className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-all duration-200"
        >
          <FiPlus className="-ml-1 mr-2 h-5 w-5" />
          Adicionar Equipamento
        </Link>
      </div>

      {/* Stats Cards */}
      <motion.div variants={itemVariants} className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div className="bg-white overflow-hidden shadow-md border border-gray-100 rounded-lg hover:shadow-lg transition-all duration-300">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-primary-100 rounded-md p-3">
                <FiTruck className="h-6 w-6 text-primary-600" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-700 truncate">Total de Equipamentos</dt>
                  <dd>
                    <div className="text-lg font-medium text-gray-900">{stats.total}</div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow-md border border-gray-100 rounded-lg hover:shadow-lg transition-all duration-300">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-red-100 rounded-md p-3">
                <FiAlertTriangle className="h-6 w-6 text-red-600" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-700 truncate">Alto Risco</dt>
                  <dd>
                    <div className="text-lg font-medium text-gray-900">{stats.highRisk}</div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow-md border border-gray-100 rounded-lg hover:shadow-lg transition-all duration-300">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-yellow-100 rounded-md p-3">
                <FiTool className="h-6 w-6 text-yellow-600" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-700 truncate">Necessitam Manutenção</dt>
                  <dd>
                    <div className="text-lg font-medium text-gray-900">{stats.needsMaintenance}</div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow-md border border-gray-100 rounded-lg hover:shadow-lg transition-all duration-300">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-green-100 rounded-md p-3">
                <FiCheckCircle className="h-6 w-6 text-green-600" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-700 truncate">Baixo Risco</dt>
                  <dd>
                    <div className="text-lg font-medium text-gray-900">{stats.lowRisk}</div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Charts and Alerts */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        {/* Risk Distribution Chart */}
        <motion.div variants={itemVariants} className="bg-white overflow-hidden shadow-md border border-gray-100 rounded-lg hover:shadow-lg transition-all duration-300">
          <div className="p-5">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Distribuição de Risco</h3>
            <div className="mt-2 h-64 flex items-center justify-center">
              <div className="w-full max-w-xs">
                <Doughnut 
                  data={riskDistributionData} 
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
        </motion.div>

        {/* Equipment Health Trend */}
        <motion.div variants={itemVariants} className="bg-white overflow-hidden shadow-md border border-gray-100 rounded-lg hover:shadow-lg transition-all duration-300">
          <div className="p-5">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Tendência de Saúde dos Equipamentos</h3>
            <div className="mt-2 h-64">
              <Line 
                data={healthTrendData} 
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
                      min: 0,
                      max: 100,
                      title: {
                        display: true,
                        text: 'Saúde (%)',
                      },
                    },
                  },
                }} 
              />
            </div>
          </div>
        </motion.div>
      </div>

      {/* Recent Alerts */}
      <motion.div variants={itemVariants} className="bg-white shadow-md border border-gray-100 overflow-hidden sm:rounded-lg hover:shadow-lg transition-all duration-300">
        <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
          <h3 className="text-lg leading-6 font-medium text-gray-900">Alertas Recentes</h3>
          <Link to="/reports" className="text-sm font-medium text-primary-600 hover:text-primary-500">
            Ver todos
          </Link>
        </div>
        <ul className="divide-y divide-gray-200">
          {recentAlerts.length > 0 ? (
            recentAlerts.map((alert) => (
              <li key={alert.id}>
                <Link to={`/equipment/${alert.equipmentId}`} className="block hover:bg-gray-50">
                  <div className="px-4 py-4 sm:px-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div className={`flex-shrink-0 h-4 w-4 rounded-full ${alert.severity === 'high' ? 'bg-red-500' : alert.severity === 'medium' ? 'bg-yellow-500' : 'bg-green-500'}`}></div>
                        <p className="ml-2 text-sm font-medium text-gray-900 truncate">{alert.equipmentName}</p>
                      </div>
                      <div className="ml-2 flex-shrink-0 flex">
                        <p className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">
                          {alert.component}
                        </p>
                      </div>
                    </div>
                    <div className="mt-2 sm:flex sm:justify-between">
                      <div className="sm:flex">
                        <p className="text-sm text-gray-700">{alert.message}</p>
                      </div>
                      <div className="mt-2 flex items-center text-sm text-gray-700 sm:mt-0">
                        <FiCalendar className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-500" />
                        <p>
                          {new Date(alert.createdAt).toLocaleDateString('pt-BR')}
                        </p>
                      </div>
                    </div>
                  </div>
                </Link>
              </li>
            ))
          ) : (
            <li className="px-4 py-5 sm:px-6 text-center text-gray-700">
              Nenhum alerta recente encontrado
            </li>
          )}
        </ul>
      </motion.div>
    </motion.div>
  );
};

export default Dashboard;