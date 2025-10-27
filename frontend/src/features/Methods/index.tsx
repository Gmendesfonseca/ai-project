'use client';

import { useState, useTransition } from 'react';
import { GraphVisualization } from './components/GraphVisualization';
import Form from './components/Form';
import { PageComposition } from '@/components/Page';

export interface Graph {
  nodes: string[];
  edges: string[][];
}

const defaultGraph: Graph = {
  nodes: [],
  edges: [],
};

export default function MainPage() {
  const [loading, startTransition] = useTransition();
  const [response, setResponse] = useState<string[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [graph, setGraph] = useState<Graph>(defaultGraph);

  return (
    <PageComposition.Container>
      <PageComposition.Title>Algoritmos de Busca</PageComposition.Title>
      <PageComposition.Content>
        <Form
          graph={graph}
          loading={loading}
          setGraph={setGraph}
          setError={setError}
          setResponse={setResponse}
          startTransition={startTransition}
        />
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

        <div>
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
              Insira os dados do grafo e execute uma busca para ver os
              resultados
            </div>
          )}
        </div>
      </PageComposition.Content>
    </PageComposition.Container>
  );
}
