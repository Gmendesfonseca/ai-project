'use client';

import { useState, useTransition } from 'react';
import { useForm } from 'react-hook-form';
import { SearchTypes } from './helper';
import { GraphVisualization } from './GraphVisualization';
import { AxiosHttpAdapter } from '@core/infra/http/axios.adapter';
import { UninformedSearchHttpGateway } from '@core/infra/gateways/http/uninformed-search.gateway';
import { InformedSearchHttpGateway } from '@core/infra/gateways/http/informed-search.gateway';

interface SearchFormData {
  type: SearchTypes;
  start: string;
  goal: string;
  limit: number;
  maxLimit: number;
}

interface Graph {
  nodes: string[];
  edges: string[][];
}

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

function parseFileContent(fileContent: string[]) {
  const pairNodes = fileContent.map((line) => line.split(','));
  const parsedNodes = Array.from(
    new Set(pairNodes.flat().map((node) => node.trim())),
  ).filter((node) => node !== '');
  const parsedGraph = pairNodes.map((pair) => pair.map((node) => node.trim()));
  return { nodes: parsedNodes, edges: parsedGraph };
}

const options: { value: SearchTypes; label: string }[] = [
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

export default function MainPage() {
  const [response, setResponse] = useState<string[] | null>(null);
  const [loading, startTransition] = useTransition();
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
      type: SearchTypes.BREADTH,
      start: '',
      goal: '',
      limit: 0,
      maxLimit: 0,
    },
  });

  const watchType = watch('type');

  const httpClient = new AxiosHttpAdapter();
  const gateway = {
    uniformed: new UninformedSearchHttpGateway(httpClient),
    informed: new InformedSearchHttpGateway(httpClient),
  };

  async function onSubmit(data: SearchFormData) {
    startTransition(async () => {
      setError(null);

      try {
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
          [SearchTypes.BREADTH]: () =>
            gateway.uniformed.breadthFirst(baseParams),
          [SearchTypes.DEPTH]: () => gateway.uniformed.depthFirst(baseParams),
          [SearchTypes.DEPTH_LIMITED]: () =>
            gateway.uniformed.depthLimited({
              ...baseParams,
              limit: Number(data.limit),
            }),
          [SearchTypes.ITERATIVE]: () =>
            gateway.uniformed.iterativeDeepening({
              ...baseParams,
              max_limit: Number(data.maxLimit),
            }),
          [SearchTypes.BIDIRECTIONAL]: () =>
            gateway.uniformed.bidirectional(baseParams),
          [SearchTypes.UNIFORMED_COST]: () =>
            gateway.informed.uniformCost({
              ...baseParams,
              heuristics: graph.nodes.map(() => 0),
            }),
          [SearchTypes.A_STAR]: () =>
            gateway.informed.aStar({
              ...baseParams,
              heuristics: graph.nodes.map(() => 0),
            }),
          [SearchTypes.GREEDY]: () =>
            gateway.informed.greedy({
              ...baseParams,
              heuristics: graph.nodes.map(() => 0),
            }),
          [SearchTypes.IDA_STAR]: () =>
            gateway.informed.idaStar({
              ...baseParams,
              heuristics: graph.nodes.map(() => 0),
            }),
        };

        const response = await options[data.type]();
        setResponse(response?.path || []);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Ocorreu um erro');
        setResponse(null);
      }
    });
  }

  async function handleFileUpload(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;
    const text = await file.text();
    const lines = text.split('\n').map((line) => line.trim());
    lines.pop();
    const graph = parseFileContent(lines);
    setGraph(graph);
    event.target.value = '';
  }

  return (
    <div
      style={{
        padding: '20px',
        maxWidth: '1200px',
        margin: '0 auto',
      }}
    >
      <h1>Algoritmos de Busca</h1>

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
              {options.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
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

          {watchType === SearchTypes.DEPTH_LIMITED && (
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

          {watchType === SearchTypes.ITERATIVE && (
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
          disabled={loading}
          style={{
            padding: '12px 24px',
            backgroundColor: loading ? '#ccc' : '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer',
            fontSize: '16px',
            marginTop: '20px',
          }}
        >
          {loading ? 'Buscando...' : 'Executar Busca'}
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

      {!response && !error && !loading && (
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
