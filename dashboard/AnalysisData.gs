const ANALYSIS_DATA = {
  queryTypes: [
    { key: 'single_hop', label: 'Single-hop', description: 'Direct fact or concept answerable from one primary source.' },
    { key: 'paraphrasing', label: 'Paraphrasing', description: 'Same underlying concept expressed using different wording from the corpus.' },
    { key: 'comparative', label: 'Comparative', description: 'Requires contrasting two concepts, models, or pipeline components.' },
    { key: 'multi_hop', label: 'Multi-hop', description: 'Requires combining evidence from multiple concepts or documents.' },
    { key: 'conditional', label: 'Conditional', description: 'Asks what follows when a stated condition or capability is missing.' },
    { key: 'abstract', label: 'Abstract', description: 'Requires synthesizing a higher-level explanation from several details.' },
    { key: 'counterfactual', label: 'Counterfactual', description: 'Requires reasoning about downstream consequences of a hypothetical change.' }
  ],
  queryTypeScores: {
    chunk_small: {
      single_hop: { count: 4, document_recall: 1.000, context_precision: 0.9583, context_recall: 0.9167, correctness: 1.000, composite: 0.9688 },
      paraphrasing: { count: 2, document_recall: 0.250, context_precision: 0.1667, context_recall: 0.750, correctness: 0.500, composite: 0.6042 },
      comparative: { count: 2, document_recall: 0.750, context_precision: 1.000, context_recall: 1.000, correctness: 1.000, composite: 1.000 },
      multi_hop: { count: 4, document_recall: 0.5417, context_precision: 0.5417, context_recall: 0.7083, correctness: 0.500, composite: 0.6875 },
      conditional: { count: 2, document_recall: 0.5833, context_precision: 0.7917, context_recall: 1.000, correctness: 1.000, composite: 0.9479 },
      abstract: { count: 1, document_recall: 1.000, context_precision: 1.000, context_recall: 0.500, correctness: 1.000, composite: 0.875 },
      counterfactual: { count: 1, document_recall: 0.250, context_precision: 1.000, context_recall: 0.500, correctness: 0.000, composite: 0.625 }
    },
    chunk_large: {
      single_hop: { count: 4, document_recall: 1.000, context_precision: 0.8542, context_recall: 1.000, correctness: 1.000, composite: 0.9635 },
      paraphrasing: { count: 2, document_recall: 0.750, context_precision: 0.750, context_recall: 1.000, correctness: 1.000, composite: 0.9375 },
      comparative: { count: 2, document_recall: 1.000, context_precision: 1.000, context_recall: 1.000, correctness: 1.000, composite: 1.000 },
      multi_hop: { count: 4, document_recall: 0.7917, context_precision: 0.6667, context_recall: 1.000, correctness: 1.000, composite: 0.9167 },
      conditional: { count: 2, document_recall: 0.4167, context_precision: 0.7917, context_recall: 1.000, correctness: 1.000, composite: 0.9479 },
      abstract: { count: 1, document_recall: 0.500, context_precision: 1.000, context_recall: 1.000, correctness: 1.000, composite: 1.000 },
      counterfactual: { count: 1, document_recall: 0.250, context_precision: 0.000, context_recall: 0.000, correctness: 0.000, composite: 0.250 }
    },
    topk_2: {
      single_hop: { count: 4, document_recall: 1.000, context_precision: 1.000, context_recall: 0.9375, correctness: 1.000, composite: 0.9844 },
      paraphrasing: { count: 2, document_recall: 0.250, context_precision: 0.500, context_recall: 0.500, correctness: 0.500, composite: 0.625 },
      comparative: { count: 2, document_recall: 0.750, context_precision: 1.000, context_recall: 1.000, correctness: 1.000, composite: 1.000 },
      multi_hop: { count: 4, document_recall: 0.5417, context_precision: 0.500, context_recall: 0.7083, correctness: 0.500, composite: 0.6771 },
      conditional: { count: 2, document_recall: 0.5833, context_precision: 0.750, context_recall: 1.000, correctness: 1.000, composite: 0.9375 },
      abstract: { count: 1, document_recall: 1.000, context_precision: 1.000, context_recall: 0.000, correctness: 1.000, composite: 0.750 },
      counterfactual: { count: 1, document_recall: 0.250, context_precision: 1.000, context_recall: 0.500, correctness: 1.000, composite: 0.875 }
    },
    topk_5: {
      single_hop: { count: 4, document_recall: 1.000, context_precision: 0.9389, context_recall: 0.9375, correctness: 1.000, composite: 0.9691 },
      paraphrasing: { count: 2, document_recall: 0.750, context_precision: 0.250, context_recall: 1.000, correctness: 1.000, composite: 0.8125 },
      comparative: { count: 2, document_recall: 1.000, context_precision: 1.000, context_recall: 1.000, correctness: 1.000, composite: 1.000 },
      multi_hop: { count: 4, document_recall: 0.7917, context_precision: 0.5014, context_recall: 0.8333, correctness: 0.750, composite: 0.7712 },
      conditional: { count: 2, document_recall: 1.000, context_precision: 0.7694, context_recall: 1.000, correctness: 1.000, composite: 0.9424 },
      abstract: { count: 1, document_recall: 1.000, context_precision: 0.8875, context_recall: 0.500, correctness: 1.000, composite: 0.8469 },
      counterfactual: { count: 1, document_recall: 0.250, context_precision: 1.000, context_recall: 0.500, correctness: 0.000, composite: 0.625 }
    },
    embed_minilm: {
      single_hop: { count: 4, document_recall: 1.000, context_precision: 0.9583, context_recall: 1.000, correctness: 1.000, composite: 0.9896 },
      paraphrasing: { count: 2, document_recall: 0.250, context_precision: 0.8333, context_recall: 0.750, correctness: 1.000, composite: 0.8958 },
      comparative: { count: 2, document_recall: 0.750, context_precision: 1.000, context_recall: 1.000, correctness: 1.000, composite: 1.000 },
      multi_hop: { count: 4, document_recall: 0.5417, context_precision: 0.875, context_recall: 0.7083, correctness: 0.500, composite: 0.7708 },
      conditional: { count: 2, document_recall: 0.5833, context_precision: 1.000, context_recall: 1.000, correctness: 1.000, composite: 1.000 },
      abstract: { count: 1, document_recall: 1.000, context_precision: 1.000, context_recall: 0.500, correctness: 1.000, composite: 0.875 },
      counterfactual: { count: 1, document_recall: 0.250, context_precision: 1.000, context_recall: 0.500, correctness: 0.000, composite: 0.625 }
    },
    embed_mpnet: {
      single_hop: { count: 4, document_recall: 1.000, context_precision: 0.875, context_recall: 0.9167, correctness: 1.000, composite: 0.9479 },
      paraphrasing: { count: 2, document_recall: 0.750, context_precision: 0.9167, context_recall: 0.750, correctness: 1.000, composite: 0.9167 },
      comparative: { count: 2, document_recall: 0.750, context_precision: 1.000, context_recall: 1.000, correctness: 1.000, composite: 1.000 },
      multi_hop: { count: 4, document_recall: 0.4583, context_precision: 0.7917, context_recall: 0.7917, correctness: 0.500, composite: 0.7708 },
      conditional: { count: 2, document_recall: 0.5833, context_precision: 0.9167, context_recall: 1.000, correctness: 1.000, composite: 0.9792 },
      abstract: { count: 1, document_recall: 0.500, context_precision: 1.000, context_recall: 0.500, correctness: 0.000, composite: 0.625 },
      counterfactual: { count: 1, document_recall: 0.250, context_precision: 0.8333, context_recall: 0.500, correctness: 1.000, composite: 0.8333 }
    },
    final_combined: {
      single_hop: { count: 4, document_recall: 1.000, context_precision: 0.850, context_recall: 1.000, correctness: 1.000, composite: 0.9625 },
      paraphrasing: { count: 2, document_recall: 0.750, context_precision: 0.725, context_recall: 1.000, correctness: 1.000, composite: 0.9313 },
      comparative: { count: 2, document_recall: 1.000, context_precision: 0.9583, context_recall: 1.000, correctness: 1.000, composite: 0.9896 },
      multi_hop: { count: 4, document_recall: 0.875, context_precision: 0.7167, context_recall: 1.000, correctness: 1.000, composite: 0.9292 },
      conditional: { count: 2, document_recall: 0.8333, context_precision: 0.7417, context_recall: 1.000, correctness: 1.000, composite: 0.9354 },
      abstract: { count: 1, document_recall: 1.000, context_precision: 0.750, context_recall: 1.000, correctness: 1.000, composite: 0.9375 },
      counterfactual: { count: 1, document_recall: 0.250, context_precision: 0.325, context_recall: 1.000, correctness: 1.000, composite: 0.8313 }
    }
  },
  failureCases: [
    {
      id: 'q04', type: 'paraphrasing', label: 'Semantic retrieval miss', icon: '🔍', config: 'topk_2',
      question: 'How can a computer-vision system follow the flight path of the shuttlecock rather than merely locating it in individual images?',
      diagnosis: 'The question expresses “tracking” indirectly. At k=2, semantically adjacent trajectory/detection documents outranked the ground-truth shuttle-tracking source.',
      before: { document_recall: 0.000, context_recall: 0.500, faithfulness: 1.000, correctness: 0.000 },
      after: { document_recall: 1.000, context_recall: 1.000, faithfulness: 1.000, correctness: 1.000 },
      relevant: ['badminton_03_shuttle_tracking.txt'],
      retrieved: ['badminton_11_trajectory_analysis.txt', 'badminton_02_shuttle_detection.txt'],
      afterNote: 'The final configuration retrieves the shuttle-tracking evidence directly and answers the paraphrased query correctly.'
    },
    {
      id: 'q08', type: 'multi_hop', label: 'Missing second hop', icon: '🧩', config: 'chunk_small',
      question: 'Why would a badminton system use an object detector together with court calibration when measuring player movement across the playing area?',
      diagnosis: 'Retrieval captured player detection but missed court calibration / homography. The grounded generator correctly refused instead of inventing the missing second hop.',
      before: { document_recall: 0.000, context_recall: 0.500, faithfulness: 1.000, correctness: 0.000 },
      after: { document_recall: 0.500, context_recall: 1.000, faithfulness: 1.000, correctness: 1.000 },
      relevant: ['badminton_16_yolo.txt', 'badminton_10_court_analysis.txt'],
      retrieved: ['badminton_05_player_detection.txt', 'badminton_05_player_detection.txt', 'badminton_06_player_tracking.txt'],
      afterNote: 'The final run reaches full context coverage and correctness even though source-level recall is only 50%, showing why chunk-level context metrics add information beyond source labels.'
    },
    {
      id: 'q15', type: 'counterfactual', label: 'Downstream dependency miss', icon: '🔗', config: 'chunk_large',
      question: 'Suppose TrackNetV3 becomes unreliable. Which types of analysis would be most affected and why?',
      diagnosis: 'The retriever found the failed component but not enough evidence about downstream dependencies. The answer therefore captured shuttle tracking but missed the broader consequences.',
      before: { document_recall: 0.250, context_recall: 0.000, faithfulness: 1.000, correctness: 0.000 },
      after: { document_recall: 0.250, context_recall: 1.000, faithfulness: 1.000, correctness: 1.000 },
      relevant: ['badminton_17_tracknetv3.txt', 'badminton_08_hit_detection.txt', 'badminton_11_trajectory_analysis.txt', 'badminton_14_shot_classification.txt'],
      retrieved: ['badminton_17_tracknetv3.txt', 'badminton_16_yolo.txt', 'badminton_16_yolo.txt'],
      afterNote: 'The final run becomes correct with full context recall despite low annotated-source recall — a useful example of source-level labels being coarser than semantic evidence coverage.'
    },
    {
      id: 'q07', type: 'multi_hop', label: 'Generation / answer-focus miss', icon: '✍️', config: 'embed_mpnet',
      question: 'How can shuttlecock tracking information contribute to identifying the moment when a player strikes the shuttlecock?',
      diagnosis: 'The required evidence was present (100% context recall), but the generator emphasized downstream uses such as rally segmentation instead of the mechanism the question asked for.',
      before: { document_recall: 0.500, context_recall: 1.000, faithfulness: 1.000, correctness: 0.000 },
      after: { document_recall: 1.000, context_recall: 1.000, faithfulness: 1.000, correctness: 1.000 },
      relevant: ['badminton_03_shuttle_tracking.txt', 'badminton_08_hit_detection.txt'],
      retrieved: ['badminton_08_hit_detection.txt', 'badminton_11_trajectory_analysis.txt', 'badminton_11_trajectory_analysis.txt'],
      afterNote: 'This is the cleanest generation-failure example: retrieval coverage was already complete, so more retrieval alone was not the core issue.'
    }
  ]
};
