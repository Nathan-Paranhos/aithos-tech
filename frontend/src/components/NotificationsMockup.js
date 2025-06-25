import React from 'react';
import { motion } from 'framer-motion';
import { FaExclamationTriangle, FaCheckCircle, FaInfoCircle } from 'react-icons/fa';

const NotificationItem = ({ type, message, time }) => {
  let icon;
  let bgColor;
  let textColor;

  switch (type) {
    case 'alert':
      icon = <FaExclamationTriangle className="text-red-500" />;
      bgColor = 'bg-red-900';
      textColor = 'text-red-200';
      break;
    case 'success':
      icon = <FaCheckCircle className="text-green-500" />;
      bgColor = 'bg-green-900';
      textColor = 'text-green-200';
      break;
    case 'info':
    default:
      icon = <FaInfoCircle className="text-blue-500" />;
      bgColor = 'bg-blue-900';
      textColor = 'text-blue-200';
      break;
  }

  return (
    <div className={`flex items-center p-3 rounded-lg mb-2 ${bgColor}`}>
      <div className="mr-3">{icon}</div>
      <div className="flex-grow">
        <p className={`font-semibold ${textColor}`}>{message}</p>
        <p className="text-xs text-gray-400">{time}</p>
      </div>
    </div>
  );
};

const NotificationsMockup = () => {
  const notifications = [
    { id: 1, type: 'alert', message: 'Sensor de temperatura do Trator 3 com anomalia.', time: '2 min atrás' },
    { id: 2, type: 'success', message: 'Manutenção preventiva do Pulverizador 1 concluída.', time: '1 hora atrás' },
    { id: 3, type: 'info', message: 'Nível de combustível do Gerador 2 está baixo.', time: '3 horas atrás' },
    { id: 4, type: 'alert', message: 'Pressão do óleo da Colheitadeira 5 crítica!', time: 'Ontem' },
  ];

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
          Notificações (Mockup)
        </motion.h2>
        <div className="flex justify-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            viewport={{ once: true, amount: 0.5 }}
            className="relative w-72 h-auto bg-gray-800 rounded-3xl shadow-2xl p-4 border-4 border-gray-700"
          >
            {/* Phone Bezel */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-24 h-6 bg-gray-900 rounded-b-xl"></div>
            <div className="absolute bottom-2 left-1/2 -translate-x-1/2 w-16 h-1 bg-gray-700 rounded-full"></div>

            <div className="bg-gray-900 rounded-xl p-4 h-full overflow-y-auto">
              <h3 className="text-xl font-bold mb-4 text-left">Alertas Recentes</h3>
              {notifications.map(notif => (
                <NotificationItem key={notif.id} {...notif} />
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default NotificationsMockup;