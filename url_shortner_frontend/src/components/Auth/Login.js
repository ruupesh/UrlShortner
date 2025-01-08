import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Auth.css';
import { login } from '../../services/api';

const Login = ({ setToken }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault(); // Prevent default form submission
    try {
      const response = await login({ username, password });
      const { access } = response.data;
      localStorage.setItem('token', access);
      setToken(access);
      setError(null);
      navigate('/shortener');
    } catch (err) {
      setError('Invalid username or password. Please try again.');
    }
  };

  return (
    <div className="auth-container">
      <h1>Login</h1>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Login</button> {/* Use type="submit" */}
      </form>
      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default Login;
