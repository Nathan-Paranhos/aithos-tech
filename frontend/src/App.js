import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { auth } from './firebase';
import { onAuthStateChanged } from 'firebase/auth';

// Layouts
import DashboardLayout from './layouts/DashboardLayout';
import AuthLayout from './layouts/AuthLayout';

// Pages
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import ForgotPassword from './pages/auth/ForgotPassword';
import Dashboard from './pages/dashboard/Dashboard';
import EquipmentList from './pages/equipment/EquipmentList';
import EquipmentDetail from './pages/equipment/EquipmentDetail';
import EquipmentAdd from './pages/equipment/EquipmentAdd';
import Reports from './pages/reports/Reports';
import Profile from './pages/profile/Profile';
import NotFound from './pages/NotFound';
import Hero from './components/Hero';
import Problem from './components/Problem';
import Solution from './components/Solution';
import HowItWorks from './components/HowItWorks';
import DashboardMockup from './components/DashboardMockup';
import NotificationsMockup from './components/NotificationsMockup';
import Validation from './components/Validation';
import Roadmap from './components/Roadmap';
import CTA from './components/CTA';
import Contact from './components/Contact';
import Footer from './components/Footer';
import DataUpload from './pages/DataUpload'; // Import the DataUpload component

// Context
import { AuthProvider } from './contexts/AuthContext';

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setCurrentUser(user);
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  // Protected route component
  const ProtectedRoute = ({ children }) => {
    if (loading) return <div className="flex items-center justify-center h-screen">Carregando...</div>;
    if (!currentUser) return <Navigate to="/auth/login" />;
    return children;
  };

  // Public route component (accessible only when not logged in)
  const PublicRoute = ({ children }) => {
    if (loading) return <div className="flex items-center justify-center h-screen">Carregando...</div>;
    if (currentUser) return <Navigate to="/dashboard" />;
    return children;
  };

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Carregando...</div>;
  }

  return (
    <AuthProvider value={{ currentUser }}>
      <Routes>
        {/* Root Route - Redirect based on authentication status */}
        <Route path="/" element={currentUser ? <Navigate to="/dashboard" /> : <Navigate to="/auth/login" />} />

        {/* Auth Routes */}
        <Route path="/auth" element={<PublicRoute><AuthLayout /></PublicRoute>}>
          <Route index element={<Navigate to="/auth/login" replace />} />
          <Route path="login" element={<Login />} />
          <Route path="register" element={<Register />} />
          <Route path="forgot-password" element={<ForgotPassword />} />
        </Route>
        <Route path="/register" element={<Navigate to="/auth/register" replace />} />
        <Route path="/forgot-password" element={<Navigate to="/auth/forgot-password" replace />} />

        {/* Dashboard Routes */}
        <Route path="/" element={<ProtectedRoute><DashboardLayout /></ProtectedRoute>}>
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="equipment" element={<EquipmentList />} />
          <Route path="equipment/add" element={<EquipmentAdd />} />
          <Route path="equipment/:id" element={<EquipmentDetail />} />
          <Route path="reports" element={<Reports />} />
          <Route path="profile" element={<Profile />} />
          <Route path="data-upload" element={<DataUpload />} /> // Add the new protected route
        </Route>

        {/* 404 Route */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </AuthProvider>
  );
}

export default App;