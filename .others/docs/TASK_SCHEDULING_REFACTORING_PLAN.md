# Plano de Refatoração: Sequenciamento de Tarefas com Setups

## Visão Geral da Refatoração

Estender o sistema atual de busca em grafos para incluir uma implementação específica do problema de **Sequenciamento de Tarefas em Linhas de Produção com Setups**, modelado como um ATSP (Asymmetric Traveling Salesman Problem). Esta extensão será integrada ao sistema existente mantendo a arquitetura atual.

---

## 1. Análise do Estado Atual vs. Estado Desejado

### Estado Atual (Sistema Existente)

- **Backend**: Flask com classes `UninformedSearch` e `InformedSearch`
- **Nós**: Classes `Node` e `NodeP` para busca tradicional
- **Entrada**: Grafos com adjacências e heurísticas pré-definidas
- **Frontend**: React/TypeScript com arquitetura limpa (gateways/adapters)
- **Algoritmos**: BFS, DFS, A*, Greedy, IDA*, etc. para grafos genéricos

### Estado Desejado (Extensão Específica)

- **Entrada**: Conjunto de tarefas J={1,2,...,n} e matriz de custos de setup s\_{ij}
- **Objetivo**: Encontrar sequência que minimize custo total de setups
- **Representação**: Estados como (bitmask_restantes, última_tarefa)
- **Heurística**: H1 (mínimos de saída), H2 (MST), H3 (famílias de produtos)
- **Integração**: Nova feature no sistema existente sem quebrar funcionalidades

---

## 2. Estruturas de Dados Necessárias

### 2.1 Extensão da Classe Node: TaskSchedulingNode

```python
# Herda de NodeP para manter compatibilidade com InformedSearch
class TaskSchedulingNode(NodeP):
    def __init__(self, remaining_bitmask: int, last_task: int,
                 g_cost: float, h_cost: float, parent=None):
        # v1 = f_cost (para ordenação na priority queue)
        # v2 = g_cost (custo acumulado)
        super().__init__(parent, (remaining_bitmask, last_task), g_cost + h_cost, None, None, g_cost)
        self.remaining_bitmask = remaining_bitmask
        self.last_task = last_task
        self.h_cost = h_cost
        self.sequence = []  # Será populada durante reconstrução do caminho

    def is_goal_state(self) -> bool:
        return self.remaining_bitmask == 0

    def __eq__(self, other):
        if not isinstance(other, TaskSchedulingNode):
            return False
        return (self.remaining_bitmask == other.remaining_bitmask and
                self.last_task == other.last_task)

    def __hash__(self):
        return hash((self.remaining_bitmask, self.last_task))
```

### 2.2 Classe SetupMatrix para Gerenciar Custos

```python
class SetupMatrix:
    def __init__(self, tasks: List[int], setup_costs: Dict[str, float]):
        """
        Args:
            tasks: Lista de IDs das tarefas [1, 2, 3, ...]
            setup_costs: Dicionário com chaves "(i,j)" e valores de custo
        """
        self.tasks = tasks
        self.setup_costs = {}
        self.n_tasks = len(tasks)

        # Converte chaves string para tuplas inteiras
        for key, cost in setup_costs.items():
            i, j = map(int, key.strip("()").split(","))
            self.setup_costs[(i, j)] = cost

    def get_setup_cost(self, from_task: int, to_task: int) -> float:
        return self.setup_costs.get((from_task, to_task), float('inf'))

    def validate_matrix(self) -> bool:
        """Verifica se a matriz está completa para todas as tarefas"""
        for i in [0] + self.tasks:  # Inclui nó inicial 0
            for j in self.tasks:
                if i != j and (i, j) not in self.setup_costs:
                    return False
        return True
```

### 2.3 Classe TaskFamily (Para Heurística H3)

