import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FiUpload, FiDatabase, FiList } from 'react-icons/fi';
import DataUploadForm from '../components/DataUploadForm';

function DataUpload() {
  const [uploads, setUploads] = useState([]);

  // Handle successful upload
  const handleUploadSuccess = (uploadData) => {
    setUploads(prev => [uploadData, ...prev]);
  };

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.5
      }
    }
  };

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-6"
    >
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Upload de Dados Operacionais</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Upload Form */}
        <div className="lg:col-span-2">
          <DataUploadForm onSuccess={handleUploadSuccess} />
        </div>

        {/* Instructions */}
        <motion.div variants={itemVariants} className="bg-white rounded-lg shadow-sm overflow-hidden">
          <div className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Instruções</h2>
            <div className="space-y-4">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <FiUpload className="h-5 w-5 text-primary-500 mt-0.5" />
                </div>
                <div className="ml-3">
                  <p className="text-sm text-gray-700">Faça upload de arquivos CSV ou Excel contendo dados operacionais dos equipamentos.</p>
                </div>
              </div>
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <FiDatabase className="h-5 w-5 text-primary-500 mt-0.5" />
                </div>
                <div className="ml-3">
                  <p className="text-sm text-gray-700">Os arquivos devem conter colunas para: horas de uso, temperatura, vibração, e outras métricas relevantes.</p>
                </div>
              </div>
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <FiList className="h-5 w-5 text-primary-500 mt-0.5" />
                </div>
                <div className="ml-3">
                  <p className="text-sm text-gray-700">Após o upload, os dados serão processados e utilizados para atualizar as previsões de manutenção.</p>
                </div>
              </div>
            </div>

            <div className="mt-6 p-4 bg-gray-50 rounded-md">
              <h3 className="text-sm font-medium text-gray-700 mb-2">Formato do Arquivo</h3>
              <p className="text-xs text-gray-600 mb-2">Exemplo de estrutura CSV:</p>
              <pre className="text-xs bg-gray-100 p-2 rounded overflow-x-auto">
                data,horas_uso,temperatura,vibracao,carga<br/>
                2024-05-01,16000,72,4.2,85<br/>
                2024-05-02,16008,75,4.5,90<br/>
                2024-05-03,16016,78,5.1,88<br/>
              </pre>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Recent Uploads */}
      {uploads.length > 0 && (
        <motion.div variants={itemVariants} className="bg-white rounded-lg shadow-sm overflow-hidden">
          <div className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Uploads Recentes</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Arquivo</th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tipo</th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data/Hora</th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {uploads.map((upload, index) => (
                    <tr key={index}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{upload.fileName}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {upload.dataType === 'operational' ? 'Dados Operacionais' : 
                         upload.dataType === 'maintenance' ? 'Registros de Manutenção' : 'Registros de Falhas'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(upload.timestamp).toLocaleString('pt-BR')}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                          Processado
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </motion.div>
      )}
    </motion.div>
  );
}

export default DataUpload;
