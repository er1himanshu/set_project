export interface ImageMetadata {
  id: number;
  filename: string;
  original_url?: string;
  upload_method: string;
  storage_url?: string;
  storage_provider?: string;
  format: string;
  width?: number;
  height?: number;
  size_bytes?: number;
  aspect_ratio?: number;
  processing_status: string;
  quality_score?: number;
  quality_reasons?: string[];
  validation_passed: boolean;
  validation_errors?: string[];
  compliance_passed?: boolean;
  compliance_flags?: string[];
  is_duplicate: boolean;
  duplicate_of_id?: number;
  similarity_score?: number;
  cluster_id?: string;
  created_at?: string;
  updated_at?: string;
  processed_at?: string;
}

export interface ImageUploadResponse {
  id: number;
  filename: string;
  upload_method: string;
  processing_status: string;
  message: string;
}

export interface ConfigResponse {
  max_image_size_mb: number;
  allowed_formats: string[];
  min_aspect_ratio: number;
  max_aspect_ratio: number;
  min_resolution: number;
  min_quality_score: number;
  min_sharpness_score: number;
  min_brightness_score: number;
}
