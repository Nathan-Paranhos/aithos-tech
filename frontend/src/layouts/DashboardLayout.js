import React, { useState, useEffect } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { motion } from 'framer-motion';
import { 
  FiHome, 
  FiTruck, 
  FiFileText, 
  FiUser, 
  FiLogOut, 
  FiMenu, 
  FiX, 
  FiBell 
} from 'react-icons/fi';

const DashboardLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [userData, setUserData] = useState(null);
  const { currentUser, logout, getUserData } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      const data = await getUserData();
      setUserData(data);
    };

    fetchUserData();
  }, [getUserData]);

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Falha ao sair:', error);
    }
  };

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: FiHome },
    { name: 'Equipamentos', href: '/equipment', icon: FiTruck },
    { name: 'Relatórios', href: '/reports', icon: FiFileText },
    { name: 'Perfil', href: '/profile', icon: FiUser },
  ];

  return (
    <div className="h-screen flex overflow-hidden bg-white">
      {/* Sidebar for mobile */}
      <div className="md:hidden">
        {sidebarOpen && (
          <div className="fixed inset-0 flex z-40">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="fixed inset-0"
              onClick={() => setSidebarOpen(false)}
            >
              <div className="absolute inset-0 bg-gray-600 opacity-75"></div>
            </motion.div>
            
            <motion.div
              initial={{ x: -300 }}
              animate={{ x: 0 }}
              exit={{ x: -300 }}
              transition={{ duration: 0.3 }}
              className="relative flex-1 flex flex-col max-w-xs w-full bg-primary-800"
            >
              <div className="absolute top-0 right-0 -mr-12 pt-2">
                <button
                  className="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
                  onClick={() => setSidebarOpen(false)}
                >
                  <span className="sr-only">Fechar menu</span>
                  <FiX className="h-6 w-6 text-white" />
                </button>
              </div>
              
              <div className="flex-1 h-0 pt-5 pb-4 overflow-y-auto">
                <div className="flex-shrink-0 flex items-center px-4">
                <h1 className="text-2xl font-bold text-white">AgroGuard</h1>
              </div>
                <nav className="mt-5 px-2 space-y-1">
                  {navigation.map((item) => {
                    const isActive = location.pathname === item.href;
                    return (
                      <Link
                        key={item.name}
                        to={item.href}
                        className={`group flex items-center px-2 py-2 text-base font-medium rounded-md ${isActive ? 'bg-primary-900 text-white' : 'text-primary-100 hover:bg-primary-700'}`}
                      >
                        <item.icon className={`mr-4 h-6 w-6 ${isActive ? 'text-white' : 'text-primary-300 group-hover:text-white'}`} />
                        {item.name}
                      </Link>
                    );
                  })}
                </nav>
              </div>
              
              <div className="flex-shrink-0 flex border-t border-primary-700 p-4">
                <div className="flex items-center">
                  <div>
                    <div className="bg-primary-900 rounded-full h-10 w-10 flex items-center justify-center text-white font-bold">
                      {currentUser?.displayName?.charAt(0) || 'U'}
                    </div>
                  </div>
                  <div className="ml-3">
                    <p className="text-base font-medium text-white">
                      {currentUser?.displayName || 'Usuário'}
                    </p>
                    <p className="text-sm font-medium text-primary-200">
                      {userData?.companyName || 'Empresa'}
                    </p>
                  </div>
                </div>
                <button
                  onClick={handleLogout}
                  className="ml-auto flex items-center justify-center bg-primary-700 rounded-md p-1 hover:bg-primary-600"
                >
                  <FiLogOut className="h-6 w-6 text-white" />
                </button>
              </div>
            </motion.div>
            
            <div className="flex-shrink-0 w-14">
              {/* Force sidebar to shrink to fit close icon */}
            </div>
          </div>
        )}
      </div>

      {/* Static sidebar for desktop */}
      <div className="hidden md:flex md:flex-shrink-0">
        <div className="flex flex-col w-64">
          <div className="flex flex-col h-0 flex-1 bg-primary-800">
            <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
              <div className="flex items-center flex-shrink-0 px-4">
                <h1 className="text-2xl font-bold text-white">AgroGuard</h1>
              </div>
              <nav className="mt-5 flex-1 px-2 space-y-1">
                {navigation.map((item) => {
                  const isActive = location.pathname === item.href;
                  return (
                    <Link
                      key={item.name}
                      to={item.href}
                      className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md ${isActive ? 'bg-primary-900 text-white' : 'text-primary-100 hover:bg-primary-700'}`}
                    >
                      <item.icon className={`mr-3 h-5 w-5 ${isActive ? 'text-white' : 'text-primary-300 group-hover:text-white'}`} />
                      {item.name}
                    </Link>
                  );
                })}
              </nav>
            </div>
            <div className="flex-shrink-0 flex border-t border-primary-700 p-4">
              <div className="flex items-center">
                <div>
                  <div className="bg-primary-900 rounded-full h-9 w-9 flex items-center justify-center text-white font-bold">
                    {currentUser?.displayName?.charAt(0) || 'U'}
                  </div>
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-white">
                    {currentUser?.displayName || 'Usuário'}
                  </p>
                  <p className="text-xs font-medium text-primary-200">
                    {userData?.companyName || 'Empresa'}
                  </p>
                </div>
                <button
                  onClick={handleLogout}
                  className="ml-auto flex items-center justify-center bg-primary-700 rounded-md p-1 hover:bg-primary-600"
                >
                  <FiLogOut className="h-5 w-5 text-white" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex flex-col w-0 flex-1 overflow-hidden">
        <div className="md:hidden pl-1 pt-1 sm:pl-3 sm:pt-3">
          <button
            className="-ml-0.5 -mt-0.5 h-12 w-12 inline-flex items-center justify-center rounded-md text-gray-500 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
            onClick={() => setSidebarOpen(true)}
          >
            <span className="sr-only">Abrir menu</span>
            <FiMenu className="h-6 w-6" />
          </button>
        </div>

        {/* Top navbar */}
        <div className="relative z-10 flex-shrink-0 flex h-16 bg-white shadow-sm">
          <div className="flex-1 px-4 flex justify-between">
            <div className="flex-1 flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                {navigation.find(item => item.href === location.pathname)?.name || 'AgroGuard'}
              </h1>
            </div>
            <div className="ml-4 flex items-center md:ml-6">
              <button className="p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                <span className="sr-only">Ver notificações</span>
                <FiBell className="h-6 w-6" />
              </button>
            </div>
          </div>
        </div>

        {/* Main content area */}
        <main className="flex-1 relative overflow-y-auto focus:outline-none">
          <div className="py-6">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
              <Outlet />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;