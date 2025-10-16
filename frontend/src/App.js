import React, { useState } from 'react';
import axios from 'axios';
import ImageUpload from './components/ImageUpload';
import ProductList from './components/ProductList';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadedImageUrl, setUploadedImageUrl] = useState(null);
  const [similarProducts, setSimilarProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [similarityFilter, setSimilarityFilter] = useState(0.3); // Initial filter value at 30%

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      // Create a temporary URL for the image preview
      setUploadedImageUrl(URL.createObjectURL(file));
      // Clear previous results when a new image is selected
      setSimilarProducts([]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file first!');
      return;
    }
    setLoading(true);
    setError(null); // Clear previous errors on new upload
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
     // Inside the handleUpload function in frontend/src/App.js

      const response = await axios.post(`${process.env.REACT_APP_API_URL}/api/find_similar`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setSimilarProducts(response.data);
    } catch (error) {
      console.error('Error uploading file:', error);
      setError('Could not find similar products. The server might be down or an error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Filter the products based on the slider value before passing them to the list
  const filteredProducts = similarProducts.filter(p => p.similarity_score >= similarityFilter);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Style Muse</h1>
        <p className="subtitle">Upload an image to find visually similar fashion products.</p>
        
        <ImageUpload onUpload={handleUpload} onFileChange={handleFileChange} loading={loading} />

        {/* --- Image Preview Section --- */}
        {uploadedImageUrl && (
          <div className="image-preview-container">
            <h2>Your Image</h2>
            <img src={uploadedImageUrl} alt="Uploaded preview" className="image-preview" />
          </div>
        )}

        {/* --- Filter Section --- */}
        {similarProducts.length > 0 && (
          <div className="filter-container">
            <label htmlFor="similarity">Minimum Similarity: {(similarityFilter * 100).toFixed(0)}%</label>
            <input
              id="similarity"
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={similarityFilter}
              onChange={(e) => setSimilarityFilter(e.target.value)}
            />
          </div>
        )}

        {/* --- Results Section --- */}
        <ProductList products={filteredProducts} loading={loading} error={error} />

      </header>
    </div>
  );
}

export default App;