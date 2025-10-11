import type { BaseInput, BaseOutput } from '.';

export type HeuristicInput = BaseInput & {
  heuristics: number[];
};

export interface InformedSearchGateway {
  uniformCost(payload: BaseInput): BaseOutput;
  aStar(payload: HeuristicInput): BaseOutput;
  greedy(payload: HeuristicInput): BaseOutput;
  idaStar(payload: HeuristicInput): BaseOutput;
}
