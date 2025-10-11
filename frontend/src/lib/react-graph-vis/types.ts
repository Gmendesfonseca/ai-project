import { Network } from 'vis-network';
import { DataSet } from 'vis-data';
import type { Options, Node, Edge } from 'vis-network';

type NetworkEvents =
  | 'click'
  | 'doubleClick'
  | 'oncontext'
  | 'hold'
  | 'release'
  | 'select'
  | 'selectNode'
  | 'selectEdge'
  | 'deselectNode'
  | 'deselectEdge'
  | 'dragStart'
  | 'dragging'
  | 'dragEnd'
  | 'hoverNode'
  | 'blurNode'
  | 'hoverEdge'
  | 'blurEdge'
  | 'zoom'
  | 'showPopup'
  | 'hidePopup'
  | 'startStabilizing'
  | 'stabilizationProgress'
  | 'stabilizationIterationsDone'
  | 'stabilized'
  | 'resize'
  | 'initRedraw'
  | 'beforeDrawing'
  | 'afterDrawing'
  | 'animationFinished'
  | 'configChange';

type GraphEvents = {
  [event in NetworkEvents]?: (params?: any) => void;
};

interface GraphData {
  nodes?: Node[] | DataSet<Node>;
  edges?: Edge[] | DataSet<Edge>;
}

interface NetworkGraphProps {
  graph: GraphData;
  options?: Options;
  events?: GraphEvents;
  getNetwork?: (network: Network) => void;
  identifier?: string;
  style?: React.CSSProperties;
  getNodes?: (nodes: DataSet<Node>) => void;
  getEdges?: (edges: DataSet<Edge>) => void;
}

interface NetworkGraphState {
  identifier: string;
}

interface DiffResult<T> {
  removed: T[];
  unchanged: T[];
  updated: T[];
  added: T[];
}

interface PatchEdgesParams {
  edgesRemoved: any[];
  edgesAdded: any[];
  edgesChanged: any[];
}

interface PatchNodesParams {
  nodesRemoved: any[];
  nodesAdded: any[];
  nodesChanged: any[];
}

interface Hierarchical {
  enabled?: boolean;
  levelSeparation?: number;
  nodeSpacing?: number;
  treeSpacing?: number;
  blockShifting?: boolean;
  edgeMinimization?: boolean;
  parentCentralization?: boolean;
  direction?: 'UD' | 'DU' | 'LR' | 'RL';
  sortMethod?: string;
  shakeTowards?: string;
}

interface Keyboard {
  enabled: boolean;
  speed: Speed;
  bindToWindow: boolean;
  autoFocus: boolean;
}

interface BaseSolver {
  centralGravity: number;
  springLength: number;
  springConstant: number;
  damping: number;
}

interface BarnesHut extends BaseSolver {
  avoidOverlap: number;
  theta: number;
  gravitationalConstant: number;
}

interface ForceAtlas2Based extends BaseSolver {
  avoidOverlap: number;
  theta: number;
  gravitationalConstant: number;
}

interface Repulsion extends BaseSolver {
  nodeDistance: number;
}

interface HierarchicalRepulsion extends BaseSolver {
  nodeDistance: number;
}

interface Stabilization {
  enabled?: boolean;
  iterations?: number;
  updateInterval?: number;
  onlyDynamicEdges?: boolean;
  fit?: boolean;
}

interface Coordinates {
  x: number;
  y: number;
}

interface Speed extends Coordinates {
  zoom: number;
}

interface ControlNodeStyle {}

interface Interaction {
  dragNodes?: boolean;
  dragView?: boolean;
  hideEdgesOnDrag?: boolean;
  hideEdgesOnZoom?: boolean;
  hideNodesOnDrag?: boolean;
  hover?: boolean;
  hoverConnectedEdges?: boolean;
  keyboard?: Keyboard;
  multiselect?: boolean;
  navigationButtons?: boolean;
  selectable?: boolean;
  selectConnectedEdges?: boolean;
  tooltipDelay?: number;
  zoomSpeed?: number;
  zoomView?: boolean;
}

interface Configure {
  enabled?: boolean;
  filter?:
    | 'nodes'
    | 'edges'
    | 'layout'
    | 'interaction'
    | 'manipulation'
    | 'physics'
    | 'selection'
    | 'renderer';
  showButton?: boolean;
  container?: HTMLElement;
}

interface Layout {
  randomSeed?: number | string;
  improvedLayout?: boolean;
  clusterThreshold?: number;
  hierarchical?: Hierarchical | boolean;
}

interface Manipulation {
  enabled?: boolean;
  initiallyActive?: boolean;
  addNode?: boolean;
  addEdge?: boolean;
  editNode?: any;
  editEdge?: boolean;
  deleteNode?: boolean;
  deleteEdge?: boolean;
  controlNodeStyle?: ControlNodeStyle;
}

interface Physics {
  enabled?: boolean;
  barnesHut?: BarnesHut;
  forceAtlas2Based?: ForceAtlas2Based;
  repulsion?: Repulsion;
  hierarchicalRepulsion?: HierarchicalRepulsion;
  maxVelocity?: number;
  minVelocity?: number;
  solver?:
    | 'barnesHut'
    | 'repulsion'
    | 'hierarchicalRepulsion'
    | 'forceAtlas2Based';
  stabilization?: Stabilization;
  timestep?: number;
  adaptiveTimestep?: boolean;
  wind?: Coordinates;
}

export type {
  NetworkGraphProps,
  NetworkGraphState,
  Options,
  DiffResult,
  Interaction,
  PatchEdgesParams,
  PatchNodesParams,
  Configure,
  Layout,
  Manipulation,
  Physics,
  GraphEvents,
  GraphData,
};
