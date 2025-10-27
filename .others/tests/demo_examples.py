#!/usr/bin/env python3
"""
Example problems and demonstrations for Task Scheduling implementation
"""
from service.implementation.TaskSchedulingSearch import TaskSchedulingSearch
from service.implementation.TaskSchedulingData import SetupMatrix
from service.implementation.TaskFamily import TaskFamily

def demo_manufacturing_line():
    """Demonstrate a realistic manufacturing line scenario"""
    
    print("Manufacturing Line Setup Example")
    print("=" * 50)
    print("Scenario: Paint shop with 4 different colors")
    print("Setup costs represent cleaning/changeover time between colors")
    print()
    
    # Tasks represent different paint colors
    tasks = [1, 2, 3, 4]  # Colors: Red, Blue, Green, Yellow
    task_names = {0: "Start", 1: "Red", 2: "Blue", 3: "Green", 4: "Yellow"}
    
    # Setup costs (in minutes) - similar colors have lower setup costs
    setup_costs = {
        # From start position to any color
        "(0,1)": 15,  # Start -> Red
        "(0,2)": 18,  # Start -> Blue  
        "(0,3)": 12,  # Start -> Green
        "(0,4)": 20,  # Start -> Yellow
        
        # Between colors - similar colors cost less
        "(1,2)": 25,  # Red -> Blue (high contrast)
        "(1,3)": 8,   # Red -> Green (similar hue)
        "(1,4)": 12,  # Red -> Yellow (warm colors)
        
        "(2,1)": 22,  # Blue -> Red
        "(2,3)": 30,  # Blue -> Green (high contrast)
        "(2,4)": 28,  # Blue -> Yellow (complement)
        
        "(3,1)": 10,  # Green -> Red
        "(3,2)": 35,  # Green -> Blue
        "(3,4)": 6,   # Green -> Yellow (nature colors)
        
        "(4,1)": 14,  # Yellow -> Red
        "(4,2)": 32,  # Yellow -> Blue
        "(4,3)": 5,   # Yellow -> Green
    }
    
    setup_matrix = SetupMatrix(tasks, setup_costs)
    search = TaskSchedulingSearch()
    
    # Test different algorithms
    algorithms = [
        ("A* with H1", "a_star", "h1"),
        ("A* with H2", "a_star", "h2"),
        ("Greedy Best-First", "greedy", "h1"),
        ("Uniform Cost Search", "uniform_cost", None)
    ]
    
    results = []
    for name, method, heuristic in algorithms:
        if method == "a_star":
            sequence, cost = search.a_star_scheduling(tasks, setup_matrix, heuristic)
        elif method == "greedy":
            sequence, cost = search.greedy_scheduling(tasks, setup_matrix, heuristic)
        elif method == "uniform_cost":
            sequence, cost = search.uniform_cost_scheduling(tasks, setup_matrix)
        
        results.append((name, sequence, cost))
        
        # Convert sequence to color names
        color_sequence = [task_names[task] for task in sequence]
        print(f"{name:20}: {' -> '.join(color_sequence)}")
        print(f"{' '*20}  Total setup time: {cost} minutes")
        
        # Show detailed setup costs
        setup_details = []
        prev = 0
        for task in sequence:
            setup_cost = setup_matrix.get_setup_cost(prev, task)
            setup_details.append(f"{task_names[prev]} -> {task_names[task]}: {setup_cost}min")
            prev = task
        
        print(f"{' '*20}  Details: {', '.join(setup_details)}")
        print()
    
    # Find best solution
    best_cost = min(result[2] for result in results)
    print(f"Best solution found: {best_cost} minutes total setup time")

