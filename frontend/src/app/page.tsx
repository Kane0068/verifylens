'use client';

import { useState } from 'react';
import { Upload, AlertCircle } from 'lucide-react';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setFile(file);
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Dosya tipini belirle
      const mediaType = file.type.includes('video') ? 'video' : 
                       file.type.includes('audio') ? 'audio' : 'text';

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/analyze/${mediaType}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Analysis failed');

      const result = await response.json();
      setAnalysis(result);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            VerifyLens
          </h1>
          <p className="text-xl text-gray-600">
            AI-powered media verification platform
          </p>
        </div>

        {/* Upload Section */}
        <div className="bg-white rounded-lg shadow-md p-8 mb-8">
          <div className="flex flex-col items-center justify-center border-2 border-dashed border-gray-300 rounded-lg p-12">
            <Upload className="h-12 w-12 text-gray-400 mb-4" />
            <label className="block">
              <span className="sr-only">Choose file</span>
              <input 
                type="file" 
                className="block w-full text-sm text-gray-500
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-full file:border-0
                  file:text-sm file:font-semibold
                  file:bg-blue-50 file:text-blue-700
                  hover:file:bg-blue-100"
                onChange={handleFileUpload}
                accept=".txt,.mp3,.mp4"
              />
            </label>
            <p className="text-sm text-gray-500 mt-2">
              Support for .txt, .mp3, and .mp4 files
            </p>
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
            <p className="mt-4 text-gray-600">Analyzing your media...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-8">
            <div className="flex">
              <AlertCircle className="h-5 w-5 text-red-500" />
              <div className="ml-3">
                <p className="text-red-700">Error: {error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Results Section */}
        {analysis && (
          <div className="bg-white rounded-lg shadow-md p-8">
            <h2 className="text-2xl font-bold mb-4">Analysis Results</h2>
            {Object.entries(analysis).map(([key, value]) => (
              <div key={key} className="mb-6">
                <h3 className="text-lg font-semibold mb-2">{key}</h3>
                <pre className="bg-gray-50 p-4 rounded-lg overflow-auto">
                  {JSON.stringify(value, null, 2)}
                </pre>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
