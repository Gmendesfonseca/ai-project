export interface TaskSchedulingInput {
  tasks: number[];
  setup_matrix: Record<string, number>;
  heuristic?: string;
  families?: Record<number, string>;
  depth_limit?: number;
  max_depth?: number;
}

export interface TaskSchedulingResponse {
  sequence: number[];
  total_cost: number;
  setup_details: Array<{
    from: number;
    to: number;
    cost: number;
  }>;
  heuristic?: string;
  algorithm: string;
}

export type TaskSchedulingOutput = Promise<TaskSchedulingResponse | null>;

export interface TaskSchedulingGateway {
  aStar(payload: TaskSchedulingInput): TaskSchedulingOutput;
  greedy(payload: TaskSchedulingInput): TaskSchedulingOutput;
  uniformCost(
    payload: Omit<TaskSchedulingInput, 'heuristic' | 'families'>,
  ): TaskSchedulingOutput;
  breadthFirst(
    payload: Omit<TaskSchedulingInput, 'heuristic' | 'families'>,
  ): TaskSchedulingOutput;
  depthFirst(
    payload: Omit<TaskSchedulingInput, 'heuristic' | 'families'>,
  ): TaskSchedulingOutput;
  depthLimited(payload: TaskSchedulingInput): TaskSchedulingOutput;
  iterativeDeepening(payload: TaskSchedulingInput): TaskSchedulingOutput;
  bidirectional(
    payload: Omit<TaskSchedulingInput, 'heuristic' | 'families'>,
  ): TaskSchedulingOutput;
  idaStar(payload: TaskSchedulingInput): TaskSchedulingOutput;
}
