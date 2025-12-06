import React, { useState, useEffect } from 'react';
import { getConfig } from '../services/api';
import { ConfigResponse } from '../types';

const ConfigPage: React.FC = () => {
  const [config, setConfig] = useState<ConfigResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchConfig = async () => {
      try {
        const data = await getConfig();
        setConfig(data);
      } catch (error) {
        console.error('Failed to fetch config:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchConfig();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-gray-500">Loading configuration...</div>
      </div>
    );
  }

  if (!config) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-red-500">Failed to load configuration</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Configuration</h1>
          <p className="mt-2 text-gray-600">
            Current system configuration and rule thresholds
          </p>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-md p-6 space-y-6">
          {/* Image Validation Rules */}
          <div>
            <h2 className="text-xl font-bold mb-4">Image Validation Rules</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="border-l-4 border-blue-500 pl-4">
                <div className="text-sm font-medium text-gray-600">Maximum File Size</div>
                <div className="text-2xl font-bold text-gray-900">
                  {config.max_image_size_mb} MB
                </div>
              </div>
              <div className="border-l-4 border-blue-500 pl-4">
                <div className="text-sm font-medium text-gray-600">Minimum Resolution</div>
                <div className="text-2xl font-bold text-gray-900">
                  {config.min_resolution}px
                </div>
              </div>
              <div className="border-l-4 border-blue-500 pl-4">
                <div className="text-sm font-medium text-gray-600">Allowed Formats</div>
                <div className="text-lg font-bold text-gray-900">
                  {config.allowed_formats.join(', ').toUpperCase()}
                </div>
              </div>
              <div className="border-l-4 border-blue-500 pl-4">
                <div className="text-sm font-medium text-gray-600">Aspect Ratio Range</div>
                <div className="text-lg font-bold text-gray-900">
                  {config.min_aspect_ratio} - {config.max_aspect_ratio}
                </div>
              </div>
            </div>
          </div>

          {/* Quality Thresholds */}
          <div>
            <h2 className="text-xl font-bold mb-4">Quality Thresholds</h2>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
                <span className="font-medium text-gray-700">Minimum Quality Score</span>
                <span className="text-lg font-bold text-blue-600">
                  {(config.min_quality_score * 100).toFixed(0)}%
                </span>
              </div>
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
                <span className="font-medium text-gray-700">Minimum Sharpness Score</span>
                <span className="text-lg font-bold text-blue-600">
                  {(config.min_sharpness_score * 100).toFixed(0)}%
                </span>
              </div>
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
                <span className="font-medium text-gray-700">Minimum Brightness Score</span>
                <span className="text-lg font-bold text-blue-600">
                  {(config.min_brightness_score * 100).toFixed(0)}%
                </span>
              </div>
            </div>
          </div>

          {/* Info Box */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg
                  className="h-5 w-5 text-blue-400"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-blue-800">
                  Configuration Information
                </h3>
                <div className="mt-2 text-sm text-blue-700">
                  <p>
                    These thresholds are used to validate and assess image quality.
                    Images that don't meet these criteria may be flagged or rejected.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ConfigPage;
