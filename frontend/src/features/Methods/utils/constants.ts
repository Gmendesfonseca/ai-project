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

export const TaskSchedulingTypes = {
  TASK_A_STAR: 'TASK_A_STAR',
  TASK_GREEDY: 'TASK_GREEDY',
  TASK_UNIFORM_COST: 'TASK_UNIFORM_COST',
} as const;
export type TaskSchedulingTypes =
  (typeof TaskSchedulingTypes)[keyof typeof TaskSchedulingTypes];

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

export const taskSchedulingOptions: {
  value: TaskSchedulingTypes;
  label: string;
}[] = [
  {
    value: TaskSchedulingTypes.TASK_A_STAR,
    label: 'A* - Task Scheduling',
  },
  {
    value: TaskSchedulingTypes.TASK_GREEDY,
    label: 'Greedy - Task Scheduling',
  },
  {
    value: TaskSchedulingTypes.TASK_UNIFORM_COST,
    label: 'Custo Uniforme - Task Scheduling',
  },
];

export const heuristicOptions = [
  { value: 'h1', label: 'H1 - Mínimos de Saída' },
  { value: 'h2', label: 'H2 - MST Simétrico' },
  { value: 'h3', label: 'H3 - Famílias de Produtos' },
];
