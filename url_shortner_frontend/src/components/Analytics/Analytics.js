import React, { useEffect, useState } from 'react';
import './Analytics.css';
import { getAnalytics, deleteURL } from '../../services/api';

const Analytics = ({ token }) => {
  const [analytics, setAnalytics] = useState([]);
  const [error, setError] = useState(null);

  const fetchAnalytics = async () => {
    try {
      const response = await getAnalytics(token);
      setAnalytics(response.data);
    } catch (err) {
      setError('Failed to fetch analytics. Please try again.');
    }
  };

  const handleDelete = async (shortUrl) => {
    try {
      await deleteURL(shortUrl, token);
      setAnalytics(analytics.filter((url) => url.short_url !== shortUrl)); // Remove the deleted URL from the table
      setError(null);
    } catch (err) {
      setError('Failed to delete the URL. Please try again.');
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, [token]);

  return (
    <div className="analytics">
      <h1>Your Analytics</h1>
      {error && <p className="error">{error}</p>}
      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Original URL</th>
              <th>Short URL</th>
              <th>Click Count</th>
              <th>Created At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {analytics.map((url, index) => (
              <tr key={index}>
                <td>
                  <a href={url.original_url} target="_blank" rel="noopener noreferrer">
                    {url.original_url}
                  </a>
                </td>
                <td>
                  <a href={url.short_url} target="_blank" rel="noopener noreferrer">
                    {url.short_url}
                  </a>
                </td>
                <td>{url.click_count || 0}</td>
                <td>
                  {url.created_at
                    ? new Date(url.created_at).toLocaleString()
                    : "N/A"}
                </td>
                <td>
                  <button
                    className="delete-button"
                    onClick={() => handleDelete(url.short_url)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Analytics;
