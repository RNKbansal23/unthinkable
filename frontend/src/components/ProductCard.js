// frontend/src/components/ProductCard.js
import React from 'react';
import './ProductCard.css'; // We'll create this file for styling

const ProductCard = ({ product }) => {
  // The backend now serves images from http://localhost:5000/images/
  const imageUrl = `http://localhost:5000/images/${product.product_details.image_filename}`;
  const score = (product.similarity_score * 100).toFixed(2); // Convert score to percentage

  return (
    <div className="product-card">
      <img src={imageUrl} alt={product.product_details.name} className="product-image" />
      <div className="product-info">
        <h3 className="product-name">{product.product_details.name}</h3>
        <p className="product-category">{product.product_details.category}</p>
        <p className="product-score">Similarity: {score}%</p>
      </div>
    </div>
  );
};

export default ProductCard;