'use client';

import { useState, useTransition } from 'react';
import TaskSchedulingForm from './components/TaskSchedulingForm';
import TaskSequenceVisualization from './components/TaskSequenceVisualization';
import type { TaskSchedulingResponse } from '@core/domain/gateway/task-scheduling.gateway';
import { PageComposition } from '@/components/Page';

export interface TaskSchedulingData {
  tasks: number[];
  setupMatrix: Record<string, number>;
  families?: Record<number, string>;
}

const defaultData: TaskSchedulingData = {
  tasks: [],
  setupMatrix: {},
  families: {},
};

export default function TaskSchedulePage() {
  const [loading, startTransition] = useTransition();
  const [response, setResponse] = useState<TaskSchedulingResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<TaskSchedulingData>(defaultData);

  return (
    <PageComposition.Container>
      <PageComposition.Title>
        Sequenciamento de Tarefas com Setups
      </PageComposition.Title>
      <PageComposition.Content>
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
      </PageComposition.Content>
    </PageComposition.Container>
  );
}
