import type { TaskSchedulingData } from '..';

export function formatTaskDataForDisplay(data: TaskSchedulingData): {
  tasksString: string;
  setupMatrixString: string;
  familiesString: string;
} {
  // Format tasks as comma-separated string
  const tasksString = data.tasks.join(',');

  // Format setup matrix
  const setupMatrixString = Object.entries(data.setupMatrix)
    .map(([key, value]) => `${key}: ${value}`)
    .join('\n');

  // Format families
  const familiesString = data.families
    ? Object.entries(data.families)
        .map(([task, family]) => `${task}: ${family}`)
        .join('\n')
    : '';

  return {
    tasksString,
    setupMatrixString,
    familiesString,
  };
}

export function validateTaskData(data: TaskSchedulingData): string[] {
  const errors: string[] = [];

  // Validate tasks
  if (!data.tasks || data.tasks.length === 0) {
    errors.push('Nenhuma tarefa foi definida');
  }

  // Validate setup matrix
  if (!data.setupMatrix || Object.keys(data.setupMatrix).length === 0) {
    errors.push('Matriz de setup vazia');
  }

  // Check if setup matrix covers all necessary task transitions
  if (data.tasks.length > 1) {
    let missingTransitions = 0;

    for (const task1 of data.tasks) {
      for (const task2 of data.tasks) {
        if (task1 !== task2) {
          const key1 = `(${task1},${task2})`;

          if (!data.setupMatrix[key1] && task1 !== 0) {
            missingTransitions++;
          }
        }
      }
    }

    // Check initial setups (from task 0 to all tasks)
    for (const task of data.tasks) {
      const initialKey = `(0,${task})`;
      if (!data.setupMatrix[initialKey]) {
        missingTransitions++;
      }
    }

    if (missingTransitions > 0) {
      errors.push(`Faltam ${missingTransitions} transições na matriz de setup`);
    }
  }

  // Validate families if provided
  if (data.families) {
    const familyTasks = new Set(Object.keys(data.families).map(Number));
    const undefinedTasks = data.tasks.filter((task) => !familyTasks.has(task));

    if (undefinedTasks.length > 0) {
      errors.push(`Tarefas sem família definida: ${undefinedTasks.join(', ')}`);
    }
  }

  return errors;
}
