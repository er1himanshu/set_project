import React from 'react';
import { Image } from '../types';

interface ImageDetailsModalProps {
  image: Image | null;
  onClose: () => void;
}

export const ImageDetailsModal: React.FC<ImageDetailsModalProps> = ({ image, onClose }) => {
  if (!image) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b px-6 py-4 flex justify-between items-center">
          <h2 className="text-2xl font-bold">Image Details</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl font-bold"
          >
            ×
          </button>
        </div>
        
        <div className="p-6 space-y-4">
          {/* Basic Info */}
          <div className="border-b pb-4">
            <h3 className="text-lg font-semibold mb-3">Basic Information</h3>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <span className="font-medium text-gray-700">ID:</span>
                <span className="ml-2 text-gray-900">{image.id}</span>
              </div>
              <div>
                <span className="font-medium text-gray-700">Status:</span>
                <span className="ml-2 text-gray-900 capitalize">{image.status}</span>
              </div>
              <div className="col-span-2">
                <span className="font-medium text-gray-700">Filename:</span>
                <span className="ml-2 text-gray-900 break-all">{image.filename}</span>
              </div>
              {image.original_url && (
                <div className="col-span-2">
                  <span className="font-medium text-gray-700">Original URL:</span>
                  <a
                    href={image.original_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="ml-2 text-blue-600 hover:underline break-all"
                  >
                    {image.original_url}
                  </a>
                </div>
              )}
              <div>
                <span className="font-medium text-gray-700">Format:</span>
                <span className="ml-2 text-gray-900">{image.format || '-'}</span>
              </div>
              <div>
                <span className="font-medium text-gray-700">File Size:</span>
                <span className="ml-2 text-gray-900">
                  {image.file_size ? `${(image.file_size / 1024).toFixed(2)} KB` : '-'}
                </span>
              </div>
              <div>
                <span className="font-medium text-gray-700">Dimensions:</span>
                <span className="ml-2 text-gray-900">
                  {image.width && image.height ? `${image.width} × ${image.height}` : '-'}
                </span>
              </div>
              <div>
                <span className="font-medium text-gray-700">Uploaded:</span>
                <span className="ml-2 text-gray-900">
                  {new Date(image.created_at).toLocaleString()}
                </span>
              </div>
            </div>
          </div>

          {/* Quality Analysis */}
          <div className="border-b pb-4">
            <h3 className="text-lg font-semibold mb-3">Quality Analysis</h3>
            <div className="space-y-2">
              <div>
                <span className="font-medium text-gray-700">Quality Score:</span>
                <span className="ml-2 text-xl font-bold">
                  {image.quality_score !== null && image.quality_score !== undefined ? (
                    <span className={
                      image.quality_score >= 0.8 ? 'text-green-600' :
                      image.quality_score >= 0.6 ? 'text-yellow-600' :
                      'text-red-600'
                    }>
                      {image.quality_score.toFixed(2)}
                    </span>
                  ) : (
                    <span className="text-gray-400">Pending</span>
                  )}
                </span>
              </div>
              {image.quality_reasons && image.quality_reasons.length > 0 && (
                <div>
                  <span className="font-medium text-gray-700">Reasons:</span>
                  <ul className="ml-6 mt-2 list-disc text-gray-900">
                    {image.quality_reasons.map((reason, idx) => (
                      <li key={idx}>{reason}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* Compliance */}
          <div className="border-b pb-4">
            <h3 className="text-lg font-semibold mb-3">Compliance Check</h3>
            <div className="space-y-2">
              <div>
                <span className="font-medium text-gray-700">Is Compliant:</span>
                <span className="ml-2">
                  {image.is_compliant === null || image.is_compliant === undefined ? (
                    <span className="text-gray-400">Pending</span>
                  ) : image.is_compliant ? (
                    <span className="text-green-600 font-semibold">✓ Yes</span>
                  ) : (
                    <span className="text-red-600 font-semibold">✗ No</span>
                  )}
                </span>
              </div>
              {image.compliance_flags && image.compliance_flags.length > 0 && (
                <div>
                  <span className="font-medium text-gray-700">Flags:</span>
                  <ul className="ml-6 mt-2 list-disc text-gray-900">
                    {image.compliance_flags.map((flag, idx) => (
                      <li key={idx}>{flag}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* Duplicate Detection */}
          <div className="pb-4">
            <h3 className="text-lg font-semibold mb-3">Duplicate Detection</h3>
            <div className="space-y-2 text-sm">
              <div>
                <span className="font-medium text-gray-700">Is Duplicate:</span>
                <span className="ml-2 text-gray-900">
                  {image.is_duplicate ? '⚠ Yes' : 'No'}
                </span>
              </div>
              {image.duplicate_of_id && (
                <div>
                  <span className="font-medium text-gray-700">Duplicate Of ID:</span>
                  <span className="ml-2 text-gray-900">{image.duplicate_of_id}</span>
                </div>
              )}
              {image.cluster_id && (
                <div>
                  <span className="font-medium text-gray-700">Cluster ID:</span>
                  <span className="ml-2 text-gray-900 font-mono text-xs">{image.cluster_id}</span>
                </div>
              )}
            </div>
          </div>

          {/* Error Message */}
          {image.error_message && (
            <div className="bg-red-50 border border-red-200 rounded-md p-4">
              <h3 className="text-lg font-semibold text-red-800 mb-2">Error</h3>
              <p className="text-sm text-red-700">{image.error_message}</p>
            </div>
          )}
        </div>
        
        <div className="sticky bottom-0 bg-gray-50 px-6 py-4 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
