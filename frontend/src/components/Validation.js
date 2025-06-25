import React from 'react';
import { motion } from 'framer-motion';
import { FaChartLine, FaUsers, FaDollarSign } from 'react-icons/fa';

const StatCard = ({ icon, value, label }) => (
  <motion.div
    initial={{ opacity: 0, y: 50 }}
    whileInView={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.6, ease: "easeOut" }}
    viewport={{ once: true, amount: 0.5 }}
    className="bg-gray-900 p-6 rounded-lg shadow-lg border border-burgundy-700 flex flex-col items-center justify-center"
  >
    {icon && React.cloneElement(icon, { className: "text-5xl text-burgundy-500 mb-4" })}
    <p className="text-4xl font-bold text-white mb-2">{value}</p>
    <p className="text-lg text-gray-300">{label}</p>
  </motion.div>
);

const Validation = () => {
  return (
    <section className="py-20 bg-gray-900 text-white text-center">
      <div className="container mx-auto px-4">
        <motion.h2
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          viewport={{ once: true, amount: 0.5 }}
          className="text-4xl md:text-5xl font-extrabold mb-12 text-burgundy-500"
        >
          Resultados Comprovados
        </motion.h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <StatCard icon={<FaChartLine />} value="+25%" label="Aumento da Produtividade" />
          <StatCard icon={<FaDollarSign />} value="-30%" label="Redução de Custos de Manutenção" />
          <StatCard icon={<FaUsers />} value="99%" label="Satisfação do Cliente" />
        </div>
      </div>
    </section>
  );
};

export default Validation;