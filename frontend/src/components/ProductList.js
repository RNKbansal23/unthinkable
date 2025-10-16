import React from 'react';
import ProductCard from './ProductCard';
import './ProductList.css';

const ProductList = ({ products, loading, error }) => {
  // 1. Handle error state
  if (error) {
    return <p className="error-message">{error}</p>;
  }

  // 2. Handle loading state
  if (loading) {
    return <h2 className="loading-message">Finding similar products...</h2>;
  }

  // 3. Handle no results state (initial or after filtering)
  if (!products || products.length === 0) {
    return <p>No similar products found. Try uploading an image or adjusting the filter!</p>;
  }

  // 4. Display the results
  return (
    <div>
      <h2>Similar Products</h2>
      <div className="product-list-grid">
        {products.map((product) => (
          <ProductCard key={product.product_details.id} product={product} />
        ))}
      </div>
    </div>
  );
};

export default ProductList;