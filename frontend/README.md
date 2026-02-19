# AI-Powered Product Recommendation - Frontend

This is the React-based frontend component of the AI-Powered Product Recommendation Engine. It provides a clean, responsive interface that allows users to browse products, set preferences, and receive personalized AI-driven recommendations.

## Project Structure
```
frontend/
│
├── public/
│ └── index.html # HTML template
│
├── src/
│ ├── App.js # Main application component with state management
│ ├── index.js # React entry point
│ │
│ ├── components/
│ │ ├── Catalog.js # Product catalog with search, filter, and sort
│ │ ├── UserPreferences.js # Preference selection form
│ │ ├── Recommendations.js # AI recommendations display
│ │ └── BrowsingHistory.js # User browsing history tracker
│ │
│ ├── services/
│ │ └── api.js # API client for backend communication
│ │
│ └── styles/
│ ├── App.css # Main application styles
│ ├── Catalog.css # Product catalog styles
│ ├── UserPreferences.css # Preferences form styles
│ ├── Recommendations.css # Recommendations display styles
│ ├── BrowsingHistory.css # Browsing history styles
│ └── index.css # Global styles
│
├── package.json # NPM dependencies
└── README.md # This file
```
## Setup Instructions
### Prerequisites
- Node.js (v14 or higher)
- NPM or Yarn
- Backend server running on port 5000
1. Navigate to frontend directory
    ```bash
    cd frontend
    ```

2. Install dependencies:
    ```bash
    npm install
    ```

3. Start the development server:
   ```
   npm start
   ```

The application will open at `http://localhost:3000`.

## Implemented Features

### 1. Catalog Component (components/Catalog.js)

- Grid-based product display with responsive layout
- Real-time search functionality across product names, brands, and categories
- Category filtering with dropdown selection
- Multiple sorting options (name, price low-to-high, price high-to-low, rating)
- Visual indication for previously viewed products
- Clean text-based cards displaying:
    - Product name, brand, category, and subcategory
    - Price and rating
    - Product description (truncated)
    - Tags and inventory status
    - "Viewed" badge for browsing history items

### 2. User Preferences Component (components/UserPreferences.js)

- Price range selection with radio buttons (All, $0-50, $50-100, $100+)
- Multi-select category preferences with checkboxes
- Multi-select brand preferences (limited to 10 selections)
- Clear all preferences functionality
- Real-time preference summary display
- Visual feedback for selected options
- Validation and user-friendly warnings

### 3. Recommendations Component (components/Recommendations.js)

- Displays 5 personalized product recommendations
- Shows AI-generated explanations for each recommendation
- Confidence score visualization (1-10 scale with progress bar)
- Comprehensive product details for each recommendation
- Product features list
- Loading state with spinner during API calls
- Error state handling with user-friendly messages
- Empty state when no recommendations available
- Clickable products to add to browsing history

### 4. Browsing History Component (components/BrowsingHistory.js)
- Chronological list of viewed products
- Individual item removal capability
- Clear all history functionality
- Compact product information display
- Summary statistics (total products, categories, brands viewed)
- Empty state with helpful prompts
- Persistent across tab switches

## Error Handling:
- Network errors are caught and displayed to users
- Fallback states for failed API calls
- Retry functionality through the "Get AI Recommendations" button

## UI/UX Features
### Responsive Design:
- Mobile-first responsive grid layouts
- Flexible navigation that adapts to screen size
- Responsive form controls and buttons
- Optimized for screens from 320px to 4K

### Navigation:
- Tab-based navigation between main features
- Persistent "Get AI Recommendations" button
- Visual indication of active tab
- Browsing history count in navigation