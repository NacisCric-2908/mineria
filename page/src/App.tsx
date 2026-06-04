import React, { useState, useMemo, useEffect } from 'react';
import {
  LayoutDashboard,
  BrainCircuit,
  BarChart3,
  ChevronRight,
  GraduationCap,
  Users,
  Briefcase,
  TrendingUp,
  Database,
  Search,
  Menu,
  AlertCircle,
  DollarSign,
  Maximize2,
  X as XIcon,
  ImageIcon,
  FileDown,
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  PieChart,
  Pie,
} from 'recharts';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';
import LogoColor from '../images/LogoColor.png';
import LogoBlanco from '../images/LogoBlanco.png';
import {
  fetchSummaries,
  fetchEda,
  fetchClustering,
  predictCsv,
  downloadPredictions,
  checkHealth,
  type ModelMetrics,
  type ClassificationMetrics,
  type RegressionMetrics,
  type EdaResponse,
  type ClusteringResponse,
  type PredictionResult,
  type ClassificationResult,
  type RegressionResult,
  type SummariesResponse,
} from './api';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// --- Types ---

type ViewState = 'landing' | 'login' | 'dashboard';
type ModelID = 'eda' | 'logistica' | 'knn' | 'decision-tree' | 'salario' | 'logistica-pca' | 'decision-tree-pca' | 'naive-bayes' | 'svm' | 'clustering';

interface ModelInfo {
  id: ModelID;
  name: string;
  description: string;
  category: 'analysis' | 'ml' | 'ml-pca';
  icon: React.ReactNode;
  metrics?: ModelMetrics;
}

const MODEL_DEFINITIONS: Omit<ModelInfo, 'metrics'>[] = [
  {
    id: 'eda',
    name: 'Análisis Institucional',
    description: 'Insights globales extraídos de LinkedIn, Handshake e Indeed.',
    category: 'analysis',
    icon: <BarChart3 className="w-5 h-5" />,
  },
  {
    id: 'clustering',
    name: 'Análisis de Clustering',
    description: 'KMeans, Clustering Jerárquico y DBSCAN sobre perfiles de estudiantes.',
    category: 'analysis',
    icon: <Users className="w-5 h-5" />,
  },
  {
    id: 'logistica',
    name: 'Regresión Logística',
    description: 'Probabilidad base de oferta laboral con regularización L2.',
    category: 'ml',
    icon: <BrainCircuit className="w-5 h-5" />,
  },
  {
    id: 'knn',
    name: 'K-Nearest Neighbors',
    description: 'Clasificación por proximidad con reducción PCA al 90%.',
    category: 'ml-pca',
    icon: <Users className="w-5 h-5" />,
  },
  {
    id: 'decision-tree',
    name: 'Árbol de Decisión',
    description: 'Mapeo jerárquico de criterios de contratación.',
    category: 'ml',
    icon: <Database className="w-5 h-5" />,
  },
  {
    id: 'salario',
    name: 'Predicción de Salario',
    description: 'Regresión Lasso para estimar el salario de oferta laboral.',
    category: 'ml',
    icon: <DollarSign className="w-5 h-5" />,
  },
  {
    id: 'logistica-pca',
    name: 'Logística + PCA',
    description: 'Regresión Logística con reducción dimensional PCA al 90% de varianza.',
    category: 'ml-pca',
    icon: <BrainCircuit className="w-5 h-5" />,
  },
  {
    id: 'decision-tree-pca',
    name: 'Árbol de Decisión + PCA',
    description: 'Árbol de Decisión con reducción dimensional PCA al 90% de varianza.',
    category: 'ml-pca',
    icon: <Database className="w-5 h-5" />,
  },
  {
    id: 'naive-bayes',
    name: 'Naive Bayes',
    description: 'Clasificador probabilístico Gaussian con ajuste de umbral F-beta (1.5).',
    category: 'ml',
    icon: <BrainCircuit className="w-5 h-5" />,
  },
  {
    id: 'svm',
    name: 'Support Vector Machine',
    description: 'SVM con kernel RBF y threshold F-beta para clasificación de oferta laboral.',
    category: 'ml',
    icon: <BrainCircuit className="w-5 h-5" />,
  },
];

// --- Shared UI Components ---

const SidebarItem = ({
  item,
  active,
  onClick,
}: {
  item: ModelInfo;
  active: boolean;
  onClick: () => void;
}) => (
  <button
    onClick={onClick}
    className={cn(
      'w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all group',
      active
        ? 'bg-red-800 text-white shadow-lg shadow-red-900/20'
        : 'text-slate-400 hover:text-white hover:bg-white/10'
    )}
  >
    <span
      className={cn(
        'transition-colors',
        active ? 'text-white' : 'text-slate-500 group-hover:text-red-400'
      )}
    >
      {item.icon}
    </span>
    {item.name}
    {active && <ChevronRight className="w-4 h-4 ml-auto" />}
  </button>
);

const KPICard = ({
  title,
  value,
  icon,
  sub,
}: {
  title: string;
  value: string;
  icon: React.ReactNode;
  sub: string;
}) => (
  <div className="card p-6 flex items-start justify-between">
    <div>
      <p className="text-slate-500 text-sm font-medium mb-1">{title}</p>
      <h3 className="text-2xl font-bold text-slate-800">{value}</h3>
      <p className="text-xs text-green-600 font-medium mt-2">{sub}</p>
    </div>
    <div className="p-3 bg-red-50 text-red-800 rounded-lg">{icon}</div>
  </div>
);

const MetricPill = ({ label, value, formatted }: { label: string; value: string | number; formatted?: string }) => (
  <div className="bg-slate-50 px-4 py-3 rounded-xl border border-slate-100">
    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{label}</p>
    <p className="text-xl font-black text-red-800">
      {formatted ?? (typeof value === 'number' ? `${(value * 100).toFixed(1)}%` : (value || '—'))}
    </p>
  </div>
);

const Footer = ({ dark = false }: { dark?: boolean }) => (
  <footer
    className={cn(
      'py-12 border-t mt-auto',
      dark ? 'bg-slate-900 border-white/5 text-slate-400' : 'bg-white border-slate-100 text-slate-500'
    )}
  >
    <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-4 gap-12">
      <div className="col-span-1 md:col-span-2 space-y-4">
        <div className="flex items-center gap-2">
          <img
            src={dark ? LogoBlanco : LogoColor}
            alt="UniCareer ML"
            className="h-7 w-auto object-contain"
          />
        </div>
        <p className="text-sm max-w-sm leading-relaxed">
          Potenciando la toma de decisiones institucionales mediante el análisis predictivo de datos
          laborales a gran escala.
        </p>
      </div>
      <div>
        <h5
          className={cn(
            'font-bold text-xs uppercase tracking-widest mb-4',
            dark ? 'text-white' : 'text-slate-900'
          )}
        >
          Plataforma
        </h5>
        <ul className="text-sm space-y-2">
          <li>
            <a href="#" className="hover:text-red-800 transition-colors">
              Análisis de Datos
            </a>
          </li>
          <li>
            <a href="#" className="hover:text-red-800 transition-colors">
              Modelos .PKL
            </a>
          </li>
          <li>
            <a href="#" className="hover:text-red-800 transition-colors">
              Seguridad de Datos
            </a>
          </li>
        </ul>
      </div>
      <div>
        <h5
          className={cn(
            'font-bold text-xs uppercase tracking-widest mb-4',
            dark ? 'text-white' : 'text-slate-900'
          )}
        >
          Legal
        </h5>
        <ul className="text-sm space-y-2">
          <li>
            <a href="#" className="hover:text-red-800 transition-colors">
              Privacidad
            </a>
          </li>
          <li>
            <a href="#" className="hover:text-red-800 transition-colors">
              Términos
            </a>
          </li>
          <li>
            <a href="#" className="hover:text-red-800 transition-colors">
              Cookies
            </a>
          </li>
        </ul>
      </div>
    </div>
    <div className="max-w-7xl mx-auto px-6 mt-12 pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4 text-xs">
      <p>© 2026 Academia Moderna — Departamento de Ciencia de Datos</p>
      <div className="flex gap-4">
        <span className="flex items-center gap-1">
          <div className="w-2 h-2 rounded-full bg-green-500" /> v1.2.4-stable
        </span>
      </div>
    </div>
  </footer>
);

