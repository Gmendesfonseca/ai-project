import type { TaskSchedulingResponse } from '@core/domain/gateway/task-scheduling.gateway';
import type { TaskSchedulingData } from '..';

interface Props {
  response: TaskSchedulingResponse | null;
  error: string | null;
  data: TaskSchedulingData;
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
