import React, { useState, useEffect } from 'react';
import { UploadForm } from '../components/UploadForm';
import { ImageTable } from '../components/ImageTable';
import { ImageDetailsModal } from '../components/ImageDetailsModal';
import { listImages } from '../utils/api';
import { Image } from '../types';

export const Home: React.FC = () => {
  const [images, setImages] = useState<Image[]>([]);
  const [selectedImage, setSelectedImage] = useState<Image | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchImages = async () => {
    setLoading(true);
    try {
      const data = await listImages();
      setImages(data);
    } catch (error) {
      console.error('Failed to fetch images:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchImages();
    // Poll for updates every 5 seconds
    const interval = setInterval(fetchImages, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Image Quality Analysis System
          </h1>
          <p className="mt-2 text-gray-600">
            Upload and analyze images for e-commerce platforms
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-1">
            <UploadForm onUploadSuccess={fetchImages} />
          </div>
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-bold mb-4">Quick Stats</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600">{images.length}</div>
                  <div className="text-sm text-gray-600">Total Images</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600">
                    {images.filter(img => img.status === 'completed').length}
                  </div>
                  <div className="text-sm text-gray-600">Processed</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-yellow-600">
                    {images.filter(img => img.status === 'processing' || img.status === 'pending').length}
                  </div>
                  <div className="text-sm text-gray-600">In Progress</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-red-600">
                    {images.filter(img => img.status === 'failed').length}
                  </div>
                  <div className="text-sm text-gray-600">Failed</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="mb-4 flex justify-between items-center">
          <h2 className="text-2xl font-bold text-gray-900">Images</h2>
          <button
            onClick={fetchImages}
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400"
          >
            {loading ? 'Refreshing...' : 'Refresh'}
          </button>
        </div>

        <ImageTable images={images} onSelectImage={setSelectedImage} />
      </div>

      <ImageDetailsModal image={selectedImage} onClose={() => setSelectedImage(null)} />
    </div>
  );
};
