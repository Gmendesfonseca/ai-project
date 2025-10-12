from backend.service.base.InformedSearch import InformedSearch
from .TaskSchedulingNode import TaskSchedulingNode
from .TaskSchedulingData import SetupMatrix, TaskFamily
from .TaskSchedulingHeuristics import TaskSchedulingHeuristics
from typing import List, Tuple, Optional

class TaskSchedulingSearch(InformedSearch):
    def __init__(self):
        super().__init__()
        self.heuristics_handler = TaskSchedulingHeuristics()
 
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    def a_star_scheduling(self, tasks: List[int], setup_matrix: SetupMatrix,
                         heuristic_type: str = "h1",
                         families: Optional[TaskFamily] = None) -> Tuple[List[int], float]:
        """
        A* especializado para sequenciamento de tarefas

        Args:
            tasks: Lista de tarefas [1, 2, 3, ...]
            setup_matrix: Matriz de custos de setup
            heuristic_type: "h1", "h2", ou "h3"
            families: Para heurística h3

        Returns:
            (sequencia_otima, custo_total)
        """
        # Estado inicial: todas as tarefas restantes, começando do nó 0
        initial_bitmask = (1 << len(tasks)) - 1  # Todos os bits setados
        start_node = TaskSchedulingNode(initial_bitmask, 0, 0.0, 0.0)
        start_node.h_cost = self._calculate_heuristic(start_node, setup_matrix,
                                                     heuristic_type, families)
        start_node.v1 = start_node.v2 + start_node.h_cost  # f = g + h

        # Lista de nós abertos (ordenada por f-cost)
        open_list = [start_node]
        closed_set = set()

        while open_list:
            current = open_list.pop(0)

            if current.is_goal_state():
                sequence = self._reconstruct_sequence(current, tasks)
                return sequence, current.v2  # Retorna sequência e custo g

            state_key = (current.remaining_bitmask, current.last_task)
            if state_key in closed_set:
                continue
            closed_set.add(state_key)

            # Gerar sucessores
            successors = self._generate_successors(current, setup_matrix, tasks,
                                                  heuristic_type, families)

            for successor in successors:
                succ_key = (successor.remaining_bitmask, successor.last_task)
                if succ_key not in closed_set:
                    self.insert_ordered(open_list, successor)

        return [], float('inf')  # Nenhuma solução encontrada
 
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    def greedy_scheduling(self, tasks: List[int], setup_matrix: SetupMatrix,
                         heuristic_type: str = "h1",
                         families: Optional[TaskFamily] = None) -> Tuple[List[int], float]:
        """Busca gulosa para sequenciamento (usa apenas heurística)"""
        # Similar ao A* mas ordena apenas por h-cost
        initial_bitmask = (1 << len(tasks)) - 1
        start_node = TaskSchedulingNode(initial_bitmask, 0, 0.0, 0.0)
        start_node.h_cost = self._calculate_heuristic(start_node, setup_matrix,
                                                     heuristic_type, families)
        start_node.v1 = start_node.h_cost  # f = h apenas (greedy)

        open_list = [start_node]
        closed_set = set()

        while open_list:
            current = open_list.pop(0)

            if current.is_goal_state():
                sequence = self._reconstruct_sequence(current, tasks)
                return sequence, current.v2

            state_key = (current.remaining_bitmask, current.last_task)
            if state_key in closed_set:
                continue
            closed_set.add(state_key)

            successors = self._generate_successors(current, setup_matrix, tasks,
                                                  heuristic_type, families)

            for successor in successors:
                successor.v1 = successor.h_cost  # Greedy: usa apenas h
                succ_key = (successor.remaining_bitmask, successor.last_task)
                if succ_key not in closed_set:
                    self.insert_ordered(open_list, successor)

        return [], float('inf')
 
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    def uniform_cost_scheduling(self, tasks: List[int],
                               setup_matrix: SetupMatrix) -> Tuple[List[int], float]:
        """Custo uniforme (Dijkstra) para sequenciamento"""
        initial_bitmask = (1 << len(tasks)) - 1
        start_node = TaskSchedulingNode(initial_bitmask, 0, 0.0, 0.0)
        start_node.v1 = 0.0  # Ordena por g-cost apenas

        open_list = [start_node]
        closed_set = set()

        while open_list:
            current = open_list.pop(0)

            if current.is_goal_state():
                sequence = self._reconstruct_sequence(current, tasks)
                return sequence, current.v2

            state_key = (current.remaining_bitmask, current.last_task)
            if state_key in closed_set:
                continue
            closed_set.add(state_key)

            successors = self._generate_successors_uniform(current, setup_matrix, tasks)

            for successor in successors:
                succ_key = (successor.remaining_bitmask, successor.last_task)
                if succ_key not in closed_set:
                    self.insert_ordered(open_list, successor)

        return [], float('inf')
    
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    def _generate_successors(self, current: TaskSchedulingNode, setup_matrix: SetupMatrix,
                           tasks: List[int], heuristic_type: str,
                           families: Optional[TaskFamily] = None) -> List[TaskSchedulingNode]:
        """Gera todos os estados sucessores válidos"""
        successors = []

        # Itera sobre cada posição de bit no bitmask
        for i in range(len(tasks)):
            if current.remaining_bitmask & (1 << i):  # Se tarefa i ainda não foi processada
                task_id = tasks[i]

                # Remove tarefa do bitmask
                new_remaining = current.remaining_bitmask & ~(1 << i)

                # Calcula custo de setup
                setup_cost = setup_matrix.get_setup_cost(current.last_task, task_id)
                new_g_cost = current.v2 + setup_cost  # v2 é o g_cost atual

                # Cria novo nó
                new_node = TaskSchedulingNode(new_remaining, task_id, new_g_cost, 0.0, current)
                new_node.h_cost = self._calculate_heuristic(new_node, setup_matrix,
                                                          heuristic_type, families)
                new_node.v1 = new_g_cost + new_node.h_cost  # f = g + h

                successors.append(new_node)

        return successors
 
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    def _generate_successors_uniform(self, current: TaskSchedulingNode,
                                   setup_matrix: SetupMatrix,
                                   tasks: List[int]) -> List[TaskSchedulingNode]:
        """
        Gera sucessores para busca de custo uniforme (sem heurística)

        :param current: Nó atual
        :param setup_matrix: Matriz de custos de setup
        :param tasks: Lista de todas as tarefas possíveis
        :return: Lista de nós sucessores
        """
        successors = []

        for i in range(len(tasks)):
            if current.remaining_bitmask & (1 << i):
                task_id = tasks[i]
                new_remaining = current.remaining_bitmask & ~(1 << i)
                setup_cost = setup_matrix.get_setup_cost(current.last_task, task_id)
                new_g_cost = current.v2 + setup_cost

                new_node = TaskSchedulingNode(new_remaining, task_id, new_g_cost, 0.0, current)
                new_node.v1 = new_g_cost  # Para ordenação por g-cost apenas

                successors.append(new_node)

        return successors
 
    # -------------------------------------------------------------------------
    # CÁLCULO DA HEURÍSTICA
    # -------------------------------------------------------------------------
    def _calculate_heuristic(self, node: TaskSchedulingNode, setup_matrix: SetupMatrix,
                           heuristic_type: str, families: Optional[TaskFamily] = None) -> float:
        """
        Calcula heurística baseada no tipo especificado
        
        :param node: Nó atual
        :param setup_matrix: Matriz de custos de setup
        :param heuristic_type: "h1", "h2", ou "h3"
        :param families: Instância de TaskFamily para h3
        :return: Valor da heurística
        """
        if heuristic_type == "h1":
            return self.heuristics_handler.h1_minimum_outgoing_edges(node, setup_matrix)
        elif heuristic_type == "h2":
            return self.heuristics_handler.h2_mst_symmetric(node, setup_matrix)
        elif heuristic_type == "h3" and families:
            return self.heuristics_handler.h3_product_families(node, setup_matrix, families)
        else:
            return 0.0  # Fallback para custo uniforme
 
    # -------------------------------------------------------------------------
    # RECONSTRUÇÃO DA SEQUÊNCIA
    # -------------------------------------------------------------------------
    def _reconstruct_sequence(self, goal_node: TaskSchedulingNode,
                             tasks: List[int]) -> List[int]:
        """
        Reconstrói a sequência de tarefas a partir do nó objetivo
        
        :param goal_node: Nó objetivo 
        :param tasks: Lista de todas as tarefas possíveis
        :return: Sequência de tarefas agendadas
        """
        sequence = []
        current = goal_node

        # Reconstrói caminho do objetivo para o início
        while current and current.parent:
            if current.last_task != 0:  # Ignora nó inicial fictício
                sequence.append(current.last_task)
            current = current.parent

        sequence.reverse()
        return sequence