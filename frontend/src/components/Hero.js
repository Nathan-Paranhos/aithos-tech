import React from 'react';
import { motion } from 'framer-motion';

const Hero = () => {
  return (
    <section className="relative h-screen flex items-center justify-center text-center overflow-hidden bg-black">
      {/* Background Grid */}
      <div className="absolute inset-0 z-0 opacity-20" style={{ backgroundImage: 'url("data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%239C92AC\' fill-opacity=\'0.1\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'%3E%3C/path%3E%3C/g%3E%3C/g%3E%3C/svg%3E")' }}></div>

      {/* Animated Floating Elements */}
      <motion.div
        className="absolute top-1/4 left-1/4 w-24 h-24 bg-burgundy-500 rounded-full mix-blend-lighten filter blur-xl opacity-30"
        animate={{ y: [0, 50, 0], x: [0, 30, 0] }}
        transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
      ></motion.div>
      <motion.div
        className="absolute bottom-1/4 right-1/4 w-32 h-32 bg-burgundy-700 rounded-full mix-blend-lighten filter blur-xl opacity-30"
        animate={{ y: [0, -50, 0], x: [0, -30, 0] }}
        transition={{ duration: 12, repeat: Infinity, ease: "easeInOut" }}
      ></motion.div>

      <div className="relative z-10 p-4">
        {/* Animated Logo */}
        <motion.div
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="mb-8"
        >
          {/* Replace with your actual logo component or SVG */}
          <svg width="100" height="100" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7V17L12 22L22 17V7L12 2Z" stroke="#6D1F2F" strokeWidth="2" strokeLinejoin="round"/>
            <path d="M12 7L17 10L12 13L7 10L12 7Z" stroke="#6D1F2F" strokeWidth="2" strokeLinejoin="round"/>
            <path d="M2 7L12 12L22 7" stroke="#6D1F2F" strokeWidth="2" strokeLinejoin="round"/>
            <path d="M12 12V22" stroke="#6D1F2F" strokeWidth="2" strokeLinejoin="round"/>
          </svg>
        </motion.div>

        {/* Impactful Title */}
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
          className="text-5xl md:text-7xl font-extrabold text-white mb-4 leading-tight"
        >
          AgroGuard
        </motion.h1>

        {/* Subtitle/Description */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4, ease: "easeOut" }}
          className="text-xl md:text-2xl text-gray-300 mb-8 max-w-2xl mx-auto"
        >
          Monitoramento inteligente para a agricultura do futuro.
        </motion.p>

        {/* CTAs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6, ease: "easeOut" }}
          className="flex justify-center space-x-4"
        >
          <button className="bg-burgundy-600 hover:bg-burgundy-700 text-white font-bold py-3 px-8 rounded-full transition duration-300">
            Saiba Mais
          </button>
          <button className="bg-transparent border border-burgundy-600 text-burgundy-300 hover:bg-burgundy-600 hover:text-white font-bold py-3 px-8 rounded-full transition duration-300">
            Comece Agora
          </button>
        </motion.div>
      </div>
    </section>
  );
};

export default Hero;