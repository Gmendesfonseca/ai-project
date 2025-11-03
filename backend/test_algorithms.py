#!/usr/bin/env python3
"""
Script de Teste para Algoritmos de Busca
Executa todos os testes descritos em TESTES_DE_MESA.md
"""

import requests
import json
from typing import Dict, Any, List
import time

BASE_URL = "http://localhost:5000"

# Cores para output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}")
    print(f"{text:^70}")
    print(f"{'='*70}{Colors.ENDC}\n")

def print_result(algorithm: str, result: Dict[str, Any], elapsed: float):
    print(f"{Colors.OKBLUE}{algorithm}:{Colors.ENDC}")
    print(f"  Path/Sequence: {Colors.OKGREEN}{result.get('path') or result.get('sequence')}{Colors.ENDC}")
    if 'total_cost' in result:
        cost = result['total_cost']
        print(f"  Total Cost: {Colors.OKCYAN}{cost if cost is not None else 'Infinity'}{Colors.ENDC}")
    print(f"  Time: {Colors.WARNING}{elapsed:.4f}s{Colors.ENDC}")
    print()

def test_graph_search():
    """Testa algoritmos de busca em grafos"""
    print_header("TESTES DE BUSCA EM GRAFOS")
    
    # Dados do grafo de teste
    graph_data = {
        "start": "A",
        "goal": "E",
        "nodes": ["A", "B", "C", "D", "E"],
        "graph": {
            "A": [{"node": "B", "weight": 1}, {"node": "C", "weight": 4}],
            "B": [{"node": "C", "weight": 2}, {"node": "D", "weight": 5}],
            "C": [{"node": "D", "weight": 1}, {"node": "E", "weight": 6}],
            "D": [{"node": "E", "weight": 3}]
        }
    }
    
    # Heurísticas para algoritmos informados
    heuristics = {
        "A": 8, "B": 6, "C": 5, "D": 3, "E": 0
    }
    
    algorithms = [
        ("BFS", "/search/uninformed/breadth_first", graph_data),
        ("DFS", "/search/uninformed/depth_first", graph_data),
        ("Depth-Limited (limit=2)", "/search/uninformed/depth_limited", {**graph_data, "limit": 2}),
        ("Iterative Deepening", "/search/uninformed/iterative_deepening", {**graph_data, "max_limit": 10}),
        ("Bidirectional", "/search/uninformed/bidirectional", graph_data),
        ("Uniform Cost", "/search/uninformed/uniform_cost", graph_data),
        ("A*", "/search/informed/a_star", {**graph_data, "heuristics": heuristics}),
        ("Greedy", "/search/informed/greedy", {**graph_data, "heuristics": heuristics}),
        ("IDA*", "/search/informed/ida_star", {**graph_data, "heuristics": heuristics}),
    ]
    
    results = []
    
    for name, endpoint, data in algorithms:
        try:
            start_time = time.time()
            response = requests.post(f"{BASE_URL}{endpoint}", json=data, timeout=30)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                print_result(name, result, elapsed)
                results.append((name, result, elapsed, True))
            else:
                print(f"{Colors.FAIL}{name}: Error {response.status_code}{Colors.ENDC}")
                results.append((name, {}, 0, False))
        except Exception as e:
            print(f"{Colors.FAIL}{name}: Exception - {str(e)}{Colors.ENDC}")
            results.append((name, {}, 0, False))
    
    return results

