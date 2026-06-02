import React, { useState, useEffect } from 'react';
import { fetchGalleryItems } from '../services/api';
import { Award, Calendar } from 'lucide-react';
import './Gallery.css';

export default function Gallery() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadGallery() {
      try {
        setLoading(true);
        const data = await fetchGalleryItems();
        setItems(data);
        setError(null);
      } catch (err) {
        console.error(err);
        setError("Unable to load the achievements gallery. Please ensure the backend server is running.");
      } finally {
        setLoading(false);
      }
    }
    loadGallery();
  }, []);

  return (
    <div className="gallery-page container section">
      <h1 className="section-title font-serif">Achievements Gallery</h1>
      <p className="section-subtitle">
        A visual showcase of milestones, leadership summits, creative performances, and memorable moments.
      </p>

      {loading && (
        <div className="gallery-loading">
          <div className="spinner"></div>
          <p>Assembling historical highlights...</p>
        </div>
      )}

      {error && (
        <div className="gallery-error glass-panel">
          <Award size={36} className="error-icon" />
          <p>{error}</p>
          <button className="btn btn-outline" onClick={() => window.location.reload()}>
            Try Again
          </button>
        </div>
      )}

      {!loading && !error && (
        <div className="gallery-grid">
          {items.map((item) => (
            <div key={item.id} className="gallery-card glass-panel">
              <div className="card-image-container">
                <img src={item.image_url} alt={item.title} className="card-image" loading="lazy" />
              </div>
              <div className="card-info">
                <div className="card-date">
                  <Calendar size={12} />
                  <span>{item.date}</span>
                </div>
                <h3 className="card-title font-serif">{item.title}</h3>
                <p className="card-description">{item.description}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {!loading && !error && items.length === 0 && (
        <div className="gallery-empty">
          <p>No gallery archives found.</p>
        </div>
      )}
    </div>
  );
}
