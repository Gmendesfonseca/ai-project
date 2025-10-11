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

export const methodOptions: { value: SearchTypes; label: string }[] = [
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
