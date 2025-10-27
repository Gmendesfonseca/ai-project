#!/usr/bin/env python3
"""
Simple test for TaskScheduling implementation
"""
from service.implementation.TaskSchedulingSearch import TaskSchedulingSearch
from service.implementation.TaskSchedulingData import SetupMatrix
from service.implementation.TaskFamily import TaskFamily

def test_basic_functionality():
    """Test basic task scheduling functionality"""
    
    # Create a simple 3-task problem
    tasks = [1, 2, 3]
    setup_costs = {
        "(0,1)": 5,
        "(0,2)": 8,
        "(0,3)": 12,
        "(1,2)": 3,
        "(1,3)": 7,
        "(2,1)": 4,
        "(2,3)": 6,
        "(3,1)": 9,
        "(3,2)": 2
    }
    
    # Create setup matrix
    setup_matrix = SetupMatrix(tasks, setup_costs)
    
    # Validate matrix
    is_valid = setup_matrix.validate_matrix()
    print(f"Setup matrix is valid: {is_valid}")
    
    # Test setup cost retrieval
    cost = setup_matrix.get_setup_cost(0, 1)
    print(f"Setup cost from 0 to 1: {cost}")
    
    # Create search instance
    search = TaskSchedulingSearch()
    
    # Test A* with H1 heuristic
    print("\nTesting A* with H1 heuristic:")
    sequence, total_cost = search.a_star_scheduling(tasks, setup_matrix, "h1")
    print(f"Optimal sequence: {sequence}")
    print(f"Total cost: {total_cost}")
    
    # Test Greedy
    print("\nTesting Greedy with H1 heuristic:")
    sequence_greedy, cost_greedy = search.greedy_scheduling(tasks, setup_matrix, "h1")
    print(f"Greedy sequence: {sequence_greedy}")
    print(f"Greedy cost: {cost_greedy}")
    
    # Test Uniform Cost
    print("\nTesting Uniform Cost:")
    sequence_uc, cost_uc = search.uniform_cost_scheduling(tasks, setup_matrix)
    print(f"Uniform cost sequence: {sequence_uc}")
    print(f"Uniform cost: {cost_uc}")

if __name__ == "__main__":
    test_basic_functionality()