```python
class TaskFamily:
    def __init__(self, family_assignments: Dict[int, str] = None):
        self.families = family_assignments or {}

    def same_family(self, task1: int, task2: int) -> bool:
        if not self.families:
            return False
        return (task1 in self.families and task2 in self.families and
                self.families[task1] == self.families[task2])

    def get_min_interfamily_cost(self, setup_matrix: SetupMatrix) -> float:
        """Retorna o menor custo entre tarefas de famílias diferentes"""
        if not self.families:
            return 0.0

        min_cost = float('inf')
        for i in setup_matrix.tasks:
            for j in setup_matrix.tasks:
                if i != j and not self.same_family(i, j):
                    cost = setup_matrix.get_setup_cost(i, j)
                    if cost < min_cost:
                        min_cost = cost
        return min_cost if min_cost != float('inf') else 0.0
```

---

## 3. Plano de Refatoração Detalhado

### Fase 1: Extensão dos Módulos Existentes (2-3 dias)

#### 3.1 Criar `TaskSchedulingNode.py`

```python
# Herda de NodeP mantendo compatibilidade com sistema existente
from .NodeP import NodeP

class TaskSchedulingNode(NodeP):
    def __init__(self, remaining_bitmask: int, last_task: int,
                 g_cost: float, h_cost: float, parent=None):
        super().__init__(parent, (remaining_bitmask, last_task),
                        g_cost + h_cost, None, None, g_cost)
        self.remaining_bitmask = remaining_bitmask
        self.last_task = last_task
        self.h_cost = h_cost

    def is_goal_state(self) -> bool:
        return self.remaining_bitmask == 0

    def get_remaining_tasks(self, task_list: List[int]) -> List[int]:
        """Converte bitmask para lista de tarefas restantes"""
        remaining = []
        for i, task in enumerate(task_list):
            if self.remaining_bitmask & (1 << i):
                remaining.append(task)
        return remaining

    def __eq__(self, other):
        return (isinstance(other, TaskSchedulingNode) and
                self.remaining_bitmask == other.remaining_bitmask and
                self.last_task == other.last_task)

    def __hash__(self):
        return hash((self.remaining_bitmask, self.last_task))
```

#### 3.2 Criar `TaskSchedulingData.py`

```python
# Consolidação das estruturas de dados para o problema
from typing import Dict, List, Tuple
import json

class SetupMatrix:
    def __init__(self, tasks: List[int], setup_costs: Dict[str, float]):
        self.tasks = tasks
        self.setup_costs = {}
        self.n_tasks = len(tasks)

        # Processar custos de entrada no formato "(i,j)": cost
        for key, cost in setup_costs.items():
            i, j = map(int, key.strip("()").split(","))
            self.setup_costs[(i, j)] = cost

    def get_setup_cost(self, from_task: int, to_task: int) -> float:
        return self.setup_costs.get((from_task, to_task), float('inf'))

    def validate_matrix(self) -> bool:
        # Verificar se todos os custos necessários estão presentes
        for i in [0] + self.tasks:
            for j in self.tasks:
                if i != j and (i, j) not in self.setup_costs:
                    return False
        return True

class TaskFamily:
    def __init__(self, family_assignments: Dict[int, str] = None):
        self.families = family_assignments or {}

    def same_family(self, task1: int, task2: int) -> bool:
        if not self.families:
            return False
        return (task1 in self.families and task2 in self.families and
                self.families[task1] == self.families[task2])
```

#### 3.3 Criar `TaskSchedulingHeuristics.py`

