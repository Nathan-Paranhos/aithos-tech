import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiArrowLeft, FiSave, FiX, FiInfo } from 'react-icons/fi';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { collection, addDoc, serverTimestamp } from 'firebase/firestore';
import { db } from '../../firebase';
import { useAuth } from '../../contexts/AuthContext';

function EquipmentAdd() {
  const navigate = useNavigate();
  const { currentUser } = useAuth();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  // Validation schema
  const validationSchema = Yup.object({
    nome: Yup.string().required('Nome do equipamento é obrigatório'),
    fabricante: Yup.string().required('Fabricante é obrigatório'),
    modelo: Yup.string().required('Modelo é obrigatório'),
    tipo: Yup.string().required('Tipo de equipamento é obrigatório'),
    data_instalacao: Yup.date().required('Data de instalação é obrigatória'),
    localizacao: Yup.string().required('Localização é obrigatória'),
    responsavel: Yup.string().required('Responsável é obrigatório'),
    horas_uso: Yup.number().required('Horas de uso é obrigatório').min(0, 'Horas de uso deve ser maior ou igual a 0'),
    mtbf: Yup.number().required('MTBF é obrigatório').min(0, 'MTBF deve ser maior ou igual a 0'),
    temperatura_atual: Yup.string().required('Temperatura atual é obrigatória'),
    vibracao_atual: Yup.string().required('Vibração atual é obrigatória'),
  });

  // Initial form values
  const initialValues = {
    nome: '',
    fabricante: '',
    modelo: '',
    tipo: '',
    data_instalacao: new Date().toISOString().split('T')[0],
    localizacao: '',
    responsavel: '',
    horas_uso: 0,
    mtbf: 0,
    temperatura_atual: '',
    vibracao_atual: '',
    ultima_falha: '',
    ultima_manutencao: '',
    componentes_criticos: '',
    notas: '',
  };

  // Handle form submission
  const handleSubmit = async (values, { setSubmitting, resetForm }) => {
    setIsSubmitting(true);
    setError('');
    
    try {
      // Format componentes_criticos as array
      const componentes = values.componentes_criticos
        ? values.componentes_criticos.split(',').map(item => item.trim())
        : [];

      // Calculate risk level based on hours_uso and mtbf
      let riskLevel = 'low';
      const hoursRatio = values.horas_uso / values.mtbf;
      
      if (hoursRatio > 0.9) {
        riskLevel = 'high';
      } else if (hoursRatio > 0.7) {
        riskLevel = 'medium';
      }

      // Calculate score_risco based on hours_uso and mtbf
      const scoreRisco = Math.min(Math.round(hoursRatio * 100), 100) + '%';

      // Prepare equipment data
      const equipmentData = {
        ...values,
        horas_uso: Number(values.horas_uso),
        mtbf: Number(values.mtbf),
        componentes_criticos: componentes,
        riskLevel,
        score_risco: scoreRisco,
        previsao_falha: `${Math.max(0, Math.round(values.mtbf - values.horas_uso))}h restantes`,
        probabilidade_falha_5d: `${Math.min(Math.round(hoursRatio * 100 + 10), 100)}%`,
        userId: currentUser.uid,
        createdAt: serverTimestamp(),
        updatedAt: serverTimestamp(),
      };

      // In a real app, save to Firestore
      // await addDoc(collection(db, 'equipments'), equipmentData);
      
      console.log('Equipment data to be saved:', equipmentData);
      
      // Show success message
      setSuccess(true);
      
      // Reset form after 2 seconds and redirect
      setTimeout(() => {
        resetForm();
        navigate('/equipment');
      }, 2000);
    } catch (error) {
      console.error('Error adding equipment:', error);
      setError('Erro ao adicionar equipamento. Por favor, tente novamente.');
    } finally {
      setSubmitting(false);
      setIsSubmitting(false);
    }
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

  // Equipment types for dropdown
  const equipmentTypes = [
    'Motor Elétrico',
    'Bomba Hidráulica',
    'Compressor',
    'Trator',
    'Colheitadeira',
    'Pulverizador',
    'Esteira Transportadora',
    'Gerador',
    'Transformador',
    'Outro'
  ];

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-6"
    >
      {/* Header with back button */}
      <div className="flex items-center">
        <Link to="/equipment" className="mr-4 p-2 rounded-full hover:bg-gray-200 transition-all duration-200">
          <FiArrowLeft className="h-5 w-5 text-gray-600" />
        </Link>
        <h1 className="text-2xl font-bold text-gray-900">Adicionar Novo Equipamento</h1>
      </div>

      {/* Success message */}
      {success && (
        <motion.div 
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mb-4 rounded shadow-md hover:shadow-lg transition-all duration-300"
        >
          <p className="font-medium">Equipamento adicionado com sucesso!</p>
          <p>Redirecionando para a lista de equipamentos...</p>
        </motion.div>
      )}

      {/* Error message */}
      {error && (
        <motion.div 
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4 rounded shadow-md hover:shadow-lg transition-all duration-300"
        >
          <p className="font-medium">Erro!</p>
          <p>{error}</p>
        </motion.div>
      )}

      {/* Form */}
      <motion.div variants={itemVariants} className="bg-white rounded-lg shadow-md border border-gray-100 hover:shadow-lg transition-all duration-300 overflow-hidden">
        <div className="p-6">
          <Formik
            initialValues={initialValues}
            validationSchema={validationSchema}
            onSubmit={handleSubmit}
          >
            {({ isSubmitting, errors, touched }) => (
              <Form className="space-y-8">
                {/* Basic Information Section */}
                <div>
                  <h2 className="text-lg font-semibold text-gray-900 mb-4 border-b border-gray-100 pb-2">Informações Básicas</h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div>
                      <label htmlFor="nome" className="block text-sm font-medium text-gray-700 mb-1">Nome do Equipamento*</label>
                      <Field
                        type="text"
                        name="nome"
                        id="nome"
                        className={`input-field w-full ${errors.nome && touched.nome ? 'border-red-500' : ''}`}
                        placeholder="Ex: Motor WEG W22"
                      />
                      <ErrorMessage name="nome" component="div" className="mt-1 text-sm text-red-600" />
                    </div>

                    <div>
                      <label htmlFor="fabricante" className="block text-sm font-medium text-gray-700 mb-1">Fabricante*</label>
                      <Field
                        type="text"
                        name="fabricante"
                        id="fabricante"
                        className={`input-field w-full ${errors.fabricante && touched.fabricante ? 'border-red-500' : ''}`}
                        placeholder="Ex: WEG"
                      />
                      <ErrorMessage name="fabricante" component="div" className="mt-1 text-sm text-red-600" />
                    </div>

                    <div>
                      <label htmlFor="modelo" className="block text-sm font-medium text-gray-700 mb-1">Modelo*</label>
                      <Field
                        type="text"
                        name="modelo"
                        id="modelo"
                        className={`input-field w-full ${errors.modelo && touched.modelo ? 'border-red-500' : ''}`}
                        placeholder="Ex: W22-200CV"
                      />
                      <ErrorMessage name="modelo" component="div" className="mt-1 text-sm text-red-600" />
                    </div>

                    <div>
                      <label htmlFor="tipo" className="block text-sm font-medium text-gray-700 mb-1">Tipo de Equipamento*</label>
                      <Field
                        as="select"
                        name="tipo"
                        id="tipo"
                        className={`input-field w-full ${errors.tipo && touched.tipo ? 'border-red-500' : ''}`}
                      >
                        <option value="">Selecione um tipo</option>
                        {equipmentTypes.map((type, index) => (
                          <option key={index} value={type}>{type}</option>
                        ))}
                      </Field>
                      <ErrorMessage name="tipo" component="div" className="mt-1 text-sm text-red-600" />
                    </div>

                    <div>
                      <label htmlFor="data_instalacao" className="block text-sm font-medium text-gray-700 mb-1">Data de Instalação*</label>
                      <Field
                        type="date"
                        name="data_instalacao"
                        id="data_instalacao"
                        className={`input-field w-full ${errors.data_instalacao && touched.data_instalacao ? 'border-red-500' : ''}`}
                      />
                      <ErrorMessage name="data_instalacao" component="div" className="mt-1 text-sm text-red-600" />
                    </div>

                    <div>
                      <label htmlFor="localizacao" className="block text-sm font-medium text-gray-700 mb-1">Localização*</label>
                      <Field
                        type="text"
                        name="localizacao"
                        id="localizacao"
                        className={`input-field w-full ${errors.localizacao && touched.localizacao ? 'border-red-500' : ''}`}
                        placeholder="Ex: Linha de produção A - Setor 3"
                      />
                      <ErrorMessage name="localizacao" component="div" className="mt-1 text-sm text-red-600" />
                    </div>

                    <div>
                      <label htmlFor="responsavel" className="block text-sm font-medium text-gray-700 mb-1">Responsável*</label>
                      <Field
                        type="text"
                        name="responsavel"
                        id="responsavel"
                        className={`input-field w-full ${errors.responsavel && touched.responsavel ? 'border-red-500' : ''}`}
                        placeholder="Ex: Carlos Mendes"
                      />
                      <ErrorMessage name="responsavel" component="div" className="mt-1 text-sm text-red-600" />
                    </div>
                  </div>
                </div>

                {/* Operational Metrics Section */}
                <div>
                  <h2 className="text-lg font-semibold text-gray-900 mb-4 border-b border-gray-100 pb-2">Métricas Operacionais</h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div>
                      <label htmlFor="horas_uso" className="block text-sm font-medium text-gray-700 mb-1">Horas de Uso*</label>
                      <Field
                        type="number"
                        name="horas_uso"
                        id="horas_uso"
                        min="0"
                        className={`input-field w-full ${errors.horas_uso && touched.horas_uso ? 'border-red-500' : ''}`}
                        placeholder="Ex: 16300"
                      />
                      <ErrorMessage name="horas_uso" component="div" className="mt-1 text-sm text-red-600" />
                    </div>

                    <div>
                      <label htmlFor="mtbf" className="block text-sm font-medium text-gray-700 mb-1">
                        <span>MTBF (horas)*</span>
                        <span className="ml-1 inline-flex items-center" title="Tempo Médio Entre Falhas (Mean Time Between Failures)">
                          <FiInfo className="h-4 w-4 text-gray-500 hover:text-gray-700 transition-colors duration-200" />
                        </span>
                      </label>
                      <Field
                        type="number"
                        name="mtbf"
                        id="mtbf"
                        min="0"
                        className={`input-field w-full ${errors.mtbf && touched.mtbf ? 'border-red-500' : ''}`}
                        placeholder="Ex: 18000"
                      />
                      <ErrorMessage name="mtbf" component="div" className="mt-1 text-sm text-red-600" />
                    </div>

                    <div>
                      <label htmlFor="temperatura_atual" className="block text-sm font-medium text-gray-700 mb-1">Temperatura Atual*</label>
                      <Field
                        type="text"
                        name="temperatura_atual"
                        id="temperatura_atual"
                        className={`input-field w-full ${errors.temperatura_atual && touched.temperatura_atual ? 'border-red-500' : ''}`}
                        placeholder="Ex: 78°C"
                      />
                      <ErrorMessage name="temperatura_atual" component="div" className="mt-1 text-sm text-red-600" />
                    </div>

                    <div>
                      <label htmlFor="vibracao_atual" className="block text-sm font-medium text-gray-700 mb-1">Vibração Atual*</label>
                      <Field
                        type="text"
                        name="vibracao_atual"
                        id="vibracao_atual"
                        className={`input-field w-full ${errors.vibracao_atual && touched.vibracao_atual ? 'border-red-500' : ''}`}
                        placeholder="Ex: 5.8 mm/s"
                      />
                      <ErrorMessage name="vibracao_atual" component="div" className="mt-1 text-sm text-red-600" />
                    </div>

                    <div>
                      <label htmlFor="ultima_falha" className="block text-sm font-medium text-gray-700 mb-1">Data da Última Falha</label>
                      <Field
                        type="date"
                        name="ultima_falha"
                        id="ultima_falha"
                        className="input-field w-full"
                      />
                    </div>

                    <div>
                      <label htmlFor="ultima_manutencao" className="block text-sm font-medium text-gray-700 mb-1">Data da Última Manutenção</label>
                      <Field
                        type="date"
                        name="ultima_manutencao"
                        id="ultima_manutencao"
                        className="input-field w-full"
                      />
                    </div>
                  </div>
                </div>

                {/* Additional Information Section */}
                <div>
                  <h2 className="text-lg font-semibold text-gray-900 mb-4 border-b border-gray-100 pb-2">Informações Adicionais</h2>
                  <div className="grid grid-cols-1 gap-6">
                    <div>
                      <label htmlFor="componentes_criticos" className="block text-sm font-medium text-gray-700 mb-1">Componentes Críticos</label>
                      <Field
                        type="text"
                        name="componentes_criticos"
                        id="componentes_criticos"
                        className="input-field w-full"
                        placeholder="Ex: Rolamento dianteiro, Rolamento traseiro, Estator (separados por vírgula)"
                      />
                      <p className="mt-1 text-sm text-gray-600">Separe os componentes por vírgula</p>
                    </div>

                    <div>
                      <label htmlFor="notas" className="block text-sm font-medium text-gray-700 mb-1">Notas e Observações</label>
                      <Field
                        as="textarea"
                        name="notas"
                        id="notas"
                        rows="4"
                        className="input-field w-full"
                        placeholder="Informações adicionais sobre o equipamento..."
                      />
                    </div>
                  </div>
                </div>

                {/* Form Actions */}
                <div className="flex justify-end space-x-3">
                  <Link 
                    to="/equipment" 
                    className="btn-outline flex items-center px-4 py-2 shadow-sm hover:shadow-md transition-all duration-200"
                  >
                    <FiX className="mr-2" />
                    Cancelar
                  </Link>
                  <button 
                    type="submit" 
                    className="btn-primary flex items-center px-4 py-2 shadow-sm hover:shadow-md transition-all duration-200" 
                    disabled={isSubmitting}
                  >
                    <FiSave className="mr-2" />
                    {isSubmitting ? 'Salvando...' : 'Salvar Equipamento'}
                  </button>
                </div>
              </Form>
            )}
          </Formik>
        </div>
      </motion.div>
    </motion.div>
  );
}

export default EquipmentAdd;