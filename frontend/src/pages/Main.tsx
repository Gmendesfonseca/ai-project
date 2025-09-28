'use client';

import { useState } from 'react';
import { UninformedSearchHttpGateway } from '../@core/infra/gateways/http/uninformed-search.gateway';
import { AxiosHttpAdapter } from '../@core/infra/http/axios.adapter';

const UninformedSearchTypes = {
  BREADTH: 'BREADTH',
  DEPTH: 'DEPTH',
  DEPTH_LIMITED: 'DEPTH_LIMITED',
  ITERATIVE: 'ITERATIVE',
  BIDIRECTIONAL: 'BIDIRECTIONAL',
};
type UninformedSearchTypes =
  (typeof UninformedSearchTypes)[keyof typeof UninformedSearchTypes];

export const MainPage = () => {
  const [response, setResponse] = useState<string[] | null>(null);
  const [type, setType] = useState<UninformedSearchTypes>(
    UninformedSearchTypes.BREADTH,
  );
  const [goal, setGoal] = useState('');
  const [start, setStart] = useState('');
  const [nodes, setNodes] = useState({});
  const [graph, setGraph] = useState<any>(null);
  const [limit, setLimit] = useState(0);
  const [maxLimit, setMaxLimit] = useState(0);

  const httpClient = new AxiosHttpAdapter();
  const gateway = new UninformedSearchHttpGateway(httpClient);

  async function handleBreadthFirst() {
    return gateway.breadthFirst({
      goal,
      graph,
      nodes,
      start,
    });
  }

  async function handleDepthFirst() {
    return gateway.depthFirst({
      goal,
      graph,
      nodes,
      start,
    });
  }

  async function handleDepthLimited() {
    return gateway.depthLimited({
      goal,
      graph,
      limit,
      nodes,
      start,
    });
  }

  async function handleIterativeDeepening() {
    return gateway.iterativeDeepening({
      goal,
      graph,
      max_limit: maxLimit,
      nodes,
      start,
    });
  }

  async function handleBidirectional() {
    return gateway.bidirectional({
      goal,
      graph,
      nodes,
      start,
    });
  }

  async function handleSubmit() {
    const options = {
      [UninformedSearchTypes.BREADTH]: handleBreadthFirst,
      [UninformedSearchTypes.DEPTH]: handleDepthFirst,
      [UninformedSearchTypes.DEPTH_LIMITED]: handleDepthLimited,
      [UninformedSearchTypes.ITERATIVE]: handleIterativeDeepening,
      [UninformedSearchTypes.BIDIRECTIONAL]: handleBidirectional,
    };
    const response = await options[type]();
    setResponse(response?.path || null);
  }

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        handleSubmit();
      }}
    >
      <select
        onChange={(e) => setType(e.target.value as UninformedSearchTypes)}
      >
        <option value={UninformedSearchTypes.BREADTH}>Amplitude</option>
        <option value={UninformedSearchTypes.DEPTH}>Profundidade</option>
        <option value={UninformedSearchTypes.DEPTH_LIMITED}>
          Profundidade Limitada
        </option>
        <option value={UninformedSearchTypes.ITERATIVE}>
          Profundidade Iterativa
        </option>
        <option value={UninformedSearchTypes.BIDIRECTIONAL}>
          Bidirecional
        </option>
      </select>
      <div>
        Resultado:
        {response ? response.join(' -> ') : 'Nenhum resultado'}
      </div>
      <input
        type="text"
        placeholder="Start"
        onChange={(e) => setStart(e.target.value)}
      />
      <input
        type="text"
        placeholder="Goal"
        onChange={(e) => setGoal(e.target.value)}
      />
      <input
        type="text"
        placeholder="Graph"
        onChange={(e) => setGraph(e.target.value)}
      />
      <input
        type="text"
        placeholder="Nodes"
        onChange={(e) => setNodes(e.target.value)}
      />
      <input
        step="1"
        type="number"
        placeholder="Limit"
        onChange={(e) => setLimit(Number(e.target.value))}
      />
      <input
        type="number"
        step="1"
        placeholder="MaxLimit"
        onChange={(e) => setMaxLimit(Number(e.target.value))}
      />
      <button type="submit">Executar</button>
    </form>
  );
};
