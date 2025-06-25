import React from 'react';
import { motion } from 'framer-motion';
import { FaChartLine, FaBell, FaShieldAlt } from 'react-icons/fa'; // Example icons

const Solution = () => {
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
          A Solução: AgroGuard
        </motion.h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2, ease: "easeOut" }}
            viewport={{ once: true, amount: 0.5 }}
            className="bg-black p-8 rounded-lg shadow-lg border border-burgundy-700"
          >
            <FaChartLine className="text-5xl text-burgundy-500 mx-auto mb-4" />
            <h3 className="text-2xl font-semibold mb-4 text-burgundy-300">Monitoramento Preditivo</h3>
            <p className="text-gray-300">Utilizamos IA para prever falhas antes que aconteçam, otimizando a manutenção e reduzindo custos.</p>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4, ease: "easeOut" }}
            viewport={{ once: true, amount: 0.5 }}
            className="bg-black p-8 rounded-lg shadow-lg border border-burgundy-700"
          >
            <FaBell className="text-5xl text-burgundy-500 mx-auto mb-4" />
            <h3 className="text-2xl font-semibold mb-4 text-burgundy-300">Alertas Inteligentes</h3>
            <p className="text-gray-300">Receba notificações em tempo real sobre a saúde dos seus equipamentos, onde quer que esteja.</p>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6, ease: "easeOut" }}
            viewport={{ once: true, amount: 0.5 }}
            className="bg-black p-8 rounded-lg shadow-lg border border-burgundy-700"
          >
            <FaShieldAlt className="text-5xl text-burgundy-500 mx-auto mb-4" />
            <h3 className="text-2xl font-semibold mb-4 text-burgundy-300">Segurança e Confiabilidade</h3>
            <p className="text-gray-300">Garanta a operação contínua e segura de suas máquinas com nossa plataforma robusta.</p>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default Solution;