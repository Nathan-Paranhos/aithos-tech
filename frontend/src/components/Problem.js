import React from 'react';
import { motion } from 'framer-motion';

const Problem = () => {
  return (
    <section className="py-20 bg-black text-white text-center">
      <div className="container mx-auto px-4">
        <motion.h2
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          viewport={{ once: true, amount: 0.5 }}
          className="text-4xl md:text-5xl font-extrabold mb-12 text-burgundy-500"
        >
          O Problema
        </motion.h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2, ease: "easeOut" }}
            viewport={{ once: true, amount: 0.5 }}
            className="bg-gray-900 p-8 rounded-lg shadow-lg border border-burgundy-700"
          >
            <h3 className="text-2xl font-semibold mb-4 text-burgundy-300">Manutenção Reativa</h3>
            <p className="text-gray-300">Ações corretivas após a falha do equipamento resultam em tempo de inatividade não planejado e custos elevados.</p>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4, ease: "easeOut" }}
            viewport={{ once: true, amount: 0.5 }}
            className="bg-gray-900 p-8 rounded-lg shadow-lg border border-burgundy-700"
          >
            <h3 className="text-2xl font-semibold mb-4 text-burgundy-300">Falta de Dados</h3>
            <p className="text-gray-300">Decisões de manutenção baseadas em estimativas, não em dados precisos e em tempo real.</p>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6, ease: "easeOut" }}
            viewport={{ once: true, amount: 0.5 }}
            className="bg-gray-900 p-8 rounded-lg shadow-lg border border-burgundy-700"
          >
            <h3 className="text-2xl font-semibold mb-4 text-burgundy-300">Perda de Produtividade</h3>
            <p className="text-gray-300">Equipamentos parados significam menos produção e impacto direto na rentabilidade.</p>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default Problem;