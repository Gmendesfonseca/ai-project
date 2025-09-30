import Graph from '@/lib/react-graph-vis';

const options = {
  layout: {
    hierarchical: false,
  },
  physics: {
    enabled: false,
    stabilization: { iterations: 150 },
  },
  nodes: {
    shape: 'circle',
    size: 25,
    font: {
      size: 16,
      color: '#000000',
    },
    borderWidth: 2,
    shadow: true,
  },
  edges: {
    width: 2,
    color: { inherit: false },
    arrows: {
      to: {
        enabled: true,
        scaleFactor: 1,
      },
    },
    shadow: true,
    smooth: true,
  },
  interaction: {
    hover: true,
    selectConnectedEdges: false,
  },
};
type GraphVisualizationProps = {
  nodes: string[];
  edges: string[][];
  path?: string[];
};

export function GraphVisualization({
  nodes,
  edges,
  path,
}: GraphVisualizationProps) {
  if (!nodes || !edges) return null;

  const isEdgeInPath = (from: string, to: string): boolean => {
    if (!path || path.length < 2) return false;

    for (let i = 0; i < path.length - 1; i++) {
      if (path[i] === from && path[i + 1] === to) {
        return true;
      }
    }
    return false;
  };

  const events = {
    select: ({ nodes, edges }: { nodes: string[]; edges: string[] }) => {
      console.log('Selected nodes:');
      console.log(nodes);
      console.log('Selected edges:');
      console.log(edges);
      if (nodes.length > 0) {
        alert('Selected node: ' + nodes[0]);
      }
    },
  };

  const graphData = {
    nodes: nodes.map((node) => ({
      id: node,
      label: node,
      color: path?.includes(node) ? '#4CAF50' : '#E3F2FD',
      font: {
        color: path?.includes(node) ? '#FFFFFF' : '#333333',
        size: path?.includes(node) ? 18 : 16,
      },
      borderWidth: path?.includes(node) ? 3 : 2,
      borderColor: path?.includes(node) ? '#2E7D32' : '#1976D2',
    })),
    edges: edges.map(([from, to], index) => ({
      id: `edge-${from}-${to}-${index}`,
      from,
      to,
      color: isEdgeInPath(from, to) ? '#4CAF50' : '#666666',
      width: isEdgeInPath(from, to) ? 4 : 2,
      arrows: {
        to: {
          enabled: true,
          scaleFactor: isEdgeInPath(from, to) ? 1.2 : 1,
        },
      },
    })),
  };

  return (
    <div
      style={{
        marginTop: '20px',
        padding: '20px',
        border: '2px solid #e0e0e0',
        borderRadius: '12px',
        backgroundColor: '#fafafa',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      }}
    >
      <h3 style={{ margin: '0 0 15px 0', color: '#333' }}>
        Graph Visualization
      </h3>
      {path && path.length > 0 && (
        <div
          style={{
            marginBottom: '15px',
            padding: '10px',
            backgroundColor: '#e8f5e8',
            borderRadius: '8px',
            border: '1px solid #4CAF50',
          }}
        >
          <strong style={{ color: '#2E7D32' }}>Path Found: </strong>
          <span style={{ color: '#1B5E20' }}>{path.join(' → ')}</span>
        </div>
      )}
      <div
        style={{
          height: '400px',
          border: '1px solid #ddd',
          borderRadius: '8px',
        }}
      >
        <Graph
          key={`graph-${nodes.join('-')}-${path?.join('-') || 'no-path'}`}
          graph={graphData}
          options={options}
          events={events}
          style={{ width: '100%', height: '100%' }}
        />
      </div>
    </div>
  );
}
