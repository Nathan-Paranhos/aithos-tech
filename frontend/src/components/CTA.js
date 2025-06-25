import React from 'react';
import { motion } from 'framer-motion';

const CTA = () => {
  return (
    <section className="py-20 bg-burgundy-800 text-white text-center">
      <div className="container mx-auto px-4">
        <motion.h2
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          viewport={{ once: true, amount: 0.5 }}
          className="text-4xl md:text-5xl font-extrabold mb-6"
        >
          Pronto para Transformar sua Agricultura?
        </motion.h2>
        <motion.p
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2, ease: "easeOut" }}
          viewport={{ once: true, amount: 0.5 }}
          className="text-xl md:text-2xl mb-10 max-w-3xl mx-auto"
        >
          Junte-se à revolução da agricultura inteligente com AgroGuard.
        </motion.p>
        <motion.button
          initial={{ opacity: 0, scale: 0.8 }}
          whileInView={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.4, ease: "easeOut" }}
          viewport={{ once: true, amount: 0.5 }}
          className="bg-white text-burgundy-800 hover:bg-gray-200 font-bold py-4 px-10 rounded-full text-lg transition duration-300"
        >
          Solicite uma Demonstração
        </motion.button>
      </div>
    </section>
  );
};

export default CTA;