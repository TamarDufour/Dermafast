import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = ({ username, previousLogin, onLogout }) => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center items-center p-4">
      <div className="max-w-md w-full bg-white shadow-md rounded-lg p-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-800 mb-4">
            Hello {username}! Welcome to DermaFast.
          </h1>
          <p className="text-gray-600 mb-8">
            Your previous login was at {previousLogin}.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <button
              onClick={() => navigate('/questionnaire')}
              className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg transition duration-300 ease-in-out transform hover:scale-105"
            >
              Check a new mole
            </button>
            <button className="bg-gray-700 hover:bg-gray-800 text-white font-bold py-2 px-4 rounded-lg transition duration-300 ease-in-out transform hover:scale-105">
              My appointments
            </button>
          </div>
          <div className="mt-8">
            <button
              onClick={onLogout}
              className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition ease-in-out duration-150"
            >
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
