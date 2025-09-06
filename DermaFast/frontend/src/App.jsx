import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import AuthForm from './components/AuthForm';
import HomePage from './components/HomePage';
import CheckMolePage from './components/CheckMolePage';
import MoleQuestionnairePage from './components/MoleQuestionnairePage';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const checkAuth = () => {
      const token = localStorage.getItem('authToken');
      const userData = localStorage.getItem('userData');
      
      if (token && userData) {
        setIsAuthenticated(true);
        setUser(JSON.parse(userData));
      }
    };
    
    checkAuth();
  }, []);

  const handleLogin = (nationalId) => {
    localStorage.setItem('authToken', 'dummy-token');
    localStorage.setItem('userData', JSON.stringify({ nationalId }));
    setIsAuthenticated(true);
    setUser({ nationalId });
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData');
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route
            path="/login"
            element={!isAuthenticated ? <AuthForm onLogin={handleLogin} /> : <Navigate to="/" />}
          />
          <Route
            path="/"
            element={
              isAuthenticated ? (
                <HomePage
                  username={user?.nationalId}
                  previousLogin={new Date().toLocaleString()}
                  onLogout={handleLogout}
                />
              ) : (
                <Navigate to="/login" />
              )
            }
          />
          <Route
            path="/check-mole"
            element={isAuthenticated ? <CheckMolePage /> : <Navigate to="/login" />}
          />
          <Route
            path="/questionnaire"
            element={isAuthenticated ? <MoleQuestionnairePage nationalId={user?.nationalId} /> : <Navigate to="/login" />}
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;