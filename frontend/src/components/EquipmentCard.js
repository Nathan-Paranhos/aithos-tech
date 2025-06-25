import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiAlertTriangle, FiTool, FiClock, FiBarChart2 } from 'react-icons/fi';

const EquipmentCard = ({ equipment }) => {
  // Determine status color based on risk level
  const getStatusColor = (riskLevel) => {
    switch (riskLevel) {
      case 'high':
        return 'bg-danger-500';
      case 'medium':
        return 'bg-warning-500';
      case 'low':
        return 'bg-primary-500';
      default:
        return 'bg-gray-500';
    }
  };

  // Format hours with thousand separator
  const formatHours = (hours) => {
    return hours.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  };

  return (
    <motion.div
      whileHover={{ y: -5, transition: { duration: 0.2 } }}
      className="bg-white rounded-lg shadow-md border border-gray-100 hover:shadow-lg transition-all duration-300 overflow-hidden"
    >
      <div className="p-5">
        <div className="flex justify-between items-start">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 truncate">{equipment.nome}</h3>
            <p className="text-sm text-gray-700">{equipment.modelo}</p>
          </div>
          <div className={`${getStatusColor(equipment.riskLevel)} h-3 w-3 rounded-full`}></div>
        </div>
        
        <div className="mt-4 grid grid-cols-2 gap-3">
          <div className="flex items-center">
            <FiClock className="h-5 w-5 text-gray-400 mr-2" />
            <span className="text-sm text-gray-700">{formatHours(equipment.horas_uso)} h</span>
          </div>
          <div className="flex items-center">
            <FiBarChart2 className="h-5 w-5 text-gray-400 mr-2" />
            <span className="text-sm text-gray-700">MTBF: {formatHours(equipment.mtbf)} h</span>
          </div>
          <div className="flex items-center">
            <FiAlertTriangle className="h-5 w-5 text-gray-400 mr-2" />
            <span className="text-sm text-gray-700">Risco: {equipment.score_risco}</span>
          </div>
          <div className="flex items-center">
            <FiTool className="h-5 w-5 text-gray-400 mr-2" />
            <span className="text-sm text-gray-700">{equipment.previsao_falha}</span>
          </div>
        </div>
        
        <div className="mt-5 flex justify-between">
          <Link 
            to={`/equipment/${equipment.id}`}
            className="text-primary-600 hover:text-primary-800 text-sm font-medium transition-all duration-200 hover:underline"
          >
            Ver detalhes
          </Link>
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-burgundy text-white">
            {equipment.acao_sugerida ? 'Ação sugerida' : 'Monitorar'}
          </span>
        </div>
      </div>
    </motion.div>
  );
};

export default EquipmentCard;