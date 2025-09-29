export const UninformedSearchTypes = {
  BREADTH: 'BREADTH',
  DEPTH: 'DEPTH',
  DEPTH_LIMITED: 'DEPTH_LIMITED',
  ITERATIVE: 'ITERATIVE',
  BIDIRECTIONAL: 'BIDIRECTIONAL',
} as const;
export type UninformedSearchTypes =
  (typeof UninformedSearchTypes)[keyof typeof UninformedSearchTypes];