```python
from typing import List, Dict, Set
from .TaskSchedulingNode import TaskSchedulingNode
from .TaskSchedulingData import SetupMatrix, TaskFamily
import heapq

class TaskSchedulingHeuristics:
    @staticmethod
    def h1_minimum_outgoing_edges(node: TaskSchedulingNode, setup_matrix: SetupMatrix) -> float:
        """Heurística H1: Soma dos mínimos de saída menos o maior"""
        if node.remaining_bitmask == 0:
            return 0.0

        remaining_tasks = node.get_remaining_tasks(setup_matrix.tasks)

        # Custo mínimo para sair da última tarefa
        min_from_current = min(setup_matrix.get_setup_cost(node.last_task, task)
                              for task in remaining_tasks)

        # Custos mínimos de saída para cada tarefa restante
        outgoing_costs = []
        for task in remaining_tasks:
            others = [t for t in remaining_tasks if t != task]
            if others:  # Se não é a última tarefa
                min_out = min(setup_matrix.get_setup_cost(task, other)
                             for other in others)
                outgoing_costs.append(min_out)

        # Soma todos menos o maior (última tarefa não tem saída)
        total_outgoing = sum(outgoing_costs)
        if outgoing_costs:
            total_outgoing -= max(outgoing_costs)

        return min_from_current + total_outgoing

    @staticmethod
    def h2_mst_symmetric(node: TaskSchedulingNode, setup_matrix: SetupMatrix) -> float:
        """Heurística H2: MST para casos aproximadamente simétricos"""
        if node.remaining_bitmask == 0:
            return 0.0

        remaining_tasks = node.get_remaining_tasks(setup_matrix.tasks)

        # Custo mínimo para conectar à última tarefa
        min_connection = min(setup_matrix.get_setup_cost(node.last_task, task)
                            for task in remaining_tasks)

        # MST sobre tarefas restantes
        mst_cost = TaskSchedulingHeuristics._compute_mst(remaining_tasks, setup_matrix)

        return min_connection + mst_cost

    @staticmethod
    def h3_product_families(node: TaskSchedulingNode, setup_matrix: SetupMatrix,
                           families: TaskFamily) -> float:
        """Heurística H3: Baseada em famílias de produtos"""
        if node.remaining_bitmask == 0 or not families.families:
            return 0.0

        remaining_tasks = node.get_remaining_tasks(setup_matrix.tasks)

        # Identifica famílias restantes
        remaining_families = set()
        for task in remaining_tasks:
            if task in families.families:
                remaining_families.add(families.families[task])

        # Remove família atual se existe
        current_family = families.families.get(node.last_task)
        if current_family in remaining_families:
            remaining_families.remove(current_family)

        # Estima custo por trocas de família
        if remaining_families:
            min_interfamily = families.get_min_interfamily_cost(setup_matrix)
            return len(remaining_families) * min_interfamily

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
```

### Fase 2: Extensão da Classe InformedSearch (3-4 dias)

#### 3.4 Criar `TaskSchedulingSearch.py`

```python
from .InformedSearch import InformedSearch
from .TaskSchedulingNode import TaskSchedulingNode
from .TaskSchedulingData import SetupMatrix, TaskFamily
from .TaskSchedulingHeuristics import TaskSchedulingHeuristics
from typing import List, Tuple, Optional, Dict

class TaskSchedulingSearch(InformedSearch):
    def __init__(self):
        super().__init__()
        self.heuristics_handler = TaskSchedulingHeuristics()

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
```

#### 3.5 Implementar Métodos Auxiliares na TaskSchedulingSearch

```python
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

    def _generate_successors_uniform(self, current: TaskSchedulingNode,
                                   setup_matrix: SetupMatrix,
                                   tasks: List[int]) -> List[TaskSchedulingNode]:
        """Gera sucessores para busca de custo uniforme (sem heurística)"""
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

    def _calculate_heuristic(self, node: TaskSchedulingNode, setup_matrix: SetupMatrix,
                           heuristic_type: str, families: Optional[TaskFamily] = None) -> float:
        """Calcula heurística baseada no tipo especificado"""
        if heuristic_type == "h1":
            return self.heuristics_handler.h1_minimum_outgoing_edges(node, setup_matrix)
        elif heuristic_type == "h2":
            return self.heuristics_handler.h2_mst_symmetric(node, setup_matrix)
        elif heuristic_type == "h3" and families:
            return self.heuristics_handler.h3_product_families(node, setup_matrix, families)
        else:
            return 0.0  # Fallback para custo uniforme

    def _reconstruct_sequence(self, goal_node: TaskSchedulingNode,
                             tasks: List[int]) -> List[int]:
        """Reconstrói a sequência de tarefas a partir do nó objetivo"""
        sequence = []
        current = goal_node

        # Reconstrói caminho do objetivo para o início
        while current and current.parent:
            if current.last_task != 0:  # Ignora nó inicial fictício
                sequence.append(current.last_task)
            current = current.parent

        sequence.reverse()
        return sequence
```

### Fase 3: Implementação das Heurísticas (2-3 dias)

#### 3.6 H1: Mínimos de Saída (ATSP)

```python
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
```

#### 3.7 H2: MST para Setups Simétricos