def demo_product_families():
    """Demonstrate H3 heuristic with product families"""
    
    print("\n\nProduct Families Example")
    print("=" * 40)
    print("Scenario: Electronics assembly with component families")
    print("Family A: Resistors, Family B: Capacitors")
    print("Setup within family = 2min, between families = 15min")
    print()
    
    tasks = [1, 2, 3, 4, 5, 6]
    task_names = {
        0: "Start", 1: "R1-100Ω", 2: "R2-220Ω", 3: "R3-470Ω",
        4: "C1-10µF", 5: "C2-22µF", 6: "C3-47µF"
    }
    
    # Define families
    families = TaskFamily({
        1: "Resistors", 2: "Resistors", 3: "Resistors",
        4: "Capacitors", 5: "Capacitors", 6: "Capacitors"
    })
    
    # Setup costs reflecting family structure
    setup_costs = {}
    
    # From start to any component
    for task in tasks:
        setup_costs[f"(0,{task})"] = 10
    
    # Between components
    for i in tasks:
        for j in tasks:
            if i != j:
                if families.same_family(i, j):
                    setup_costs[f"({i},{j})"] = 2  # Same family
                else:
                    setup_costs[f"({i},{j})"] = 15  # Different family
    
    setup_matrix = SetupMatrix(tasks, setup_costs)
    search = TaskSchedulingSearch()
    
    # Compare with and without family awareness
    print("Without family awareness (H1):")
    seq_h1, cost_h1 = search.a_star_scheduling(tasks, setup_matrix, "h1")
    component_seq = [task_names[task] for task in seq_h1]
    print(f"  Sequence: {' -> '.join(component_seq)}")
    print(f"  Cost: {cost_h1} minutes")
    
    print("\nWith family awareness (H3):")
    seq_h3, cost_h3 = search.a_star_scheduling(tasks, setup_matrix, "h3", families)
    component_seq = [task_names[task] for task in seq_h3]
    print(f"  Sequence: {' -> '.join(component_seq)}")
    print(f"  Cost: {cost_h3} minutes")
    
    # Analyze family transitions
    def count_family_changes(sequence, families):
        changes = 0
        for i in range(len(sequence) - 1):
            if not families.same_family(sequence[i], sequence[i+1]):
                changes += 1
        return changes
    
    h1_changes = count_family_changes(seq_h1, families)
    h3_changes = count_family_changes(seq_h3, families)
    
    print(f"\nFamily transitions:")
    print(f"  H1 approach: {h1_changes} family changes")
    print(f"  H3 approach: {h3_changes} family changes")
    print(f"  Improvement: {cost_h1 - cost_h3} minutes saved")

def demo_small_problem_step_by_step():
    """Step-by-step demonstration of A* algorithm"""
    
    print("\n\nStep-by-Step A* Demonstration")
    print("=" * 45)
    print("Small 3-task problem to show algorithm steps")
    print()
    
    tasks = [1, 2, 3]
    setup_costs = {
        "(0,1)": 8, "(0,2)": 12, "(0,3)": 15,
        "(1,2)": 4, "(1,3)": 10,
        "(2,1)": 6, "(2,3)": 3,
        "(3,1)": 9, "(3,2)": 5
    }
    
    setup_matrix = SetupMatrix(tasks, setup_costs)
    
    print("Setup cost matrix:")
    print("     To:  1   2   3")
    print("From 0:   8  12  15")
    print("     1:   -   4  10") 
    print("     2:   6   -   3")
    print("     3:   9   5   -")
    print()
    
    # Manual verification of optimal solution
    print("All possible sequences:")
    all_sequences = [
        ([1,2,3], 8 + 4 + 3),  # 0->1->2->3
        ([1,3,2], 8 + 10 + 5), # 0->1->3->2
        ([2,1,3], 12 + 6 + 10), # 0->2->1->3
        ([2,3,1], 12 + 3 + 9),  # 0->2->3->1
        ([3,1,2], 15 + 9 + 4),  # 0->3->1->2
        ([3,2,1], 15 + 5 + 6),  # 0->3->2->1
    ]
    
    for seq, cost in all_sequences:
        print(f"  {seq}: {cost}")
    
    optimal_cost = min(cost for _, cost in all_sequences)
    optimal_seqs = [seq for seq, cost in all_sequences if cost == optimal_cost]
    
    print(f"\nOptimal cost: {optimal_cost}")
    print(f"Optimal sequence(s): {optimal_seqs}")
    
    # Now run A*
    search = TaskSchedulingSearch()
    found_seq, found_cost = search.a_star_scheduling(tasks, setup_matrix, "h1")
    
    print(f"\nA* found: {found_seq} with cost {found_cost}")
    print(f"Verification: {'✓ OPTIMAL' if found_cost == optimal_cost else '✗ SUBOPTIMAL'}")

if __name__ == "__main__":
    demo_manufacturing_line()
    demo_product_families()
    demo_small_problem_step_by_step()
    
    print("\n" + "=" * 60)
    print("Demonstration complete!")
    print("\nKey takeaways:")
    print("- A* with good heuristics finds optimal solutions efficiently")
    print("- H3 heuristic leverages problem structure (families)")
    print("- Greedy is fast but may miss optimal solutions")
    print("- The choice of algorithm depends on problem size and requirements")