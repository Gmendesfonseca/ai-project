export const SearchTypes = {
  BREADTH: 'BREADTH',
  DEPTH: 'DEPTH',
  DEPTH_LIMITED: 'DEPTH_LIMITED',
  ITERATIVE: 'ITERATIVE',
  BIDIRECTIONAL: 'BIDIRECTIONAL',
  UNIFORMED_COST: 'UNIFORMED_COST',
  A_STAR: 'A_STAR',
  GREEDY: 'GREEDY',
  IDA_STAR: 'IDA_STAR',
} as const;
export type SearchTypes = (typeof SearchTypes)[keyof typeof SearchTypes];

export type Options = { value: SearchTypes; label: string };

export const methodOptions: Options[] = [
  {
    value: SearchTypes.BREADTH,
    label: 'Amplitude',
  },
  {
    value: SearchTypes.DEPTH,
    label: 'Profundidade',
  },
  {
    value: SearchTypes.DEPTH_LIMITED,
    label: 'Limitada em Profundidade',
  },
  {
    value: SearchTypes.ITERATIVE,
    label: 'Aprofundamento Iterativo',
  },
  {
    value: SearchTypes.BIDIRECTIONAL,
    label: 'Bidirecional',
  },
  {
    value: SearchTypes.UNIFORMED_COST,
    label: 'Custo Uniforme',
  },
  {
    value: SearchTypes.A_STAR,
    label: 'A*',
  },
  {
    value: SearchTypes.GREEDY,
    label: 'Greedy',
  },
  {
    value: SearchTypes.IDA_STAR,
    label: 'AIA*',
  },
];

export const taskSchedulingOptions: Options[] = [
  {
    value: SearchTypes.A_STAR,
    label: 'A*',
  },
  {
    value: SearchTypes.GREEDY,
    label: 'Greedy',
  },
  {
    value: SearchTypes.IDA_STAR,
    label: 'AIA* (A* com memória limitada)',
  },
  {
    value: SearchTypes.UNIFORMED_COST,
    label: 'Custo Uniforme (Dijkstra)',
  },
  {
    value: SearchTypes.BREADTH,
    label: 'Amplitude (BFS)',
  },
  {
    value: SearchTypes.DEPTH,
    label: 'Profundidade (DFS)',
  },
  {
    value: SearchTypes.DEPTH_LIMITED,
    label: 'Profundidade Limitada',
  },
  {
    value: SearchTypes.ITERATIVE,
    label: 'Aprofundamento Iterativo',
  },
  {
    value: SearchTypes.BIDIRECTIONAL,
    label: 'Busca Bidirecional',
  },
];

export const heuristicOptions = [
  { value: 'h1', label: 'H1 - Mínimos de Saída' },
  { value: 'h2', label: 'H2 - MST Simétrico' },
  { value: 'h3', label: 'H3 - Famílias de Produtos' },
];
