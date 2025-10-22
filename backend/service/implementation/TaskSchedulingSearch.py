from ..base.InformedSearch import InformedSearch
from .TaskSchedulingNode import TaskSchedulingNode
from .TaskSchedulingData import SetupMatrix
from .TaskFamily import TaskFamily
from .TaskSchedulingHeuristics import TaskSchedulingHeuristics
from typing import List, Tuple, Optional
from collections import deque
import logging

class TaskSchedulingSearch(InformedSearch):
    def __init__(self):
        super().__init__()
        self.heuristics_handler = TaskSchedulingHeuristics()
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    # -------------------------------------------------------------------------
    # BREADTH-FIRST SEARCH
    # -------------------------------------------------------------------------
    def breadth_first_scheduling(self, tasks: List[int], setup_matrix: SetupMatrix) -> Tuple[List[int], float]:
        """
        Busca em largura para sequenciamento
        """
        
        start_node = self._get_initial_state(tasks)

        # Fila para busca em largura
        queue = deque([start_node])
        visited = set()
        
        while queue:
            current = queue.popleft()
            
            if current.is_goal_state():
                sequence = self._reconstruct_sequence(current, tasks)
                return sequence, current.v2
            
            state_key = (current.remaining_bitmask, current.last_task)
            if state_key in visited:
                continue
            visited.add(state_key)
            
            # Gerar sucessores
            successors = self._generate_successors_uniform(current, setup_matrix, tasks)
            
            for successor in successors:
                succ_key = (successor.remaining_bitmask, successor.last_task)
                if succ_key not in visited:
                    queue.append(successor)
        
        return [], float('inf')

    # -------------------------------------------------------------------------
    # DEPTH-FIRST SEARCH
    # -------------------------------------------------------------------------
    def depth_first_scheduling(self, tasks: List[int], setup_matrix: SetupMatrix) -> Tuple[List[int], float]:
        """
        Busca em profundidade para sequenciamento
        """
        start_node = self._get_initial_state(tasks)
        start_node.depth = 0
        
        # Pilha para busca em profundidade
        stack = deque([start_node])
        visited = set()
        
        while stack:
            current = stack.pop()
            
            if current.is_goal_state():
                sequence = self._reconstruct_sequence(current, tasks)
                return sequence, current.v2
            
            state_key = (current.remaining_bitmask, current.last_task)
            if state_key in visited:
                continue
            visited.add(state_key)
            
            # Gerar sucessores
            successors = self._generate_successors_uniform(current, setup_matrix, tasks)
            
            # Adicionar sucessores na ordem reversa para manter consistência com DFS
            for successor in reversed(successors):
                successor.depth = current.depth + 1
                succ_key = (successor.remaining_bitmask, successor.last_task)
                if succ_key not in visited:
                    stack.append(successor)
        
        return [], float('inf')

    # -------------------------------------------------------------------------
    # DEPTH-LIMITED SEARCH
    # -------------------------------------------------------------------------
    def depth_limited_scheduling(self, tasks: List[int], setup_matrix: SetupMatrix, depth_limit: int) -> Tuple[List[int], float]:
        """
        Busca em profundidade limitada para sequenciamento
        
        :param tasks: Lista de tarefas [1, 2, 3, ...]
        :param depth_limit: Limite máximo de profundidade
        :return: (sequencia_otima, custo_total) ou ([], inf) se não encontrar solução
        """
        start_node = self._get_initial_state(tasks)
        start_node.depth = 0
        
        # Pilha para busca em profundidade
        stack = deque([start_node])
        visited = set()
        
        while stack:
            current = stack.pop()
            
            if current.is_goal_state():
                sequence = self._reconstruct_sequence(current, tasks)
                return sequence, current.v2
            
            # Verifica se ainda não excedeu o limite de profundidade
            if current.depth < depth_limit:
                state_key = (current.remaining_bitmask, current.last_task)
                if state_key in visited:
                    continue
                visited.add(state_key)
                
                # Gerar sucessores
                successors = self._generate_successors_uniform(current, setup_matrix, tasks)
                
                # Adicionar sucessores na ordem reversa para manter consistência com DFS
                for successor in reversed(successors):
                    successor.depth = current.depth + 1
                    succ_key = (successor.remaining_bitmask, successor.last_task)
                    if succ_key not in visited:
                        stack.append(successor)
        
        return [], float('inf')

    # -------------------------------------------------------------------------
    # ITERATIVE DEEPENING SEARCH
    # -------------------------------------------------------------------------
    def iterative_deepening_scheduling(self, tasks: List[int], setup_matrix: SetupMatrix) -> Tuple[List[int], float]:
        """
        Busca em profundidade iterativa para sequenciamento

        :param tasks: Lista de tarefas [1, 2, 3, ...]
        :param setup_matrix: Matriz de configuração
        :return: (sequencia_otima, custo_total) ou ([], inf) se não encontrar solução
        """
        max_depth = len(tasks) + 1  # Profundidade máxima possível
        
        for depth_limit in range(1, max_depth + 1):
            self.logger.info(f"Tentando limite de profundidade: {depth_limit}")
            
            result = self.depth_limited_scheduling(
                tasks, setup_matrix, depth_limit
            )
            
            if result[0]:  # Se encontrou uma solução
                return result
        
        return [], float('inf')
    
    # -------------------------------------------------------------------------
    # BIDIRECTIONAL SEARCH
    # -------------------------------------------------------------------------
    def bidirectional_scheduling(self, tasks: List[int], setup_matrix: SetupMatrix) -> Tuple[List[int], float]:
        """
        Busca bidirecional para sequenciamento

        :param tasks: Lista de tarefas [1, 2, 3, ...]
        :param setup_matrix: Matriz de configuração
        :return: (sequencia_otima, custo_total) ou ([], inf) se não encontrar solução
        """
        from collections import deque
        
        # Inicialização dos estados e filas
        queues, visited = self._initialize_bidirectional_search(tasks)
        
        while queues['forward'] and queues['backward']:
            # Tenta expansão nas duas direções
            result = self._expand_bidirectional_forward(queues, visited, setup_matrix, tasks)
            if result:
                return result
                
            result = self._expand_bidirectional_backward(queues, visited, setup_matrix, tasks)
            if result:
                return result
        
        return [], float('inf')

    # -------------------------------------------------------------------------
    # UNIFORM COST SEARCH
    # -------------------------------------------------------------------------
    def uniform_cost_scheduling(self, tasks: List[int], setup_matrix: SetupMatrix) -> Tuple[List[int], float]:
        """Custo uniforme (Dijkstra) para sequenciamento"""
        start_node = self._get_initial_state(tasks)
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
    # GREEDY SEARCH
    # -------------------------------------------------------------------------
    def greedy_scheduling(self, tasks: List[int], setup_matrix: SetupMatrix, heuristic_type: str = "h1", families: Optional[TaskFamily] = None) -> Tuple[List[int], float]:
        """
        Busca gulosa para sequenciamento (usa apenas heurística)
        
        :param tasks: Lista de tarefas [1, 2, 3, ...]
        :param setup_matrix: Matriz de custos de setup
        :param heuristic_type: "h1", "h2", ou "h3"
        :param families: Para heurística h3
        :return: (sequencia_otima, custo_total) ou ([], inf) se não encontrar solução
        """
        # Similar ao A* mas ordena apenas por h-cost
        start_node = self._get_initial_state(tasks)
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
    # A* SEARCH
    # -------------------------------------------------------------------------
    def a_star_scheduling(self, tasks: List[int], setup_matrix: SetupMatrix,
                         heuristic_type: str = "h1",
                         families: Optional[TaskFamily] = None) -> Tuple[List[int], float]:
        """
        A* especializado para sequenciamento de tarefas

        :param tasks: Lista de tarefas [1, 2, 3, ...]
        :param setup_matrix: Matriz de custos de setup
        :param heuristic_type: "h1", "h2", ou "h3"
        :param families: Para heurística h3

        :return: (sequencia_otima, custo_total)
        """
        initial_bitmask = (1 << len(tasks)) - 1  # Todos os bits setados
        start_node = TaskSchedulingNode(initial_bitmask, 0, 0.0, 0.0)
        start_node.h_cost = self._calculate_heuristic(start_node, setup_matrix,
                                                     heuristic_type, families)
        start_node.v1 = start_node.v2 + start_node.h_cost

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
    # IDA* (iterative deepening A*)
    # -------------------------------------------------------------------------
    def ida_star_scheduling(self, tasks: List[int], setup_matrix: SetupMatrix,
                           heuristic_type: str = "h1",
                           families: Optional[TaskFamily] = None) -> Tuple[List[int], float]:
        """
        IDA* especializado para sequenciamento de tarefas
        
        :param tasks: Lista de tarefas [1, 2, 3, ...]
        :param setup_matrix: Matriz de custos de setup
        :param heuristic_type: "h1", "h2", ou "h3"
        :param families: Para heurística h3
        """
        # Estado inicial
        start_node = self._get_initial_state(tasks)
        start_node.h_cost = self._calculate_heuristic(start_node, setup_matrix,
                                                     heuristic_type, families)
        
        # Limite inicial é a heurística do estado inicial
        bound = start_node.h_cost
        
        while True:
            self.logger.info(f"IDA* com limite f: {bound}")
            
            result = self._ida_star_search(start_node, bound, setup_matrix, tasks,
                                         heuristic_type, families)
            
            if isinstance(result, tuple):  # Encontrou solução
                return result
            elif result == float('inf'):  # Não há solução
                return [], float('inf')
            else:  # Novo limite
                bound = result

    #-------------------------------------------------------------------------
    # INITIAL STATE
    #-------------------------------------------------------------------------
    def _get_initial_state(self, tasks: List[int]) -> Tuple[TaskSchedulingNode, int]:
        """
        Retorna o estado inicial para o sequenciamento de tarefas
        
        :param tasks: Lista de tarefas [1, 2, 3, ...]
        :return: (nó_inicial, bitmask_inicial)
        """
        initial_bitmask = (1 << len(tasks)) - 1  # Todos os bits setados
        start_node = TaskSchedulingNode(initial_bitmask, 0, 0.0, 0.0)
        return start_node, initial_bitmask

    # -------------------------------------------------------------------------
    # SUCCESSORS FOR GRAPH
    # -------------------------------------------------------------------------
    def _generate_successors(self, current: TaskSchedulingNode, setup_matrix: SetupMatrix,
                           tasks: List[int], heuristic_type: str,
                           families: Optional[TaskFamily] = None) -> List[TaskSchedulingNode]:
        """
        Gera todos os estados sucessores válidos
        
        :param current: Nó atual
        :param setup_matrix: Matriz de custos de setup
        :param tasks: Lista de todas as tarefas possíveis
        :param heuristic_type: Tipo de heurística ("h1", "h2", "h3")
        :param families: Instância de TaskFamily para h3
        :return: Lista de nós sucessores
        """
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
                new_node.v1 = new_g_cost + new_node.h_cost

                successors.append(new_node)

        return successors
 
    # -------------------------------------------------------------------------
    # SUCCESSORS FOR UNIFORM COST SEARCH
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

    # -------------------------------------------------------------------------
    # HELPER METHODS FOR BIDIRECTIONAL SEARCH
    # -------------------------------------------------------------------------
    def _initialize_bidirectional_search(self, tasks: List[int]):
        """
        Inicializa estruturas para busca bidirecional
        
        :param tasks: Lista de tarefas [1, 2, 3, ...]
        :return: (filas, visitados)
        """
        from collections import deque
        
        # Estado inicial: todas as tarefas restantes
        start_node, initial_bitmask = self._get_initial_state(tasks)

        # Estado final: nenhuma tarefa restante
        final_bitmask = 0
        goal_node = TaskSchedulingNode(final_bitmask, 0, 0.0, 0.0)
        
        queues = {
            'forward': deque([start_node]),
            'backward': deque([goal_node])
        }
        
        visited = {
            'forward': {(initial_bitmask, 0): start_node},
            'backward': {(final_bitmask, 0): goal_node}
        }
        
        return queues, visited

    def _expand_bidirectional_forward(self, queues: dict, visited: dict, setup_matrix: SetupMatrix, tasks: List[int]):
        """
        Expande busca na direção forward
        
        :param queues: Filas de busca
        :param visited: Nós visitados
        :param setup_matrix: Matriz de configuração
        :param tasks: Lista de tarefas
        :return: (sequencia, custo) se encontrar ponto de encontro, senão None
        """
        if not queues['forward']:
            return None
            
        current = queues['forward'].popleft()
        state_key = (current.remaining_bitmask, current.last_task)
        
        # Verifica se encontrou ponto de encontro
        if state_key in visited['backward']:
            meeting_node = visited['backward'][state_key]
            sequence = self._reconstruct_bidirectional_path(current, meeting_node, tasks)
            total_cost = current.v2 + meeting_node.v2
            return sequence, total_cost
        
        # Gerar e adicionar sucessores
        successors = self._generate_successors_uniform(current, setup_matrix, tasks)
        for successor in successors:
            succ_key = (successor.remaining_bitmask, successor.last_task)
            if succ_key not in visited['forward']:
                visited['forward'][succ_key] = successor
                queues['forward'].append(successor)
        
        return None

    def _expand_bidirectional_backward(self, queues: dict, visited: dict, setup_matrix: SetupMatrix, tasks: List[int]):
        """
        Expande busca na direção backward
        
        :param queues: Filas de busca
        :param visited: Nós visitados
        :param setup_matrix: Matriz de configuração
        :param tasks: Lista de tarefas
        :return: (sequencia, custo) se encontrar ponto de encontro, senão None
        """
        if not queues['backward']:
            return None
            
        current = queues['backward'].popleft()
        state_key = (current.remaining_bitmask, current.last_task)
        
        # Verifica se encontrou ponto de encontro
        if state_key in visited['forward']:
            meeting_node = visited['forward'][state_key]
            sequence = self._reconstruct_bidirectional_path(meeting_node, current, tasks)
            total_cost = meeting_node.v2 + current.v2
            return sequence, total_cost
        
        # Gerar e adicionar sucessores reversos
        successors = self._generate_successors_reverse(current, setup_matrix, tasks)
        for successor in successors:
            succ_key = (successor.remaining_bitmask, successor.last_task)
            if succ_key not in visited['backward']:
                visited['backward'][succ_key] = successor
                queues['backward'].append(successor)
        
        return None

    def _generate_successors_reverse(self, current: TaskSchedulingNode, setup_matrix: SetupMatrix, tasks: List[int]) -> List[TaskSchedulingNode]:
        """
        Gera sucessores para busca reversa (adiciona tarefas em vez de remover)
        
        :param current: Nó atual
        :param setup_matrix: Matriz de custos de setup
        :param tasks: Lista de todas as tarefas possíveis
        :return: Lista de nós sucessores
        """
        successors = []
        
        for i in range(len(tasks)):
            if not (current.remaining_bitmask & (1 << i)):  # Se tarefa i não está no bitmask
                task_id = tasks[i]
                
                # Adiciona tarefa ao bitmask
                new_remaining = current.remaining_bitmask | (1 << i)
                
                # Calcula custo de setup reverso
                setup_cost = setup_matrix.get_setup_cost(task_id, current.last_task)
                new_g_cost = current.v2 + setup_cost
                
                new_node = TaskSchedulingNode(new_remaining, task_id, new_g_cost, 0.0, current)
                new_node.v1 = new_g_cost
                
                successors.append(new_node)
        
        return successors
    
    def _reconstruct_bidirectional_path(self, forward_node: TaskSchedulingNode, backward_node: TaskSchedulingNode) -> List[int]:
        """
        Reconstrói caminho de busca bidirecional
        
        :param forward_node: Nó do lado forward no ponto de encontro
        :param backward_node: Nó do lado backward no ponto de encontro
        :return: Sequência completa de tarefas
        """
        # Caminho do início até o ponto de encontro
        forward_path = []
        current = forward_node
        while current and current.parent:
            if current.last_task != 0:
                forward_path.append(current.last_task)
            current = current.parent
        forward_path.reverse()
        
        # Caminho do ponto de encontro até o final
        backward_path = []
        current = backward_node
        while current and current.parent:
            if current.last_task != 0:
                backward_path.append(current.last_task)
            current = current.parent
        
        return forward_path + backward_path
    
    # -------------------------------------------------------------------------
    # HELPER METHOD FOR IDA*
    # -------------------------------------------------------------------------
    def _ida_star_search(self, node: TaskSchedulingNode, bound: float, setup_matrix: SetupMatrix, tasks: List[int], heuristic_type: str, families: Optional[TaskFamily]):
        """
        Busca recursiva para IDA*
        
        :param node: Nó atual
        :param bound: Limite atual de f-cost
        :param setup_matrix: Matriz de configuração
        :param tasks: Lista de tarefas
        :param heuristic_type: Tipo de heurística
        :param families: Instância de TaskFamily para h3
        :return: (sequencia, custo) se encontrar solução, senão novo limite
        """
        f_cost = node.v2 + node.h_cost
        
        if f_cost > bound:
            return f_cost
        
        if node.is_goal_state():
            sequence = self._reconstruct_sequence(node, tasks)
            return sequence, node.v2
        
        min_cost = float('inf')
        
        successors = self._generate_successors(node, setup_matrix, tasks,
                                             heuristic_type, families)
        
        for successor in successors:
            result = self._ida_star_search(successor, bound, setup_matrix, tasks,
                                         heuristic_type, families)
            
            if isinstance(result, tuple):  # Encontrou solução
                return result
            elif result < min_cost:
                min_cost = result
        
        return min_cost