```python
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
```

#### 3.8 H3: Famílias de Produtos

```python
def h3_product_families(self, state: TaskSchedulingNode, families: TaskFamily) -> float:
    """
    Quando setups intrafamília são zero, conta trocas de família necessárias
    """
    if state.remaining_bitmask == 0:
        return 0.0

    remaining_tasks = self._bitmask_to_tasks(state.remaining_bitmask)

    # Conta famílias diferentes restantes
    remaining_families = set(
        families.families[task] for task in remaining_tasks
        if task in families.families
    )

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
```

### Fase 4: Integração com API e Frontend Existentes (2 dias)

#### 3.9 Novos Endpoints em `app.py`

```python
# Importações adicionais no topo do arquivo
from service.TaskSchedulingSearch import TaskSchedulingSearch
from service.TaskSchedulingData import SetupMatrix, TaskFamily

@app.route('/scheduling/task-sequence/a_star', methods=['POST'])
def task_sequence_a_star() -> Any:
    """A* para sequenciamento de tarefas com setups"""
    data = get_json_data()
    try:
        search = TaskSchedulingSearch()

        tasks = data['tasks']
        setup_costs = data['setup_matrix']
        heuristic = data.get('heuristic', 'h1')
        family_data = data.get('families')

        # Criar estruturas de dados
        setup_matrix = SetupMatrix(tasks, setup_costs)
        if not setup_matrix.validate_matrix():
            abort(400, description="Matriz de setup incompleta")

        families = TaskFamily(family_data) if family_data else None

        # Executar algoritmo
        sequence, cost = search.a_star_scheduling(tasks, setup_matrix, heuristic, families)

        # Calcular detalhes dos setups
        setup_details = []
        if sequence:
            prev = 0  # Nó inicial
            for task in sequence:
                setup_cost = setup_matrix.get_setup_cost(prev, task)
                setup_details.append({
                    "from": prev,
                    "to": task,
                    "cost": setup_cost
                })
                prev = task

        return jsonify({
            'sequence': sequence,
            'total_cost': cost,
            'setup_details': setup_details,
            'algorithm': 'A*',
            'heuristic': heuristic
        })

    except KeyError as e:
        logging.error(f"Missing key: {e}")
        abort(400, description=f"Missing key: {e}")
    except Exception as e:
        logging.error(f"Error in A* task scheduling: {e}")
        abort(500, description=str(e))

@app.route('/scheduling/task-sequence/greedy', methods=['POST'])
def task_sequence_greedy() -> Any:
    """Busca gulosa para sequenciamento de tarefas"""
    data = get_json_data()
    try:
        search = TaskSchedulingSearch()

        tasks = data['tasks']
        setup_costs = data['setup_matrix']
        heuristic = data.get('heuristic', 'h1')
        family_data = data.get('families')

        setup_matrix = SetupMatrix(tasks, setup_costs)
        if not setup_matrix.validate_matrix():
            abort(400, description="Matriz de setup incompleta")

        families = TaskFamily(family_data) if family_data else None
        sequence, cost = search.greedy_scheduling(tasks, setup_matrix, heuristic, families)

        setup_details = []
        if sequence:
            prev = 0
            for task in sequence:
                setup_cost = setup_matrix.get_setup_cost(prev, task)
                setup_details.append({"from": prev, "to": task, "cost": setup_cost})
                prev = task

        return jsonify({
            'sequence': sequence,
            'total_cost': cost,
            'setup_details': setup_details,
            'algorithm': 'Greedy',
            'heuristic': heuristic
        })

    except KeyError as e:
        logging.error(f"Missing key: {e}")
        abort(400, description=f"Missing key: {e}")
    except Exception as e:
        logging.error(f"Error in greedy task scheduling: {e}")
        abort(500, description=str(e))

@app.route('/scheduling/task-sequence/uniform_cost', methods=['POST'])
def task_sequence_uniform_cost() -> Any:
    """Custo uniforme para sequenciamento de tarefas"""
    data = get_json_data()
    try:
        search = TaskSchedulingSearch()

        tasks = data['tasks']
        setup_costs = data['setup_matrix']

        setup_matrix = SetupMatrix(tasks, setup_costs)
        if not setup_matrix.validate_matrix():
            abort(400, description="Matriz de setup incompleta")

        sequence, cost = search.uniform_cost_scheduling(tasks, setup_matrix)

        setup_details = []
        if sequence:
            prev = 0
            for task in sequence:
                setup_cost = setup_matrix.get_setup_cost(prev, task)
                setup_details.append({"from": prev, "to": task, "cost": setup_cost})
                prev = task

        return jsonify({
            'sequence': sequence,
            'total_cost': cost,
            'setup_details': setup_details,
            'algorithm': 'Uniform Cost'
        })

    except KeyError as e:
        logging.error(f"Missing key: {e}")
        abort(400, description=f"Missing key: {e}")
    except Exception as e:
        logging.error(f"Error in uniform cost task scheduling: {e}")
        abort(500, description=str(e))
```

