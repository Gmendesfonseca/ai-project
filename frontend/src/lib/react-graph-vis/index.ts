import React, { Component, createRef } from 'react';
import type { RefObject } from 'react';
import * as _ from 'lodash';
import { DataSet } from 'vis-data';
import { Network } from 'vis-network';
import { v4 as uuidv4 } from 'uuid';
import type { NetworkGraphProps, NetworkGraphState } from './types';

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

const diff = <T extends Record<string, any>>(
  current: T[],
  next: T[],
  field: string = 'id',
): DiffResult<T> => {
  // consider caching this value between updates
  const nextIds = new Set(next.map((item) => item[field]));
  const removed = current.filter((item) => !nextIds.has(item[field]));

  const unchanged = _.intersectionWith(next, current, _.isEqual);

  const updated = _.differenceWith(
    _.intersectionWith(next, current, (a: T, b: T) => a[field] === b[field]),
    unchanged,
    _.isEqual,
  );

  const added = _.differenceWith(
    _.differenceWith(next, current, _.isEqual),
    updated,
    _.isEqual,
  );

  return {
    removed,
    unchanged,
    updated,
    added,
  };
};

class Graph extends Component<NetworkGraphProps, NetworkGraphState> {
  private container: RefObject<HTMLDivElement | null>;
  private Network!: Network;
  private edges!: DataSet<any>;
  private nodes!: DataSet<any>;

  static defaultProps: Partial<NetworkGraphProps> = {
    graph: { nodes: [], edges: [] },
    style: { width: '100%', height: '100%' },
  };

  constructor(props: NetworkGraphProps) {
    super(props);

    const { identifier } = props;

    this.updateGraph = this.updateGraph.bind(this);
    this.state = {
      identifier: identifier !== undefined ? identifier : uuidv4(),
    };
    this.container = createRef<HTMLDivElement>();
  }

  componentDidMount(): void {
    this.edges = new DataSet();
    if (this.props.graph.edges) {
      const normalizedEdges = this.props.graph.edges.map((edge, index) => ({
        ...edge,
        id: edge.id || `edge-${edge.from}-${edge.to}-${index}`,
      }));
      this.edges.add(normalizedEdges);
    }
    this.nodes = new DataSet();
    if (this.props.graph.nodes) {
      const normalizedNodes = this.props.graph.nodes.map((node, index) => ({
        ...node,
        id: node.id || `node-${index}`,
      }));
      this.nodes.add(normalizedNodes);
    }
    this.updateGraph();
  }

  shouldComponentUpdate(
    nextProps: NetworkGraphProps,
    _nextState: NetworkGraphState,
  ): boolean {
    const nodesChange = !_.isEqual(
      this.props.graph.nodes,
      nextProps.graph.nodes,
    );
    const edgesChange = !_.isEqual(
      this.props.graph.edges,
      nextProps.graph.edges,
    );
    const optionsChange = !_.isEqual(this.props.options, nextProps.options);
    const eventsChange = !_.isEqual(this.props.events, nextProps.events);

    const hasSignificantChanges =
      (nodesChange &&
        (!this.props.graph.nodes ||
          !nextProps.graph.nodes ||
          this.props.graph.nodes.length === 0 ||
          nextProps.graph.nodes.length === 0)) ||
      (edgesChange &&
        (!this.props.graph.edges ||
          !nextProps.graph.edges ||
          this.props.graph.edges.length === 0 ||
          nextProps.graph.edges.length === 0));

    if (hasSignificantChanges) {
      this.rebuildDataSets(nextProps);
      return false;
    }

    if (nodesChange) {
      const idIsEqual = (n1: any, n2: any): boolean => n1.id === n2.id;
      const currentNodes = Array.isArray(this.props.graph.nodes)
        ? this.props.graph.nodes
        : [];
      const nextNodes = Array.isArray(nextProps.graph.nodes)
        ? nextProps.graph.nodes
        : [];

      // Ensure all nodes have IDs
      const normalizedCurrentNodes = currentNodes.map((node, index) => ({
        ...node,
        id: node.id || `node-${index}`,
      }));
      const normalizedNextNodes = nextNodes.map((node, index) => ({
        ...node,
        id: node.id || `node-${index}`,
      }));

      const nodesRemoved = _.differenceWith(
        normalizedCurrentNodes,
        normalizedNextNodes,
        idIsEqual,
      );
      const nodesAdded = _.differenceWith(
        normalizedNextNodes,
        normalizedCurrentNodes,
        idIsEqual,
      );
      const nodesChanged = _.differenceWith(
        _.differenceWith(
          normalizedNextNodes,
          normalizedCurrentNodes,
          _.isEqual,
        ),
        nodesAdded,
        _.isEqual,
      );

      this.patchNodes({
        nodesRemoved,
        nodesAdded,
        nodesChanged,
      });
    }

    if (edgesChange) {
      const currentEdges = Array.isArray(this.props.graph.edges)
        ? this.props.graph.edges
        : [];
      const nextEdges = Array.isArray(nextProps.graph.edges)
        ? nextProps.graph.edges
        : [];

      // Ensure all edges have IDs
      const normalizedCurrentEdges = currentEdges.map((edge, index) => ({
        ...edge,
        id: edge.id || `edge-${edge.from}-${edge.to}-${index}`,
      }));
      const normalizedNextEdges = nextEdges.map((edge, index) => ({
        ...edge,
        id: edge.id || `edge-${edge.from}-${edge.to}-${index}`,
      }));

      const {
        removed: edgesRemoved,
        added: edgesAdded,
        updated: edgesChanged,
      } = diff(normalizedCurrentEdges, normalizedNextEdges);

      this.patchEdges({
        edgesRemoved,
        edgesAdded,
        edgesChanged,
      });
    }

    if (optionsChange && this.Network) {
      this.Network.setOptions(nextProps.options || {});
    }

    if (eventsChange && this.Network) {
      // Remove old event listeners
      const events = this.props.events || {};
      Object.keys(events).forEach((eventName) => {
        const handler = events[eventName as keyof typeof events];
        if (handler) {
          this.Network.off(eventName as any, handler);
        }
      });

      // Add new event listeners
      const nextEvents = nextProps.events || {};
      Object.keys(nextEvents).forEach((eventName) => {
        const handler = nextEvents[eventName as keyof typeof nextEvents];
        if (handler) {
          this.Network.on(eventName as any, handler);
        }
      });
    }

    return false;
  }

