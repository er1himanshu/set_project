import axios from 'axios';
import { API_ENDPOINTS } from '../config/api';
import { ImageMetadata, ImageUploadResponse, ConfigResponse } from '../types';

export const api = axios.create({
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadImageFile = async (file: File): Promise<ImageUploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post(API_ENDPOINTS.uploadFile, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const uploadImageUrl = async (url: string): Promise<ImageUploadResponse> => {
  const response = await api.post(API_ENDPOINTS.uploadUrl, { url });
  return response.data;
};

export const listImages = async (): Promise<ImageMetadata[]> => {
  const response = await api.get(API_ENDPOINTS.listImages);
  return response.data;
};

export const getImage = async (id: number): Promise<ImageMetadata> => {
  const response = await api.get(API_ENDPOINTS.getImage(id));
  return response.data;
};

export const deleteImage = async (id: number): Promise<void> => {
  await api.delete(API_ENDPOINTS.deleteImage(id));
};

export const getConfig = async (): Promise<ConfigResponse> => {
  const response = await api.get(API_ENDPOINTS.getConfig);
  return response.data;
};