// --- Landing & Login ---

const LandingPage = ({ onStart }: { onStart: () => void }) => (
  <div className="min-h-screen bg-white font-sans text-slate-900 flex flex-col selection:bg-red-100 selection:text-red-900">
    <nav className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between w-full">
      <div className="flex items-center gap-2">
        <img src={LogoColor} alt="UniCareer ML" className="h-9 w-auto object-contain" />
      </div>
      <div className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-500 mr-8 ml-auto">
        <a href="#" className="hover:text-red-800 transition-colors">Instituciones</a>
        <a href="#" className="hover:text-red-800 transition-colors">Modelos</a>
        <a href="#" className="hover:text-red-800 transition-colors">Seguridad</a>
      </div>
      <button
        onClick={onStart}
        className="px-6 py-2.5 text-sm font-bold text-white bg-red-800 rounded-full hover:bg-slate-900 transition-all shadow-xl shadow-red-900/10 active:scale-95"
      >
        Acceso Portal
      </button>
    </nav>

    <main className="flex-1 max-w-7xl mx-auto px-6 pt-12 pb-24 grid lg:grid-cols-2 gap-16 items-center">
      <div className="space-y-8 animate-in fade-in slide-in-from-left-8 duration-1000">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-red-50 text-red-800 rounded-full text-[10px] font-black uppercase tracking-widest border border-red-100 italic">
          <Briefcase className="w-3 h-3" />
          The future of employability
        </div>
        <h1 className="text-7xl font-black text-slate-900 leading-[0.95] tracking-tighter">
          Donde los Datos se vuelven <span className="text-red-800">Carreras.</span>
        </h1>
        <p className="text-xl text-slate-500 leading-relaxed max-w-lg font-medium">
          Dashboard inteligente para instituciones académicas. Procesamiento masivo de datos mediante
          modelos <span className="text-slate-900 font-bold">.pkl</span> entrenados para predecir el
          éxito laboral.
        </p>
        <div className="flex flex-col sm:flex-row items-start sm:items-center gap-5">
          <button
            onClick={onStart}
            className="px-10 py-5 bg-red-800 text-white rounded-2xl font-black text-lg hover:bg-slate-900 transition-all shadow-2xl shadow-red-900/30 active:scale-95 group flex items-center gap-2"
          >
            Sincronizar Datos
            <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </button>
          <div className="flex flex-col">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">
              Integraciones API
            </span>
            <div className="flex gap-4 opacity-40 grayscale hover:grayscale-0 transition-all">
              <div className="font-black text-sm">LinkedIn</div>
              <div className="font-black text-sm">Handshake</div>
              <div className="font-black text-sm">Indeed</div>
            </div>
          </div>
        </div>
      </div>

      <div className="relative animate-in zoom-in-95 fade-in duration-1000 delay-300">
        <div className="absolute -inset-10 bg-red-800/5 rounded-full blur-3xl" />
        <div className="relative h-[500px] w-full flex items-center justify-center">
          <div className="grid grid-cols-2 gap-4 w-full">
            <div className="space-y-4">
              <div className="card p-6 aspect-square flex flex-col justify-between bg-red-900 text-white border-none shadow-2xl -rotate-3 transition-transform hover:rotate-0 duration-500">
                <BarChart3 className="w-12 h-12 opacity-50" />
                <div>
                  <div className="h-2 w-12 bg-white/20 rounded-full mb-2" />
                  <div className="h-4 w-24 bg-white rounded-full" />
                </div>
              </div>
              <div className="card p-6 h-40 flex items-center justify-center bg-slate-900 text-white border-none shadow-xl rotate-6 transition-transform hover:rotate-0 duration-500">
                <Search className="w-8 h-8 opacity-40 text-red-500 animate-pulse" />
              </div>
            </div>
            <div className="space-y-4 pt-12">
              <div className="card p-6 h-48 bg-white border-slate-200 shadow-xl -rotate-6 transition-transform hover:rotate-0 duration-500">
                <div className="flex gap-2">
                  {[1, 2, 3].map((i) => (
                    <div key={i} className="w-2 h-2 rounded-full bg-slate-100" />
                  ))}
                </div>
                <div className="mt-6 space-y-3">
                  <div className="h-2 w-full bg-slate-100 rounded-full" />
                  <div className="h-2 w-[80%] bg-slate-100 rounded-full" />
                  <div className="h-2 w-[40%] bg-red-800 rounded-full" />
                </div>
              </div>
              <div className="card p-6 aspect-square flex items-center justify-center bg-red-600 text-white border-none shadow-2xl rotate-3 transition-transform hover:rotate-0 duration-500">
                <BrainCircuit className="w-16 h-16" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <div className="max-w-7xl mx-auto px-6 py-20">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
        {[
          { label: 'Registros Activos', val: '100,000' },
          { label: 'Variables Analizadas', val: '40' },
          { label: 'Modelos Entrenados', val: '9' },
          { label: 'Inferencia en Lote', val: 'Real .pkl' },
        ].map((s) => (
          <div key={s.label}>
            <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1 italic">
              {s.label}
            </p>
            <p className="text-3xl font-black text-slate-900 tracking-tighter">{s.val}</p>
          </div>
        ))}
      </div>
    </div>

    <Footer />
  </div>
);

const LoginPage = ({ onLogin }: { onLogin: () => void }) => (
  <div className="min-h-screen bg-slate-50 flex flex-col selection:bg-red-100 selection:text-red-900">
    <div className="flex-1 flex items-center justify-center px-6 py-20">
      <div className="w-full max-w-md">
        <div className="flex flex-col items-center mb-8">
          <div className="w-16 h-16 bg-red-800 rounded-2xl flex items-center justify-center shadow-2xl shadow-red-900/30 mb-4">
            <GraduationCap className="text-white w-10 h-10" />
          </div>
          <h2 className="text-2xl font-bold">Acceso Institucional</h2>
          <p className="text-slate-500 text-sm font-medium">Portal de Ciencia de Datos Académicos</p>
        </div>

        <div className="card p-8 bg-white shadow-xl border-none ring-1 ring-slate-100">
          <form
            className="space-y-6"
            onSubmit={(e) => {
              e.preventDefault();
              onLogin();
            }}
          >
            <div className="space-y-2">
              <label className="text-sm font-bold text-slate-700">Email Corporativo</label>
              <input
                type="email"
                defaultValue="admin@universidad.edu"
                className="input-field bg-slate-50"
                placeholder="admin@universidad.edu"
              />
            </div>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <label className="text-sm font-bold text-slate-700">Contraseña</label>
                <a href="#" className="text-xs text-red-800 font-bold">
                  ¿Olvidó su clave?
                </a>
              </div>
              <input
                type="password"
                defaultValue="password123"
                className="input-field bg-slate-50"
              />
            </div>
            <button
              type="submit"
              className="btn-primary w-full py-4 text-sm font-black uppercase tracking-widest shadow-xl shadow-red-900/20"
            >
              Entrar al Dashboard
            </button>
          </form>
        </div>

        <p className="text-center text-xs text-slate-400 mt-8 font-medium">
          Sistema en cumplimiento con GDPR y Protección de Datos Estudiantiles.
        </p>
      </div>
    </div>
    <Footer />
  </div>
);

