import React, { useState, useEffect, useCallback } from 'react';
import './styles/App.css';
import Catalog from './components/Catalog';
import UserPreferences from './components/UserPreferences';
import Recommendations from './components/Recommendations';
import BrowsingHistory from './components/BrowsingHistory';
import { fetchProducts, fetchRecommendations } from './services/api';

function App() {
  const [products, setProducts] = useState([]);
  const [browsingHistory, setBrowsingHistory] = useState([]);
  const [preferences, setPreferences] = useState({
    priceRange: 'all',
    categories: [],
    brands: []
  });
  const [recommendations, setRecommendations] = useState([]);
  const [loadingProducts, setLoadingProducts] = useState(true);
  const [loadingRecommendations, setLoadingRecommendations] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('catalog');

  // Load products on mount
  useEffect(() => {
    loadProducts();
  }, []);

  // Load recommendations when preferences or browsing history changes
  useEffect(() => {
    if (products.length > 0 && (browsingHistory.length > 0 || 
        preferences.categories.length > 0 || 
        preferences.brands.length > 0 || 
        preferences.priceRange !== 'all')) {
      loadRecommendations();
    }
  }, [preferences, browsingHistory, products.length]);

  const loadProducts = async () => {
    try {
      setLoadingProducts(true);
      const data = await fetchProducts();
      setProducts(data);
    } catch (err) {
      setError('Failed to load products');
      console.error('Error loading products:', err);
    } finally {
      setLoadingProducts(false);
    }
  };

  const loadRecommendations = async () => {
    try {
      setLoadingRecommendations(true);
      setError(null);
      const data = await fetchRecommendations(preferences, browsingHistory);
      setRecommendations(data.recommendations || []);
    } catch (err) {
      setError('Failed to get recommendations. Please try again.');
      console.error('Error loading recommendations:', err);
    } finally {
      setLoadingRecommendations(false);
    }
  };

  const handleProductClick = (product) => {
    if (!browsingHistory.includes(product.id)) {
      setBrowsingHistory(prev => [...prev, product.id].slice(-20)); // Keep last 20 items
    }
  };

  const handlePreferencesChange = useCallback((newPreferences) => {
    setPreferences(newPreferences);
  }, []);

  const handleClearHistory = () => {
    setBrowsingHistory([]);
    setRecommendations([]);
  };

  const handleRemoveFromHistory = (productId) => {
    setBrowsingHistory(prev => prev.filter(id => id !== productId));
  };

  if (loadingProducts) {
    return (
      <div className="app-loading">
        <div className="spinner"></div>
        <p>Loading products...</p>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="app-header">
        <h1>🤖 AI-Powered Product Recommendations</h1>
        <nav className="app-nav">
          <button 
            className={activeTab === 'catalog' ? 'active' : ''}
            onClick={() => setActiveTab('catalog')}
          >
            Catalog
          </button>
          <button 
            className={activeTab === 'preferences' ? 'active' : ''}
            onClick={() => setActiveTab('preferences')}
          >
            Preferences
          </button>
          <button 
            className={activeTab === 'recommendations' ? 'active' : ''}
            onClick={() => setActiveTab('recommendations')}
          >
            Recommendations
          </button>
          <button 
            className={activeTab === 'history' ? 'active' : ''}
            onClick={() => setActiveTab('history')}
          >
            History {browsingHistory.length > 0 && `(${browsingHistory.length})`}
          </button>
        </nav>
      </header>

      <main className="app-main">
        <div className="content-container">
          {activeTab === 'catalog' && (
            <Catalog 
              products={products}
              onProductClick={handleProductClick}
              browsingHistory={browsingHistory}
            />
          )}
          
          {activeTab === 'preferences' && (
            <UserPreferences 
              products={products}
              onPreferencesChange={handlePreferencesChange}
            />
          )}
          
          {activeTab === 'recommendations' && (
            <Recommendations 
              recommendations={recommendations}
              loading={loadingRecommendations}
              error={error}
              onProductClick={handleProductClick}
            />
          )}
          
          {activeTab === 'history' && (
            <BrowsingHistory 
              browsingHistory={browsingHistory}
              products={products}
              onClearHistory={handleClearHistory}
              onRemoveItem={handleRemoveFromHistory}
            />
          )}
        </div>
        
        <button 
          className="get-recommendations-btn"
          onClick={loadRecommendations}
          disabled={loadingRecommendations}
        >
          {loadingRecommendations ? 'Getting Recommendations...' : 'Get AI Recommendations'}
        </button>
      </main>
    </div>
  );
}

export default App;