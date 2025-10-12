from typing import List
from .TaskSchedulingNode import TaskSchedulingNode
from .TaskSchedulingData import SetupMatrix
from .TaskFamily import TaskFamily
import heapq
  
class TaskSchedulingHeuristics:
    @staticmethod
    def h1_minimum_outgoing_edges(self, state: TaskSchedulingNode) -> float:
      """
      Implementa heurística H1: soma dos menores custos de saída
      para cada tarefa restante, menos o maior (uma tarefa não terá saída)
      """
      if state.remaining_bitmask == 0:
          return 0.0

      remaining_tasks = self._bitmask_to_tasks(state.remaining_bitmask)

      # Custo mínimo para sair da última tarefa processada
      min_cost_from_last = min(
          self.setup_matrix.get_cost(state.last_task, task)
          for task in remaining_tasks
      )

      # Custo mínimo de saída para cada tarefa restante
      outgoing_costs = []
      for from_task in remaining_tasks:
          if len(remaining_tasks) > 1:  # Se não é a última tarefa
              min_out = min(
                  self.setup_matrix.get_cost(from_task, to_task)
                  for to_task in remaining_tasks if to_task != from_task
              )
              outgoing_costs.append(min_out)

      # Soma todos menos o maior (uma tarefa será a última)
      total_outgoing = sum(outgoing_costs)
      if outgoing_costs:
          total_outgoing -= max(outgoing_costs)

      return min_cost_from_last + total_outgoing
    
    @staticmethod
    def h2_mst_symmetric(self, state: TaskSchedulingNode) -> float:
      """
      Para casos onde s_ij ≈ s_ji, usa árvore geradora mínima
      """
      if state.remaining_bitmask == 0:
          return 0.0

      remaining_tasks = self._bitmask_to_tasks(state.remaining_bitmask)

      # Custo para conectar última tarefa ao componente
      min_connection = min(
          self.setup_matrix.get_cost(state.last_task, task)
          for task in remaining_tasks
      )

      # MST sobre tarefas restantes
      mst_cost = self._compute_mst(remaining_tasks)

      return min_connection + mst_cost
    
    @staticmethod
    def h3_product_families(self, state: TaskSchedulingNode, families: TaskFamily) -> float:
      """
      Quando setups intrafamília são zero, conta trocas de família necessárias
      """
      if state.remaining_bitmask == 0:
          return 0.0

      remaining_tasks = self._bitmask_to_tasks(state.remaining_bitmask)

      # Conta famílias diferentes restantes
      remaining_families = {
          families.families[task] for task in remaining_tasks
          if task in families.families
      }

      # Se última tarefa tem família conhecida
      last_family = families.families.get(state.last_task)
      if last_family and last_family in remaining_families:
          remaining_families.remove(last_family)

      # Número mínimo de trocas de família × menor custo inter-família
      family_switches = len(remaining_families)
      if family_switches > 0:
          min_interfamily_cost = self._get_min_interfamily_cost(families)
          return family_switches * min_interfamily_cost

      return 0.0
  

    @staticmethod
    def _compute_mst(tasks: List[int], setup_matrix: SetupMatrix) -> float:
        """Computa MST usando algoritmo de Prim adaptado"""
        if len(tasks) <= 1:
            return 0.0

        visited = set()
        min_heap = [(0, tasks[0])]
        mst_cost = 0.0

        while min_heap and len(visited) < len(tasks):
            cost, current = heapq.heappop(min_heap)

            if current in visited:
                continue

            visited.add(current)
            mst_cost += cost

            # Adiciona arestas para nós não visitados
            for next_task in tasks:
                if next_task not in visited:
                    edge_cost = min(
                        setup_matrix.get_setup_cost(current, next_task),
                        setup_matrix.get_setup_cost(next_task, current)
                    )
                    heapq.heappush(min_heap, (edge_cost, next_task))

        return mst_cost
      
    @staticmethod
    def _bitmask_to_tasks(bitmask: int) -> List[int]:
        """
        Converte bitmask para lista de IDs de tarefas
        
        :param bitmask: Bitmask representando tarefas restantes
        :return: Lista de IDs de tarefas restantes
        """
        tasks = []
        index = 0
        while bitmask > 0:
            if bitmask & 1:
                tasks.append(index + 1)  # Supondo IDs começam em 1
            bitmask >>= 1
            index += 1
        return tasks
