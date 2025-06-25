import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiUser, FiMail, FiPhone, FiBell, FiEdit2, FiSave, FiX, FiBarChart2 } from 'react-icons/fi';
import { useAuth } from '../../contexts/AuthContext';
import { authService } from '../../services/api';

function Profile() {
  const { currentUser, updateUserProfile } = useAuth();
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [userStats, setUserStats] = useState({
    totalEquipment: 0,
    totalAlerts: 0,
    totalReports: 0,
    lastLogin: null
  });
  
  const [formData, setFormData] = useState({
    displayName: '',
    email: '',
    phoneNumber: '',
    companyName: '',
    notificationPreferences: {
      email: true,
      whatsapp: false,
      highRiskOnly: false
    }
  });

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

  // Carregar dados do usuário
  useEffect(() => {
    const loadUserData = async () => {
      try {
        setLoading(true);
        
        // Em um ambiente real, descomentar estas linhas para buscar dados do backend
        // const userResponse = await authService.getCurrentUser();
        // const userData = userResponse.data;
        
        // Dados de exemplo para demonstração
        const userData = {
          displayName: currentUser?.displayName || 'Usuário AgroGuard',
          email: currentUser?.email || 'usuario@agroguard.com',
          phoneNumber: '+55 (11) 98765-4321',
          companyName: 'Fazenda Modelo Ltda.',
          notificationPreferences: {
            email: true,
            whatsapp: true,
            highRiskOnly: false
          },
          stats: {
            totalEquipment: 12,
            totalAlerts: 28,
            totalReports: 15,
            lastLogin: new Date('2024-05-15T08:30:00')
          }
        };
        
        setFormData({
          displayName: userData.displayName,
          email: userData.email,
          phoneNumber: userData.phoneNumber || '',
          companyName: userData.companyName || '',
          notificationPreferences: userData.notificationPreferences || {
            email: true,
            whatsapp: false,
            highRiskOnly: false
          }
        });
        
        setUserStats(userData.stats || {
          totalEquipment: 0,
          totalAlerts: 0,
          totalReports: 0,
          lastLogin: null
        });
        
        setLoading(false);
      } catch (error) {
        console.error('Erro ao carregar dados do usuário:', error);
        setLoading(false);
      }
    };

    loadUserData();
  }, [currentUser]);

  // Manipular mudanças no formulário
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  // Manipular mudanças nas preferências de notificação
  const handleNotificationChange = (e) => {
    const { name, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      notificationPreferences: {
        ...prev.notificationPreferences,
        [name]: checked
      }
    }));
  };

  // Salvar alterações
  const handleSave = async () => {
    try {
      setSaving(true);
      
      // Em um ambiente real, descomentar estas linhas para atualizar dados no backend
      // await authService.updateUser({
      //   display_name: formData.displayName,
      //   phone_number: formData.phoneNumber,
      //   company_name: formData.companyName,
      //   notification_preferences: formData.notificationPreferences
      // });
      
      // Simulação de atualização
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Atualizar contexto de autenticação
      if (updateUserProfile) {
        updateUserProfile({
          displayName: formData.displayName
        });
      }
      
      setSaving(false);
      setEditing(false);
      
      // Exibir mensagem de sucesso
      alert('Perfil atualizado com sucesso!');
      
    } catch (error) {
      console.error('Erro ao atualizar perfil:', error);
      setSaving(false);
      alert('Erro ao atualizar perfil. Tente novamente.');
    }
  };

  // Cancelar edição
  const handleCancel = () => {
    // Recarregar dados originais
    setEditing(false);
  };

  // Formatar data
  const formatDate = (date) => {
    if (!date) return 'N/A';
    return new Date(date).toLocaleString('pt-BR');
  };

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-6"
    >
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Perfil do Usuário</h1>
        {!editing && (
          <button
            onClick={() => setEditing(true)}
            className="flex items-center px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
          >
            <FiEdit2 className="mr-2" /> Editar Perfil
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Informações do Perfil */}
        <motion.div variants={itemVariants} className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-100 lg:col-span-2">
          <div className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Informações Pessoais</h2>
            
            {loading ? (
              <p className="text-center py-4">Carregando dados do usuário...</p>
            ) : (
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="displayName" className="block text-sm font-medium text-gray-900 mb-1">Nome Completo</label>
                    {editing ? (
                      <input
                        type="text"
                        id="displayName"
                        name="displayName"
                        value={formData.displayName}
                        onChange={handleInputChange}
                        className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                    ) : (
                      <div className="flex items-center">
                        <FiUser className="text-gray-400 mr-2" />
                        <span className="text-gray-900">{formData.displayName}</span>
                      </div>
                    )}
                  </div>
                  
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-gray-900 mb-1">E-mail</label>
                    <div className="flex items-center">
                      <FiMail className="text-gray-400 mr-2" />
                      <span className="text-gray-900">{formData.email}</span>
                    </div>
                  </div>
                  
                  <div>
                    <label htmlFor="phoneNumber" className="block text-sm font-medium text-gray-900 mb-1">Telefone</label>
                    {editing ? (
                      <input
                        type="text"
                        id="phoneNumber"
                        name="phoneNumber"
                        value={formData.phoneNumber}
                        onChange={handleInputChange}
                        className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                    ) : (
                      <div className="flex items-center">
                        <FiPhone className="text-gray-400 mr-2" />
                        <span className="text-gray-900">{formData.phoneNumber || 'Não informado'}</span>
                      </div>
                    )}
                  </div>
                  
                  <div>
                    <label htmlFor="companyName" className="block text-sm font-medium text-gray-900 mb-1">Empresa</label>
                    {editing ? (
                      <input
                        type="text"
                        id="companyName"
                        name="companyName"
                        value={formData.companyName}
                        onChange={handleInputChange}
                        className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                    ) : (
                      <div className="flex items-center">
                        <span className="text-gray-900">{formData.companyName || 'Não informado'}</span>
                      </div>
                    )}
                  </div>
                </div>
                
                {editing && (
                  <div className="flex justify-end space-x-3 pt-4">
                    <button
                      onClick={handleCancel}
                      className="flex items-center px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-all duration-200"
                      disabled={saving}
                    >
                      <FiX className="mr-2" /> Cancelar
                    </button>
                    <button
                      onClick={handleSave}
                      className="flex items-center px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-all duration-200 shadow-sm"
                      disabled={saving}
                    >
                      {saving ? 'Salvando...' : (
                        <>
                          <FiSave className="mr-2" /> Salvar Alterações
                        </>
                      )}
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </motion.div>

        {/* Estatísticas do Usuário */}
        <motion.div variants={itemVariants} className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-100">
          <div className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Estatísticas</h2>
            {loading ? (
              <p className="text-center py-4">Carregando estatísticas...</p>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center justify-between py-2 border-b border-gray-200">
                  <span className="text-sm text-gray-600">Equipamentos Cadastrados</span>
                  <span className="text-sm font-medium text-gray-900">{userStats.totalEquipment}</span>
                </div>
                <div className="flex items-center justify-between py-2 border-b border-gray-200">
                  <span className="text-sm text-gray-600">Alertas Recebidos</span>
                  <span className="text-sm font-medium text-gray-900">{userStats.totalAlerts}</span>
                </div>
                <div className="flex items-center justify-between py-2 border-b border-gray-200">
                  <span className="text-sm text-gray-600">Relatórios Gerados</span>
                  <span className="text-sm font-medium text-gray-900">{userStats.totalReports}</span>
                </div>
                <div className="flex items-center justify-between py-2">
                  <span className="text-sm text-gray-600">Último Acesso</span>
                  <span className="text-sm font-medium text-gray-900">{formatDate(userStats.lastLogin)}</span>
                </div>
              </div>
            )}
          </div>
        </motion.div>
      </div>

      {/* Preferências de Notificação */}
      <motion.div variants={itemVariants} className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-100">
        <div className="p-6">
          <div className="flex items-center mb-4">
            <FiBell className="text-primary-500 mr-2" />
            <h2 className="text-lg font-semibold text-gray-900">Preferências de Notificação</h2>
          </div>
          
          {loading ? (
            <p className="text-center py-4">Carregando preferências...</p>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="email"
                  name="email"
                  checked={formData.notificationPreferences.email}
                  onChange={handleNotificationChange}
                  disabled={!editing}
                  className="h-5 w-5 text-primary-600 focus:ring-primary-500 border-gray-300 rounded cursor-pointer"
                />
                <label htmlFor="email" className="ml-2 block text-sm text-gray-900 font-medium">
                  Receber notificações por e-mail
                </label>
              </div>
              
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="whatsapp"
                  name="whatsapp"
                  checked={formData.notificationPreferences.whatsapp}
                  onChange={handleNotificationChange}
                  disabled={!editing}
                  className="h-5 w-5 text-primary-600 focus:ring-primary-500 border-gray-300 rounded cursor-pointer"
                />
                <label htmlFor="whatsapp" className="ml-2 block text-sm text-gray-900 font-medium">
                  Receber notificações por WhatsApp
                </label>
              </div>
              
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="highRiskOnly"
                  name="highRiskOnly"
                  checked={formData.notificationPreferences.highRiskOnly}
                  onChange={handleNotificationChange}
                  disabled={!editing}
                  className="h-5 w-5 text-primary-600 focus:ring-primary-500 border-gray-300 rounded cursor-pointer"
                />
                <label htmlFor="highRiskOnly" className="ml-2 block text-sm text-gray-900 font-medium">
                  Receber apenas alertas de alto risco
                </label>
              </div>
              
              <div className="mt-4 text-sm text-gray-700">
                <p>As notificações incluem alertas de risco, lembretes de manutenção e relatórios automáticos.</p>
              </div>
            </div>
          )}
        </div>
      </motion.div>
    </motion.div>
  );
}

export default Profile;