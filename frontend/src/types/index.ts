export interface Image {
  id: number;
  filename: string;
  original_url?: string;
  storage_path?: string;
  file_size?: number;
  width?: number;
  height?: number;
  format?: string;
  status: string;
  quality_score?: number;
  quality_reasons?: string[];
  is_compliant?: boolean;
  compliance_flags?: string[];
  is_duplicate: boolean;
  duplicate_of_id?: number;
  cluster_id?: string;
  created_at: string;
  updated_at?: string;
  processed_at?: string;
  error_message?: string;
}

export interface Config {
  max_file_size_mb: number;
  min_width: number;
  min_height: number;
  max_width: number;
  max_height: number;
  allowed_formats: string[];
  min_quality_score: number;
  min_resolution_threshold: number;
  max_compression_artifacts: number;
}

export interface UploadResponse {
  id: number;
  filename: string;
  status: string;
  message: string;
}
