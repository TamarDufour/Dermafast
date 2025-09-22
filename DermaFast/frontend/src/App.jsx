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
      const authToken = localStorage.getItem('authToken');
      
      if (authToken) {
        try {
          const tokenData = JSON.parse(authToken);
          if (tokenData && tokenData.access_token && tokenData.national_id) {
            setIsAuthenticated(true);
            setUser({ nationalId: tokenData.national_id });
          } else {
            localStorage.removeItem('authToken');
          }
        } catch (e) {
          console.error('Error parsing auth token:', e);
          localStorage.removeItem('authToken');
        }
      }
    };
    
    checkAuth();
  }, []);

  const handleLogin = (loginData) => {
    // loginData contains the full response from /api/login including access_token
    localStorage.setItem('authToken', JSON.stringify(loginData));
    setIsAuthenticated(true);
    setUser({ nationalId: loginData.national_id });
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData'); // Keep for backward compatibility
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route
            path="/"
            element={
              isAuthenticated ? (
                <HomePage
                  username={user?.nationalId}
                  onLogout={handleLogout}
                />
              ) : (
                <AuthForm onLogin={handleLogin} />
              )
            }
          />
          <Route
            path="/check-mole"
            element={isAuthenticated ? <CheckMolePage /> : <Navigate to="/" />}
          />
          <Route
            path="/questionnaire"
            element={isAuthenticated ? <MoleQuestionnairePage nationalId={user?.nationalId} /> : <Navigate to="/" />}
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;