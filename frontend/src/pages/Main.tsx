'use client';

import { useState } from 'react';
import { useDependencies } from '../@core/infra/di/dependency-context';
import { UninformedSearchHttpGateway } from '../@core/infra/gateways/http/uninformed-search.gateway';

const UninformedSearchTypes = {
  BREADTH: 'BREADTH',
  DEPTH: 'DEPTH',
  DEPTH_LIMITED: 'DEPTH_LIMITED',
  Iterative: 'Iterative',
  bidirectional: 'bidirectional',
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

  const { httpClient } = useDependencies();
  const gateway = new UninformedSearchHttpGateway(httpClient);

  function handleBreadthFirst() {
    return gateway.breadthFirst({
      goal,
      graph,
      nodes,
      start,
    });
  }

  function handleDepthFirst() {
    return gateway.depthFirst({
      goal,
      graph,
      nodes,
      start,
    });
  }

  function handleDepthLimited() {
    return gateway.depthLimited({
      goal,
      graph,
      limit,
      nodes,
      start,
    });
  }

  function handleIterativeDeepening() {
    return gateway.iterativeDeepening({
      goal,
      graph,
      max_limit: maxLimit,
      nodes,
      start,
    });
  }

  function handleBidirectional() {
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
      [UninformedSearchTypes.Iterative]: handleIterativeDeepening,
      [UninformedSearchTypes.bidirectional]: handleBidirectional,
    };
    const response = await options[type]();
    setResponse(response);
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
        <option value={UninformedSearchTypes.BREADTH}>Breadth First</option>
        <option value={UninformedSearchTypes.DEPTH}>Depth First</option>
        <option value={UninformedSearchTypes.DEPTH_LIMITED}>
          Depth Limited
        </option>
        <option value={UninformedSearchTypes.Iterative}>
          Iterative Deepening
        </option>
        <option value={UninformedSearchTypes.bidirectional}>
          Bidirectional
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
