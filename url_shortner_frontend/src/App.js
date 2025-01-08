import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import Shortener from './components/Shortener/Shortener';
import Analytics from './components/Analytics/Analytics';

const App = () => {
  const [token, setToken] = useState(localStorage.getItem('token'));

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  return (
    <Router>
      <Navbar token={token} onLogout={handleLogout} />
      <Routes>
        <Route
          path="/shortener"
          element={token ? <Shortener token={token} /> : <Navigate to="/login" />}
        />
        <Route
          path="/analytics"
          element={token ? <Analytics token={token} /> : <Navigate to="/login" />}
        />
        <Route
          path="/login"
          element={token ? <Navigate to="/shortener" /> : <Login setToken={setToken} />}
        />
        <Route
          path="/register"
          element={token ? <Navigate to="/shortener" /> : <Register />}
        />
        {/* <Route path="/login" element={<Login setToken={setToken} />} /> */}
        {/* <Route path="/register" element={<Register />} /> */}
        {/* Redirect root to login */}
        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
};

export default App;