#### 3.10 Integração com Frontend Existente

##### 3.10.1 Extensão dos Tipos e Constantes

```typescript
// Em src/features/Methods/utils/constants.ts - Adicionar novos tipos
export const TaskSchedulingTypes = {
  TASK_A_STAR: 'TASK_A_STAR',
  TASK_GREEDY: 'TASK_GREEDY',
  TASK_UNIFORM_COST: 'TASK_UNIFORM_COST',
} as const;

export type TaskSchedulingTypes =
  (typeof TaskSchedulingTypes)[keyof typeof TaskSchedulingTypes];

// Adicionar ao methodOptions existente
export const taskSchedulingOptions: {
  value: TaskSchedulingTypes;
  label: string;
}[] = [
  {
    value: TaskSchedulingTypes.TASK_A_STAR,
    label: 'A* - Sequenciamento de Tarefas',
  },
  {
    value: TaskSchedulingTypes.TASK_GREEDY,
    label: 'Greedy - Sequenciamento de Tarefas',
  },
  {
    value: TaskSchedulingTypes.TASK_UNIFORM_COST,
    label: 'Custo Uniforme - Sequenciamento de Tarefas',
  },
];

export const heuristicOptions = [
  { value: 'h1', label: 'H1 - Mínimos de Saída' },
  { value: 'h2', label: 'H2 - MST Simétrico' },
  { value: 'h3', label: 'H3 - Famílias de Produtos' },
];
```

##### 3.10.2 Extensão dos Gateways

```typescript
// Em src/core/domain/gateway/task-scheduling.gateway.ts - NOVO ARQUIVO
export interface TaskSchedulingInput {
  tasks: number[];
  setup_matrix: Record<string, number>;
  heuristic?: 'h1' | 'h2' | 'h3';
  families?: Record<number, string>;
}

export interface TaskSchedulingResponse {
  sequence: number[];
  total_cost: number;
  setup_details: Array<{
    from: number;
    to: number;
    cost: number;
  }>;
  algorithm: string;
  heuristic?: string;
}

export interface TaskSchedulingGateway {
  aStar(payload: TaskSchedulingInput): Promise<TaskSchedulingResponse | null>;
  greedy(payload: TaskSchedulingInput): Promise<TaskSchedulingResponse | null>;
  uniformCost(
    payload: Omit<TaskSchedulingInput, 'heuristic' | 'families'>,
  ): Promise<TaskSchedulingResponse | null>;
}
```

##### 3.10.3 Implementação HTTP Gateway

```typescript
// Em src/core/infra/gateways/http/task-scheduling.gateway.ts - NOVO ARQUIVO
import type { HttpClientPort } from '@core/domain/ports/http-client.port';
import type {
  TaskSchedulingGateway,
  TaskSchedulingInput,
  TaskSchedulingResponse,
} from '@core/domain/gateway/task-scheduling.gateway';

export class TaskSchedulingHttpGateway implements TaskSchedulingGateway {
  constructor(private readonly httpClient: HttpClientPort) {}

  async aStar(
    payload: TaskSchedulingInput,
  ): Promise<TaskSchedulingResponse | null> {
    const response = await this.httpClient.post<TaskSchedulingResponse>(
      '/scheduling/task-sequence/a_star',
      payload,
    );
    return response.data || null;
  }

  async greedy(
    payload: TaskSchedulingInput,
  ): Promise<TaskSchedulingResponse | null> {
    const response = await this.httpClient.post<TaskSchedulingResponse>(
      '/scheduling/task-sequence/greedy',
      payload,
    );
    return response.data || null;
  }

  async uniformCost(
    payload: Omit<TaskSchedulingInput, 'heuristic' | 'families'>,
  ): Promise<TaskSchedulingResponse | null> {
    const response = await this.httpClient.post<TaskSchedulingResponse>(
      '/scheduling/task-sequence/uniform_cost',
      payload,
    );
    return response.data || null;
  }
}
```

