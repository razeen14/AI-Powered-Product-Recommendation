import React from 'react';
import '../styles/BrowsingHistory.css';

const BrowsingHistory = ({ browsingHistory, products, onClearHistory, onRemoveItem }) => {
  const historyProducts = browsingHistory.map(id => 
    products.find(p => p.id === id)
  ).filter(Boolean);

  if (historyProducts.length === 0) {
    return (
      <div className="browsing-history-container">
        <h2>Browsing History</h2>
        <div className="empty-history">
          <p>No browsing history yet.</p>
          <p className="hint">Click on products to add them to your history</p>
        </div>
      </div>
    );
  }

  return (
    <div className="browsing-history-container">
      <div className="history-header">
        <h2>Browsing History ({historyProducts.length})</h2>
        <button onClick={onClearHistory} className="clear-history-btn">
          Clear All
        </button>
      </div>
      
      <div className="history-list">
        {historyProducts.map(product => (
          <div key={product.id} className="history-item">
            <div className="history-item-content">
              <div className="product-info-compact">
                <h4>{product.name}</h4>
                <p className="product-details">
                  {product.brand} • {product.category} • ${product.price.toFixed(2)}
                </p>
                <p className="product-rating">Rating: ⭐ {product.rating.toFixed(1)}</p>
              </div>
            </div>
            <button 
              onClick={() => onRemoveItem(product.id)} 
              className="remove-btn"
              title="Remove from history"
            >
              ×
            </button>
          </div>
        ))}
      </div>
      
      <div className="history-summary">
        <p>Recently viewed: {historyProducts.length} products</p>
        <p className="categories-viewed">
          Categories: {[...new Set(historyProducts.map(p => p.category))].join(', ')}
        </p>
        <p className="brands-viewed">
          Brands: {[...new Set(historyProducts.map(p => p.brand))].join(', ')}
        </p>
      </div>
    </div>
  );
};

export default BrowsingHistory;