import type { TaskSchedulingResponse } from '@core/domain/gateway/task-scheduling.gateway';
import type { TaskSchedulingData } from '..';
import GraphVis, { type GraphOptions } from '@/lib/react-graph-vis';

interface Props {
  response: TaskSchedulingResponse | null;
  error: string | null;
  data: TaskSchedulingData;
}

const taskGraphOptions: GraphOptions = {
  nodes: {
    shape: 'circle',
    size: 30,
    font: {
      size: 14,
      color: '#000000',
    },
    borderWidth: 2,
    shadow: true,
  },
  edges: {
    width: 3,
    color: { inherit: false },
    arrows: {
      to: {
        enabled: true,
        scaleFactor: 1.2,
      },
    },
    shadow: true,
    smooth: {
      enabled: true,
      type: 'curvedCW',
      roundness: 0.1,
    },
  },
  layout: {
    hierarchical: false,
  },
  interaction: {
    hover: true,
    selectConnectedEdges: false,
    zoomView: false,
    dragView: true,
  },
  physics: {
    enabled: false,
    stabilization: {
      enabled: true,
      iterations: 100,
    },
  },
};

function createTaskSequenceGraph(
  tasks: number[],
  sequence: number[],
  setupMatrix: Record<string, number>,
) {
  // Create nodes - START node + task nodes
  const nodes = [
    {
      id: '0',
      label: 'START',
      color: '#007bff',
      font: { color: '#ffffff' },
      x: 0,
      y: 0,
    },
    ...tasks.map((task, index) => ({
      id: task.toString(),
      label: `T${task}`,
      color: '#28a745',
      font: { color: '#ffffff' },
      x: Math.cos((index * 2 * Math.PI) / tasks.length) * 200 + 200,
      y: Math.sin((index * 2 * Math.PI) / tasks.length) * 200 + 200,
    })),
  ];

  // Create edges - show optimal sequence path + all possible edges
  const edges: Array<{
    id: string;
    from: string;
    to: string;
    label: string;
    color: string;
    width: number;
  }> = [];

  // Add optimal sequence edges (highlighted)
  if (sequence.length > 0) {
    // Edge from START to first task
    const firstTask = sequence[0];
    const startCost = setupMatrix[`(0,${firstTask})`] || 0;
    edges.push({
      id: `optimal-0-${firstTask}`,
      from: '0',
      to: firstTask.toString(),
      label: `${startCost}`,
      color: '#28a745',
      width: 4,
    });

    // Edges between consecutive tasks in sequence
    for (let i = 0; i < sequence.length - 1; i++) {
      const fromTask = sequence[i];
      const toTask = sequence[i + 1];
      const cost = setupMatrix[`(${fromTask},${toTask})`] || 0;
      edges.push({
        id: `optimal-${fromTask}-${toTask}`,
        from: fromTask.toString(),
        to: toTask.toString(),
        label: `${cost}`,
        color: '#28a745',
        width: 4,
      });
    }
  }

  // Add all other edges (lighter color, thinner)
  Object.entries(setupMatrix).forEach(([key, cost]) => {
    const match = key.match(/\((\d+),(\d+)\)/);
    if (match) {
      const from = match[1];
      const to = match[2];
      const edgeId = `edge-${from}-${to}`;

      // Check if this edge is already in optimal sequence
      const isOptimal = edges.some((e) => e.id === `optimal-${from}-${to}`);

      if (!isOptimal) {
        edges.push({
          id: edgeId,
          from,
          to,
          label: `${cost}`,
          color: '#dc3545',
          width: 1,
        });
      }
    }
  });

  return { nodes, edges };
}

