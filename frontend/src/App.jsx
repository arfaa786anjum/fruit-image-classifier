import React, { useState } from 'react';
import Header from './components/Header';
import UploadBox from './components/UploadBox';
import ImagePreview from './components/ImagePreview';
import PredictionResult from './components/PredictionResult';
import ErrorMessage from './components/ErrorMessage';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileSelect = (selectedFile) => {
    if (!selectedFile) return;
    
    if (!['image/jpeg', 'image/png', 'image/jpg'].includes(selectedFile.type)) {
      setError("Please upload a valid JPG, JPEG, or PNG image.");
      return;
    }
    
    if (selectedFile.size > 5 * 1024 * 1024) {
      setError("Image size must be less than 5MB.");
      return;
    }

    setFile(selectedFile);
    setError(null);
    setResult(null);

    const reader = new FileReader();
    reader.onload = (e) => {
      setPreview(e.target.result);
    };
    reader.readAsDataURL(selectedFile);
  };

  const handleRemove = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
  };

  const handleClassify = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong while analyzing the image.");
      }
      
      setResult(data);
    } catch (err) {
      if (err.name === 'TypeError' && err.message === 'Failed to fetch') {
        setError("Unable to connect to the prediction service. Please try again.");
      } else {
        setError(err.message || "Unable to classify this image. Please try another image.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white font-sans text-slate-900 pb-12 selection:bg-blue-100 selection:text-blue-900">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <Header />

        <main className="flex flex-col items-center">
          <div className="text-center mb-10">
            <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-slate-900 mb-4">
              Fruit Image Classifier
            </h1>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto mb-3">
              Upload an image and let our AI identify the fruit.
            </p>
            <p className="text-sm font-medium text-slate-500">
              Supported fruits: Apple • Banana • Orange
            </p>
          </div>

          <div className="w-full">
            {!file && !result && (
              <UploadBox onFileSelect={handleFileSelect} />
            )}

            {file && !result && (
              <ImagePreview 
                preview={preview} 
                file={file} 
                onRemove={handleRemove} 
                onClassify={handleClassify}
                loading={loading}
              />
            )}

            {result && (
              <PredictionResult 
                result={result} 
                onReset={handleRemove} 
              />
            )}

            <ErrorMessage message={error} />
          </div>
        </main>
      </div>
    </div>
  );
}
