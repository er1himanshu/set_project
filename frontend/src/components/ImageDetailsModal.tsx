import React from 'react';
import { ImageMetadata } from '../types';

interface ImageDetailsModalProps {
  image: ImageMetadata | null;
  onClose: () => void;
}

const ImageDetailsModal: React.FC<ImageDetailsModalProps> = ({ image, onClose }) => {
  if (!image) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 p-6 flex justify-between items-center">
          <h2 className="text-2xl font-bold">Image Details</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl font-bold"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Basic Information */}
          <div>
            <h3 className="text-lg font-semibold mb-3">Basic Information</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="font-medium text-gray-600">ID:</span>
                <span className="ml-2">{image.id}</span>
              </div>
              <div>
                <span className="font-medium text-gray-600">Filename:</span>
                <span className="ml-2">{image.filename}</span>
              </div>
              <div>
                <span className="font-medium text-gray-600">Format:</span>
                <span className="ml-2 uppercase">{image.format}</span>
              </div>
              <div>
                <span className="font-medium text-gray-600">Upload Method:</span>
                <span className="ml-2 capitalize">{image.upload_method}</span>
              </div>
              <div>
                <span className="font-medium text-gray-600">Dimensions:</span>
                <span className="ml-2">
                  {image.width && image.height ? `${image.width}x${image.height}` : 'N/A'}
                </span>
              </div>
              <div>
                <span className="font-medium text-gray-600">Size:</span>
                <span className="ml-2">
                  {image.size_bytes ? `${(image.size_bytes / 1024 / 1024).toFixed(2)} MB` : 'N/A'}
                </span>
              </div>
              <div>
                <span className="font-medium text-gray-600">Aspect Ratio:</span>
                <span className="ml-2">
                  {image.aspect_ratio ? image.aspect_ratio.toFixed(2) : 'N/A'}
                </span>
              </div>
              <div>
                <span className="font-medium text-gray-600">Status:</span>
                <span className="ml-2 capitalize">{image.processing_status}</span>
              </div>
            </div>
          </div>

          {/* Quality Analysis */}
          <div>
            <h3 className="text-lg font-semibold mb-3">Quality Analysis</h3>
            <div className="space-y-2">
              <div>
                <span className="font-medium text-gray-600">Quality Score:</span>
                <span className="ml-2 text-lg font-bold">
                  {image.quality_score
                    ? `${(image.quality_score * 100).toFixed(0)}%`
                    : 'Pending'}
                </span>
              </div>
              {image.quality_reasons && image.quality_reasons.length > 0 && (
                <div>
                  <span className="font-medium text-gray-600">Reasons:</span>
                  <ul className="mt-2 space-y-1">
                    {image.quality_reasons.map((reason, idx) => (
                      <li key={idx} className="flex items-start">
                        <span className="text-blue-500 mr-2">•</span>
                        <span className="text-sm">{reason}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* Validation */}
          <div>
            <h3 className="text-lg font-semibold mb-3">Validation</h3>
            <div className="space-y-2">
              <div>
                <span className="font-medium text-gray-600">Validation Status:</span>
                <span
                  className={`ml-2 font-semibold ${
                    image.validation_passed ? 'text-green-600' : 'text-red-600'
                  }`}
                >
                  {image.validation_passed ? 'Passed' : 'Failed'}
                </span>
              </div>
              {image.validation_errors && image.validation_errors.length > 0 && (
                <div>
                  <span className="font-medium text-gray-600">Errors:</span>
                  <ul className="mt-2 space-y-1">
                    {image.validation_errors.map((error, idx) => (
                      <li key={idx} className="flex items-start">
                        <span className="text-red-500 mr-2">✗</span>
                        <span className="text-sm text-red-600">{error}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* Compliance */}
          <div>
            <h3 className="text-lg font-semibold mb-3">Compliance</h3>
            <div className="space-y-2">
              <div>
                <span className="font-medium text-gray-600">Compliance Status:</span>
                <span
                  className={`ml-2 font-semibold ${
                    image.compliance_passed === true
                      ? 'text-green-600'
                      : image.compliance_passed === false
                      ? 'text-red-600'
                      : 'text-gray-400'
                  }`}
                >
                  {image.compliance_passed === true
                    ? 'Passed'
                    : image.compliance_passed === false
                    ? 'Failed'
                    : 'Pending'}
                </span>
              </div>
              {image.compliance_flags && image.compliance_flags.length > 0 && (
                <div>
                  <span className="font-medium text-gray-600">Flags:</span>
                  <ul className="mt-2 space-y-1">
                    {image.compliance_flags.map((flag, idx) => (
                      <li key={idx} className="flex items-start">
                        <span className="text-yellow-500 mr-2">⚠</span>
                        <span className="text-sm text-yellow-700">{flag}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* Duplicate Detection */}
          <div>
            <h3 className="text-lg font-semibold mb-3">Duplicate Detection</h3>
            <div className="space-y-2">
              <div>
                <span className="font-medium text-gray-600">Is Duplicate:</span>
                <span
                  className={`ml-2 font-semibold ${
                    image.is_duplicate ? 'text-red-600' : 'text-green-600'
                  }`}
                >
                  {image.is_duplicate ? 'Yes' : 'No'}
                </span>
              </div>
              {image.duplicate_of_id && (
                <div>
                  <span className="font-medium text-gray-600">Duplicate of Image ID:</span>
                  <span className="ml-2">{image.duplicate_of_id}</span>
                </div>
              )}
              {image.similarity_score && (
                <div>
                  <span className="font-medium text-gray-600">Similarity Score:</span>
                  <span className="ml-2">{(image.similarity_score * 100).toFixed(0)}%</span>
                </div>
              )}
              {image.cluster_id && (
                <div>
                  <span className="font-medium text-gray-600">Cluster ID:</span>
                  <span className="ml-2 font-mono text-sm">{image.cluster_id}</span>
                </div>
              )}
            </div>
          </div>

          {/* Timestamps */}
          {image.created_at && (
            <div>
              <h3 className="text-lg font-semibold mb-3">Timestamps</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium text-gray-600">Created:</span>
                  <span className="ml-2">{new Date(image.created_at).toLocaleString()}</span>
                </div>
                {image.processed_at && (
                  <div>
                    <span className="font-medium text-gray-600">Processed:</span>
                    <span className="ml-2">{new Date(image.processed_at).toLocaleString()}</span>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-gray-50 border-t border-gray-200 p-6">
          <button
            onClick={onClose}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default ImageDetailsModal;