##### 3.10.4 Nova Feature: TaskScheduling

```typescript
// Em src/features/TaskScheduling/index.tsx - NOVA FEATURE
'use client';

import { useState, useTransition } from 'react';
import TaskSchedulingForm from './components/TaskSchedulingForm';
import TaskSequenceVisualization from './components/TaskSequenceVisualization';

interface TaskSchedulingData {
  tasks: number[];
  setupMatrix: Record<string, number>;
  families?: Record<number, string>;
}

const defaultData: TaskSchedulingData = {
  tasks: [],
  setupMatrix: {},
};

export default function TaskSchedulingPage() {
  const [loading, startTransition] = useTransition();
  const [response, setResponse] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [taskData, setTaskData] = useState<TaskSchedulingData>(defaultData);

  return (
    <div style={{ width: '100%', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ textAlign: 'center' }}>
        Sequenciamento de Tarefas com Setups
      </h1>

      <div style={{ marginTop: '30px', display: 'flex', gap: '40px' }}>
        <TaskSchedulingForm
          taskData={taskData}
          loading={loading}
          setTaskData={setTaskData}
          setError={setError}
          setResponse={setResponse}
          startTransition={startTransition}
        />

        <TaskSequenceVisualization
          response={response}
          error={error}
          taskData={taskData}
        />
      </div>
    </div>
  );
}
```

### Fase 5: Testes e Validação (2 dias)

#### 3.11 Casos de Teste

```python
# test_task_scheduling.py
class TestTaskScheduling:
    + test_small_instance_optimal_solution()
    + test_heuristic_admissibility()
    + test_symmetric_vs_asymmetric_costs()
    + test_product_families_optimization()
    + test_performance_large_instances()
```

#### 3.12 Geradores de Instâncias de Teste

```python
class TaskSchedulingGenerator:
    + generate_random_setup_matrix(n_tasks: int, cost_range: Tuple[float, float])
    + generate_family_based_costs(families: Dict, intra_cost: float, inter_cost_range: Tuple)
    + generate_benchmark_instances(sizes: List[int])
```

---

## 4. Cronograma de Implementação Revisado

| Fase      | Atividade                                    | Duração        | Responsável  |
| --------- | -------------------------------------------- | -------------- | ------------ |
| 1         | Criar módulos de extensão (TaskScheduling\*) | 2-3 dias       | Backend Dev  |
| 2         | Integrar com InformedSearch existente        | 2-3 dias       | Backend Dev  |
| 3         | Implementar heurísticas H1, H2, H3           | 2 dias         | Backend Dev  |
| 4         | Criar endpoints na API Flask                 | 1 dia          | Backend Dev  |
| 5         | Estender frontend com nova feature           | 2-3 dias       | Frontend Dev |
| 6         | Testes e validação integrados                | 2 dias         | QA + Dev     |
| **Total** | **Extensão completa do sistema**             | **11-14 dias** |              |

---

## 5. Arquivos a Serem Criados/Modificados

### Novos Arquivos Backend

```
backend/service/
├── TaskSchedulingNode.py         # Extensão de NodeP para ATSP
├── TaskSchedulingData.py         # SetupMatrix e TaskFamily
├── TaskSchedulingHeuristics.py   # H1, H2, H3 implementadas
├── TaskSchedulingSearch.py       # Extensão de InformedSearch
└── TaskSchedulingGenerator.py    # Gerador de instâncias de teste
```

### Novos Arquivos Frontend

