// frontend/src/components/ProductList.js
import React from 'react';
import ProductCard from './ProductCard';
import './ProductList.css'; // We'll create this for the grid layout

const ProductList = ({ products }) => {
  if (!products || products.length === 0) {
    return <p>No similar products found yet. Try uploading an image!</p>;
  }

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