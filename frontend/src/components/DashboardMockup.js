import React from 'react';
import { motion } from 'framer-motion';
import { Line, Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend);

const DashboardMockup = () => {
  const lineData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Produtividade',
        data: [65, 59, 80, 81, 56, 70],
        fill: false,
        borderColor: '#6D1F2F',
        tension: 0.1,
      },
    ],
  };

  const barData = {
    labels: ['Equipamento A', 'Equipamento B', 'Equipamento C', 'Equipamento D'],
    datasets: [
      {
        label: 'Horas de Operação',
        data: [120, 150, 90, 130],
        backgroundColor: '#6D1F2F',
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: 'white',
        },
      },
      title: {
        display: true,
        text: 'Dados de Desempenho (Simulado)',
        color: 'white',
      },
    },
    scales: {
      x: {
        ticks: {
          color: 'white',
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
      },
      y: {
        ticks: {
          color: 'white',
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
      },
    },
  };

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
          Dashboard (Simulação)
        </motion.h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2, ease: "easeOut" }}
            viewport={{ once: true, amount: 0.5 }}
            className="bg-black p-6 rounded-lg shadow-lg border border-burgundy-700 h-80"
          >
            <Line data={lineData} options={chartOptions} />
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4, ease: "easeOut" }}
            viewport={{ once: true, amount: 0.5 }}
            className="bg-black p-6 rounded-lg shadow-lg border border-burgundy-700 h-80"
          >
            <Bar data={barData} options={chartOptions} />
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default DashboardMockup;