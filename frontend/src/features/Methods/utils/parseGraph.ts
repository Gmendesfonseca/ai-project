import type { Graph } from '..';

export function parseGraph({ nodes, edges }: Graph): string[][] {
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