def test_task_scheduling():
    """Testa algoritmos de sequenciamento de tarefas"""
    print_header("TESTES DE SEQUENCIAMENTO DE TAREFAS")
    
    # Dados do problema de sequenciamento (4 tarefas)
    scheduling_data = {
        "tasks": [1, 2, 3, 4],
        "setup_matrix": {
            "(0,1)": 10, "(0,2)": 15, "(0,3)": 8, "(0,4)": 12,
            "(1,2)": 5, "(1,3)": 12, "(1,4)": 8,
            "(2,1)": 7, "(2,3)": 4, "(2,4)": 10,
            "(3,1)": 12, "(3,2)": 6, "(3,4)": 5,
            "(4,1)": 9, "(4,2)": 10, "(4,3)": 7
        }
    }
    
    # Dados com famílias para H3
    scheduling_data_h3 = {
        **scheduling_data,
        "families": {
            "1": "A", "2": "A", "3": "B", "4": "B"
        }
    }
    
    algorithms = [
        ("BFS", "/scheduling/task-sequence/breadth_first", scheduling_data),
        ("DFS", "/scheduling/task-sequence/depth_first", scheduling_data),
        ("Depth-Limited (limit=4)", "/scheduling/task-sequence/depth_limited", {**scheduling_data, "depth_limit": 4}),
        ("Iterative Deepening", "/scheduling/task-sequence/iterative_deepening", scheduling_data),
        ("Bidirectional", "/scheduling/task-sequence/bidirectional", scheduling_data),
        ("Uniform Cost", "/scheduling/task-sequence/uniform_cost", scheduling_data),
        ("A* (H1)", "/scheduling/task-sequence/a_star", {**scheduling_data, "heuristic": "h1"}),
        ("A* (H2)", "/scheduling/task-sequence/a_star", {**scheduling_data, "heuristic": "h2"}),
        ("A* (H3)", "/scheduling/task-sequence/a_star", {**scheduling_data_h3, "heuristic": "h3"}),
        ("Greedy (H1)", "/scheduling/task-sequence/greedy", {**scheduling_data, "heuristic": "h1"}),
        ("IDA* (H1)", "/scheduling/task-sequence/ida_star", {**scheduling_data, "heuristic": "h1"}),
    ]
    
    results = []
    
    for name, endpoint, data in algorithms:
        try:
            start_time = time.time()
            response = requests.post(f"{BASE_URL}{endpoint}", json=data, timeout=30)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                print_result(name, result, elapsed)
                
                # Mostrar detalhes de setup se disponível
                if 'setup_details' in result:
                    print(f"  {Colors.OKCYAN}Setup Details:{Colors.ENDC}")
                    for detail in result['setup_details']:
                        print(f"    {detail['from']} → {detail['to']}: {detail['cost']}")
                    print()
                
                results.append((name, result, elapsed, True))
            else:
                print(f"{Colors.FAIL}{name}: Error {response.status_code} - {response.text}{Colors.ENDC}")
                results.append((name, {}, 0, False))
        except Exception as e:
            print(f"{Colors.FAIL}{name}: Exception - {str(e)}{Colors.ENDC}")
            results.append((name, {}, 0, False))
    
    return results

def print_comparison_table(results: List[tuple], title: str):
    """Imprime tabela comparativa de resultados"""
    print_header(f"COMPARAÇÃO - {title}")
    
    print(f"{'Algoritmo':<25} {'Custo':<10} {'Tempo (s)':<12} {'Status':<10}")
    print("-" * 70)
    
    for name, result, elapsed, success in results:
        if success:
            cost = result.get('total_cost', 'N/A')
            cost_str = str(cost) if cost is not None else "∞"
            status = f"{Colors.OKGREEN}✓{Colors.ENDC}"
        else:
            cost_str = "N/A"
            status = f"{Colors.FAIL}✗{Colors.ENDC}"
        
        print(f"{name:<25} {cost_str:<10} {elapsed:<12.4f} {status}")
    
    print()

def main():
    """Função principal"""
    print(f"{Colors.BOLD}{Colors.HEADER}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║          SUITE DE TESTES - ALGORITMOS DE BUSCA                    ║")
    print("║                                                                    ║")
    print("║  Este script executa todos os testes descritos em                 ║")
    print("║  TESTES_DE_MESA.md para validar os algoritmos implementados.      ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")
    
    # Verificar se o servidor está rodando
    try:
        requests.get(BASE_URL, timeout=5)
        print(f"{Colors.OKGREEN}✓ Servidor backend detectado em {BASE_URL}{Colors.ENDC}\n")
    except requests.exceptions.RequestException:
        print(f"{Colors.FAIL}✗ ERRO: Servidor backend não encontrado em {BASE_URL}{Colors.ENDC}")
        print(f"{Colors.WARNING}Por favor, inicie o backend antes de executar os testes:{Colors.ENDC}")
        print("  cd backend && ./run.sh\n")
        return
    
    # Executar testes de grafos
    graph_results = test_graph_search()
    
    # Executar testes de sequenciamento
    scheduling_results = test_task_scheduling()
    
    # Mostrar tabelas comparativas
    print_comparison_table(graph_results, "BUSCA EM GRAFOS")
    print_comparison_table(scheduling_results, "SEQUENCIAMENTO DE TAREFAS")
    
    # Resumo final
    total_tests = len(graph_results) + len(scheduling_results)
    successful_tests = sum(1 for _, _, _, success in graph_results + scheduling_results if success)
    
    print_header("RESUMO FINAL")
    print(f"Total de testes: {total_tests}")
    print(f"Sucessos: {Colors.OKGREEN}{successful_tests}{Colors.ENDC}")
    print(f"Falhas: {Colors.FAIL}{total_tests - successful_tests}{Colors.ENDC}")
    
    if successful_tests == total_tests:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}✓ Todos os testes passaram com sucesso!{Colors.ENDC}\n")
    else:
        print(f"\n{Colors.WARNING}⚠ Alguns testes falharam. Verifique os logs acima.{Colors.ENDC}\n")

if __name__ == "__main__":
    main()