// --- Image Gallery ---

interface GalleryImage {
  filename: string;
  label: string;
  section: string;
}

interface GalleryTab {
  id: string;
  label: string;
  images: GalleryImage[];
}

const GALLERY_CONFIGS: Record<string, GalleryTab[]> = {
  eda: [
    {
      id: 'exploracion',
      label: 'Exploración',
      images: [
        { filename: '04_exploracion_dataset_dimensions.png', label: 'Dimensiones del Dataset', section: 'silver' },
        { filename: '04_tipos_variables.png', label: 'Tipos de Variables', section: 'silver' },
        { filename: '04_valores_faltantes.png', label: 'Valores Faltantes', section: 'silver' },
        { filename: '04_tamaño_escala_dataset.png', label: 'Escala del Dataset', section: 'silver' },
        { filename: '04_relevancia_calidad_4preguntas.png', label: 'Calidad de los Datos', section: 'silver' },
        { filename: 'visualizacion_limpieza_resumen.png', label: 'Resumen de Limpieza', section: 'silver' },
      ],
    },
    {
      id: 'distribuciones',
      label: 'Distribuciones',
      images: [
        { filename: 'histogramas_base.png', label: 'Histogramas de Variables', section: 'silver' },
        { filename: 'boxplots_base.png', label: 'Boxplots Generales', section: 'silver' },
        { filename: 'scatterplots_base.png', label: 'Scatter Plots Base', section: 'silver' },
      ],
    },
    {
      id: 'bivariado',
      label: 'Análisis Bivariado',
      images: [
        { filename: '05_bivariado_scatter_plots.png', label: 'Scatter Bivariado', section: 'silver' },
        { filename: '06_bivariado_heatmap_correlacion.png', label: 'Heatmap de Correlación', section: 'silver' },
        { filename: '07_bivariado_pairplot.png', label: 'Pairplot Completo', section: 'silver' },
        { filename: '08_bivariado_boxplot_violin_strip.png', label: 'Boxplot · Violin · Strip', section: 'silver' },
        { filename: '09_bivariado_lineas_areas_barras.png', label: 'Líneas · Áreas · Barras', section: 'silver' },
        { filename: 'correlation_matrix.png', label: 'Matriz de Correlación', section: 'silver' },
      ],
    },
  ],
  logistica: [
    {
      id: 'optimizado',
      label: 'Modelo Optimizado',
      images: [
        { filename: 'logistic_regression_roc_curve.png', label: 'Curva ROC', section: 'logistica' },
        { filename: 'logistic_regression_precision_recall_curve.png', label: 'Precisión-Recall', section: 'logistica' },
        { filename: 'logistic_regression_confusion_matrix.png', label: 'Matriz de Confusión', section: 'logistica' },
        { filename: 'logistic_regression_threshold_tradeoff.png', label: 'Análisis de Umbral', section: 'logistica' },
        { filename: 'logistic_regression_top_coefficients.png', label: 'Top Coeficientes', section: 'logistica' },
      ],
    },
    {
      id: 'base',
      label: 'Modelo Base',
      images: [
        { filename: 'logistic_roc_base.png', label: 'Curva ROC (Base)', section: 'logistica' },
        { filename: 'logistic_pr_base.png', label: 'Precisión-Recall (Base)', section: 'logistica' },
        { filename: 'logistic_confusion_matrix_base.png', label: 'Confusión (Base)', section: 'logistica' },
        { filename: 'logistic_threshold_base.png', label: 'Umbral (Base)', section: 'logistica' },
      ],
    },
  ],
  knn: [
    {
      id: 'pca',
      label: 'Modelo PCA (Optimizado)',
      images: [
        { filename: 'knn_roc_pca.png', label: 'Curva ROC — PCA', section: 'knn' },
        { filename: 'knn_pr_pca.png', label: 'Precisión-Recall — PCA', section: 'knn' },
        { filename: 'knn_confusion_pca.png', label: 'Confusión — PCA', section: 'knn' },
        { filename: 'knn_threshold_pca.png', label: 'Umbral — PCA', section: 'knn' },
        { filename: 'knn_pca_variance.png', label: 'Varianza Explicada PCA', section: 'knn' },
        { filename: 'knn_pca_loadings.png', label: 'PCA Loadings', section: 'knn' },
        { filename: 'knn_model_comparison.png', label: 'Base vs PCA', section: 'knn' },
      ],
    },
    {
      id: 'base',
      label: 'Modelo Base',
      images: [
        { filename: 'knn_roc_base.png', label: 'Curva ROC (Base)', section: 'knn' },
        { filename: 'knn_pr_base.png', label: 'Precisión-Recall (Base)', section: 'knn' },
        { filename: 'knn_confusion_base.png', label: 'Confusión (Base)', section: 'knn' },
        { filename: 'knn_threshold_base.png', label: 'Umbral (Base)', section: 'knn' },
      ],
    },
  ],
  'decision-tree': [
    {
      id: 'optimizado',
      label: 'Modelo Optimizado',
      images: [
        { filename: 'decision_tree_roc_curve.png', label: 'Curva ROC', section: 'decision-tree' },
        { filename: 'decision_tree_precision_recall_curve.png', label: 'Precisión-Recall', section: 'decision-tree' },
        { filename: 'decision_tree_confusion_matrix.png', label: 'Matriz de Confusión', section: 'decision-tree' },
        { filename: 'decision_tree_threshold_tradeoff.png', label: 'Análisis de Umbral', section: 'decision-tree' },
        { filename: 'decision_tree_feature_importance.png', label: 'Importancia de Variables', section: 'decision-tree' },
        { filename: 'decision_tree_tree_preview.png', label: 'Vista del Árbol', section: 'decision-tree' },
      ],
    },
    {
      id: 'reglas',
      label: 'Reglas & Comparativa',
      images: [
        { filename: 'decision_tree_rule_comparison.png', label: 'Comparativa de Reglas', section: 'decision-tree' },
      ],
    },
    {
      id: 'base',
      label: 'Modelo Base',
      images: [
        { filename: 'decision_tree_roc_base.png', label: 'Curva ROC (Base)', section: 'decision-tree' },
        { filename: 'decision_tree_pr_base.png', label: 'Precisión-Recall (Base)', section: 'decision-tree' },
        { filename: 'decision_tree_confusion_base.png', label: 'Confusión (Base)', section: 'decision-tree' },
        { filename: 'decision_tree_threshold_base.png', label: 'Umbral (Base)', section: 'decision-tree' },
      ],
    },
  ],
  salario: [
    {
      id: 'lasso',
      label: 'Lasso (Mejor Modelo)',
      images: [
        { filename: 'lasso_real_vs_predicho.png', label: 'Real vs Predicho', section: 'salario' },
        { filename: 'lasso_residuos_vs_prediccion.png', label: 'Residuos vs Predicción', section: 'salario' },
        { filename: 'lasso_residuos_hist.png', label: 'Histograma de Residuos', section: 'salario' },
        { filename: 'lasso_top_weights.png', label: 'Top Pesos del Modelo', section: 'salario' },
      ],
    },
    {
      id: 'comparativa',
      label: 'Comparativa de Modelos',
      images: [
        { filename: 'comparacion_r2_test.png', label: 'Comparación R² (Test)', section: 'regresion' },
        { filename: 'comparacion_rmse_test.png', label: 'Comparación RMSE (Test)', section: 'regresion' },
      ],
    },
  ],
  'logistica-pca': [
    {
      id: 'resultados',
      label: 'Resultados PCA',
      images: [
        { filename: 'logistica_pca_roc_curve.png', label: 'Curva ROC', section: 'logistica-pca' },
        { filename: 'logistica_pca_pr_curve.png', label: 'Precisión-Recall', section: 'logistica-pca' },
        { filename: 'logistica_pca_confusion_matrix.png', label: 'Matriz de Confusión', section: 'logistica-pca' },
        { filename: 'logistica_pca_pca_variance.png', label: 'Varianza Explicada PCA', section: 'logistica-pca' },
        { filename: 'logistica_pca_threshold.png', label: 'Análisis de Umbral', section: 'logistica-pca' },
      ],
    },
  ],
  'decision-tree-pca': [
    {
      id: 'resultados',
      label: 'Resultados PCA',
      images: [
        { filename: 'decision_tree_pca_roc_curve.png', label: 'Curva ROC', section: 'decision-tree-pca' },
        { filename: 'decision_tree_pca_pr_curve.png', label: 'Precisión-Recall', section: 'decision-tree-pca' },
        { filename: 'decision_tree_pca_confusion_matrix.png', label: 'Matriz de Confusión', section: 'decision-tree-pca' },
        { filename: 'decision_tree_pca_pca_variance.png', label: 'Varianza Explicada PCA', section: 'decision-tree-pca' },
        { filename: 'decision_tree_pca_threshold.png', label: 'Análisis de Umbral', section: 'decision-tree-pca' },
      ],
    },
  ],
  'naive-bayes': [
    {
      id: 'resultados',
      label: 'Modelo Optimizado',
      images: [
        { filename: 'naive_bayes_confusion_matrix.png', label: 'Matriz de Confusión', section: 'naive-bayes' },
        { filename: 'naive_bayes_roc_curve.png', label: 'Curva ROC', section: 'naive-bayes' },
        { filename: 'naive_bayes_precision_recall_curve.png', label: 'Precisión-Recall', section: 'naive-bayes' },
        { filename: 'naive_bayes_threshold_tradeoff.png', label: 'Análisis de Umbral', section: 'naive-bayes' },
        { filename: 'naive_bayes_model_comparison.png', label: 'Comparativa Base vs Optimizado', section: 'naive-bayes' },
      ],
    },
    {
      id: 'base',
      label: 'Modelo Base',
      images: [
        { filename: 'naive_bayes_confusion_matrix_base.png', label: 'Confusión (Base)', section: 'naive-bayes' },
        { filename: 'naive_bayes_roc_base.png', label: 'Curva ROC (Base)', section: 'naive-bayes' },
        { filename: 'naive_bayes_pr_base.png', label: 'Precisión-Recall (Base)', section: 'naive-bayes' },
        { filename: 'naive_bayes_target_distribution.png', label: 'Distribución del Target', section: 'naive-bayes' },
      ],
    },
  ],
  svm: [
    {
      id: 'optimizado',
      label: 'Modelo Optimizado (RBF)',
      images: [
        { filename: 'svm_confusion_matrix.png',       label: 'Matriz de Confusión',     section: 'svm' },
        { filename: 'svm_roc_curve.png',              label: 'Curva ROC',               section: 'svm' },
        { filename: 'svm_precision_recall_curve.png', label: 'Precisión-Recall',        section: 'svm' },
        { filename: 'svm_threshold_tradeoff.png',     label: 'Análisis de Umbral',      section: 'svm' },
        { filename: 'svm_model_comparison.png',       label: 'Comparativa Base vs RBF', section: 'svm' },
      ],
    },
    {
      id: 'base',
      label: 'Modelo Base (Lineal)',
      images: [
        { filename: 'svm_confusion_matrix_base.png',  label: 'Confusión (Base)',        section: 'svm' },
        { filename: 'svm_roc_curve_base.png',         label: 'Curva ROC (Base)',        section: 'svm' },
        { filename: 'svm_pr_base.png',                label: 'Precisión-Recall (Base)', section: 'svm' },
        { filename: 'comparativa_modelos_svm.png',    label: 'Comparativa Original',    section: 'svm' },
        { filename: 'efecto_C_svm_rbf.png',           label: 'Efecto del Parámetro C',  section: 'svm' },
      ],
    },
  ],
};

