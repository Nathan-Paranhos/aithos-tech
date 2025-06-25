import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { motion } from 'framer-motion';
import { FiUser, FiMail, FiLock, FiBriefcase, FiAlertCircle } from 'react-icons/fi';

const Register = () => {
  const { signup } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const validationSchema = Yup.object().shape({
    name: Yup.string()
      .required('Nome é obrigatório')
      .min(2, 'Nome deve ter pelo menos 2 caracteres'),
    companyName: Yup.string()
      .required('Nome da empresa é obrigatório')
      .min(2, 'Nome da empresa deve ter pelo menos 2 caracteres'),
    email: Yup.string()
      .email('Email inválido')
      .required('Email é obrigatório'),
    password: Yup.string()
      .required('Senha é obrigatória')
      .min(6, 'Senha deve ter pelo menos 6 caracteres'),
    confirmPassword: Yup.string()
      .oneOf([Yup.ref('password'), null], 'Senhas não conferem')
      .required('Confirmação de senha é obrigatória'),
  });

  const handleSubmit = async (values) => {
    try {
      setError('');
      setLoading(true);
      await signup(values.email, values.password, values.name, values.companyName);
      navigate('/dashboard');
    } catch (error) {
      console.error('Erro ao registrar:', error);
      setError('Falha ao criar conta. ' + (error.message || 'Tente novamente mais tarde.'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-2 text-center text-3xl font-extrabold text-gray-900">Criar nova conta</h2>
      </div>

      {error && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-md bg-red-50 p-4 mt-4"
        >
          <div className="flex">
            <div className="flex-shrink-0">
              <FiAlertCircle className="h-5 w-5 text-red-400" />
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">{error}</h3>
            </div>
          </div>
        </motion.div>
      )}

      <Formik
        initialValues={{
          name: '',
          companyName: '',
          email: '',
          password: '',
          confirmPassword: ''
        }}
        validationSchema={validationSchema}
        onSubmit={handleSubmit}
      >
        {({ errors, touched }) => (
          <Form className="space-y-4 mt-6">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                Nome completo
              </label>
              <div className="mt-1 relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <FiUser className="h-5 w-5 text-gray-400" />
                </div>
                <Field
                  type="text"
                  name="name"
                  id="name"
                  className={`block w-full pl-10 pr-3 py-2 border ${errors.name && touched.name ? 'border-red-300' : 'border-gray-300'} rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500`}
                  placeholder="Seu nome"
                />
              </div>
              <ErrorMessage name="name" component="p" className="mt-2 text-sm text-red-600" />
            </div>

            <div>
              <label htmlFor="companyName" className="block text-sm font-medium text-gray-700">
                Nome da empresa
              </label>
              <div className="mt-1 relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <FiBriefcase className="h-5 w-5 text-gray-400" />
                </div>
                <Field
                  type="text"
                  name="companyName"
                  id="companyName"
                  className={`block w-full pl-10 pr-3 py-2 border ${errors.companyName && touched.companyName ? 'border-red-300' : 'border-gray-300'} rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500`}
                  placeholder="Nome da empresa"
                />
              </div>
              <ErrorMessage name="companyName" component="p" className="mt-2 text-sm text-red-600" />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email
              </label>
              <div className="mt-1 relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <FiMail className="h-5 w-5 text-gray-400" />
                </div>
                <Field
                  type="email"
                  name="email"
                  id="email"
                  className={`block w-full pl-10 pr-3 py-2 border ${errors.email && touched.email ? 'border-red-300' : 'border-gray-300'} rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500`}
                  placeholder="seu@email.com"
                />
              </div>
              <ErrorMessage name="email" component="p" className="mt-2 text-sm text-red-600" />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Senha
              </label>
              <div className="mt-1 relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <FiLock className="h-5 w-5 text-gray-400" />
                </div>
                <Field
                  type="password"
                  name="password"
                  id="password"
                  className={`block w-full pl-10 pr-3 py-2 border ${errors.password && touched.password ? 'border-red-300' : 'border-gray-300'} rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500`}
                  placeholder="******"
                />
              </div>
              <ErrorMessage name="password" component="p" className="mt-2 text-sm text-red-600" />
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
                Confirmar senha
              </label>
              <div className="mt-1 relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <FiLock className="h-5 w-5 text-gray-400" />
                </div>
                <Field
                  type="password"
                  name="confirmPassword"
                  id="confirmPassword"
                  className={`block w-full pl-10 pr-3 py-2 border ${errors.confirmPassword && touched.confirmPassword ? 'border-red-300' : 'border-gray-300'} rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500`}
                  placeholder="******"
                />
              </div>
              <ErrorMessage name="confirmPassword" component="p" className="mt-2 text-sm text-red-600" />
            </div>

            <div className="mt-6">
              <button
                type="submit"
                disabled={loading}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Registrando...' : 'Registrar'}
              </button>
            </div>
          </Form>
        )}
      </Formik>

      <div className="mt-6 text-center">
        <p className="text-sm text-gray-600">
          Já tem uma conta?{' '}
          <Link to="/auth/login" className="font-medium text-primary-600 hover:text-primary-500">
            Entrar
          </Link>
        </p>
      </div>
    </>
  );
};

export default Register;