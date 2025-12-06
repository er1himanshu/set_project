import React, { useState } from 'react';
import { uploadImageFile, uploadImageUrl } from '../services/api';

interface UploadFormProps {
  onUploadSuccess: () => void;
}

const UploadForm: React.FC<UploadFormProps> = ({ onUploadSuccess }) => {
  const [uploadMethod, setUploadMethod] = useState<'file' | 'url'>('file');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [imageUrl, setImageUrl] = useState('');
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setError('');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setUploading(true);
    setMessage('');
    setError('');

    try {
      if (uploadMethod === 'file') {
        if (!selectedFile) {
          setError('Please select a file');
          return;
        }
        const response = await uploadImageFile(selectedFile);
        setMessage(response.message);
        setSelectedFile(null);
      } else {
        if (!imageUrl) {
          setError('Please enter a URL');
          return;
        }
        const response = await uploadImageUrl(imageUrl);
        setMessage(response.message);
        setImageUrl('');
      }
      onUploadSuccess();
    } catch (err: any) {
      setError(err.response?.data?.detail?.errors?.join(', ') || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold mb-4">Upload Image</h2>
      
      {/* Upload Method Toggle */}
      <div className="flex gap-4 mb-4">
        <button
          className={`px-4 py-2 rounded ${
            uploadMethod === 'file'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700'
          }`}
          onClick={() => setUploadMethod('file')}
        >
          Upload File
        </button>
        <button
          className={`px-4 py-2 rounded ${
            uploadMethod === 'url'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700'
          }`}
          onClick={() => setUploadMethod('url')}
        >
          Upload from URL
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        {uploadMethod === 'file' ? (
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Select Image File</label>
            <input
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none"
            />
            {selectedFile && (
              <p className="mt-2 text-sm text-gray-600">
                Selected: {selectedFile.name} ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
              </p>
            )}
          </div>
        ) : (
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Image URL</label>
            <input
              type="url"
              value={imageUrl}
              onChange={(e) => setImageUrl(e.target.value)}
              placeholder="https://example.com/image.jpg"
              className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        )}

        <button
          type="submit"
          disabled={uploading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {uploading ? 'Uploading...' : 'Upload Image'}
        </button>
      </form>

      {message && (
        <div className="mt-4 p-3 bg-green-100 text-green-800 rounded-lg">
          {message}
        </div>
      )}

      {error && (
        <div className="mt-4 p-3 bg-red-100 text-red-800 rounded-lg">
          {error}
        </div>
      )}
    </div>
  );
};

export default UploadForm;
