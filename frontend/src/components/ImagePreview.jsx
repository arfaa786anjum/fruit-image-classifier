import React from 'react';
import { X } from 'lucide-react';

export default function ImagePreview({ preview, file, onRemove, onClassify, loading }) {
  const formatSize = (bytes) => {
    if (!bytes) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  return (
    <div className="w-full max-w-xl mx-auto flex flex-col items-center">
      <div className="w-full bg-white border border-slate-200 rounded-2xl p-4 shadow-sm mb-6">
        <div className="relative w-full aspect-video bg-slate-100 rounded-xl overflow-hidden flex items-center justify-center mb-4">
          <img src={preview} alt="Preview" className="max-w-full max-h-full object-contain" />
          {loading && (
             <div className="absolute inset-0 bg-white/70 backdrop-blur-sm flex flex-col items-center justify-center">
                <div className="w-8 h-8 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mb-3"></div>
                <span className="text-sm font-semibold text-slate-700">Analyzing image...</span>
             </div>
          )}
        </div>
        
        <div className="flex items-center justify-between">
          <div className="flex flex-col overflow-hidden">
            <span className="text-sm font-semibold text-slate-800 truncate">{file?.name}</span>
            <span className="text-xs text-slate-500">{formatSize(file?.size)}</span>
          </div>
          <button 
            onClick={onRemove}
            disabled={loading}
            className="text-sm text-red-600 hover:text-red-700 font-medium px-3 py-1.5 rounded-lg hover:bg-red-50 transition-colors disabled:opacity-50"
          >
            Remove
          </button>
        </div>
      </div>

      <button
        onClick={onClassify}
        disabled={loading}
        className="w-full max-w-xs px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-semibold rounded-lg shadow-sm transition-colors"
      >
        Classify Image
      </button>
    </div>
  );
}
