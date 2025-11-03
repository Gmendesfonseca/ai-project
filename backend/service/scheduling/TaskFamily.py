from typing import Dict
from .TaskSchedulingData import SetupMatrix

class TaskFamily:
    def __init__(self, family_assignments: Dict[int, str] = None):
        """
        :param family_assignments: Dicionário com chaves como IDs de tarefas e valores como nomes de famílias
        """
        self.families = family_assignments or {}

    def same_family(self, task1: int, task2: int) -> bool:
        """
        Verifica se duas tarefas pertencem à mesma família
        
        :param task1: ID da primeira tarefa
        :param task2: ID da segunda tarefa
        :return: Verdadeiro se ambas as tarefas pertencem à mesma família, falso caso contrário.
        """
        if not self.families:
            return False
        return (task1 in self.families and task2 in self.families and
                self.families[task1] == self.families[task2])

    def get_min_interfamily_cost(self, setup_matrix: SetupMatrix) -> float:
        """
        Retorna o menor custo entre tarefas de famílias diferentes
        
        :param setup_matrix: Instância de SetupMatrix com os custos de setup
        :return: Menor custo entre tarefas de famílias diferentes
        """
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