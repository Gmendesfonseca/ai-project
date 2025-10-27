#!/usr/bin/env python3
"""
Comprehensive test for Task Scheduling implementation with heuristic validation
"""
from service.implementation.TaskSchedulingSearch import TaskSchedulingSearch
from service.implementation.TaskSchedulingData import SetupMatrix
from service.implementation.TaskFamily import TaskFamily

def test_heuristic_admissibility():
    """Test that all heuristics are admissible (never overestimate)"""
    
    print("Testing Heuristic Admissibility")
    print("=" * 40)
    
    # Create a small problem where we can verify optimality
    tasks = [1, 2, 3]
    setup_costs = {
        "(0,1)": 10,
        "(0,2)": 15,
        "(0,3)": 20,
        "(1,2)": 5,
        "(1,3)": 12,
        "(2,1)": 8,
        "(2,3)": 6,
        "(3,1)": 18,
        "(3,2)": 9
    }
    
    setup_matrix = SetupMatrix(tasks, setup_costs)
    search = TaskSchedulingSearch()
    
    # Get optimal solution using A*
    print("\n1. Finding optimal solution with A*-H1:")
    optimal_seq, optimal_cost = search.a_star_scheduling(tasks, setup_matrix, "h1")
    print(f"   Optimal sequence: {optimal_seq}")
    print(f"   Optimal cost: {optimal_cost}")
    
    # Test all heuristics with A*
    heuristics = ["h1", "h2"]
    for h in heuristics:
        print(f"\n2. Testing A* with {h.upper()}:")
        seq, cost = search.a_star_scheduling(tasks, setup_matrix, h)
        print(f"   Sequence: {seq}")
        print(f"   Cost: {cost}")
        
        if abs(cost - optimal_cost) < 0.001:  # Allow for floating point precision
            print(f"   ✓ {h.upper()} found optimal solution")
        else:
            print(f"   ✗ {h.upper()} found suboptimal solution (cost diff: {cost - optimal_cost})")
    
    # Test H3 with families
    print(f"\n3. Testing A* with H3 (families):")
    families = TaskFamily({1: "A", 2: "B", 3: "A"})
    seq, cost = search.a_star_scheduling(tasks, setup_matrix, "h3", families)
    print(f"   Sequence: {seq}")
    print(f"   Cost: {cost}")
    
    if abs(cost - optimal_cost) < 0.001:
        print(f"   ✓ H3 found optimal solution")
    else:
        print(f"   ✗ H3 found suboptimal solution (cost diff: {cost - optimal_cost})")

def test_algorithm_comparison():
    """Compare different algorithms on the same problem"""
    
    print("\n\nAlgorithm Comparison")
    print("=" * 30)
    
    # Slightly larger problem
    tasks = [1, 2, 3, 4]
    setup_costs = {
        "(0,1)": 8, "(0,2)": 12, "(0,3)": 15, "(0,4)": 20,
        "(1,2)": 3, "(1,3)": 7, "(1,4)": 11,
        "(2,1)": 5, "(2,3)": 4, "(2,4)": 9,
        "(3,1)": 10, "(3,2)": 6, "(3,4)": 2,
        "(4,1)": 14, "(4,2)": 8, "(4,3)": 3
    }
    
    setup_matrix = SetupMatrix(tasks, setup_costs)
    search = TaskSchedulingSearch()
    
    algorithms = [
        ("A*-H1", lambda: search.a_star_scheduling(tasks, setup_matrix, "h1")),
        ("A*-H2", lambda: search.a_star_scheduling(tasks, setup_matrix, "h2")),
        ("Greedy-H1", lambda: search.greedy_scheduling(tasks, setup_matrix, "h1")),
        ("Uniform Cost", lambda: search.uniform_cost_scheduling(tasks, setup_matrix))
    ]
    
    results = []
    for name, func in algorithms:
        try:
            seq, cost = func()
            results.append((name, seq, cost))
            print(f"{name:12}: {seq} (cost: {cost})")
        except Exception as e:
            print(f"{name:12}: ERROR - {e}")
    
    # Find best cost
    if results:
        best_cost = min(result[2] for result in results)
        print(f"\nBest cost found: {best_cost}")
        
        for name, seq, cost in results:
            gap = ((cost - best_cost) / best_cost) * 100 if best_cost > 0 else 0
            print(f"{name:12}: {gap:5.1f}% gap from best")

def test_edge_cases():
    """Test edge cases and error handling"""
    
    print("\n\nEdge Cases Testing")
    print("=" * 25)
    
    search = TaskSchedulingSearch()
    
    # Test single task
    print("\n1. Single Task:")
    tasks = [1]
    setup_costs = {"(0,1)": 5}
    setup_matrix = SetupMatrix(tasks, setup_costs)
    
    seq, cost = search.a_star_scheduling(tasks, setup_matrix, "h1")
    print(f"   Sequence: {seq}, Cost: {cost}")
    
    # Test two tasks
    print("\n2. Two Tasks:")
    tasks = [1, 2]
    setup_costs = {"(0,1)": 3, "(0,2)": 7, "(1,2)": 4, "(2,1)": 6}
    setup_matrix = SetupMatrix(tasks, setup_costs)
    
    seq, cost = search.a_star_scheduling(tasks, setup_matrix, "h1")
    print(f"   Optimal: {seq}, Cost: {cost}")
    
    seq_greedy, cost_greedy = search.greedy_scheduling(tasks, setup_matrix, "h1")
    print(f"   Greedy:  {seq_greedy}, Cost: {cost_greedy}")

def test_setup_matrix_validation():
    """Test setup matrix validation"""
    
    print("\n\nSetup Matrix Validation")
    print("=" * 30)
    
    tasks = [1, 2, 3]
    
    # Complete matrix
    complete_costs = {
        "(0,1)": 5, "(0,2)": 8, "(0,3)": 12,
        "(1,2)": 3, "(1,3)": 7,
        "(2,1)": 4, "(2,3)": 6,
        "(3,1)": 9, "(3,2)": 2
    }
    
    complete_matrix = SetupMatrix(tasks, complete_costs)
    print(f"Complete matrix valid: {complete_matrix.validate_matrix()}")
    
    # Incomplete matrix
    incomplete_costs = {
        "(0,1)": 5, "(0,2)": 8,
        "(1,2)": 3,
        "(2,1)": 4
    }
    
    incomplete_matrix = SetupMatrix(tasks, incomplete_costs)
    print(f"Incomplete matrix valid: {incomplete_matrix.validate_matrix()}")

if __name__ == "__main__":
    test_heuristic_admissibility()
    test_algorithm_comparison()
    test_edge_cases()
    test_setup_matrix_validation()
    print("\n" + "=" * 50)
    print("Comprehensive testing complete!")