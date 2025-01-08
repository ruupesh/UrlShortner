import React, { useState } from 'react';
import './Auth.css';
import { register } from '../../services/api';

const Register = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);

  const handleRegister = async (e) => {
    e.preventDefault(); // Prevent default form submission
    try {
      await register({ username, password });
      setSuccess(true);
      setError(null);
    } catch (err) {
      setError('Failed to register. Try again with a different username.');
    }
  };

  return (
    <div className="auth-container">
      <h1>Register</h1>
      <form onSubmit={handleRegister}>
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
        <button type="submit">Register</button> {/* Use type="submit" */}
      </form>
      {success && <p className="success">Registration successful. You can now log in.</p>}
      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default Register;
