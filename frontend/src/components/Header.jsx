import React from 'react';

export default function Header() {
  return (
    <header className="flex items-center justify-between py-6 border-b border-slate-100 mb-10">
      <div className="flex items-center gap-2">
        <span className="text-2xl">🍎</span>
        <span className="text-xl font-semibold text-slate-900">Fruit Classifier</span>
      </div>
      <nav className="flex items-center gap-6 text-sm font-medium text-slate-600">
        <a href="#" className="text-slate-900 font-semibold">Home</a>
        <a href="#" className="hover:text-slate-900 transition-colors">About</a>
      </nav>
    </header>
  );
}
