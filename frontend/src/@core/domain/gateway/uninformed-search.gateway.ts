export interface BaseUninformedInput {
  start: string;
  goal: string;
  nodes: Record<string, string[]>;
  graph: any;
}

export interface DepthLimited extends BaseUninformedInput {
  limit: number;
}

export interface IterativeDeepening extends BaseUninformedInput {
  max_limit: number;
}

type MethodResponse = { path: string[] };

export type BaseUniformedOutput = Promise<MethodResponse | null>;

export interface UninformedSearchGateway {
  depthLimited(payload: DepthLimited): BaseUniformedOutput;
  depthFirst(payload: BaseUninformedInput): BaseUniformedOutput;
  breadthFirst(payload: BaseUninformedInput): BaseUniformedOutput;
  bidirectional(payload: BaseUninformedInput): BaseUniformedOutput;
  iterativeDeepening(payload: IterativeDeepening): BaseUniformedOutput;
}
