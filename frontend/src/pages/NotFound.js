import React from 'react';
import { Link } from 'react-router-dom';

function NotFound() {
  return (
    <div className="flex items-center justify-center h-screen bg-gray-900 text-white">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-red-500">404</h1>
        <p className="text-xl mt-4">Page Not Found</p>
        <p className="text-gray-400 mt-2">The page you are looking for does not exist.</p>
        <Link to="/dashboard" className="mt-6 inline-block bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Go to Dashboard
        </Link>
      </div>
    </div>
  );
}

export default NotFound;