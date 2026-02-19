import React from 'react';
import '../styles/Recommendations.css';

const Recommendations = ({ recommendations, loading, error, onProductClick }) => {
  if (loading) {
    return (
      <div className="recommendations-container">
        <h2>AI Recommendations</h2>
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Generating personalized recommendations...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="recommendations-container">
        <h2>AI Recommendations</h2>
        <div className="error-state">
          <p className="error-message">⚠️ {error}</p>
        </div>
      </div>
    );
  }

  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="recommendations-container">
        <h2>AI Recommendations</h2>
        <div className="empty-state">
          <p>No recommendations available yet.</p>
          <p className="hint">Try browsing some products or setting your preferences!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="recommendations-container">
      <h2>AI Recommendations for You</h2>
      <div className="recommendations-list">
        {recommendations.map((rec, index) => (
          <div key={rec.product.id} className="recommendation-card">
            <div className="recommendation-rank">#{index + 1}</div>
            <div className="recommendation-content">
              <div className="product-section" onClick={() => onProductClick(rec.product)}>
                <div className="product-details">
                  <h3>{rec.product.name}</h3>
                  <p className="product-meta">
                    {rec.product.brand} • {rec.product.category} • {rec.product.subcategory}
                  </p>
                  <p className="product-description">{rec.product.description}</p>
                  <div className="product-stats">
                    <span className="price">${rec.product.price.toFixed(2)}</span>
                    <span className="rating">⭐ {rec.product.rating.toFixed(1)}</span>
                    <span className="inventory">
                      {rec.product.inventory > 0 ? `✓ ${rec.product.inventory} in stock` : '✗ Out of stock'}
                    </span>
                  </div>
                  <div className="product-features">
                    <strong>Features:</strong>
                    <ul>
                      {rec.product.features.slice(0, 3).map((feature, idx) => (
                        <li key={idx}>{feature}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
              
              <div className="recommendation-reason">
                <div className="confidence-score">
                  <span className="confidence-label">Confidence:</span>
                  <div className="confidence-bar">
                    <div 
                      className="confidence-fill" 
                      style={{ width: `${rec.confidence_score * 10}%` }}
                    ></div>
                  </div>
                  <span className="confidence-value">{rec.confidence_score}/10</span>
                </div>
                <p className="explanation">
                  <strong>Why we recommend this:</strong> {rec.explanation}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Recommendations;