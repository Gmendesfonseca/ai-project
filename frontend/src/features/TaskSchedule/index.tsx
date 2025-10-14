'use client';

import { useState, useTransition } from 'react';
import TaskSchedulingForm from './components/TaskSchedulingForm';
import TaskSequenceVisualization from './components/TaskSequenceVisualization';
import type { TaskSchedulingResponse } from '@core/domain/gateway/task-scheduling.gateway';

export interface TaskSchedulingData {
  tasks: number[];
  setupMatrix: Record<string, number>;
  families?: Record<number, string>;
}

const defaultData: TaskSchedulingData = {
  tasks: [],
  setupMatrix: {},
};

export default function TaskSchedulePage() {
  const [loading, startTransition] = useTransition();
  const [response, setResponse] = useState<TaskSchedulingResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<TaskSchedulingData>(defaultData);

  return (
    <div
      style={{
        width: '100%',
        maxWidth: '1200px',
        margin: '0 auto',
      }}
    >
      <div style={{ textAlign: 'center', marginBottom: '20px' }}>
        <h1>Sequenciamento de Tarefas com Setups</h1>
        <div
          style={{
            display: 'flex',
            gap: '20px',
            justifyContent: 'center',
            marginTop: '10px',
          }}
        >
          <a
            href="/"
            style={{
              padding: '10px 20px',
              backgroundColor: '#007bff',
              color: 'white',
              textDecoration: 'none',
              borderRadius: '5px',
            }}
          >
            Algoritmos de Busca
          </a>
          <a
            href="/task-scheduling"
            style={{
              padding: '10px 20px',
              backgroundColor: '#28a745',
              color: 'white',
              textDecoration: 'none',
              borderRadius: '5px',
            }}
          >
            Task Scheduling
          </a>
        </div>
      </div>
      <div
        style={{
          marginTop: '30px',
          display: 'flex',
          gap: '40px',
        }}
      >
        <TaskSchedulingForm
          data={data}
          loading={loading}
          setData={setData}
          setError={setError}
          setResponse={setResponse}
          startTransition={startTransition}
        />
        <TaskSequenceVisualization
          response={response}
          error={error}
          data={data}
        />
      </div>
    </div>
  );
}
