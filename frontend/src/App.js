// frontend/src/App.js
import React, { useState } from 'react';
import axios from 'axios';
import ImageUpload from './components/ImageUpload';
import ProductList from './components/ProductList';
import './App.css';

function App() {
    const [selectedFile, setSelectedFile] = useState(null);
    // Near the top of the App component in frontend/src/App.js
const [similarProducts, setSimilarProducts] = useState([]); // Change this 
    const [loading, setLoading] = useState(false);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            alert('Please select a file first!');
            return;
        }
        setLoading(true);
        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await axios.post('http://localhost:5000/api/find_similar', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setSimilarProducts(response.data.similar_products);
        } catch (error) {
            console.error('Error uploading file:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>Style Muse</h1>
                <ImageUpload onUpload={handleUpload} onFileChange={handleFileChange} loading={loading} />
                <ProductList products={similarProducts} />
            </header>
        </div>
    );
}

export default App;