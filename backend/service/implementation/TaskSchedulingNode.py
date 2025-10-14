from ..base.NodeP import NodeP
from typing import List

class TaskSchedulingNode(NodeP):
    def __init__(self, remaining_bitmask: int, last_task: int,
                 g_cost: float, h_cost: float, parent=None):
      """
      :param remaining_bitmask: Bitmask representando tarefas restantes
      :param last_task: Última tarefa agendada
      :param g_cost: Custo acumulado até este nó
      :param h_cost: Custo heurístico estimado até o objetivo
      :param parent: Nó pai (padrão: None)"""
      # v1 = f_cost (para ordenação na priority queue)
      # v2 = g_cost (custo acumulado)
      super().__init__(parent, state=(remaining_bitmask, last_task), v1=(g_cost + h_cost), previous=None, next_node=None, v2=g_cost)
      self.remaining_bitmask = remaining_bitmask
      self.last_task = last_task
      self.h_cost = h_cost
      self.sequence = []  # Será populada durante reconstrução do caminho

    def is_goal_state(self) -> bool:
      """
      Verifica se todas as tarefas foram agendadas (bitmask zerada).

      :return: Verdadeiro se todas as tarefas foram agendadas, falso caso contrário.
      """
      return self.remaining_bitmask == 0
    
    def get_remaining_tasks(self, task_list: List[int]) -> List[int]:
      """
      Converte bitmask para lista de tarefas restantes
      
      :param task_list: Lista de todas as tarefas possíveis
      :return: Lista de tarefas restantes
      """
      remaining = []
      for i, task in enumerate(task_list):
          if self.remaining_bitmask & (1 << i):
              remaining.append(task)
      return remaining

    def __eq__(self, other):
      """
      Compara dois nós com base no estado (bitmask e última tarefa).
      Dois nós são iguais se tiverem a mesma bitmask e a mesma última tarefa.
      
      :param other: Outro nó a ser comparado.
      :return: Verdadeiro se os nós forem iguais, falso caso contrário.
      """
      if not isinstance(other, TaskSchedulingNode):
          return False
      return (self.remaining_bitmask == other.remaining_bitmask and
              self.last_task == other.last_task)

    def __hash__(self):
      """
      Retorna o hash do nó com base no estado (bitmask e última tarefa).
      
      :return: Hash do nó.
      """
      return hash((self.remaining_bitmask, self.last_task))