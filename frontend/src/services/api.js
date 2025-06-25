import axios from 'axios';
import { getAuth } from 'firebase/auth';

// Cria uma instância do axios com a URL base da API
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar o token de autenticação em todas as requisições
api.interceptors.request.use(async (config) => {
  try {
    const auth = getAuth();
    const user = auth.currentUser;
    
    if (user) {
      const token = await user.getIdToken();
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  } catch (error) {
    console.error('Erro ao obter token de autenticação:', error);
    return config;
  }
});

// Interceptor para tratar erros de resposta
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Se o erro for 401 (Não autorizado) e não for uma requisição de retry
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const auth = getAuth();
        const user = auth.currentUser;
        
        if (user) {
          // Força a atualização do token
          const newToken = await user.getIdToken(true);
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        console.error('Erro ao atualizar token:', refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

// Serviços de autenticação
export const authService = {
  register: (userData) => api.post('/auth/register', userData),
  login: (email, password) => api.post('/auth/login/email', { email, password }),
  forgotPassword: (email) => api.post('/auth/forgot-password', { email }),
  resetPassword: (email, code, newPassword) => 
    api.post('/auth/reset-password', { email, code, new_password: newPassword }),
  getCurrentUser: () => api.get('/auth/me'),
  updateUser: (userData) => api.put('/auth/me', userData),
  logout: () => api.post('/auth/logout'),
};

// Serviços de equipamentos
export const equipmentService = {
  getAllEquipment: (filters = {}) => api.get('/equipment', { params: filters }),
  getEquipmentById: (id) => api.get(`/equipment/${id}`),
  createEquipment: (data) => api.post('/equipment', data),
  updateEquipment: (id, data) => api.put(`/equipment/${id}`, data),
  deleteEquipment: (id) => api.delete(`/equipment/${id}`),
  getEquipmentStats: () => api.get('/equipment/stats'),
  addOperationalData: (id, data) => api.post(`/equipment/${id}/operational-data`, data),
  analyzeEquipmentHealth: (id) => api.get(`/equipment/${id}/health-analysis`),
  addComponent: (id, data) => api.post(`/equipment/${id}/components`, data),
  updateComponent: (equipmentId, componentId, data) => 
    api.put(`/equipment/${equipmentId}/components/${componentId}`, data),
  removeComponent: (equipmentId, componentId) => 
    api.delete(`/equipment/${equipmentId}/components/${componentId}`),
};

// Serviços de alertas
export const alertService = {
  getAllAlerts: (filters = {}) => api.get('/alerts', { params: filters }),
  getAlertById: (id) => api.get(`/alerts/${id}`),
  createAlert: (data) => api.post('/alerts', data),
  updateAlert: (id, data) => api.put(`/alerts/${id}`, data),
  deleteAlert: (id) => api.delete(`/alerts/${id}`),
  getAlertStats: () => api.get('/alerts/stats'),
  getRecentAlerts: (limit = 5) => api.get('/alerts/recent', { params: { limit } }),
  resolveAlert: (id, notes) => api.post(`/alerts/${id}/resolve`, { notes }),
  generateAlerts: (equipmentId = null) => 
    api.post('/alerts/generate', null, { params: { equipment_id: equipmentId } }),
  sendNotification: (id) => api.post(`/alerts/${id}/notify`),
};

// Serviços de manutenção
export const maintenanceService = {
  getAllMaintenance: (filters = {}) => api.get('/maintenance', { params: filters }),
  getMaintenanceById: (id) => api.get(`/maintenance/${id}`),
  createMaintenance: (data) => api.post('/maintenance', data),
  updateMaintenance: (id, data) => api.put(`/maintenance/${id}`, data),
  deleteMaintenance: (id) => api.delete(`/maintenance/${id}`),
  getMaintenanceStats: () => api.get('/maintenance/stats'),
  getUpcomingMaintenance: (days = 30) => 
    api.get('/maintenance/upcoming', { params: { days } }),
  completeMaintenance: (id, data) => api.post(`/maintenance/${id}/complete`, data),
  scheduleMaintenance: (equipmentId = null) => 
    api.post('/maintenance/schedule', null, { params: { equipment_id: equipmentId } }),
  getEquipmentMaintenanceHistory: (equipmentId, limit = 10) => 
    api.get(`/maintenance/equipment/${equipmentId}`, { params: { limit } }),
};

// Serviços de relatórios
export const reportService = {
  getAllReports: (filters = {}) => api.get('/reports', { params: filters }),
  getReportById: (id) => api.get(`/reports/${id}`),
  createReport: (data) => api.post('/reports', data),
  updateReport: (id, data) => api.put(`/reports/${id}`, data),
  deleteReport: (id) => api.delete(`/reports/${id}`),
  generateHealthReport: (equipmentId) => 
    api.post('/reports/generate/health', null, { params: { equipment_id: equipmentId } }),
  generateMaintenanceReport: (equipmentId, fromDate = null, toDate = null) => 
    api.post('/reports/generate/maintenance', null, { 
      params: { 
        equipment_id: equipmentId,
        from_date: fromDate,
        to_date: toDate 
      } 
    }),
  generatePredictionReport: (equipmentId, daysAhead = 90) => 
    api.post('/reports/generate/prediction', null, { 
      params: { 
        equipment_id: equipmentId,
        days_ahead: daysAhead 
      } 
    }),
  generateSummaryReport: (fromDate = null, toDate = null) => 
    api.post('/reports/generate/summary', null, { 
      params: { 
        from_date: fromDate,
        to_date: toDate 
      } 
    }),
  generatePdfReport: (reportId) => api.get(`/reports/${reportId}/pdf`),
  getEquipmentReports: (equipmentId, limit = 10) => 
    api.get(`/reports/equipment/${equipmentId}`, { params: { limit } }),
};

// Serviços de IA
export const aiService = {
  predictEquipmentFailure: (equipmentId, daysAhead = 30) => 
    api.get(`/ai/predict/${equipmentId}`, { params: { days_ahead: daysAhead } }),
  recommendMaintenanceSchedule: (equipmentId) => 
    api.get(`/ai/maintenance-schedule/${equipmentId}`),
  analyzeOperationalData: (equipmentId) => 
    api.get(`/ai/analyze/${equipmentId}`),
  trainCustomModel: (equipmentId) => 
    api.post(`/ai/train/${equipmentId}`),
};

export default api;