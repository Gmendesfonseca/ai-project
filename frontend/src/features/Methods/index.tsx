'use client';

import { useState, useTransition } from 'react';
import { GraphVisualization } from './components/GraphVisualization';
import Form from './components/Form';

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
    <div
      style={{
        width: '100%',
        maxWidth: '1200px',
        margin: '0 auto',
      }}
    >
      <h1
        style={{
          textAlign: 'center',
        }}
      >
        Algoritmos de Busca
      </h1>
      <div
        style={{
          marginTop: '30px',
          display: 'flex',
          gap: '40px',
        }}
      >
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
      </div>
    </div>
  );
}
