import React from 'react';
import { motion } from 'framer-motion';
import { FaCode, FaRocket, FaLightbulb } from 'react-icons/fa';

const RoadmapItem = ({ icon, title, description, delay }) => (
  <motion.div
    initial={{ opacity: 0, y: 50 }}
    whileInView={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.6, delay, ease: "easeOut" }}
    viewport={{ once: true, amount: 0.5 }}
    className="bg-gray-900 p-6 rounded-lg shadow-lg border border-burgundy-700 flex flex-col items-center text-center"
  >
    {icon && React.cloneElement(icon, { className: "text-5xl text-burgundy-500 mb-4" })}
    <h3 className="text-2xl font-semibold mb-2 text-burgundy-300">{title}</h3>
    <p className="text-gray-300">{description}</p>
  </motion.div>
);

const Roadmap = () => {
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
          Próximos Passos (Roadmap)
        </motion.h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <RoadmapItem
            icon={<FaLightbulb />}
            title="Fase 1: Lançamento MVP"
            description="Lançamento da plataforma com funcionalidades essenciais de monitoramento e alertas."
            delay={0.2}
          />
          <RoadmapItem
            icon={<FaCode />}
            title="Fase 2: Expansão de Recursos"
            description="Integração com mais tipos de sensores, relatórios avançados e personalização de dashboards."
            delay={0.4}
          />
          <RoadmapItem
            icon={<FaRocket />}
            title="Fase 3: Otimização e IA Avançada"
            description="Aprimoramento dos algoritmos de IA, manutenção preditiva e integração com sistemas de gestão."
            delay={0.6}
          />
        </div>
      </div>
    </section>
  );
};

export default Roadmap;