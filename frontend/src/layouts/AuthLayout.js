import React from 'react';
import { Outlet } from 'react-router-dom';
import { motion } from 'framer-motion';

const AuthLayout = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <motion.div 
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="flex justify-center"
        >
          <div className="text-center">
            <h1 className="text-5xl font-extrabold text-white drop-shadow-lg">AgroGuard</h1>
            <p className="mt-3 text-lg text-gray-300">
              Manutenção preditiva inteligente para equipamentos industriais, agrícolas e automotivos
            </p>
          </div>
        </motion.div>
      </div>

      <motion.div 
        initial={{ y: 50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="mt-8 sm:mx-auto sm:w-full sm:max-w-md"
      >
        <div className="bg-gray-800 py-8 px-4 shadow-2xl rounded-lg sm:px-10 border border-gray-700">
          <Outlet />
        </div>
      </motion.div>
    </div>
  );
};

export default AuthLayout;