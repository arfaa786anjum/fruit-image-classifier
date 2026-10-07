import React from 'react';
import { AlertCircle } from 'lucide-react';

export default function ErrorMessage({ message }) {
  if (!message) return null;
  return (
    <div className="w-full max-w-xl mx-auto mt-4 p-4 rounded-lg bg-red-50 border border-red-100 flex items-start gap-3">
      <AlertCircle className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
      <p className="text-sm font-medium text-red-800 leading-relaxed">{message}</p>
    </div>
  );
}
