import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = ({ token, onLogout }) => (
  <nav className="navbar">

    {token ? (
      <>
          <Link to="/shortener">Shorten URL</Link>
        <Link to="/analytics">Analytics</Link>
        <button onClick={onLogout}>Logout</button>
      </>
    ) : (
      <>
        <Link to="/login">Login</Link>
        <Link to="/register">Register</Link>
      </>
    )}
  </nav>
);

export default Navbar;
