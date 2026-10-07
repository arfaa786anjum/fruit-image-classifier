import React, { useRef, useState } from 'react';
import { UploadCloud } from 'lucide-react';

export default function UploadBox({ onFileSelect }) {
  const fileInputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      onFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      onFileSelect(e.target.files[0]);
    }
  };

  return (
    <div className="flex flex-col items-center">
      <div
        className={`w-full max-w-xl p-10 border-2 border-dashed rounded-2xl flex flex-col items-center justify-center transition-all cursor-pointer bg-slate-50 ${
          isDragging ? 'border-blue-500 bg-blue-50 shadow-md' : 'border-slate-300 hover:border-slate-400 hover:bg-slate-100'
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <UploadCloud className={`w-12 h-12 mb-4 ${isDragging ? 'text-blue-500' : 'text-slate-400'}`} />
        <h3 className="text-lg font-semibold text-slate-800 mb-1">
          {isDragging ? 'Drop your image here' : 'Drag & drop your image here'}
        </h3>
        <p className="text-sm text-slate-500 mb-6">or click to browse from your device</p>
        
        <input
          type="file"
          accept="image/jpeg,image/png,image/jpg"
          className="hidden"
          ref={fileInputRef}
          onChange={handleFileChange}
        />
        <button
          className="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors shadow-sm"
          onClick={(e) => {
            e.stopPropagation();
            fileInputRef.current?.click();
          }}
        >
          Choose Image
        </button>
      </div>
      <p className="mt-4 text-xs font-medium text-slate-500">
        JPG, JPEG or PNG • Maximum size: 5MB
      </p>
    </div>
  );
}
