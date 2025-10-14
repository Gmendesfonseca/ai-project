import type { TaskSchedulingData } from '..';

interface ParsedTaskData {
  tasks: number[];
  setupMatrix: Record<string, number>;
  families?: Record<number, string>;
}

export function parseTaskFile(fileContent: string[]): TaskSchedulingData {
  const result: ParsedTaskData = {
    tasks: [],
    setupMatrix: {},
    families: undefined,
  };

  const taskSet = new Set<number>();

  for (const line of fileContent) {
    const trimmedLine = line.trim();

    // Skip empty lines
    if (!trimmedLine) continue;

    // Parse setup matrix entries in format "from,to:cost"
    const setupMatch = trimmedLine.match(/^(\d+),(\d+):(\d+(?:\.\d+)?)$/);
    if (setupMatch) {
      const [, from, to, cost] = setupMatch;
      const fromNum = parseInt(from);
      const toNum = parseInt(to);

      result.setupMatrix[`(${fromNum},${toNum})`] = parseFloat(cost);

      // Add tasks to set (exclude task 0 which represents initial state)
      if (fromNum !== 0) taskSet.add(fromNum);
      if (toNum !== 0) taskSet.add(toNum);
    }
  }

  // Convert task set to sorted array
  result.tasks = Array.from(taskSet).sort((a, b) => a - b);

  return result;
}
