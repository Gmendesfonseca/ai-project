import type { Graph } from '..';

export function parseFileContent(fileContent: string[]): Graph {
  const pairNodes = fileContent.map((line) => line.split(','));
  const parsedNodes = Array.from(
    new Set(pairNodes.flat().map((node) => node.trim())),
  ).filter((node) => node !== '');
  const parsedGraph = pairNodes.map((pair) => pair.map((node) => node.trim()));
  return { nodes: parsedNodes, edges: parsedGraph };
}
