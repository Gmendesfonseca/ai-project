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
