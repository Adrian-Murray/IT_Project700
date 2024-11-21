import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Login from './components/auth/Login';
import SignUp from './components/auth/SignUp';
import Dashboard from './components/dashboard/Dashboard';
import Assessment from './components/assessment/Assessment';
import SkillsSelection from './components/skills/SkillsSelection';
import CareerPath from './components/career/CareerPath';
import Layout from './components/layout/Layout';
import ProtectedRoute from './components/auth/ProtectedRoute';
import { AuthProvider } from './context/AuthContext';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const userId = localStorage.getItem('userId');
    setIsAuthenticated(!!userId);
  }, []);

  return (
    <AuthProvider>
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={!isAuthenticated ? <Login setAuth={setIsAuthenticated} /> : <Navigate to="/dashboard" />} />
                <Route path="/signup" element={!isAuthenticated ? <SignUp setAuth={setIsAuthenticated} /> : <Navigate to="/assessment" />} />
                
                <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} />}>
                <Route element={<Layout />}>
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/assessment" element={<Assessment />} />
                    <Route path="/skills" element={<SkillsSelection />} />
                    <Route path="/career" element={<CareerPath />} />
                </Route>
                </Route>
                
                <Route path="/" element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} />} />
            </Routes>
        </BrowserRouter>
    </AuthProvider>    
  );
}

export default App;