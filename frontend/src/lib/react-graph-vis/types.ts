import { Network } from 'vis-network';
import { DataSet } from 'vis-data';
import type { Options, Node, Edge } from 'vis-network';

export { Network, DataSet };
export type { Options, Node, Edge };

export type NetworkEvents =
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

export type GraphEvents = {
  [event in NetworkEvents]?: (params?: any) => void;
};

export interface GraphData {
  nodes?: Node[] | DataSet<Node>;
  edges?: Edge[] | DataSet<Edge>;
}

export interface NetworkGraphProps {
  graph: GraphData;
  options?: Options;
  events?: GraphEvents;
  getNetwork?: (network: Network) => void;
  identifier?: string;
  style?: React.CSSProperties;
  getNodes?: (nodes: DataSet<Node>) => void;
  getEdges?: (edges: DataSet<Edge>) => void;
}

export interface NetworkGraphState {
  identifier: string;
}