  componentDidUpdate(): void {
    this.updateGraph();
  }

  private patchEdges({
    edgesRemoved,
    edgesAdded,
    edgesChanged,
  }: PatchEdgesParams): void {
    // Remove edges first
    if (edgesRemoved.length > 0) {
      const idsToRemove = edgesRemoved
        .map((edge) => edge.id)
        .filter((id) => id !== undefined);
      if (idsToRemove.length > 0) {
        this.edges.remove(idsToRemove);
      }
    }

    // Filter out duplicates from edgesAdded to prevent duplicate ID errors
    const existingIds = new Set(this.edges.getIds());
    const uniqueEdgesToAdd = edgesAdded.filter(
      (edge) => !edge.id || !existingIds.has(edge.id),
    );

    // Add only unique edges
    if (uniqueEdgesToAdd.length > 0) {
      this.edges.add(uniqueEdgesToAdd);
    }

    // Update existing edges
    if (edgesChanged.length > 0) {
      this.edges.update(edgesChanged);
    }
  }

  private patchNodes({
    nodesRemoved,
    nodesAdded,
    nodesChanged,
  }: PatchNodesParams): void {
    // Remove nodes first
    if (nodesRemoved.length > 0) {
      const idsToRemove = nodesRemoved.map((node) => node.id);
      this.nodes.remove(idsToRemove);
    }

    // Filter out duplicates from nodesAdded to prevent duplicate ID errors
    const existingIds = new Set(this.nodes.getIds());
    const uniqueNodesToAdd = nodesAdded.filter(
      (node) => !existingIds.has(node.id),
    );

    // Add only unique nodes
    if (uniqueNodesToAdd.length > 0) {
      this.nodes.add(uniqueNodesToAdd);
    }

    // Update existing nodes
    if (nodesChanged.length > 0) {
      this.nodes.update(nodesChanged);
    }
  }

  private rebuildDataSets(props: NetworkGraphProps): void {
    // Clear existing data
    if (this.nodes) {
      this.nodes.clear();
    } else {
      this.nodes = new DataSet();
    }

    if (this.edges) {
      this.edges.clear();
    } else {
      this.edges = new DataSet();
    }

    // Add new data with proper IDs
    if (props.graph.nodes) {
      const normalizedNodes = props.graph.nodes.map((node, index) => ({
        ...node,
        id: node.id || `node-${index}`,
      }));
      this.nodes.add(normalizedNodes);
    }

    if (props.graph.edges) {
      const normalizedEdges = props.graph.edges.map((edge, index) => ({
        ...edge,
        id: edge.id || `edge-${edge.from}-${edge.to}-${index}`,
      }));
      this.edges.add(normalizedEdges);
    }
  }

  private updateGraph(): void {
    const defaultOptions = {
      physics: {
        stabilization: false,
      },
      autoResize: false,
      edges: {
        smooth: false,
        color: '#000000',
        width: 0.5,
        arrows: {
          to: {
            enabled: true,
            scaleFactor: 0.5,
          },
        },
      },
    };

    // merge user provided options with our default ones
    const options = _.defaultsDeep(this.props.options || {}, defaultOptions);

    if (this.container.current) {
      this.Network = new Network(
        this.container.current,
        {
          ...this.props.graph,
          edges: this.edges,
          nodes: this.nodes,
        },
        options,
      );

      if (this.props.getNetwork) {
        this.props.getNetwork(this.Network);
      }

      if (this.props.getNodes) {
        this.props.getNodes(this.nodes);
      }

      if (this.props.getEdges) {
        this.props.getEdges(this.edges);
      }

      // Add user provided events to network
      const events = this.props.events || {};
      Object.keys(events).forEach((eventName) => {
        const handler = events[eventName as keyof typeof events];
        if (handler) {
          this.Network.on(eventName as any, handler);
        }
      });
    }
  }

  render(): React.ReactElement {
    const { identifier } = this.state;
    const { style } = this.props;

    return React.createElement('div', {
      id: identifier,
      ref: this.container,
      style: style,
    });
  }
}

export default Graph;
export type {
  NetworkGraphProps,
  NetworkGraphState,
  GraphEvents,
  GraphData,
} from './types';
