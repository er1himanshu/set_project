const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  uploadFile: `${API_BASE_URL}/api/images/upload/file`,
  uploadUrl: `${API_BASE_URL}/api/images/upload/url`,
  listImages: `${API_BASE_URL}/api/images`,
  getImage: (id: number) => `${API_BASE_URL}/api/images/${id}`,
  getResult: (id: number) => `${API_BASE_URL}/api/images/${id}/result`,
  deleteImage: (id: number) => `${API_BASE_URL}/api/images/${id}`,
  getConfig: `${API_BASE_URL}/api/config`,
};

export default API_BASE_URL;
