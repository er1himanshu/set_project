import axios from 'axios';
import { Image, Config, UploadResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_V1 = `${API_BASE_URL}/api/v1`;

const api = axios.create({
  baseURL: API_V1,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadImageFile = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post<UploadResponse>('/upload/file', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const uploadImageUrl = async (url: string): Promise<UploadResponse> => {
  const response = await api.post<UploadResponse>('/upload/url', { url });
  return response.data;
};

export const listImages = async (): Promise<Image[]> => {
  const response = await api.get<Image[]>('/images');
  return response.data;
};

export const getImage = async (id: number): Promise<Image> => {
  const response = await api.get<Image>(`/images/${id}`);
  return response.data;
};

export const getConfig = async (): Promise<Config> => {
  const response = await api.get<Config>('/config');
  return response.data;
};
