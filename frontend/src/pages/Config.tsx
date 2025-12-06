import React, { useState, useEffect } from 'react';
import { getConfig } from '../utils/api';
import { Config as ConfigType } from '../types';

export const Config: React.FC = () => {
  const [config, setConfig] = useState<ConfigType | null>(null);
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
        <div className="text-xl text-gray-600">Loading configuration...</div>
      </div>
    );
  }

  if (!config) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-xl text-red-600">Failed to load configuration</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Configuration</h1>
          <p className="mt-2 text-gray-600">Current system thresholds and rules</p>
        </div>

        <div className="space-y-6">
          {/* Image Validation */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold mb-4 text-gray-900">Image Validation</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="border-l-4 border-blue-500 pl-4">
                <div className="text-sm text-gray-600">Max File Size</div>
                <div className="text-2xl font-bold text-gray-900">{config.max_file_size_mb} MB</div>
              </div>
              <div className="border-l-4 border-blue-500 pl-4">
                <div className="text-sm text-gray-600">Min Dimensions</div>
                <div className="text-2xl font-bold text-gray-900">
                  {config.min_width} × {config.min_height}
                </div>
              </div>
              <div className="border-l-4 border-blue-500 pl-4">
                <div className="text-sm text-gray-600">Max Dimensions</div>
                <div className="text-2xl font-bold text-gray-900">
                  {config.max_width} × {config.max_height}
                </div>
              </div>
              <div className="border-l-4 border-blue-500 pl-4">
                <div className="text-sm text-gray-600">Allowed Formats</div>
                <div className="text-lg font-bold text-gray-900">
                  {config.allowed_formats.join(', ')}
                </div>
              </div>
            </div>
          </div>

          {/* Quality Thresholds */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold mb-4 text-gray-900">Quality Analysis Thresholds</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="border-l-4 border-green-500 pl-4">
                <div className="text-sm text-gray-600">Min Quality Score</div>
                <div className="text-2xl font-bold text-gray-900">{config.min_quality_score}</div>
                <div className="text-xs text-gray-500 mt-1">0.0 to 1.0 scale</div>
              </div>
              <div className="border-l-4 border-green-500 pl-4">
                <div className="text-sm text-gray-600">Min Resolution</div>
                <div className="text-2xl font-bold text-gray-900">{config.min_resolution_threshold}px</div>
                <div className="text-xs text-gray-500 mt-1">Per dimension</div>
              </div>
              <div className="border-l-4 border-green-500 pl-4">
                <div className="text-sm text-gray-600">Max Compression Artifacts</div>
                <div className="text-2xl font-bold text-gray-900">{config.max_compression_artifacts}</div>
                <div className="text-xs text-gray-500 mt-1">0.0 to 1.0 scale</div>
              </div>
            </div>
          </div>

          {/* Info Panel */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-blue-900 mb-2">ℹ️ About These Settings</h3>
            <p className="text-sm text-blue-800">
              These are the current system thresholds used for image validation and quality analysis.
              Images that don't meet these requirements may be rejected or flagged during processing.
            </p>
            <p className="text-sm text-blue-800 mt-2">
              <strong>Note:</strong> Quality analysis and compliance checks are currently using placeholder
              logic. In production, these would be powered by machine learning models.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
