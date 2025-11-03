from typing import List, Dict

class SetupMatrix:
    def __init__(self, tasks: List[int], setup_costs: Dict[str, float]):
        """
        :param tasks: Lista de IDs das tarefas [1, 2, 3, ...]
        :param setup_costs: Dicionário com chaves "(i,j)" e valores de custo
        """
        self.tasks = tasks
        self.setup_costs = {}
        self.n_tasks = len(tasks)

        # Converte chaves string para tuplas inteiras
        for key, cost in setup_costs.items():
            i, j = map(int, key.strip("()").split(","))
            self.setup_costs[(i, j)] = cost

    def get_setup_cost(self, from_task: int, to_task: int) -> float:
      """
      Retorna o custo de setup entre duas tarefas.
      Se não houver custo definido, retorna infinito.
      
      :param from_task: ID da tarefa de origem.
      :param to_task: ID da tarefa de destino.
      :return: Custo de setup entre as tarefas.
      """
      return self.setup_costs.get((from_task, to_task), float('inf'))

    def validate_matrix(self) -> bool:
        """
        Verifica se a matriz está completa para todas as tarefas
        
        :return: Verdadeiro se a matriz estiver completa, falso caso contrário.
        """
        for i in [0] + self.tasks:  # Inclui nó inicial 0
            for j in self.tasks:
                if i != j and (i, j) not in self.setup_costs:
                    return False
        return True