```
frontend/src/core/domain/gateway/
└── task-scheduling.gateway.ts    # Interface para task scheduling

frontend/src/core/infra/gateways/http/
└── task-scheduling.gateway.ts    # Implementação HTTP

frontend/src/features/
├── Methods/
│   └── utils/
│       └── constants.ts          # [MODIFICADO] Adicionar tipos scheduling
└── TaskScheduling/               # NOVA FEATURE COMPLETA
    ├── index.tsx                 # Página principal
    ├── components/
    │   ├── TaskSchedulingForm.tsx      # Form específico
    │   ├── SetupMatrixInput.tsx        # Input de matriz
    │   ├── TaskSequenceVisualization.tsx # Visualização
    │   └── HeuristicSelector.tsx       # Seletor de heurísticas
    └── utils/
        ├── setupMatrixParser.ts        # Parser de matrizes
        ├── taskSequenceCalculations.ts # Cálculos auxiliares
        └── taskVisualizationUtils.ts   # Utilitários de visualização
```

### Arquivos Modificados

```
backend/
├── app.py                       # 3 novos endpoints task scheduling
└── requirements.txt             # heapq já existe (built-in)

frontend/
├── src/features/Methods/utils/constants.ts  # Adicionar tipos scheduling
├── src/root.tsx                 # [OPCIONAL] Adicionar rota nova feature
└── package.json                 # Sem novas dependências necessárias
```

### Estrutura Final do Sistema

```
Sistema Integrado:
├── Funcionalidades Existentes (Mantidas)
│   ├── Busca em grafos genéricos
│   ├── Algoritmos: BFS, DFS, A*, Greedy, etc.
│   └── Interface atual para grafos
└── Nova Extensão - Task Scheduling
    ├── Algoritmos específicos para ATSP
    ├── Heurísticas H1, H2, H3
    ├── Interface especializada
    └── Visualização de sequências
```

---

## 6. Considerações de Performance e Limitações

### 6.1 Otimizações Implementadas

- **Bitmask Operations**: Estados representados como (bitmask, last_task) para eficiência
- **Herança de NodeP**: Reutiliza sistema de ordenação existente (insert_ordered)
- **Closed Set**: Evita reprocessamento de estados já visitados
- **Heurísticas Admissíveis**: Garantem otimalidade mantendo performance

### 6.2 Limitações Práticas por Algoritmo

| Algoritmo      | Limite Prático | Complexidade | Uso Recomendado                          |
| -------------- | -------------- | ------------ | ---------------------------------------- |
| A\*            | ~12-15 tarefas | O(b^d)       | Soluções ótimas para instâncias pequenas |
| Greedy         | ~25-30 tarefas | O(n²)        | Soluções rápidas e boas                  |
| Custo Uniforme | ~10-12 tarefas | O(b^d)       | Baseline sem heurística                  |

### 6.3 Estratégias por Tamanho de Instância

- **≤ 10 tarefas**: A\* com H1 para solução ótima
- **11-20 tarefas**: Greedy com H1 ou H2 para boa aproximação
- **> 20 tarefas**: Implementar heurísticas construtivas futuras

### 6.4 Monitoramento de Performance

```python
# Em TaskSchedulingSearch.py - adicionar métricas
def _track_performance(self, nodes_expanded: int, time_elapsed: float,
                      solution_cost: float) -> Dict:
    return {
        'nodes_expanded': nodes_expanded,
        'time_seconds': time_elapsed,
        'solution_cost': solution_cost,
        'nodes_per_second': nodes_expanded / time_elapsed if time_elapsed > 0 else 0
    }
```

---

## 7. Extensões Futuras

### 7.1 Múltiplas Linhas de Produção

```python
class MultiLineScheduling:
    + parallel_line_assignment(tasks: List, n_lines: int)
    + load_balancing_optimization()
```

### 7.2 Tempos de Processamento

```python
class TaskWithProcessingTime:
    def __init__(self, task_id: int, processing_time: float, setup_costs: Dict):
        # Incluir p_j no cálculo do custo total
```

### 7.3 Restrições Adicionais

- Janelas de tempo (time windows)
- Precedências entre tarefas
- Recursos limitados

---

## 8. Métricas de Sucesso e Validação

### 8.1 Critérios Funcionais

