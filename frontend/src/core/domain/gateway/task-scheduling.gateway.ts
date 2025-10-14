export interface TaskSchedulingInput {
  tasks: number[];
  setup_matrix: Record<string, number>;
  heuristic?: string;
  families?: Record<number, string>;
}

export interface TaskSchedulingResponse {
  sequence: number[];
  total_cost: number;
  setup_details: Array<{
    from: number;
    to: number;
    cost: number;
  }>;
  algorithm: string;
  heuristic?: string;
}

export type TaskSchedulingOutput = Promise<TaskSchedulingResponse | null>;

export interface TaskSchedulingGateway {
  aStar(payload: TaskSchedulingInput): TaskSchedulingOutput;
  greedy(payload: TaskSchedulingInput): TaskSchedulingOutput;
  uniformCost(
    payload: Omit<TaskSchedulingInput, 'heuristic' | 'families'>,
  ): TaskSchedulingOutput;
}
