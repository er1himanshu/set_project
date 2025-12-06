import React, { useState, useEffect } from 'react';
import UploadForm from '../components/UploadForm';
import ImageTable from '../components/ImageTable';
import ImageDetailsModal from '../components/ImageDetailsModal';
import { listImages } from '../services/api';
import { ImageMetadata } from '../types';

const HomePage: React.FC = () => {
  const [images, setImages] = useState<ImageMetadata[]>([]);
  const [selectedImage, setSelectedImage] = useState<ImageMetadata | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchImages = async () => {
    try {
      setLoading(true);
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
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            Image Quality Analysis System
          </h1>
          <p className="mt-2 text-gray-600">
            AI-powered image quality analysis and management for e-commerce platforms
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Upload Form */}
          <div className="lg:col-span-1">
            <UploadForm onUploadSuccess={fetchImages} />
          </div>

          {/* Image Table */}
          <div className="lg:col-span-2">
            {loading ? (
              <div className="bg-white rounded-lg shadow-md p-12 text-center">
                <div className="text-gray-500">Loading images...</div>
              </div>
            ) : (
              <ImageTable
                images={images}
                onSelectImage={setSelectedImage}
                onRefresh={fetchImages}
              />
            )}
          </div>
        </div>
      </main>

      {/* Details Modal */}
      <ImageDetailsModal
        image={selectedImage}
        onClose={() => setSelectedImage(null)}
      />
    </div>
  );
};

export default HomePage;
