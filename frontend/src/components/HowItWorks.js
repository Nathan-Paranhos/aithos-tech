import React from 'react';
import { motion } from 'framer-motion';
import { FaCogs, FaChartBar, FaCheckCircle } from 'react-icons/fa'; // Example icons

const HowItWorks = () => {
  return (
    <section className="py-20 bg-gradient-to-b from-gray-900 to-black text-white text-center">
      <div className="container mx-auto px-4">
        <motion.h2
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          viewport={{ once: true, amount: 0.5 }}
          className="text-4xl md:text-5xl font-extrabold mb-12 text-pink-500"
        >
          Como Funciona
        </motion.h2>
        <div className="relative flex flex-col items-center">
          {/* Timeline Line */}
          <div className="absolute h-full w-1 bg-pink-700 rounded-full hidden md:block"></div>

          {/* Steps */}
          <div className="flex flex-col md:flex-row justify-center items-center w-full max-w-4xl">
            {/* Step 1 */}
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2, ease: "easeOut" }}
              viewport={{ once: true, amount: 0.5 }}
              className="flex flex-col md:flex-row items-center md:text-left text-center mb-12 md:mb-0 md:w-1/3"
            >
              <div className="md:mr-6 mb-4 md:mb-0">
                <div className="w-16 h-16 bg-pink-500 rounded-full flex items-center justify-center text-white text-3xl font-bold border-4 border-pink-700">1</div>
              </div>
              <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-pink-700">
                <FaCogs className="text-4xl text-pink-500 mx-auto md:mx-0 mb-3" />
                <h3 className="text-xl font-semibold mb-2 text-gray-200">Coleta de Dados</h3>
                <p className="text-gray-400">Sensores inteligentes coletam dados em tempo real dos seus equipamentos.</p>
              </div>
            </motion.div>

            {/* Step 2 */}
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.4, ease: "easeOut" }}
              viewport={{ once: true, amount: 0.5 }}
              className="flex flex-col md:flex-row-reverse items-center md:text-right text-center mb-12 md:mb-0 md:w-1/3"
            >
              <div className="md:ml-6 mb-4 md:mb-0">
                <div className="w-16 h-16 bg-pink-500 rounded-full flex items-center justify-center text-white text-3xl font-bold border-4 border-pink-700">2</div>
              </div>
              <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-pink-700">
                <FaChartBar className="text-4xl text-pink-500 mx-auto md:mx-0 mb-3" />
                <h3 className="text-xl font-semibold mb-2 text-gray-200">Análise Inteligente</h3>
                <p className="text-gray-400">Nossa IA processa os dados, identifica padrões e prevê possíveis falhas.</p>
              </div>
            </motion.div>

            {/* Step 3 */}
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.6, ease: "easeOut" }}
              viewport={{ once: true, amount: 0.5 }}
              className="flex flex-col md:flex-row items-center md:text-left text-center md:w-1/3"
            >
              <div className="md:mr-6 mb-4 md:mb-0">
                <div className="w-16 h-16 bg-pink-500 rounded-full flex items-center justify-center text-white text-3xl font-bold border-4 border-pink-700">3</div>
              </div>
              <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-pink-700">
                <FaCheckCircle className="text-4xl text-pink-500 mx-auto md:mx-0 mb-3" />
                <h3 className="text-xl font-semibold mb-2 text-gray-200">Manutenção Otimizada</h3>
                <p className="text-gray-400">Receba recomendações e alertas para agir proativamente, evitando paradas.</p>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;