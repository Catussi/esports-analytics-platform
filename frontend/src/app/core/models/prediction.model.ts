export interface PerformanceMetrics {
  kills: number;
  deaths: number;
  assists: number;
  headshots: number;
  adr: number;
  kast: number;
  rating: number;
}

export interface PredictionRequest extends PerformanceMetrics {}

export interface PredictionResponse {
  cluster_id: number;
  cluster_label: string;
  analytical_feedback: string;
  confidence_score: number;
  pca_components: number[];
  feature_vector: string[];
}