export default function TaskSequenceVisualization({
  response,
  error,
  data,
}: Props) {
  if (error) {
    return (
      <div
        style={{
          flex: 1,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '20px',
          border: '2px solid #dc3545',
          borderRadius: '8px',
          backgroundColor: '#f8d7da',
          color: '#721c24',
        }}
      >
        <div style={{ textAlign: 'center' }}>
          <h3>Erro</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!response) {
    return (
      <div
        style={{
          flex: 1,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '20px',
          border: '2px dashed #ccc',
          borderRadius: '8px',
          backgroundColor: '#f8f9fa',
          color: '#6c757d',
        }}
      >
        <div style={{ textAlign: 'center' }}>
          <h3>Resultado aparecerá aqui</h3>
          <p>Execute um algoritmo para ver o sequenciamento de tarefas</p>
        </div>
      </div>
    );
  }

  return (
    <div
      style={{
        flex: 1,
        padding: '20px',
        border: '2px solid #28a745',
        borderRadius: '8px',
        backgroundColor: '#d4edda',
      }}
    >
      <h3 style={{ color: '#155724', marginBottom: '20px' }}>
        Resultado - {response.algorithm}
        {response.heuristic && ` (${response.heuristic.toUpperCase()})`}
      </h3>

      {/* Graph Visualization */}
      <div style={{ marginBottom: '30px' }}>
        <h4 style={{ color: '#155724', marginBottom: '15px' }}>
          Visualização do Sequenciamento:
        </h4>
        <div
          style={{
            height: '400px',
            border: '1px solid #c3e6cb',
            borderRadius: '8px',
            backgroundColor: '#ffffff',
            overflow: 'hidden',
          }}
        >
          <GraphVis
            key={`task-graph-${response.sequence.join('-')}`}
            graph={createTaskSequenceGraph(
              data.tasks,
              response.sequence,
              data.setupMatrix,
            )}
            options={taskGraphOptions}
            style={{ width: '100%', height: '100%' }}
          />
        </div>
      </div>

      {/* Sequence Visualization */}
      <div style={{ marginBottom: '20px' }}>
        <h4 style={{ color: '#155724', marginBottom: '10px' }}>
          Sequência Ótima:
        </h4>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            flexWrap: 'wrap',
          }}
        >
          <div
            style={{
              padding: '8px 12px',
              backgroundColor: '#007bff',
              color: 'white',
              borderRadius: '20px',
              fontSize: '14px',
              fontWeight: 'bold',
            }}
          >
            START
          </div>
          {response.sequence.map((task, index) => (
            <div
              key={index}
              style={{ display: 'flex', alignItems: 'center', gap: '10px' }}
            >
              <div style={{ fontSize: '18px', color: '#155724' }}>→</div>
              <div
                style={{
                  padding: '8px 12px',
                  backgroundColor: '#28a745',
                  color: 'white',
                  borderRadius: '20px',
                  fontSize: '14px',
                  fontWeight: 'bold',
                }}
              >
                Tarefa {task}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Cost Information */}
      <div style={{ marginBottom: '20px' }}>
        <h4 style={{ color: '#155724', marginBottom: '10px' }}>Custo Total:</h4>
        <div
          style={{
            padding: '15px',
            backgroundColor: '#ffffff',
            border: '1px solid #c3e6cb',
            borderRadius: '5px',
            fontSize: '18px',
            fontWeight: 'bold',
            textAlign: 'center',
            color: '#155724',
          }}
        >
          {response.total_cost.toFixed(2)}
        </div>
      </div>

      {/* Setup Details */}
      {response.setup_details && response.setup_details.length > 0 && (
        <div style={{ marginBottom: '20px' }}>
          <h4 style={{ color: '#155724', marginBottom: '10px' }}>
            Detalhes dos Setups:
          </h4>
          <div
            style={{
              backgroundColor: '#ffffff',
              border: '1px solid #c3e6cb',
              borderRadius: '5px',
              overflow: 'hidden',
            }}
          >
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ backgroundColor: '#f8f9fa', color: '#155724' }}>
                  <th
                    style={{
                      padding: '10px',
                      border: '1px solid #dee2e6',
                      textAlign: 'left',
                    }}
                  >
                    De
                  </th>
                  <th
                    style={{
                      padding: '10px',
                      border: '1px solid #dee2e6',
                      textAlign: 'left',
                    }}
                  >
                    Para
                  </th>
                  <th
                    style={{
                      padding: '10px',
                      border: '1px solid #dee2e6',
                      textAlign: 'right',
                    }}
                  >
                    Custo
                  </th>
                </tr>
              </thead>
              <tbody>
                {response.setup_details.map((detail, index) => (
                  <tr key={index}>
                    <td
                      style={{
                        padding: '10px',
                        border: '1px solid #dee2e6',
                        color: '#155724',
                      }}
                    >
                      {detail.from === 0 ? 'START' : `Tarefa ${detail.from}`}
                    </td>
                    <td
                      style={{
                        padding: '10px',
                        border: '1px solid #dee2e6',
                        color: '#155724',
                      }}
                    >
                      Tarefa {detail.to}
                    </td>
                    <td
                      style={{
                        padding: '10px',
                        border: '1px solid #dee2e6',
                        textAlign: 'right',
                        color: '#155724',
                      }}
                    >
                      {detail.cost.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Input Summary */}
      <div>
        <h4 style={{ color: '#155724', marginBottom: '10px' }}>
          Resumo da Entrada:
        </h4>
        <div
          style={{
            backgroundColor: '#ffffff',
            border: '1px solid #c3e6cb',
            borderRadius: '5px',
            padding: '15px',
          }}
        >
          <p style={{ margin: '5px 0', color: '#155724' }}>
            <strong>Tarefas:</strong> {data.tasks.join(', ')}
          </p>
          <p style={{ margin: '5px 0', color: '#155724' }}>
            <strong>Total de setups definidos:</strong>{' '}
            {Object.keys(data.setupMatrix).length}
          </p>
          {data.families && Object.keys(data.families).length > 0 && (
            <div style={{ margin: '10px 0' }}>
              <p style={{ margin: '5px 0', color: '#155724' }}>
                <strong>Famílias:</strong>
              </p>
              <div style={{ marginLeft: '15px' }}>
                {Object.entries(data.families).map(([task, family]) => (
                  <p
                    key={task}
                    style={{
                      margin: '2px 0',
                      color: '#155724',
                      fontSize: '14px',
                    }}
                  >
                    Tarefa {task}: {family}
                  </p>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
