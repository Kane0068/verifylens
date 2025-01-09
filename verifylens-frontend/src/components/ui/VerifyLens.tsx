import React, { useState } from 'react';
import { Upload, AlertCircle, CheckCircle2 } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

const VerifyLens = () => {
  const [file, setFile] = useState(null);
  const [mediaType, setMediaType] = useState('video');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

 const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  const selectedFile = e.target.files?.[0]; // ?. ile dosya olup olmadığını kontrol edin
  if (selectedFile) {
    setFile(selectedFile);
    setError(null);
  } else {
    setError("No file selected");
  }
};


  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file to analyze');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`https://verifylens.onrender.com/analyze/${mediaType}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <Card>
          <CardHeader>
            <CardTitle className="text-3xl font-bold text-center text-gray-900">
              VerifyLens
            </CardTitle>
            <CardDescription className="text-center mt-2">
              AI-powered media verification platform
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Media Type
                </label>
                <select
                  value={mediaType}
                  onChange={(e) => setMediaType(e.target.value)}
                  className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                >
                  <option value="video">Video</option>
                  <option value="text">Text</option>
                  <option value="audio">Audio</option>
                </select>
              </div>

              <div className="border-2 border-dashed border-gray-300 rounded-lg p-12">
                <div className="text-center">
                  <Upload className="mx-auto h-12 w-12 text-gray-400" />
                  <div className="mt-4">
                    <label htmlFor="file-upload" className="cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500">
                      <span>Upload a file</span>
                      <input
                        id="file-upload"
                        name="file-upload"
                        type="file"
                        className="sr-only"
                        onChange={handleFileChange}
                      />
                    </label>
                  </div>
                  {file && (
                    <p className="mt-2 text-sm text-gray-500">
                      Selected: {file.name}
                    </p>
                  )}
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                {loading ? 'Analyzing...' : 'Analyze Media'}
              </button>
            </form>

            {error && (
              <Alert variant="destructive" className="mt-6">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {result && (
              <div className="mt-6">
                <Alert>
                  <CheckCircle2 className="h-4 w-4" />
                  <AlertTitle>Analysis Complete</AlertTitle>
                  <AlertDescription>
                    <pre className="mt-2 whitespace-pre-wrap text-sm">
                      {JSON.stringify(result, null, 2)}
                    </pre>
                  </AlertDescription>
                </Alert>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default VerifyLens;
