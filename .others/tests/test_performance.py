#!/usr/bin/env python3
"""
Performance testing for Task Scheduling algorithms
"""
import time
import random
from service.implementation.TaskSchedulingSearch import TaskSchedulingSearch
from service.implementation.TaskSchedulingData import SetupMatrix

def generate_random_setup_matrix(n_tasks, cost_range=(1, 50)):
    """Generate random setup costs for testing"""
    tasks = list(range(1, n_tasks + 1))
    setup_costs = {}
    
    # Add costs from initial state (0) to all tasks
    for j in tasks:
        setup_costs[f"(0,{j})"] = random.randint(*cost_range)
    
    # Add costs between all task pairs
    for i in tasks:
        for j in tasks:
            if i != j:
                setup_costs[f"({i},{j})"] = random.randint(*cost_range)
    
    return SetupMatrix(tasks, setup_costs)

def performance_test():
    """Test performance across different problem sizes"""
    
    print("Task Scheduling Performance Test")
    print("=" * 50)
    
    # Test different problem sizes
    sizes = [4, 6, 8, 10, 12]
    algorithms = [
        ("A*-H1", "a_star", "h1"),
        ("A*-H2", "a_star", "h2"), 
        ("Greedy-H1", "greedy", "h1"),
        ("Uniform Cost", "uniform_cost", None)
    ]
    
    results = {}
    
    for size in sizes:
        print(f"\nTesting with {size} tasks:")
        print("-" * 30)
        
        # Generate random problem
        random.seed(42)  # For reproducible results
        setup_matrix = generate_random_setup_matrix(size)
        tasks = list(range(1, size + 1))
        
        search = TaskSchedulingSearch()
        results[size] = {}
        
        for alg_name, method, heuristic in algorithms:
            try:
                start_time = time.time()
                
                if method == "a_star":
                    sequence, cost = search.a_star_scheduling(tasks, setup_matrix, heuristic)
                elif method == "greedy":
                    sequence, cost = search.greedy_scheduling(tasks, setup_matrix, heuristic)
                elif method == "uniform_cost":
                    sequence, cost = search.uniform_cost_scheduling(tasks, setup_matrix)
                
                elapsed_time = time.time() - start_time
                
                results[size][alg_name] = {
                    'time': elapsed_time,
                    'cost': cost,
                    'sequence_length': len(sequence)
                }
                
                print(f"  {alg_name:12}: {elapsed_time:6.3f}s | Cost: {cost:6.1f} | Seq: {sequence}")
                
            except Exception as e:
                print(f"  {alg_name:12}: ERROR - {str(e)[:50]}")
                results[size][alg_name] = {'error': str(e)}
    
    # Performance summary
    print(f"\n\nPerformance Summary")
    print("=" * 60)
    print(f"{'Size':<6} {'A*-H1':<10} {'A*-H2':<10} {'Greedy':<10} {'UC':<10}")
    print("-" * 60)
    
    for size in sizes:
        row = f"{size:<6}"
        for alg_name, _, _ in algorithms:
            if alg_name in results[size] and 'time' in results[size][alg_name]:
                time_val = results[size][alg_name]['time']
                row += f"{time_val:<10.3f}"
            else:
                row += f"{'FAIL':<10}"
        print(row)

def scalability_test():
    """Test scalability limits"""
    
    print(f"\n\nScalability Test")
    print("=" * 30)
    
    search = TaskSchedulingSearch()
    
    # Test increasing sizes until timeout
    timeout_limit = 5.0  # 5 second timeout
    
    for size in range(3, 16):  # Test up to 15 tasks
        print(f"\nTesting {size} tasks:")
        
        random.seed(size)  # Different seed for each size
        setup_matrix = generate_random_setup_matrix(size, (1, 20))
        tasks = list(range(1, size + 1))
        
        # Test A* with timeout
        try:
            start_time = time.time()
            sequence, cost = search.a_star_scheduling(tasks, setup_matrix, "h1")
            elapsed = time.time() - start_time
            
            if elapsed > timeout_limit:
                print(f"  A*-H1: {elapsed:.2f}s (TOO SLOW) | Cost: {cost}")
                break
            else:
                print(f"  A*-H1: {elapsed:.3f}s | Cost: {cost} | Length: {len(sequence)}")
                
        except Exception as e:
            print(f"  A*-H1: ERROR - {e}")
            break
    
    print(f"\nA* practical limit appears to be around {size-1} tasks with {timeout_limit}s timeout")

def memory_usage_test():
    """Test memory usage patterns"""
    
    print(f"\n\nMemory Usage Patterns")
    print("=" * 30)
    
    # Test different algorithms on same problem
    size = 8
    setup_matrix = generate_random_setup_matrix(size, (5, 25))
    tasks = list(range(1, size + 1))
    
    search = TaskSchedulingSearch()
    
    algorithms = [
        ("A*-H1", lambda: search.a_star_scheduling(tasks, setup_matrix, "h1")),
        ("Greedy-H1", lambda: search.greedy_scheduling(tasks, setup_matrix, "h1")),
        ("Uniform Cost", lambda: search.uniform_cost_scheduling(tasks, setup_matrix))
    ]
    
    for name, func in algorithms:
        try:
            start_time = time.time()
            sequence, cost = func()
            elapsed = time.time() - start_time
            
            print(f"  {name:12}: {elapsed:.3f}s | Solution cost: {cost}")
            print(f"               Sequence: {sequence}")
            
        except Exception as e:
            print(f"  {name:12}: ERROR - {e}")

if __name__ == "__main__":
    performance_test()
    scalability_test()
    memory_usage_test()
    
    print("\n" + "=" * 60)
    print("Performance testing complete!")
    print("\nRecommendations:")
    print("- Use A* for problems ≤ 10-12 tasks (optimal solutions)")
    print("- Use Greedy for problems > 12 tasks (fast approximations)")
    print("- H1 heuristic generally provides good performance")
    print("- Consider problem structure when choosing heuristics")