- [ ] **Integração**: Sistema existente permanece funcional após extensão
- [ ] **Corretude**: A\* encontra soluções ótimas para instâncias ≤ 10 tarefas
- [ ] **Admissibilidade**: Heurísticas H1, H2, H3 nunca superestimam custo real
- [ ] **Performance**: Tempo de resposta < 5s para instâncias de 12 tarefas
- [ ] **Usabilidade**: Interface permite entrada intuitiva de matrizes de setup

### 8.2 Critérios Técnicos

- [ ] **Arquitetura**: Extensão mantém padrões existentes (herança, gateways)
- [ ] **API**: Endpoints seguem convenções Flask existentes
- [ ] **Frontend**: Nova feature integra com arquitetura React/TypeScript
- [ ] **Testes**: Casos de teste cobrem cenários críticos (matriz inválida, sem solução)

### 8.3 Casos de Teste Essenciais

```python
# test_task_scheduling_integration.py
class TestTaskSchedulingIntegration:
    def test_small_instance_optimal_a_star():
        """Verifica solução ótima para 4 tarefas conhecida"""

    def test_heuristic_admissibility():
        """Confirma que h1, h2, h3 são admissíveis"""

    def test_greedy_vs_a_star_quality():
        """Compara qualidade das soluções greedy vs A*"""

    def test_api_endpoints_integration():
        """Testa todos os endpoints via requests HTTP"""

    def test_invalid_setup_matrix_handling():
        """Verifica tratamento de matrizes incompletas"""
```

### 8.4 Benchmarks de Validação

| Instância | Tarefas | Algoritmo  | Tempo Esperado | Custo Ótimo Conhecido |
| --------- | ------- | ---------- | -------------- | --------------------- |
| tiny_4    | 4       | A\*        | < 0.1s         | A definir             |
| small_8   | 8       | A\*        | < 1s           | A definir             |
| medium_12 | 12      | A\*/Greedy | < 5s           | A definir             |

---

## 9. Riscos e Mitigações

| Risco                                      | Probabilidade | Impacto | Mitigação                                     |
| ------------------------------------------ | ------------- | ------- | --------------------------------------------- |
| Quebra da funcionalidade existente         | Baixa         | Alto    | Extensão via herança, testes de regressão     |
| Performance inadequada (> 15 tarefas)      | Média         | Alto    | Greedy como fallback, alertas de limitação    |
| Complexidade da entrada de matriz de setup | Média         | Médio   | Templates, validação, exemplos pré-carregados |
| Bugs em operações bitmask                  | Baixa         | Alto    | Testes unitários, verificação manual          |
| Heurísticas não-admissíveis                | Baixa         | Alto    | Provas matemáticas, testes comparativos       |

## 10. Próximos Passos para Implementação

### 10.1 Ordem de Desenvolvimento Recomendada

1. **Backend Core** (Dias 1-4)

   - TaskSchedulingNode.py
   - TaskSchedulingData.py
   - TaskSchedulingHeuristics.py
   - TaskSchedulingSearch.py

2. **API Integration** (Dia 5)

   - Endpoints em app.py
   - Testes básicos via curl/Postman

3. **Frontend Extension** (Dias 6-8)

   - Gateway interfaces e implementações
   - TaskScheduling feature completa
   - Integração com sistema existente

4. **Testing & Polish** (Dias 9-10)
   - Testes automatizados
   - Documentação de API
   - Casos de exemplo

### 10.2 Critério de Pronto para Produção

- [ ] Todos os testes passam
- [ ] Performance dentro dos limites esperados
- [ ] Sistema existente continua funcionando
- [ ] Documentação completa da nova funcionalidade
- [ ] Exemplos de uso disponíveis

---

## Conclusão

Esta extensão do sistema atual manterá toda a funcionalidade existente enquanto adiciona capacidades específicas para o problema ATSP de sequenciamento de tarefas. A abordagem de herança e extensão garante compatibilidade e reutilização de código, enquanto as heurísticas especializadas oferecem performance otimizada para o domínio específico.

O sistema resultante será uma ferramenta educacional completa que demonstra tanto algoritmos de busca genéricos quanto sua aplicação especializada em um problema real da indústria.
