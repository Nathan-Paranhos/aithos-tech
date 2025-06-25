import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiPlus, FiSearch, FiFilter, FiUpload } from 'react-icons/fi';
import { collection, query, where, getDocs, orderBy } from 'firebase/firestore';
import { db } from '../../firebase';
import { useAuth } from '../../contexts/AuthContext';
import EquipmentCard from '../../components/EquipmentCard';

function EquipmentList() {
  const { currentUser } = useAuth();
  const [equipments, setEquipments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRisk, setFilterRisk] = useState('all');
  
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

        querySnapshot.forEach((doc) => {
          equipmentsList.push({ id: doc.id, ...doc.data() });
        });

        setEquipments(equipmentsList);
      } catch (error) {
        console.error('Error fetching equipments:', error);
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
      setEquipments([
        {
          id: 'demo1',
          nome: 'Motor WEG W22',
          modelo: 'WEG-W22-200CV',
          horas_uso: 16300,
          mtbf: 18000,
          ultima_falha: '2024-05-10',
          previsao_falha: '300h restantes',
          score_risco: '82%',
          acao_sugerida: 'Substituir rolamento traseiro',
          probabilidade_falha_5d: '63%',
          riskLevel: 'high'
        },
        {
          id: 'demo2',
          nome: 'Trator Agrícola',
          modelo: 'JD-6110B-110CV',
          horas_uso: 8500,
          mtbf: 12000,
          ultima_falha: '2024-03-15',
          previsao_falha: '1200h restantes',
          score_risco: '45%',
          acao_sugerida: '',
          probabilidade_falha_5d: '22%',
          riskLevel: 'medium'
        },
        {
          id: 'demo3',
          nome: 'Colheitadeira New Holland TC5070',
          modelo: 'NH-TC5070-175CV',
          horas_uso: 5200,
          mtbf: 15000,
          ultima_falha: '2023-11-20',
          previsao_falha: '3500h restantes',
          score_risco: '18%',
          acao_sugerida: '',
          probabilidade_falha_5d: '5%',
          riskLevel: 'low'
        },
        {
          id: 'demo4',
          nome: 'Pulverizador Jacto Uniport 3030',
          modelo: 'JA-UP3030-215CV',
          horas_uso: 7800,
          mtbf: 10000,
          ultima_falha: '2024-04-05',
          previsao_falha: '800h restantes',
          score_risco: '58%',
          acao_sugerida: 'Verificar bomba de pressão',
          probabilidade_falha_5d: '35%',
          riskLevel: 'medium'
        },
      ]);
    }
  }, [loading, equipments]);

  // Filter equipments based on search term and risk filter
  const filteredEquipments = equipments.filter(equipment => {
    const matchesSearch = equipment.nome.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          equipment.modelo.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesRisk = filterRisk === 'all' || equipment.riskLevel === filterRisk;
    
    return matchesSearch && matchesRisk;
  });

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
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <h1 className="text-2xl font-bold text-gray-900">Equipamentos</h1>
        <div className="flex flex-col sm:flex-row gap-3">
          <Link
            to="/data-upload"
            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm hover:shadow-md text-sm font-medium text-white bg-secondary-600 hover:bg-secondary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-secondary-500 transition-all duration-200"
          >
            <FiUpload className="-ml-1 mr-2 h-5 w-5" />
            Upload de Dados
          </Link>
          <Link
            to="/equipment/add"
            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm hover:shadow-md text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-all duration-200"
          >
            <FiPlus className="-ml-1 mr-2 h-5 w-5" />
            Adicionar Equipamento
          </Link>
        </div>
      </div>

      {/* Search and Filter */}
      <div className="bg-white p-4 rounded-lg shadow-md border border-gray-100 hover:shadow-lg transition-all duration-300">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="relative flex-grow">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <FiSearch className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              placeholder="Buscar equipamento por nome ou modelo"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="flex items-center">
            <FiFilter className="mr-2 h-5 w-5 text-gray-400" />
            <select
              className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md"
              value={filterRisk}
              onChange={(e) => setFilterRisk(e.target.value)}
            >
              <option value="all">Todos os riscos</option>
              <option value="high">Alto risco</option>
              <option value="medium">Médio risco</option>
              <option value="low">Baixo risco</option>
            </select>
          </div>
        </div>
      </div>

      {/* Equipment Grid */}
      {filteredEquipments.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredEquipments.map((equipment) => (
            <motion.div key={equipment.id} variants={itemVariants}>
              <EquipmentCard equipment={equipment} />
            </motion.div>
          ))}
        </div>
      ) : (
        <div className="bg-white p-8 rounded-lg shadow-md border border-gray-100 hover:shadow-lg transition-all duration-300 text-center">
          <p className="text-gray-700 text-lg">Nenhum equipamento encontrado.</p>
          <p className="text-gray-600 mt-2">Tente ajustar seus filtros ou adicione um novo equipamento.</p>
        </div>
      )}
    </motion.div>
  );
}

export default EquipmentList;