// frontend/src/components/ImageUpload.js
import React from 'react';

const ImageUpload = ({ onUpload, onFileChange, loading }) => {
    return (
        <div>
            <input type="file" onChange={onFileChange} />
            <button onClick={onUpload} disabled={loading}>
                {loading ? 'Searching...' : 'Find Similar'}
            </button>
        </div>
    );
};

export default ImageUpload;