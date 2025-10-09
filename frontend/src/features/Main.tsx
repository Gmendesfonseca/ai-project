'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { UninformedSearchHttpGateway } from '../@core/infra/gateways/http/uninformed-search.gateway';
import { AxiosHttpAdapter } from '../@core/infra/http/axios.adapter';
import { UninformedSearchTypes } from './helper';
import { GraphVisualization } from './GraphVisualization';

interface SearchFormData {
  type: UninformedSearchTypes;
  start: string;
  goal: string;
  limit: number;
  maxLimit: number;
}

interface Graph {
  nodes: string[];
  edges: string[][];
}

/*
 This function parses the graph to format expect in payload.
 Ex: node[0] = N1, edge[0] = [N1,N2] => [[N2], []]
*/
function parseGraph({ nodes, edges }: Graph) {
  const graph: string[][] = nodes.map(() => []);
  edges.forEach(([from, to]) => {
    const fromIndex = nodes.indexOf(from);
    const toIndex = nodes.indexOf(to);
    if (fromIndex !== -1 && toIndex !== -1) {
      graph[fromIndex].push(to);
    }
  });
  return graph;
}

export default function MainPage() {
  const [response, setResponse] = useState<string[] | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [graph, setGraph] = useState<Graph>({
    nodes: [],
    edges: [],
  });

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<SearchFormData>({
    defaultValues: {
      type: UninformedSearchTypes.BREADTH,
      start: '',
      goal: '',
      limit: 0,
      maxLimit: 0,
    },
  });

  const watchType = watch('type');

  const httpClient = new AxiosHttpAdapter();
  const gateway = new UninformedSearchHttpGateway(httpClient);

  async function onSubmit(data: SearchFormData) {
    setIsLoading(true);
    setError(null);

    try {
      // Validate if start and goal nodes exist in the graph
      if (!graph.nodes.includes(data.start)) {
        throw new Error(
          `O nó inicial '${data.start}' não existe nos nós fornecidos.`,
        );
      }
      if (!graph.nodes.includes(data.goal)) {
        throw new Error(
          `O nó objetivo '${data.goal}' não existe nos nós fornecidos.`,
        );
      }

      const baseParams = {
        start: data.start,
        goal: data.goal,
        nodes: graph.nodes,
        graph: parseGraph(graph),
      };

      const options = {
        [UninformedSearchTypes.BREADTH]: () => gateway.breadthFirst(baseParams),
        [UninformedSearchTypes.DEPTH]: () => gateway.depthFirst(baseParams),
        [UninformedSearchTypes.DEPTH_LIMITED]: () =>
          gateway.depthLimited({
            ...baseParams,
            limit: Number(data.limit),
          }),
        [UninformedSearchTypes.ITERATIVE]: () =>
          gateway.iterativeDeepening({
            ...baseParams,
            max_limit: Number(data.maxLimit),
          }),
        [UninformedSearchTypes.BIDIRECTIONAL]: () =>
          gateway.bidirectional(baseParams),
      };

      const response = await options[data.type]();
      setResponse(response?.path || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ocorreu um erro');
      setResponse(null);
    } finally {
      setIsLoading(false);
    }
  }

  async function handleFileUpload(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;
    const text = await file.text();
    const lines = text.split('\n').map((line) => line.trim());
    lines.pop();
    parseFileContent(lines);
    event.target.value = '';
  }

  function parseFileContent(fileContent: string[]) {
    const pairNodes = fileContent.map((line) => line.split(','));
    const parsedNodes = Array.from(
      new Set(pairNodes.flat().map((node) => node.trim())),
    ).filter((node) => node !== '');
    const parsedGraph = pairNodes.map((pair) =>
      pair.map((node) => node.trim()),
    );
    setGraph({ nodes: parsedNodes, edges: parsedGraph });
  }

  return (
    <div
      style={{
        padding: '20px',
        maxWidth: '1200px',
        margin: '0 auto',
      }}
    >
      <h1>Algoritmos de Busca Não Informada</h1>

      <form onSubmit={handleSubmit(onSubmit)} style={{ marginBottom: '30px' }}>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: '20px',
          }}
        >
          <div>
            <label
              style={{
                display: 'block',
                marginBottom: '5px',
                fontWeight: 'bold',
              }}
            >
              Algoritmo de Busca:
            </label>
            <input
              type="file"
              accept=".txt"
              style={{ marginBottom: '5px', display: 'block' }}
              onChange={handleFileUpload}
            />
          </div>
          <div>
            <label
              style={{
                display: 'block',
                marginBottom: '5px',
                fontWeight: 'bold',
              }}
            >
              Algoritmo de Busca:
            </label>
            <select
              {...register('type')}
              style={{
                width: '300px',
                padding: '8px',
                marginBottom: '10px',
                boxSizing: 'border-box',
              }}
            >
              <option value={UninformedSearchTypes.BREADTH}>Amplitude</option>
              <option value={UninformedSearchTypes.DEPTH}>Profundidade</option>
              <option value={UninformedSearchTypes.DEPTH_LIMITED}>
                Limitada em Profundidade
              </option>
              <option value={UninformedSearchTypes.ITERATIVE}>
                Profundidade Iterativa
              </option>
              <option value={UninformedSearchTypes.BIDIRECTIONAL}>
                Bidirecional
              </option>
            </select>
          </div>

          <div>
            <label
              style={{
                display: 'block',
                marginBottom: '5px',
                fontWeight: 'bold',
              }}
            >
              Nó Inicial:
            </label>
            <input
              {...register('start', { required: 'O nó inicial é obrigatório' })}
              type="text"
              placeholder="ex.: A"
              style={{
                width: '300px',
                padding: '8px',
                marginBottom: '5px',
                boxSizing: 'border-box',
              }}
            />
            {errors.start && (
              <div style={{ color: 'red', fontSize: '12px' }}>
                {errors.start.message}
              </div>
            )}
          </div>

          <div>
            <label
              style={{
                display: 'block',
                marginBottom: '5px',
                fontWeight: 'bold',
              }}
            >
              Nó Objetivo:
            </label>
            <input
              {...register('goal', { required: 'O nó objetivo é obrigatório' })}
              type="text"
              placeholder="ex.: D"
              style={{
                width: '300px',
                padding: '8px',
                marginBottom: '5px',
                boxSizing: 'border-box',
              }}
            />
            {errors.goal && (
              <div style={{ color: 'red', fontSize: '12px' }}>
                {errors.goal.message}
              </div>
            )}
          </div>

          {watchType === UninformedSearchTypes.DEPTH_LIMITED && (
            <div>
              <label
                style={{
                  display: 'block',
                  marginBottom: '5px',
                  fontWeight: 'bold',
                }}
              >
                Limite de Profundidade:
              </label>
              <input
                {...register('limit', {
                  required:
                    'O limite é obrigatório para busca limitada em profundidade',
                })}
                type="number"
                min="1"
                placeholder="3"
                style={{
                  width: '300px',
                  padding: '8px',
                  marginBottom: '5px',
                  boxSizing: 'border-box',
                }}
              />
              {errors.limit && (
                <div style={{ color: 'red', fontSize: '12px' }}>
                  {errors.limit.message}
                </div>
              )}
            </div>
          )}

          {watchType === UninformedSearchTypes.ITERATIVE && (
            <div>
              <label
                style={{
                  display: 'block',
                  marginBottom: '5px',
                  fontWeight: 'bold',
                }}
              >
                Limite Máximo de Profundidade:
              </label>
              <input
                {...register('maxLimit', {
                  required:
                    'O limite máximo é obrigatório para busca em profundidade iterativa',
                })}
                type="number"
                min="1"
                placeholder="5"
                style={{
                  width: '300px',
                  padding: '8px',
                  marginBottom: '5px',
                  boxSizing: 'border-box',
                }}
              />
              {errors.maxLimit && (
                <div style={{ color: 'red', fontSize: '12px' }}>
                  {errors.maxLimit.message}
                </div>
              )}
            </div>
          )}
        </div>

        <button
          type="submit"
          disabled={isLoading}
          style={{
            padding: '12px 24px',
            backgroundColor: isLoading ? '#ccc' : '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: isLoading ? 'not-allowed' : 'pointer',
            fontSize: '16px',
            marginTop: '20px',
          }}
        >
          {isLoading ? 'Buscando...' : 'Executar Busca'}
        </button>
      </form>

      {error && (
        <div
          style={{
            padding: '10px',
            backgroundColor: '#ffebee',
            color: '#c62828',
            borderRadius: '4px',
            marginBottom: '20px',
          }}
        >
          <strong>Erro:</strong> {error}
        </div>
      )}

      <GraphVisualization
        nodes={graph.nodes}
        edges={graph.edges}
        path={response}
      />

      {!response && !error && !isLoading && (
        <div
          style={{
            padding: '20px',
            textAlign: 'center',
            color: '#666',
            fontStyle: 'italic',
          }}
        >
          Insira os dados do grafo e execute uma busca para ver os resultados
        </div>
      )}
    </div>
  );
}
