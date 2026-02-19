import React, { useState, useEffect } from 'react';
import '../styles/UserPreferences.css';

const UserPreferences = ({ products, onPreferencesChange }) => {
  const [preferences, setPreferences] = useState({
    priceRange: 'all',
    categories: [],
    brands: []
  });

  const priceRanges = [
    { value: 'all', label: 'All Prices' },
    { value: '0-50', label: '$0 - $50' },
    { value: '50-100', label: '$50 - $100' },
    { value: '100+', label: '$100+' }
  ];

  const categories = [...new Set(products.map(p => p.category))].sort();
  const brands = [...new Set(products.map(p => p.brand))].sort();

  useEffect(() => {
    onPreferencesChange(preferences);
  }, [preferences, onPreferencesChange]);

  const handlePriceRangeChange = (value) => {
    setPreferences(prev => ({ ...prev, priceRange: value }));
  };

  const handleCategoryToggle = (category) => {
    setPreferences(prev => ({
      ...prev,
      categories: prev.categories.includes(category)
        ? prev.categories.filter(c => c !== category)
        : [...prev.categories, category]
    }));
  };

  const handleBrandToggle = (brand) => {
    setPreferences(prev => ({
      ...prev,
      brands: prev.brands.includes(brand)
        ? prev.brands.filter(b => b !== brand)
        : prev.brands.length < 10 ? [...prev.brands, brand] : prev.brands
    }));
  };

  const clearPreferences = () => {
    setPreferences({
      priceRange: 'all',
      categories: [],
      brands: []
    });
  };

  return (
    <div className="preferences-container">
      <div className="preferences-header">
        <h2>Your Preferences</h2>
        <button onClick={clearPreferences} className="clear-btn">Clear All</button>
      </div>

      <div className="preference-section">
        <h3>Price Range</h3>
        <div className="price-range-options">
          {priceRanges.map(range => (
            <label key={range.value} className="radio-label">
              <input
                type="radio"
                value={range.value}
                checked={preferences.priceRange === range.value}
                onChange={(e) => handlePriceRangeChange(e.target.value)}
              />
              <span>{range.label}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="preference-section">
        <h3>Categories</h3>
        <div className="checkbox-grid">
          {categories.map(category => (
            <label key={category} className="checkbox-label">
              <input
                type="checkbox"
                checked={preferences.categories.includes(category)}
                onChange={() => handleCategoryToggle(category)}
              />
              <span>{category}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="preference-section">
        <h3>Brands {preferences.brands.length > 0 && `(${preferences.brands.length}/10)`}</h3>
        <div className="checkbox-grid">
          {brands.map(brand => (
            <label 
              key={brand} 
              className={`checkbox-label ${preferences.brands.length >= 10 && !preferences.brands.includes(brand) ? 'disabled' : ''}`}
            >
              <input
                type="checkbox"
                checked={preferences.brands.includes(brand)}
                onChange={() => handleBrandToggle(brand)}
                disabled={preferences.brands.length >= 10 && !preferences.brands.includes(brand)}
              />
              <span>{brand}</span>
            </label>
          ))}
        </div>
        {preferences.brands.length >= 10 && (
          <p className="warning-text">Maximum 10 brands can be selected</p>
        )}
      </div>

      <div className="preferences-summary">
        <h4>Current Preferences:</h4>
        <ul>
          <li>Price Range: {preferences.priceRange === 'all' ? 'All Prices' : `$${preferences.priceRange}`}</li>
          <li>Categories: {preferences.categories.length > 0 ? preferences.categories.join(', ') : 'None selected'}</li>
          <li>Brands: {preferences.brands.length > 0 ? preferences.brands.join(', ') : 'None selected'}</li>
        </ul>
      </div>
    </div>
  );
};

export default UserPreferences;