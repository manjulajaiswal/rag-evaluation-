const DASHBOARD_DATA = {
  project: {
    title: 'RAG Evaluation Lab',
    subtitle: 'Badminton Computer Vision Benchmark',
    documents: 17,
    questions: 16,
    configurations: 7,
    updatedLabel: 'Final evaluation run'
  },
  metrics: [
    { key: 'document_precision', label: 'Document Precision', short: 'Doc P', group: 'Retrieval' },
    { key: 'document_recall', label: 'Document Recall', short: 'Doc R', group: 'Retrieval' },
    { key: 'context_precision', label: 'Context Precision', short: 'Ctx P', group: 'Retrieval' },
    { key: 'context_recall', label: 'Context Recall', short: 'Ctx R', group: 'Retrieval' },
    { key: 'faithfulness', label: 'Faithfulness', short: 'Faith.', group: 'Generation' },
    { key: 'correctness', label: 'Correctness', short: 'Correct.', group: 'Generation' },
    { key: 'ragas_style_composite', label: 'Composite', short: 'Composite', group: 'Overall' }
  ],
  configs: [
    {
      name: 'chunk_small', experiment: 'chunk_size', chunkSize: 80, overlap: 20, topK: 3,
      embedding: 'all-MiniLM-L6-v2',
      scores: { document_precision: 0.604, document_recall: 0.661, context_precision: 0.745, context_recall: 0.812, faithfulness: 1.000, correctness: 0.750, ragas_style_composite: 0.827 }
    },
    {
      name: 'chunk_large', experiment: 'chunk_size', chunkSize: 160, overlap: 20, topK: 3,
      embedding: 'all-MiniLM-L6-v2',
      scores: { document_precision: 0.604, document_recall: 0.766, context_precision: 0.760, context_recall: 0.938, faithfulness: 1.000, correctness: 0.938, ragas_style_composite: 0.909 }
    },
    {
      name: 'topk_2', experiment: 'top_k', chunkSize: 80, overlap: 20, topK: 2,
      embedding: 'all-MiniLM-L6-v2',
      scores: { document_precision: 0.688, document_recall: 0.661, context_precision: 0.781, context_recall: 0.755, faithfulness: 1.000, correctness: 0.812, ragas_style_composite: 0.837 }
    },
    {
      name: 'topk_5', experiment: 'top_k', chunkSize: 80, overlap: 20, topK: 5,
      embedding: 'all-MiniLM-L6-v2',
      scores: { document_precision: 0.562, document_recall: 0.870, context_precision: 0.730, context_recall: 0.880, faithfulness: 1.000, correctness: 0.875, ragas_style_composite: 0.871 }
    },
    {
      name: 'embed_minilm', experiment: 'embedding_model', chunkSize: 80, overlap: 20, topK: 3,
      embedding: 'all-MiniLM-L6-v2',
      scores: { document_precision: 0.604, document_recall: 0.661, context_precision: 0.938, context_recall: 0.833, faithfulness: 1.000, correctness: 0.812, ragas_style_composite: 0.896 }
    },
    {
      name: 'embed_mpnet', experiment: 'embedding_model', chunkSize: 80, overlap: 20, topK: 3,
      embedding: 'all-mpnet-base-v2',
      scores: { document_precision: 0.583, document_recall: 0.672, context_precision: 0.885, context_recall: 0.833, faithfulness: 1.000, correctness: 0.812, ragas_style_composite: 0.883 }
    },
    {
      name: 'final_combined', experiment: 'final_combined', chunkSize: 160, overlap: 20, topK: 5,
      embedding: 'all-MiniLM-L6-v2',
      scores: { document_precision: 0.463, document_recall: 0.870, context_precision: 0.762, context_recall: 1.000, faithfulness: 1.000, correctness: 1.000, ragas_style_composite: 0.940 }
    }
  ],
  experiments: [
    {
      id: 'chunk', title: 'Chunk Size', a: 'chunk_small', b: 'chunk_large',
      variable: '80 → 160 words',
      highlights: ['context_recall', 'correctness', 'ragas_style_composite']
    },
    {
      id: 'topk', title: 'Top-k', a: 'topk_2', b: 'topk_5',
      variable: 'k = 2 → 5',
      highlights: ['document_recall', 'context_recall', 'correctness', 'document_precision']
    },
    {
      id: 'embedding', title: 'Embedding Model', a: 'embed_minilm', b: 'embed_mpnet',
      variable: 'MiniLM → MPNet',
      highlights: ['document_recall', 'context_precision', 'ragas_style_composite']
    }
  ]
};

function doGet() {
  return HtmlService.createTemplateFromFile('Index')
    .evaluate()
    .setTitle('RAG Evaluation Dashboard')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

function getDashboardData() {
  return Object.assign({}, DASHBOARD_DATA, ANALYSIS_DATA);
}
