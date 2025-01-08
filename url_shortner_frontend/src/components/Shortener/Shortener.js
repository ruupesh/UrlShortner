import React, { useState } from 'react';
import './Shortener.css';
import { shortenURL } from '../../services/api';

const Shortener = ({ token }) => {
  const [originalURL, setOriginalURL] = useState('');
  const [shortURL, setShortURL] = useState(null);
  const [error, setError] = useState(null);

  const handleShorten = async () => {
    try {
      const response = await shortenURL({ original_url: originalURL }, token);
      setShortURL(response.data.short_url);
      setError(null);
    } catch (err) {
      setError('Failed to shorten URL. Please try again.');
    }
  };

  return (
    <div className="shortener">
      <h1>Shorten Your URL</h1>
      <input
        type="text"
        placeholder="Enter URL to shorten"
        value={originalURL}
        onChange={(e) => setOriginalURL(e.target.value)}
      />
      <button onClick={handleShorten}>Shorten</button>
      {shortURL && (
        <p>
          Shortened URL: <a href={shortURL}>{shortURL}</a>
        </p>
      )}
      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default Shortener;
