import type { BaseOutput, BaseInput } from '.';

export interface DepthLimited extends BaseInput {
  limit: number;
}

export interface IterativeDeepening extends BaseInput {
  max_limit: number;
}

export interface UninformedSearchGateway {
  depthLimited(payload: DepthLimited): BaseOutput;
  depthFirst(payload: BaseInput): BaseOutput;
  breadthFirst(payload: BaseInput): BaseOutput;
  bidirectional(payload: BaseInput): BaseOutput;
  iterativeDeepening(payload: IterativeDeepening): BaseOutput;
}
