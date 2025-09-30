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
  nodes: string;
  graph: string;
  limit: number;
  maxLimit: number;
}

export default function MainPage() {
  const [response, setResponse] = useState<string[] | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

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
      nodes: '',
      graph: '',
      limit: 0,
      maxLimit: 0,
    },
  });

  const watchType = watch('type');

  const httpClient = new AxiosHttpAdapter();
  const gateway = new UninformedSearchHttpGateway(httpClient);

  function parseGraphData(graphStr: string, nodesStr: string) {
    try {
      const nodes = JSON.parse(nodesStr);
      const graph = JSON.parse(graphStr);
      return { nodes, graph };
    } catch {
      throw new Error('Invalid JSON format for nodes or graph');
    }
  }

  async function onSubmit(data: SearchFormData) {
    setIsLoading(true);
    setError(null);

    try {
      const { nodes, graph } = parseGraphData(data.graph, data.nodes);

      const baseParams = {
        start: data.start,
        goal: data.goal,
        nodes,
        graph,
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
      setError(err instanceof Error ? err.message : 'An error occurred');
      setResponse(null);
    } finally {
      setIsLoading(false);
    }
  }

  let parsedNodes: string[] = [];
  let parsedGraph: string[][] = [];

  try {
    const nodesValue = watch('nodes');
    const graphValue = watch('graph');
    if (nodesValue && graphValue) {
      const parsed = parseGraphData(graphValue, nodesValue);
      parsedNodes = parsed.nodes;
      parsedGraph = parsed.graph;
    }
  } catch {
    // Ignore parsing errors for preview
  }

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>Uninformed Search Algorithms</h1>

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
              Search Algorithm:
            </label>
            <select
              {...register('type')}
              style={{ width: '100%', padding: '8px', marginBottom: '10px' }}
            >
              <option value={UninformedSearchTypes.BREADTH}>
                Breadth-First Search
              </option>
              <option value={UninformedSearchTypes.DEPTH}>
                Depth-First Search
              </option>
              <option value={UninformedSearchTypes.DEPTH_LIMITED}>
                Depth-Limited Search
              </option>
              <option value={UninformedSearchTypes.ITERATIVE}>
                Iterative Deepening Search
              </option>
              <option value={UninformedSearchTypes.BIDIRECTIONAL}>
                Bidirectional Search
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
              Start Node:
            </label>
            <input
              {...register('start', { required: 'Start node is required' })}
              type="text"
              placeholder="e.g., A"
              style={{ width: '100%', padding: '8px', marginBottom: '5px' }}
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
              Goal Node:
            </label>
            <input
              {...register('goal', { required: 'Goal node is required' })}
              type="text"
              placeholder="e.g., D"
              style={{ width: '100%', padding: '8px', marginBottom: '5px' }}
            />
            {errors.goal && (
              <div style={{ color: 'red', fontSize: '12px' }}>
                {errors.goal.message}
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
              Nodes (JSON array):
            </label>
            <input
              {...register('nodes', { required: 'Nodes are required' })}
              type="text"
              placeholder='["A", "B", "C", "D"]'
              style={{ width: '100%', padding: '8px', marginBottom: '5px' }}
            />
            {errors.nodes && (
              <div style={{ color: 'red', fontSize: '12px' }}>
                {errors.nodes.message}
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
              Graph (JSON array):
            </label>
            <input
              {...register('graph', { required: 'Graph is required' })}
              type="text"
              placeholder='[["B","C"],["A","D"],["A","D"],["B","C"]]'
              style={{ width: '100%', padding: '8px', marginBottom: '5px' }}
            />
            {errors.graph && (
              <div style={{ color: 'red', fontSize: '12px' }}>
                {errors.graph.message}
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
                Depth Limit:
              </label>
              <input
                {...register('limit', {
                  required: 'Limit is required for depth-limited search',
                })}
                type="number"
                min="1"
                placeholder="3"
                style={{ width: '100%', padding: '8px', marginBottom: '5px' }}
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
                Max Depth Limit:
              </label>
              <input
                {...register('maxLimit', {
                  required: 'Max limit is required for iterative deepening',
                })}
                type="number"
                min="1"
                placeholder="5"
                style={{ width: '100%', padding: '8px', marginBottom: '5px' }}
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
          {isLoading ? 'Searching...' : 'Execute Search'}
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
          <strong>Error:</strong> {error}
        </div>
      )}

      <GraphVisualization
        nodes={parsedNodes}
        edges={parsedGraph}
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
          Enter graph data and execute a search to see results
        </div>
      )}
    </div>
  );
}
