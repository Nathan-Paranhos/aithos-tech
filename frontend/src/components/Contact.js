import React from 'react';
import { motion } from 'framer-motion';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import emailjs from '@emailjs/browser';

const Contact = () => {
  const formik = useFormik({
    initialValues: {
      name: '',
      email: '',
      message: '',
    },
    validationSchema: Yup.object({
      name: Yup.string().required('O nome é obrigatório'),
      email: Yup.string().email('Email inválido').required('O email é obrigatório'),
      message: Yup.string().required('A mensagem é obrigatória'),
    }),
    onSubmit: (values, { resetForm, setSubmitting }) => {
      emailjs.send(
        'YOUR_SERVICE_ID', // Replace with your EmailJS Service ID
        'YOUR_TEMPLATE_ID', // Replace with your EmailJS Template ID
        values,
        'YOUR_PUBLIC_KEY' // Replace with your EmailJS Public Key
      )
      .then((result) => {
          alert('Mensagem enviada com sucesso!');
          resetForm();
      }, (error) => {
          alert('Falha ao enviar mensagem: ' + error.text);
      })
      .finally(() => {
        setSubmitting(false);
      });
    },
  });

  return (
    <section className="py-20 bg-gray-900 text-white">
      <div className="container mx-auto px-4">
        <motion.h2
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          viewport={{ once: true, amount: 0.5 }}
          className="text-4xl md:text-5xl font-extrabold mb-12 text-center text-burgundy-500"
        >
          Entre em Contato
        </motion.h2>
        <motion.form
          onSubmit={formik.handleSubmit}
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2, ease: "easeOut" }}
          viewport={{ once: true, amount: 0.5 }}
          className="max-w-lg mx-auto bg-black p-8 rounded-lg shadow-lg border border-burgundy-700"
        >
          <div className="mb-4">
            <label htmlFor="name" className="block text-gray-300 text-sm font-bold mb-2">Nome:</label>
            <input
              type="text"
              id="name"
              name="name"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline bg-gray-800 border-gray-700"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.name}
            />
            {formik.touched.name && formik.errors.name ? (
              <div className="text-red-500 text-xs mt-1">{formik.errors.name}</div>
            ) : null}
          </div>

          <div className="mb-4">
            <label htmlFor="email" className="block text-gray-300 text-sm font-bold mb-2">Email:</label>
            <input
              type="email"
              id="email"
              name="email"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline bg-gray-800 border-gray-700"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.email}
            />
            {formik.touched.email && formik.errors.email ? (
              <div className="text-red-500 text-xs mt-1">{formik.errors.email}</div>
            ) : null}
          </div>

          <div className="mb-6">
            <label htmlFor="message" className="block text-gray-300 text-sm font-bold mb-2">Mensagem:</label>
            <textarea
              id="message"
              name="message"
              rows="5"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline bg-gray-800 border-gray-700"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.message}
            ></textarea>
            {formik.touched.message && formik.errors.message ? (
              <div className="text-red-500 text-xs mt-1">{formik.errors.message}</div>
            ) : null}
          </div>

          <div className="flex items-center justify-between">
            <button
              type="submit"
              className="bg-burgundy-600 hover:bg-burgundy-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              disabled={formik.isSubmitting}
            >
              {formik.isSubmitting ? 'Enviando...' : 'Enviar Mensagem'}
            </button>
          </div>
        </motion.form>
      </div>
    </section>
  );
};

export default Contact;