import React from 'react';

export default function PredictionResult({ result, onReset }) {
  const { predicted_class, confidence, probabilities } = result;

  const getEmoji = (fruit) => {
    switch(fruit?.toLowerCase()) {
      case 'apple': return '🍎';
      case 'banana': return '🍌';
      case 'orange': return '🍊';
      default: return '🍏';
    }
  };

  return (
    <div className="w-full max-w-xl mx-auto flex flex-col items-center">
      <div className="w-full bg-white border border-slate-200 rounded-2xl p-8 shadow-sm mb-6 text-center">
        <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-4">Prediction</h3>
        
        <div className="text-6xl mb-4">{getEmoji(predicted_class)}</div>
        <h2 className="text-3xl font-bold text-slate-900 capitalize mb-2">{predicted_class}</h2>
        <div className="text-lg font-medium text-slate-600 mb-8">
          Confidence: <span className="text-slate-900">{(confidence * 100).toFixed(1)}%</span>
        </div>

        <div className="w-full max-w-sm mx-auto h-2 bg-slate-100 rounded-full overflow-hidden mb-6">
          <div 
            className="h-full bg-blue-600 rounded-full transition-all duration-1000 ease-out"
            style={{ width: `${confidence * 100}%` }}
          />
        </div>

        {probabilities && Object.keys(probabilities).length > 0 && (
          <div className="w-full max-w-sm mx-auto flex flex-col gap-2 text-sm">
            {Object.entries(probabilities)
              .sort((a, b) => b[1] - a[1])
              .map(([fruit, prob]) => (
                <div key={fruit} className="flex items-center justify-between">
                  <span className="capitalize text-slate-700">{fruit}</span>
                  <span className="font-medium text-slate-900">{(prob * 100).toFixed(1)}%</span>
                </div>
            ))}
          </div>
        )}
      </div>

      <button
        onClick={onReset}
        className="px-6 py-2.5 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 font-semibold rounded-lg shadow-sm transition-colors"
      >
        Try Another Image
      </button>
    </div>
  );
}
