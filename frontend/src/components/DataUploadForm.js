import React, { useState } from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { motion } from 'framer-motion';
import { FiUpload, FiCheck, FiAlertTriangle, FiX } from 'react-icons/fi';
import { ref, uploadBytes, getDownloadURL } from 'firebase/storage';
import { collection, addDoc, serverTimestamp } from 'firebase/firestore';
import { storage, db } from '../firebase';
import { useAuth } from '../contexts/AuthContext';

const DataUploadForm = ({ onSuccess, equipmentId }) => {
  const { currentUser } = useAuth();
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStatus, setUploadStatus] = useState(null); // 'success', 'error', or null
  const [uploadMessage, setUploadMessage] = useState('');

  // File validation schema
  const validationSchema = Yup.object({
    file: Yup.mixed()
      .required('Arquivo é obrigatório')
      .test(
        'fileFormat',
        'Formato não suportado. Use CSV ou Excel (xlsx/xls)',
        (value) => {
          if (!value) return false;
          const supportedFormats = ['text/csv', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
          return supportedFormats.includes(value.type) || value.name.endsWith('.csv') || value.name.endsWith('.xlsx') || value.name.endsWith('.xls');
        }
      )
      .test(
        'fileSize',
        'Arquivo muito grande. Máximo 5MB',
        (value) => {
          if (!value) return false;
          return value.size <= 5 * 1024 * 1024; // 5MB
        }
      ),
    equipmentId: Yup.string().when('allEquipment', {
      is: false,
      then: () => Yup.string().required('Selecione um equipamento'),
      otherwise: () => Yup.string().notRequired(),
    }),
    allEquipment: Yup.boolean(),
    dataType: Yup.string().required('Tipo de dados é obrigatório'),
  });

  // Initial form values
  const initialValues = {
    file: null,
    equipmentId: equipmentId || '',
    allEquipment: !equipmentId,
    dataType: 'operational', // 'operational', 'maintenance', 'failure'
  };

  // Handle form submission
  const handleSubmit = async (values, { setSubmitting, resetForm }) => {
    try {
      setUploadStatus(null);
      setUploadMessage('');
      setUploadProgress(0);

      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 300);

      // In a real app, upload to Firebase Storage
      // const fileRef = ref(storage, `uploads/${currentUser.uid}/${Date.now()}_${values.file.name}`);
      // await uploadBytes(fileRef, values.file);
      // const downloadURL = await getDownloadURL(fileRef);

      // Record the upload in Firestore
      // const uploadData = {
      //   userId: currentUser.uid,
      //   equipmentId: values.equipmentId || 'all',
      //   fileName: values.file.name,
      //   fileSize: values.file.size,
      //   fileType: values.file.type,
      //   fileUrl: downloadURL,
      //   dataType: values.dataType,
      //   uploadedAt: serverTimestamp(),
      //   status: 'pending', // 'pending', 'processed', 'error'
      // };
      // await addDoc(collection(db, 'dataUploads'), uploadData);

      // Simulate processing delay
      setTimeout(() => {
        clearInterval(progressInterval);
        setUploadProgress(100);
        setUploadStatus('success');
        setUploadMessage('Arquivo enviado com sucesso! Os dados serão processados em breve.');
        
        // Call success callback if provided
        if (onSuccess) {
          onSuccess({
            fileName: values.file.name,
            dataType: values.dataType,
            timestamp: new Date().toISOString(),
          });
        }

        // Reset form after 3 seconds
        setTimeout(() => {
          resetForm();
          setUploadProgress(0);
        }, 3000);
      }, 2000);

    } catch (error) {
      console.error('Error uploading file:', error);
      setUploadStatus('error');
      setUploadMessage('Erro ao enviar arquivo. Por favor, tente novamente.');
      setUploadProgress(0);
    } finally {
      setSubmitting(false);
    }
  };

  // Data type options
  const dataTypeOptions = [
    { value: 'operational', label: 'Dados Operacionais (horas, temperatura, vibração)' },
    { value: 'maintenance', label: 'Registros de Manutenção' },
    { value: 'failure', label: 'Registros de Falhas' },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="bg-white rounded-lg shadow-sm overflow-hidden"
    >
      <div className="p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Upload de Dados</h2>
        
        <Formik
          initialValues={initialValues}
          validationSchema={validationSchema}
          onSubmit={handleSubmit}
        >
          {({ isSubmitting, setFieldValue, values, errors, touched }) => (
            <Form className="space-y-6">
              {/* File Upload */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Arquivo CSV/Excel*</label>
                <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                  <div className="space-y-1 text-center">
                    <svg
                      className="mx-auto h-12 w-12 text-gray-400"
                      stroke="currentColor"
                      fill="none"
                      viewBox="0 0 48 48"
                      aria-hidden="true"
                    >
                      <path
                        d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                        strokeWidth={2}
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                    <div className="flex text-sm text-gray-600">
                      <label
                        htmlFor="file-upload"
                        className="relative cursor-pointer bg-white rounded-md font-medium text-primary-600 hover:text-primary-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500"
                      >
                        <span>Selecionar arquivo</span>
                        <input
                          id="file-upload"
                          name="file-upload"
                          type="file"
                          className="sr-only"
                          accept=".csv,.xlsx,.xls"
                          onChange={(event) => {
                            setFieldValue('file', event.currentTarget.files[0]);
                          }}
                        />
                      </label>
                      <p className="pl-1">ou arraste e solte</p>
                    </div>
                    <p className="text-xs text-gray-500">CSV, XLS ou XLSX até 5MB</p>
                    {values.file && (
                      <p className="text-sm text-gray-800 mt-2">
                        Arquivo selecionado: {values.file.name}
                      </p>
                    )}
                  </div>
                </div>
                {errors.file && touched.file ? (
                  <div className="text-red-500 text-sm mt-1">{errors.file}</div>
                ) : null}
              </div>

              {/* Data Type */}
              <div>
                <label htmlFor="dataType" className="block text-sm font-medium text-gray-700 mb-1">Tipo de Dados*</label>
                <Field
                  as="select"
                  name="dataType"
                  id="dataType"
                  className="input-field w-full"
                >
                  {dataTypeOptions.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </Field>
                <ErrorMessage name="dataType" component="div" className="text-red-500 text-sm mt-1" />
              </div>

              {/* Equipment Selection (only if not provided via props) */}
              {!equipmentId && (
                <div>
                  <div className="flex items-center mb-4">
                    <Field
                      type="checkbox"
                      name="allEquipment"
                      id="allEquipment"
                      className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    />
                    <label htmlFor="allEquipment" className="ml-2 block text-sm text-gray-700">
                      Aplicar a todos os equipamentos
                    </label>
                  </div>
                  
                  {!values.allEquipment && (
                    <div>
                      <label htmlFor="equipmentId" className="block text-sm font-medium text-gray-700 mb-1">Selecione o Equipamento*</label>
                      <Field
                        as="select"
                        name="equipmentId"
                        id="equipmentId"
                        className="input-field w-full"
                      >
                        <option value="">Selecione um equipamento</option>
                        <option value="demo1">Motor WEG W22</option>
                        <option value="demo2">Bomba Hidráulica KSB</option>
                        <option value="demo3">Compressor Atlas Copco</option>
                      </Field>
                      <ErrorMessage name="equipmentId" component="div" className="text-red-500 text-sm mt-1" />
                    </div>
                  )}
                </div>
              )}

              {/* Upload Progress */}
              {uploadProgress > 0 && uploadProgress < 100 && (
                <div className="mt-4">
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div
                      className="bg-primary-600 h-2.5 rounded-full"
                      style={{ width: `${uploadProgress}%` }}
                    ></div>
                  </div>
                  <p className="text-sm text-gray-500 mt-1">Enviando... {uploadProgress}%</p>
                </div>
              )}

              {/* Status Messages */}
              {uploadStatus === 'success' && (
                <div className="flex items-center text-green-600 mt-2">
                  <FiCheck className="h-5 w-5 mr-2" />
                  <span>{uploadMessage}</span>
                </div>
              )}

              {uploadStatus === 'error' && (
                <div className="flex items-center text-red-600 mt-2">
                  <FiAlertTriangle className="h-5 w-5 mr-2" />
                  <span>{uploadMessage}</span>
                </div>
              )}

              {/* Submit Button */}
              <div className="flex justify-end">
                <button
                  type="submit"
                  disabled={isSubmitting || uploadProgress > 0}
                  className="btn-primary flex items-center px-4 py-2"
                >
                  <FiUpload className="mr-2" />
                  {isSubmitting ? 'Enviando...' : 'Enviar Dados'}
                </button>
              </div>
            </Form>
          )}
        </Formik>
      </div>
    </motion.div>
  );
};

export default DataUploadForm;