const ImageGallery = ({ tabs, title }: { tabs: GalleryTab[]; title: string }) => {
  const [activeTab, setActiveTab] = useState(tabs[0]?.id ?? '');
  const [lightbox, setLightbox] = useState<{ src: string; label: string } | null>(null);

  useEffect(() => {
    if (!lightbox) return;
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') setLightbox(null); };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [lightbox]);

  const current = tabs.find((t) => t.id === activeTab) ?? tabs[0];

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <ImageIcon className="w-5 h-5 text-red-800" />
          <h4 className="text-lg font-bold text-slate-800">{title}</h4>
        </div>
        {/* Tabs */}
        <div className="flex gap-2 flex-wrap">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={cn(
                'px-3 py-1.5 rounded-full text-xs font-bold transition-all',
                activeTab === tab.id
                  ? 'bg-red-800 text-white shadow-md shadow-red-900/20'
                  : 'bg-slate-100 text-slate-500 hover:bg-slate-200 hover:text-slate-700'
              )}
            >
              {tab.label}
              <span className={cn(
                'ml-1.5 text-[9px] font-black px-1 rounded-full',
                activeTab === tab.id ? 'bg-white/20 text-white' : 'bg-slate-200 text-slate-400'
              )}>
                {tab.images.length}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-4">
        {current.images.map((img) => {
          const src = `/api/images/${img.section}/${encodeURIComponent(img.filename)}`;
          return (
            <button
              key={img.filename}
              onClick={() => setLightbox({ src, label: img.label })}
              className="card overflow-hidden text-left group focus:outline-none focus:ring-2 focus:ring-red-800 focus:ring-offset-2 rounded-xl"
            >
              <div className="relative bg-slate-50 h-44 flex items-center justify-center p-3 overflow-hidden">
                <img
                  src={src}
                  alt={img.label}
                  className="max-h-full max-w-full object-contain transition-transform duration-300 group-hover:scale-[1.06]"
                  loading="lazy"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-900/0 to-slate-900/0 group-hover:from-slate-900/30 transition-all duration-300 flex items-center justify-center">
                  <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-200 bg-white rounded-full p-2 shadow-lg">
                    <Maximize2 className="w-4 h-4 text-red-800" />
                  </div>
                </div>
              </div>
              <div className="px-3 py-2.5 border-t border-slate-100 bg-white">
                <p className="text-[11px] font-bold text-slate-600 truncate">{img.label}</p>
              </div>
            </button>
          );
        })}
      </div>

      {/* Lightbox */}
      {lightbox && (
        <div
          className="fixed inset-0 bg-black/90 z-[200] flex flex-col items-center justify-center p-4 md:p-10"
          onClick={() => setLightbox(null)}
        >
          <div
            className="relative w-full max-w-5xl flex flex-col gap-4"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Lightbox header */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-1 h-6 bg-red-600 rounded-full" />
                <p className="text-white font-bold text-sm">{lightbox.label}</p>
              </div>
              <button
                onClick={() => setLightbox(null)}
                className="text-white/60 hover:text-white p-2 rounded-full hover:bg-white/10 transition-colors"
              >
                <XIcon className="w-5 h-5" />
              </button>
            </div>
            {/* Image */}
            <div className="bg-white/5 rounded-2xl overflow-hidden flex items-center justify-center p-4 max-h-[82vh]">
              <img
                src={lightbox.src}
                alt={lightbox.label}
                className="max-h-[78vh] max-w-full object-contain rounded-lg"
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// --- EDA View ---

const COLORS = ['#991b1b', '#b91c1c', '#dc2626', '#ef4444', '#f87171', '#fca5a5'];

const EDAView = ({ apiOnline }: { apiOnline: boolean }) => {
  const [data, setData] = useState<EdaResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!apiOnline) { setLoading(false); return; }
    fetchEda()
      .then(setData)
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, [apiOnline]);

  const fmt = (n: number) =>
    new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(n);

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="card p-6 animate-pulse">
            <div className="h-4 bg-slate-100 rounded w-24 mb-3" />
            <div className="h-8 bg-slate-200 rounded w-32" />
          </div>
        ))}
      </div>
    );
  }

  if (!data) {
    return (
      <div className="card p-8 flex items-center gap-4 border-amber-200 bg-amber-50">
        <AlertCircle className="w-6 h-6 text-amber-500 shrink-0" />
        <div>
          <p className="font-bold text-amber-800">API no disponible</p>
          <p className="text-sm text-amber-700">
            Inicia el servidor con: <code className="bg-amber-100 px-1 rounded">cd page && python -m uvicorn api.server:app --reload --port 8000</code>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KPICard
          title="Total Registros"
          value={data.total_records.toLocaleString('es-CO')}
          icon={<Database className="w-6 h-6" />}
          sub="Dataset limpio · 40 variables"
        />
        <KPICard
          title="Tasa de Ofertas"
          value={`${data.offer_rate}%`}
          icon={<Briefcase className="w-6 h-6" />}
          sub="Estudiantes con oferta recibida"
        />
        <KPICard
          title="Salario Promedio"
          value={fmt(data.avg_salary)}
          icon={<TrendingUp className="w-6 h-6" />}
          sub="Entre quienes recibieron oferta"
        />
        <KPICard
          title="Integridad"
          value={`${data.completeness}%`}
          icon={<Users className="w-6 h-6" />}
          sub="Filas sin pérdidas en limpieza"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="card p-6">
          <div className="flex items-center justify-between mb-8">
            <h4 className="text-lg font-bold flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-red-800" />
              Tasa de Oferta por Plataforma
            </h4>
            <span className="text-[10px] font-bold text-slate-400 bg-slate-50 px-2 py-1 rounded">
              SILVER LAYER
            </span>
          </div>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.platform_offer_rates}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="name" tick={{ fontSize: 11, fontWeight: 600 }} />
                <YAxis tick={{ fontSize: 10 }} tickFormatter={(v) => `${v}%`} domain={[0, 50]} />
                <Tooltip formatter={(v: number) => [`${v}%`, 'Tasa de oferta']} />
                <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                  {data.platform_offer_rates.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card p-6">
          <h4 className="text-lg font-bold mb-8 flex items-center gap-2">
            <GraduationCap className="w-5 h-5 text-red-800" />
            Salario Promedio por Área (USD)
          </h4>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.salary_by_major} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f1f5f9" />
                <XAxis type="number" tick={{ fontSize: 10 }} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
                <YAxis dataKey="major" type="category" width={110} tick={{ fontSize: 10, fontWeight: 500 }} />
                <Tooltip formatter={(v: number) => [fmt(v), 'Salario promedio']} />
                <Bar dataKey="salary" fill="#991b1b" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-1 card p-6">
          <h4 className="text-sm font-bold mb-6 text-slate-400 uppercase tracking-widest">
            Registros por Plataforma
          </h4>
          <div className="h-64 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data.pie_data}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={80}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {data.pie_data.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(v: number) => [v.toLocaleString('es-CO'), 'Registros']} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="grid grid-cols-2 gap-2 mt-2">
            {data.pie_data.map((d, i) => (
              <div key={d.name} className="flex items-center gap-2 text-[10px] font-bold text-slate-500">
                <div className="w-2 h-2 rounded-full shrink-0" style={{ background: COLORS[i % COLORS.length] }} />
                {d.name}
              </div>
            ))}
          </div>
        </div>

        <div className="lg:col-span-2 card p-6 bg-slate-900 text-white relative overflow-hidden">
          <div className="absolute top-0 right-0 p-8 opacity-10">
            <LayoutDashboard className="w-48 h-48" />
          </div>
          <div className="relative z-10">
            <h4 className="text-xl font-bold mb-2">Top Correlaciones con Oferta Recibida</h4>
            <p className="text-slate-400 text-sm mb-6 max-w-lg">
              Variables con mayor correlación de Pearson con la variable objetivo (Silver Layer).
            </p>
            <div className="space-y-3">
              {data.correlations.slice(0, 6).map((c) => (
                <div key={c.feature} className="flex items-center gap-3">
                  <span className="text-xs text-slate-400 w-44 truncate font-medium">{c.feature}</span>
                  <div className="flex-1 bg-white/10 rounded-full h-2 overflow-hidden">
                    <div
                      className="h-2 rounded-full bg-red-500"
                      style={{ width: `${Math.abs(c.correlation) * 100}%` }}
                    />
                  </div>
                  <span className="text-xs font-bold w-12 text-right">{c.correlation.toFixed(3)}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* EDA Image Gallery */}
      <div className="card p-6">
        <ImageGallery tabs={GALLERY_CONFIGS['eda']} title="Visualizaciones del Análisis Exploratorio" />
      </div>
    </div>
  );
};

// --- Clustering View ---

const ClusteringView = ({ apiOnline }: { apiOnline: boolean }) => {
  const [data, setData] = useState<ClusteringResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!apiOnline) { setLoading(false); return; }
    fetchClustering()
      .then(setData)
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, [apiOnline]);

  if (loading) return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {[...Array(3)].map((_, i) => (
        <div key={i} className="card p-6 animate-pulse">
          <div className="h-4 bg-slate-100 rounded w-24 mb-3" />
          <div className="h-8 bg-slate-200 rounded w-32" />
        </div>
      ))}
    </div>
  );

  if (!data) return (
    <div className="card p-8 flex items-center gap-4 border-amber-200 bg-amber-50">
      <AlertCircle className="w-6 h-6 text-amber-500 shrink-0" />
      <div>
        <p className="font-bold text-amber-800">API no disponible</p>
        <p className="text-sm text-amber-700">
          Inicia el servidor con:{' '}
          <code className="bg-amber-100 px-1 rounded">
            python -m uvicorn api.server:app --reload --port 8000
          </code>
        </p>
      </div>
    </div>
  );

  const km = data.algorithms.kmeans;
  const hier = data.algorithms.jerarquico;
  const db = data.algorithms.dbscan;
  const CLUSTER_COLORS = ['#991b1b', '#1d4ed8'];

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <KPICard
          title="Silhouette KMeans"
          value={km.silhouette.toFixed(4)}
          icon={<Database className="w-6 h-6" />}
          sub={`k=${km.k} · estructura débil (< 0.10)`}
        />
        <KPICard
          title="Silhouette Jerárquico"
          value={hier.silhouette != null ? hier.silhouette.toFixed(4) : '—'}
          icon={<Users className="w-6 h-6" />}
          sub={`muestra ${hier.sample_size.toLocaleString('es-CO')} filas`}
        />
        <KPICard
          title="Clusters DBSCAN"
          value={String(db.n_clusters)}
          icon={<Search className="w-6 h-6" />}
          sub={`eps=${db.eps} · ${db.n_ruido.toLocaleString('es-CO')} puntos ruido`}
        />
      </div>

      <div className="card p-6">
        <h4 className="text-lg font-bold mb-4 flex items-center gap-2">
          <Users className="w-5 h-5 text-red-800" />
          Perfiles de Clusters — KMeans (k={km.k})
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          {km.cluster_profiles.map((p) => (
            <div key={p.cluster} className="bg-slate-50 rounded-xl p-5 border border-slate-100">
              <div className="flex items-center justify-between mb-4">
                <h5 className="font-bold text-slate-800">Cluster {p.cluster}</h5>
                <span
                  className="text-xs font-bold px-2 py-1 rounded-full"
                  style={{ background: CLUSTER_COLORS[p.cluster] + '22', color: CLUSTER_COLORS[p.cluster] }}
                >
                  {p.n_estudiantes.toLocaleString('es-CO')} est.
                </span>
              </div>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <p className="text-slate-400 text-xs font-bold uppercase">Plataforma</p>
                  <p className="font-bold text-red-800">{p.plataforma_dominante}</p>
                </div>
                <div>
                  <p className="text-slate-400 text-xs font-bold uppercase">Tasa de Oferta</p>
                  <p className="font-bold text-slate-800">{p.offer_rate_pct.toFixed(1)}%</p>
                </div>
                <div>
                  <p className="text-slate-400 text-xs font-bold uppercase">Aplicaciones Avg</p>
                  <p className="font-bold text-slate-800">{p.aplicaciones_promedio}</p>
                </div>
                <div>
                  <p className="text-slate-400 text-xs font-bold uppercase">Meses Búsqueda</p>
                  <p className="font-bold text-slate-800">{p.meses_busqueda_promedio}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
        <div className="p-4 bg-slate-900 text-slate-300 rounded-xl text-sm">
          <p className="font-bold text-white mb-1">Hallazgo principal</p>
          <p>{data.conclusion}</p>
        </div>
      </div>

      <div className="card p-6">
        <ImageGallery
          tabs={[{
            id: 'resultados',
            label: 'Visualizaciones',
            images: [
              { filename: 'clustering_kmeans_scatter.png', label: 'KMeans — Proyección PCA 2D', section: 'clustering' },
              { filename: 'clustering_silhouette_comparison.png', label: 'Comparativa Silhouette', section: 'clustering' },
              { filename: 'clustering_offer_rate_by_cluster.png', label: 'Tasa de Oferta por Cluster', section: 'clustering' },
            ],
          }]}
          title="Visualizaciones de Clustering"
        />
      </div>
    </div>
  );
};

// --- Model View ---

const ClassificationResultCard = ({ result }: { result: ClassificationResult }) => {
  const circ = 2 * Math.PI * 70;
  const offset = circ - (circ * result.positive_rate) / 100;
  return (
    <div className="card p-8 text-center bg-white relative overflow-hidden min-h-[300px] flex flex-col items-center justify-center border border-red-100">
      <div className="absolute top-0 right-0 p-4 opacity-5">
        <BrainCircuit className="w-32 h-32 text-red-800" />
      </div>
      <p className="text-red-400 text-[10px] font-bold uppercase tracking-widest mb-4">
        Resultado — {result.total.toLocaleString('es-CO')} registros
      </p>
      <div className="relative inline-flex items-center justify-center">
        <svg className="w-40 h-40 transform -rotate-90">
          <circle className="text-red-100" strokeWidth="12" stroke="currentColor" fill="transparent" r="70" cx="80" cy="80" />
          <circle
            className="text-red-700 transition-all duration-1000 ease-out"
            strokeWidth="12"
            strokeDasharray={circ}
            strokeDashoffset={offset}
            strokeLinecap="round"
            stroke="currentColor"
            fill="transparent"
            r="70"
            cx="80"
            cy="80"
          />
        </svg>
        <div className="absolute flex flex-col items-center">
          <span className="text-4xl font-black text-red-800">{result.positive_rate.toFixed(1)}%</span>
          <span className="text-xs text-red-400 uppercase font-bold">con oferta</span>
        </div>
      </div>
      <div className="mt-6 grid grid-cols-2 gap-4 w-full max-w-xs">
        <div className="bg-red-50 rounded-xl p-3 text-center border border-red-100">
          <p className="text-xs text-red-400 uppercase font-bold mb-1">Recibirán oferta</p>
          <p className="text-xl font-black text-red-800">{result.positive.toLocaleString('es-CO')}</p>
        </div>
        <div className="bg-red-50 rounded-xl p-3 text-center border border-red-100">
          <p className="text-xs text-red-400 uppercase font-bold mb-1">Sin oferta</p>
          <p className="text-xl font-black text-slate-700">{result.negative.toLocaleString('es-CO')}</p>
        </div>
      </div>
      <p className="mt-4 text-xs text-slate-400">
        Umbral: {Number(result.threshold_used).toFixed(3)} · P̄ = {result.avg_probability.toFixed(1)}%
      </p>
    </div>
  );
};

const RegressionResultCard = ({ result }: { result: RegressionResult }) => {
  const fmt = (n: number) =>
    new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(n);
  return (
    <div className="card p-8 bg-white relative overflow-hidden min-h-[300px] flex flex-col justify-center border border-red-100">
      <div className="absolute top-0 right-0 p-4 opacity-5">
        <DollarSign className="w-32 h-32 text-red-800" />
      </div>
      <p className="text-red-400 text-[10px] font-bold uppercase tracking-widest mb-4">
        Resultado — {result.total.toLocaleString('es-CO')} registros
      </p>
      <p className="text-red-400 text-sm font-medium mb-1">Salario Promedio Predicho</p>
      <p className="text-5xl font-black text-red-800 mb-6">{fmt(result.mean_salary)}</p>
      <div className="grid grid-cols-3 gap-3">
        <div className="bg-red-50 rounded-xl p-3 text-center border border-red-100">
          <p className="text-xs text-red-400 uppercase font-bold mb-1">Mediana</p>
          <p className="text-sm font-black text-red-800">{fmt(result.median_salary)}</p>
        </div>
        <div className="bg-red-50 rounded-xl p-3 text-center border border-red-100">
          <p className="text-xs text-red-400 uppercase font-bold mb-1">Mínimo</p>
          <p className="text-sm font-black text-slate-700">{fmt(result.min_salary)}</p>
        </div>
        <div className="bg-red-50 rounded-xl p-3 text-center border border-red-100">
          <p className="text-xs text-red-400 uppercase font-bold mb-1">Máximo</p>
          <p className="text-sm font-black text-slate-700">{fmt(result.max_salary)}</p>
        </div>
      </div>
    </div>
  );
};

const ModelView = ({ model, apiOnline }: { model: ModelInfo; apiOnline: boolean }) => {
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);

  const fmt = (n: number) =>
    new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(n);

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !apiOnline) return;
    setLoading(true);
    setError(null);
    try {
      const res = await predictCsv(model.id, file);
      setResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!file || !apiOnline) return;
    setDownloading(true);
    try {
      await downloadPredictions(model.id, file);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al descargar');
    } finally {
      setDownloading(false);
    }
  };

  const isClassification = model.metrics?.type === 'classification';
  const m = model.metrics;

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold text-slate-900 mb-2">{model.name}</h2>
          <p className="text-slate-500 max-w-2xl">{model.description}</p>
        </div>
        <div className="flex items-center gap-2 px-3 py-1 bg-red-100 text-red-800 rounded-full text-xs font-bold uppercase tracking-wider">
          <BrainCircuit className="w-3.5 h-3.5" />
          {m ? 'Modelo .PKL cargado' : 'Cargando modelo...'}
        </div>
      </div>

      {m && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {m.type === 'classification' ? (
            <>
              <MetricPill label="Accuracy" value={m.accuracy} />
              <MetricPill label="Precision" value={m.precision} />
              <MetricPill label="Recall" value={m.recall} />
              <MetricPill label="F1 Score" value={m.f1} />
            </>
          ) : (
            <>
              <MetricPill label="R² Test" value={m.r2} />
              <MetricPill label="MAE Test" value={m.mae} formatted={fmt(m.mae)} />
              <MetricPill label="RMSE Test" value={m.rmse} formatted={fmt(m.rmse)} />
              <MetricPill label="Modelo Base" value="" formatted={m.model_name} />
            </>
          )}
        </div>
      )}

      {m && m.type === 'classification' && m.pca_components != null && (
        <div className="flex items-center gap-3 flex-wrap">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-50 text-blue-800 rounded-full text-xs font-bold border border-blue-100">
            <BrainCircuit className="w-3.5 h-3.5" />
            PCA · {m.pca_components} componentes
          </div>
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-50 text-blue-800 rounded-full text-xs font-bold border border-blue-100">
            Varianza explicada: {m.pca_variance != null ? `${(m.pca_variance * 100).toFixed(1)}%` : '—'}
          </div>
        </div>
      )}

      {!apiOnline && (
        <div className="card p-4 flex items-center gap-3 border-amber-200 bg-amber-50">
          <AlertCircle className="w-5 h-5 text-amber-500 shrink-0" />
          <p className="text-sm text-amber-800">
            Servidor API inactivo. Inicia con:{' '}
            <code className="bg-amber-100 px-1 rounded text-xs">
              python -m uvicorn api.server:app --reload --port 8000
            </code>
          </p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
          <div className="card">
            <div className="p-6 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
              <div>
                <h4 className="font-bold text-slate-800">Carga por Lote (Batch Processing)</h4>
                <p className="text-xs text-slate-500">
                  {isClassification
                    ? 'CSV con columnas del dataset de empleabilidad → predice Offer_Received'
                    : 'CSV con columnas del dataset de empleabilidad → predice Offer_Salary'}
                </p>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[10px] font-bold text-slate-400 bg-slate-200 px-2 py-1 rounded">UTF-8</span>
                <span className="text-[10px] font-bold text-slate-400 bg-slate-200 px-2 py-1 rounded">DELIM: ","</span>
              </div>
            </div>

            <div className="p-8">
              <div
                className={cn(
                  'border-2 border-dashed rounded-2xl p-12 text-center transition-all group cursor-pointer',
                  file
                    ? 'border-green-500 bg-green-50/50'
                    : 'border-slate-200 hover:border-red-400 hover:bg-red-50/20'
                )}
                onClick={() => document.getElementById('csv-upload')?.click()}
              >
                <input
                  type="file"
                  id="csv-upload"
                  className="hidden"
                  accept=".csv"
                  onChange={(e) => {
                    setFile(e.target.files?.[0] || null);
                    setResult(null);
                    setError(null);
                  }}
                />
                <div className="w-16 h-16 bg-slate-100 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform">
                  <Database className={cn('w-8 h-8', file ? 'text-green-600' : 'text-slate-400 group-hover:text-red-800')} />
                </div>
                {file ? (
                  <div>
                    <p className="font-bold text-slate-800">{file.name}</p>
                    <p className="text-xs text-slate-500 mt-1">
                      {(file.size / 1024).toFixed(1)} KB listo para inferencia
                    </p>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setFile(null);
                        setResult(null);
                      }}
                      className="text-[10px] font-bold text-red-600 uppercase mt-2 hover:underline"
                    >
                      Remover archivo
                    </button>
                  </div>
                ) : (
                  <div>
                    <h5 className="font-bold text-slate-800">Arrastre su archivo .csv</h5>
                    <p className="text-sm text-slate-500 mt-1 max-w-sm mx-auto">
                      El pipeline .pkl procesará automáticamente las columnas del dataset de empleabilidad.
                    </p>
                  </div>
                )}
              </div>

              {error && (
                <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-xl flex items-start gap-2">
                  <AlertCircle className="w-4 h-4 text-red-500 mt-0.5 shrink-0" />
                  <p className="text-xs text-red-700 font-medium">{error}</p>
                </div>
              )}

              <div className="mt-8 flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="flex flex-col">
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Engine</span>
                    <span className="text-sm font-bold">{model.id}.pkl</span>
                  </div>
                  <div className="w-px h-8 bg-slate-200" />
                  <div className="flex flex-col">
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Tarea</span>
                    <span className="text-sm font-bold text-red-800">
                      {isClassification ? 'Clasificación' : 'Regresión'}
                    </span>
                  </div>
                </div>

                <button
                  onClick={handlePredict}
                  disabled={loading || !file || !apiOnline}
                  className="btn-primary flex items-center gap-2 px-8 py-4 disabled:opacity-50 disabled:active:scale-100 disabled:cursor-not-allowed shadow-xl shadow-red-900/10"
                >
                  {loading ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      Procesando...
                    </>
                  ) : (
                    <>
                      <TrendingUp className="w-5 h-5" />
                      Ejecutar Inferencia
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {m && m.type === 'classification' && (
            <div className="card p-6">
              <h4 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                <Search className="w-4 h-4 text-red-800" />
                Métricas del Modelo (umbral optimizado)
              </h4>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                <div className="p-4 bg-slate-50 rounded-xl border border-slate-100">
                  <p className="text-[10px] font-bold text-slate-400 uppercase mb-1">ROC-AUC</p>
                  <p className="text-2xl font-black text-red-800">{(m.roc_auc * 100).toFixed(1)}%</p>
                </div>
                <div className="p-4 bg-slate-50 rounded-xl border border-slate-100">
                  <p className="text-[10px] font-bold text-slate-400 uppercase mb-1">Umbral</p>
                  <p className="text-2xl font-black text-red-800">{Number(m.threshold).toFixed(3)}</p>
                </div>
                <div className="p-4 bg-slate-50 rounded-xl border border-slate-100">
                  <p className="text-[10px] font-bold text-slate-400 uppercase mb-1">Modelo</p>
                  <p className="text-lg font-black text-red-800">{m.model_name}</p>
                </div>
              </div>
            </div>
          )}

          {m && m.type === 'regression' && (
            <div className="card p-6">
              <h4 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                <Search className="w-4 h-4 text-red-800" />
                Comparativa de Modelos de Regresión
              </h4>
              <div className="overflow-x-auto">
                <table className="w-full text-xs">
                  <thead>
                    <tr className="text-slate-400 uppercase text-[10px] tracking-wider">
                      <th className="text-left pb-2 font-bold">Modelo</th>
                      <th className="text-right pb-2 font-bold">R² Test</th>
                      <th className="text-right pb-2 font-bold">MAE Test</th>
                      <th className="text-right pb-2 font-bold">RMSE Test</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {m.all_models.map((row, i) => (
                      <tr key={i} className={i === 0 ? 'text-red-800 font-bold' : 'text-slate-700'}>
                        <td className="py-2">{row.modelo} {i === 0 && <span className="ml-1 text-[9px] bg-red-100 text-red-800 px-1 rounded uppercase">mejor</span>}</td>
                        <td className="text-right py-2">{(row.R2_test * 100).toFixed(1)}%</td>
                        <td className="text-right py-2">{fmt(row.MAE_test)}</td>
                        <td className="text-right py-2">{fmt(row.RMSE_test)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>

        <div className="space-y-6">
          {result === null ? (
            <div className="card p-8 text-center min-h-[300px] flex flex-col items-center justify-center">
              <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mb-4">
                <Search className="w-8 h-8 text-slate-400" />
              </div>
              <h5 className="font-bold text-slate-800">Esperando Lote</h5>
              <p className="text-sm text-slate-500 mt-2 px-4">
                Suba un CSV y ejecute la inferencia para ver resultados reales del modelo.
              </p>
            </div>
          ) : result.type === 'classification' ? (
            <ClassificationResultCard result={result as ClassificationResult} />
          ) : (
            <RegressionResultCard result={result as RegressionResult} />
          )}

          {result && (
            <button
              onClick={handleDownload}
              disabled={downloading || !file || !apiOnline}
              className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-slate-800 hover:bg-slate-700 text-white text-sm font-bold rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {downloading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Generando CSV...
                </>
              ) : (
                <>
                  <FileDown className="w-4 h-4" />
                  Descargar predicciones (.csv)
                </>
              )}
            </button>
          )}

          <div className="card p-6 bg-slate-900 text-white">
            <h5 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-4">
              Diagnóstico del Motor
            </h5>
            <div className="space-y-3 text-xs">
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Archivo .pkl</span>
                <span className="font-mono text-[9px]">{model.id}.pkl</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Registros procesados</span>
                <span>{result ? result.total.toLocaleString('es-CO') : '—'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">API backend</span>
                <span className={apiOnline ? 'text-green-400' : 'text-red-400'}>
                  {apiOnline ? 'Conectado' : 'Inactivo'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Model Image Gallery */}
      {GALLERY_CONFIGS[model.id] && (
        <div className="card p-6">
          <ImageGallery
            tabs={GALLERY_CONFIGS[model.id]}
            title={`Visualizaciones — ${model.name}`}
          />
        </div>
      )}
    </div>
  );
};

// --- Main App ---

export default function App() {
  const [view, setView] = useState<ViewState>('landing');
  const [activePage, setActivePage] = useState<ModelID>('eda');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [summaries, setSummaries] = useState<SummariesResponse>({});
  const [apiOnline, setApiOnline] = useState(false);

  useEffect(() => {
    if (view !== 'dashboard') return;
    checkHealth().then((ok) => {
      setApiOnline(ok);
      if (ok) {
        fetchSummaries().then(setSummaries).catch(() => {});
      }
    });
  }, [view]);

  const MODELS: ModelInfo[] = useMemo(
    () =>
      MODEL_DEFINITIONS.map((def) => ({
        ...def,
        metrics: summaries[def.id as keyof SummariesResponse],
      })),
    [summaries]
  );

  const activeModel = useMemo(
    () => MODELS.find((m) => m.id === activePage) || MODELS[0],
    [MODELS, activePage]
  );

  if (view === 'landing') return <LandingPage onStart={() => setView('login')} />;
  if (view === 'login') return <LoginPage onLogin={() => setView('dashboard')} />;

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden font-sans">
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <aside
        className={cn(
          'fixed lg:static inset-y-0 left-0 w-72 bg-slate-900 text-white z-50 transform transition-transform duration-300 ease-in-out border-r border-white/5',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        )}
      >
        <div className="h-full flex flex-col p-6">
          <div
            className="flex items-center gap-3 mb-10 px-2 cursor-pointer"
            onClick={() => setView('landing')}
          >
            <img src={LogoBlanco} alt="UniCareer ML" className="h-12 w-auto object-contain" />
          </div>

          <nav className="flex-1 space-y-6 overflow-y-auto">
            <div>
              <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-3 px-4">
                Análisis Principal
              </p>
              <div className="space-y-1">
                {MODELS.filter((m) => m.category === 'analysis').map((item) => (
                  <SidebarItem
                    key={item.id}
                    item={item}
                    active={activePage === item.id}
                    onClick={() => {
                      setActivePage(item.id);
                      setSidebarOpen(false);
                    }}
                  />
                ))}
              </div>
            </div>

            <div>
              <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-3 px-4">
                Modelos Estándar
              </p>
              <div className="space-y-1">
                {MODELS.filter((m) => m.category === 'ml').map((item) => (
                  <SidebarItem
                    key={item.id}
                    item={item}
                    active={activePage === item.id}
                    onClick={() => {
                      setActivePage(item.id);
                      setSidebarOpen(false);
                    }}
                  />
                ))}
              </div>
            </div>

            <div>
              <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-3 px-4">
                Modelos con PCA
              </p>
              <div className="space-y-1">
                {MODELS.filter((m) => m.category === 'ml-pca').map((item) => (
                  <SidebarItem
                    key={item.id}
                    item={item}
                    active={activePage === item.id}
                    onClick={() => {
                      setActivePage(item.id);
                      setSidebarOpen(false);
                    }}
                  />
                ))}
              </div>
            </div>
          </nav>

          <div className="pt-6 border-t border-white/10 mt-auto">
            <div className="bg-white/5 rounded-xl p-4 flex items-center justify-between">
              <div>
                <p className="text-xs text-slate-400 mb-1">Estado API</p>
                <p className="text-sm font-medium">{apiOnline ? 'Conectado' : 'Sin conexión'}</p>
              </div>
              <div className={cn('w-2.5 h-2.5 rounded-full', apiOnline ? 'bg-green-400 animate-pulse' : 'bg-red-500')} />
            </div>
          </div>
        </div>
      </aside>

      <main className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6 sticky top-0 z-30">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="lg:hidden p-2 text-slate-500 hover:text-slate-900 transition-colors"
          >
            <Menu className="w-6 h-6" />
          </button>

          <div className="flex items-center gap-2 text-sm text-slate-500 font-medium">
            <LayoutDashboard className="w-4 h-4" />
            <ChevronRight className="w-4 h-4 opacity-30" />
            <span className="text-slate-900">
              {activeModel.category === 'analysis' ? 'Dashboard' : 'Modelos'}
            </span>
            <ChevronRight className="w-4 h-4 opacity-30" />
            <span className="text-red-800 font-bold">{activeModel.name}</span>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden md:flex items-center gap-2 px-3 py-1.5 bg-slate-50 rounded-lg border border-slate-100">
              <div className={cn('w-2 h-2 rounded-full', apiOnline ? 'bg-green-500 animate-pulse' : 'bg-amber-400')} />
              <span className="text-[10px] font-bold text-slate-600 uppercase">
                {apiOnline ? 'Engine conectado' : 'API inactiva'}
              </span>
            </div>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-4 md:p-8 scroll-smooth">
          <div className="max-w-7xl mx-auto">
            {activePage === 'eda' ? (
              <EDAView apiOnline={apiOnline} />
            ) : activePage === 'clustering' ? (
              <ClusteringView apiOnline={apiOnline} />
            ) : (
              <ModelView model={activeModel} apiOnline={apiOnline} />
            )}
          </div>

          <footer className="mt-16 pt-8 border-t border-slate-200 flex flex-col md:flex-row items-center justify-between text-slate-400 text-xs gap-4 mb-8">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-red-800" />© 2026 Academia Moderna —
              Departamento de Ciencia de Datos
            </div>
            <div className="flex gap-6">
              <a href="#" className="hover:text-red-800 transition-colors">Documentación</a>
              <a href="#" className="hover:text-red-800 transition-colors">Privacidad Estudiantil</a>
            </div>
          </footer>
        </div>
      </main>
    </div>
  );
}
