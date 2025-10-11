type MethodResponse = { path: string[] };

export interface BaseInput {
  start: string;
  goal: string;
  nodes: string[];
  graph: string[][];
}

export type BaseOutput = Promise<MethodResponse | null>;

export * from './uninformed-search.gateway';
export * from './informed-search.gateway';
