import React from 'react';
import { motion } from 'framer-motion';
import { FaFacebook, FaTwitter, FaInstagram, FaLinkedin } from 'react-icons/fa';

const Footer = () => {
  return (
    <motion.footer
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      viewport={{ once: true, amount: 0.5 }}
      className="bg-gray-900 text-white py-8"
    >
      <div className="container mx-auto px-4 text-center md:text-left">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4 text-burgundy-500">AgroGuard</h3>
            <p className="text-gray-400">Monitoramento inteligente para a agricultura do futuro.</p>
          </div>
          <div>
            <h3 className="text-xl font-bold mb-4 text-burgundy-500">Links Rápidos</h3>
            <ul className="text-gray-400">
              <li className="mb-2"><a href="#" className="hover:text-burgundy-300 transition duration-300">Home</a></li>
              <li className="mb-2"><a href="#" className="hover:text-burgundy-300 transition duration-300">Serviços</a></li>
              <li className="mb-2"><a href="#" className="hover:text-burgundy-300 transition duration-300">Sobre Nós</a></li>
              <li className="mb-2"><a href="#" className="hover:text-burgundy-300 transition duration-300">Contato</a></li>
            </ul>
          </div>
          <div>
            <h3 className="text-xl font-bold mb-4 text-burgundy-500">Siga-nos</h3>
            <div className="flex justify-center md:justify-start space-x-4">
              <a href="#" className="text-gray-400 hover:text-burgundy-300 transition duration-300"><FaFacebook className="text-2xl" /></a>
              <a href="#" className="text-gray-400 hover:text-burgundy-300 transition duration-300"><FaTwitter className="text-2xl" /></a>
              <a href="#" className="text-gray-400 hover:text-burgundy-300 transition duration-300"><FaInstagram className="text-2xl" /></a>
              <a href="#" className="text-gray-400 hover:text-burgundy-300 transition duration-300"><FaLinkedin className="text-2xl" /></a>
            </div>
          </div>
        </div>
        <div className="border-t border-gray-700 mt-8 pt-8 text-gray-500 text-sm">
          &copy; {new Date().getFullYear()} AgroGuard. Todos os direitos reservados.
        </div>
      </div>
    </motion.footer>
  );
};

export default Footer;