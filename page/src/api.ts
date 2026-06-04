export interface ClassificationMetrics {
  type: 'classification';
  model_name: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1: number;
  roc_auc: number;
  threshold: number;
  pca_components?: number;
  pca_variance?: number;
}

export interface RegressionMetrics {
  type: 'regression';
  model_name: string;
  r2: number;
  mae: number;
  rmse: number;
  all_models: Array<{ modelo: string; R2_test: number; MAE_test: number; RMSE_test: number }>;
}

export type ModelMetrics = ClassificationMetrics | RegressionMetrics;

export interface SummariesResponse {
  logistica?: ModelMetrics;
  knn?: ModelMetrics;
  'decision-tree'?: ModelMetrics;
  salario?: ModelMetrics;
  'logistica-pca'?: ModelMetrics;
  'decision-tree-pca'?: ModelMetrics;
  'naive-bayes'?: ModelMetrics;
  svm?: ModelMetrics;
}

export interface PlatformRate { name: string; value: number }
export interface SalaryByMajor { major: string; salary: number }
export interface Correlation { feature: string; correlation: number }
export interface TrackingItem { name: string; value: number }
export interface PieItem { name: string; value: number }

export interface EdaResponse {
  total_records: number;
  offer_rate: number;
  avg_salary: number;
  completeness: number;
  platform_offer_rates: PlatformRate[];
  salary_by_major: SalaryByMajor[];
  correlations: Correlation[];
  tracking: TrackingItem[];
  pie_data: PieItem[];
}

export interface ClusterProfile {
  cluster: number;
  n_estudiantes: number;
  no_oferta: number;
  si_oferta: number;
  offer_rate_pct: number;
  plataforma_dominante: string;
  aplicaciones_promedio: number;
  meses_busqueda_promedio: number;
  entrevistas_primera_ronda: number;
}

export interface ClusteringResponse {
  dataset_size: number;
  baseline_offer_rate_pct: number;
  algorithms: {
    kmeans: {
      k: number;
      silhouette: number;
      dunn: number;
      cluster_profiles: ClusterProfile[];
    };
    jerarquico: {
      k: number;
      silhouette: number | null;
      dunn: number | null;
      sample_size: number;
    };
    dbscan: {
      eps: number;
      min_samples: number;
      n_clusters: number;
      n_ruido: number;
      silhouette: number | null;
    };
  };
  conclusion: string;
}

export interface ClassificationResult {
  type: 'classification';
  total: number;
  positive: number;
  negative: number;
  positive_rate: number;
  avg_probability: number;
  threshold_used: number;
}

export interface RegressionResult {
  type: 'regression';
  total: number;
  mean_salary: number;
  median_salary: number;
  min_salary: number;
  max_salary: number;
}

export type PredictionResult = ClassificationResult | RegressionResult;

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(path, options);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail ?? 'API error');
  }
  return res.json() as Promise<T>;
}

export async function fetchSummaries(): Promise<SummariesResponse> {
  return apiFetch<SummariesResponse>('/api/summaries');
}

export async function fetchEda(): Promise<EdaResponse> {
  return apiFetch<EdaResponse>('/api/eda');
}

export async function fetchClustering(): Promise<ClusteringResponse> {
  return apiFetch<ClusteringResponse>('/api/clustering');
}

export async function predictCsv(modelId: string, file: File): Promise<PredictionResult> {
  const form = new FormData();
  form.append('file', file);
  return apiFetch<PredictionResult>(`/api/predict/${modelId}`, { method: 'POST', body: form });
}

export async function checkHealth(): Promise<boolean> {
  try {
    await apiFetch('/api/health');
    return true;
  } catch {
    return false;
  }
}

export async function downloadPredictions(modelId: string, file: File): Promise<void> {
  const form = new FormData();
  form.append('file', file);
  const res = await fetch(`/api/predict-csv/${modelId}`, { method: 'POST', body: form });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail ?? 'Error al generar CSV');
  }
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `predicciones_${modelId}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
