import logging
from typing import Any, Dict
from service.base.UninformedSearch import UninformedSearch
from service.base.InformedSearch import InformedSearch
from service.implementation.TaskSchedulingSearch import TaskSchedulingSearch
from service.implementation.TaskSchedulingData import SetupMatrix
from service.implementation.TaskFamily import TaskFamily
from flask_cors import CORS # type: ignore
from flask import Flask, request, jsonify, abort # type: ignore

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

INCORRECT_MATRIX_MSG = "Matriz de setup incompleta"

@app.route('/', methods=['GET'])
def index() -> str:
    """Health check endpoint."""
    return "<strong>Health Check:</strong> The server is running!"

def get_json_data() -> Dict[str, Any]:
    """Safely get JSON data from request."""
    data = request.get_json()
    if data is None:
        abort(400, description="Invalid or missing JSON data.")
    return data

@app.route('/search/uninformed/breadth_first', methods=['POST'])
def breadth_first() -> Any:
    data = get_json_data()
    try:
        search = UninformedSearch()
        start = data['start']
        goal = data['goal']
        nodes = data['nodes']
        graph = data['graph']
        result = search.breadth_first_search(start, goal, nodes, graph)
        return jsonify({'path': result})
    except KeyError as e:
        logging.error(f"Missing key: {e}")
        abort(400, description=f"Missing key: {e}")
    except Exception as e:
        logging.error(f"Error in breadth first search: {e}")
        abort(500, description=str(e))
        
@app.route('/search/uninformed/depth_first', methods=['POST'])
def depth_first() -> Any:
    data = get_json_data()
    try:
        search = UninformedSearch()
        start = data['start']
        goal = data['goal']
        nodes = data['nodes']
        graph = data['graph']
        result = search.depth_first_search(start, goal, nodes, graph)
        return jsonify({'path': result})
    except KeyError as e:
        logging.error(f"Missing key: {e}")
        abort(400, description=f"Missing key: {e}")
    except Exception as e:
        logging.error(f"Error in depth first search: {e}")
        abort(500, description=str(e))

@app.route('/search/uninformed/depth_limited', methods=['POST'])
def depth_limited() -> Any:
    data = get_json_data()
    try:
        search = UninformedSearch()
        start = data['start']
        goal = data['goal']
        nodes = data['nodes']
        graph = data['graph']
        limit = data['limit']
        result = search.depth_limited_search(start, goal, nodes, graph, limit)
        return jsonify({'path': result})
    except KeyError as e:
        logging.error(f"Missing key: {e}")
        abort(400, description=f"Missing key: {e}")
    except Exception as e:
        logging.error(f"Error in depth limited search: {e}")
        abort(500, description=str(e))
        
@app.route('/search/uninformed/iterative_deepening', methods=['POST'])
def iterative_deepening() -> Any:
    data = get_json_data()
    try:
        search = UninformedSearch()
        start = data['start']
        goal = data['goal']
        nodes = data['nodes']
        graph = data['graph']
        max_limit = data['max_limit']
        result = search.iterative_deepening_search(start, goal, nodes, graph, max_limit)
        return jsonify({'path': result})
    except KeyError as e:
        logging.error(f"Missing key: {e}")
        abort(400, description=f"Missing key: {e}")
    except Exception as e:
        logging.error(f"Error in iterative deepening search: {e}")
        abort(500, description=str(e))

@app.route('/search/uninformed/bidirectional', methods=['POST'])
def bidirectional() -> Any:
    data = get_json_data()
    try:
        search = UninformedSearch()
        start = data['start']
        goal = data['goal']
        nodes = data['nodes']
        graph = data['graph']
        result = search.bidirectional_search(start, goal, nodes, graph)
        return jsonify({'path': result})
    except KeyError as e:
        logging.error(f"Missing key: {e}")
        abort(400, description=f"Missing key: {e}")
    except Exception as e:
        logging.error(f"Error in bidirectional search: {e}")
        abort(500, description=str(e))
               
@app.route('/search/uninformed/uniform_cost', methods=['POST'])
def uniform_cost() -> Any:
    data = get_json_data()
    try:
        search = InformedSearch()
        start = data['start']
        goal = data['goal']
        nodes = data['nodes']
        graph = data['graph']
        result = search.uniform_cost(start, goal, nodes, graph)
        return jsonify({'path': result})
    except KeyError as e:
        logging.error(f"Missing key: {e}")
        abort(400, description=f"Missing key: {e}")
    except Exception as e:
        logging.error(f"Error in uniform cost search: {e}")
        abort(500, description=str(e))
        
@app.route('/search/informed/a_star', methods=['POST'])
def a_star() -> Any:
    data = get_json_data()
    try:
        search = InformedSearch()
        start = data['start']
        goal = data['goal']
        nodes = data['nodes']
        graph = data['graph']
        heuristics = data['heuristics']
        result = search.a_star(start, goal, nodes, graph, heuristics)
        return jsonify({'path': result})
    except KeyError as e:
        logging.error(f"Missing key: {e}")
        abort(400, description=f"Missing key: {e}")
    except Exception as e:
        logging.error(f"Error in A* search: {e}")
        abort(500, description=str(e))
        
@app.route('/search/informed/greedy', methods=['POST'])
def greedy() -> Any:
    data = get_json_data()
    try:
        search = InformedSearch()
        start = data['start']
        goal = data['goal']
        nodes = data['nodes']
        graph = data['graph']
        heuristics = data['heuristics']
        result = search.greedy(start, goal, nodes, graph, heuristics)
        return jsonify({'path': result})
    except KeyError as e:
        logging.error(f"Missing key: {e}")
        abort(400, description=f"Missing key: {e}")
    except Exception as e:
        logging.error(f"Error in greedy search: {e}")
        abort(500, description=str(e))
        
@app.route('/search/informed/ida_star', methods=['POST'])
def ida_star() -> Any:
    data = get_json_data()
    try:
        search = InformedSearch()
        start = data['start']
        goal = data['goal']
        nodes = data['nodes']
        graph = data['graph']
        heuristics = data['heuristics']
        result = search.ida_star(start, goal, nodes, graph, heuristics)
        return jsonify({'path': result})
    except KeyError as e:
        logging.error(f"Missing key: {e}")
        abort(400, description=f"Missing key: {e}")
    except Exception as e:
        logging.error(f"Error in IDA* search: {e}")
        abort(500, description=str(e))
        
@app.route('/scheduling/task-sequence/breadth_first', methods=['POST'])
def task_sequence_breadth_first() -> Any:
    """Busca em largura para sequenciamento de tarefas"""
    data = get_json_data()
    try:
        search = TaskSchedulingSearch()
        tasks = data['tasks']
        setup_costs = data['setup_matrix']
        setup_matrix = SetupMatrix(tasks, setup_costs)
        if not setup_matrix.validate_matrix():
            abort(400, description=INCORRECT_MATRIX_MSG)
        sequence, cost = search.breadth_first_scheduling(tasks, setup_matrix)
        return jsonify({
            'sequence': sequence,
            'total_cost': cost,
        })
    except KeyError as e:
        logging.error(f"Missing key: {e}")
        abort(400, description=f"Missing key: {e}")
    except Exception as e:
        logging.error(f"Error in breadth first task scheduling: {e}")
        abort(500, description=str(e))

@app.route('/scheduling/task-sequence/depth_first', methods=['POST'])
def task_sequence_depth_first() -> Any:
    """Busca em profundidade para sequenciamento de tarefas"""
    data = get_json_data()
    try:
        search = TaskSchedulingSearch()
        tasks = data['tasks']
        setup_costs = data['setup_matrix']
        setup_matrix = SetupMatrix(tasks, setup_costs)
        if not setup_matrix.validate_matrix():
            abort(400, description=INCORRECT_MATRIX_MSG)
        sequence, cost = search.depth_first_scheduling(tasks, setup_matrix)
        return jsonify({
            'sequence': sequence,
            'total_cost': cost,
        })
    except KeyError as e:
        logging.error(f"Missing key: {e}")
        abort(400, description=f"Missing key: {e}")
    except Exception as e:
        logging.error(f"Error in depth first task scheduling: {e}")
        abort(500, description=str(e))

@app.route('/scheduling/task-sequence/depth_limited', methods=['POST'])
def task_sequence_depth_limited() -> Any:
    """Busca em profundidade limitada para sequenciamento de tarefas"""
    data = get_json_data()
    try:
        search = TaskSchedulingSearch()
        tasks = data['tasks']
        setup_costs = data['setup_matrix']
        depth_limit = data.get('depth_limit', 5)
        setup_matrix = SetupMatrix(tasks, setup_costs)
        if not setup_matrix.validate_matrix():
            abort(400, description=INCORRECT_MATRIX_MSG)
        sequence, cost = search.depth_limited_scheduling(tasks, setup_matrix, depth_limit)
        return jsonify({
            'sequence': sequence,
            'total_cost': cost,
        })
    except KeyError as e:
        logging.error(f"Missing key: {e}")
        abort(400, description=f"Missing key: {e}")
    except Exception as e:
        logging.error(f"Error in depth limited task scheduling: {e}")
        abort(500, description=str(e))

@app.route('/scheduling/task-sequence/iterative_deepening', methods=['POST'])
def task_sequence_iterative_deepening() -> Any:
    """Busca em profundidade iterativa para sequenciamento de tarefas"""
    data = get_json_data()
    try:
        search = TaskSchedulingSearch()
        tasks = data['tasks']
        setup_costs = data['setup_matrix']
        setup_matrix = SetupMatrix(tasks, setup_costs)
        if not setup_matrix.validate_matrix():
            abort(400, description=INCORRECT_MATRIX_MSG)
        sequence, cost = search.iterative_deepening_scheduling(tasks, setup_matrix)
        return jsonify({
            'sequence': sequence,
            'total_cost': cost,
        })
    except KeyError as e:
        logging.error(f"Missing key: {e}")
        abort(400, description=f"Missing key: {e}")
    except Exception as e:
        logging.error(f"Error in iterative deepening task scheduling: {e}")
        abort(500, description=str(e))

@app.route('/scheduling/task-sequence/bidirectional', methods=['POST'])
def task_sequence_bidirectional() -> Any:
    """Busca bidirecional para sequenciamento de tarefas"""
    data = get_json_data()
    try:
        search = TaskSchedulingSearch()
        tasks = data['tasks']
        setup_costs = data['setup_matrix']
        setup_matrix = SetupMatrix(tasks, setup_costs)
        if not setup_matrix.validate_matrix():
            abort(400, description=INCORRECT_MATRIX_MSG)
        sequence, cost = search.bidirectional_scheduling(tasks, setup_matrix)
        return jsonify({
            'sequence': sequence,
            'total_cost': cost,
        })
    except KeyError as e:
        logging.error(f"Missing key: {e}")
        abort(400, description=f"Missing key: {e}")
    except Exception as e:
        logging.error(f"Error in bidirectional task scheduling: {e}")
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
            abort(400, description=INCORRECT_MATRIX_MSG)

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
        })

    except KeyError as e:
        logging.error(f"Missing key: {e}")
        abort(400, description=f"Missing key: {e}")
    except Exception as e:
        logging.error(f"Error in uniform cost task scheduling: {e}")
        abort(500, description=str(e))

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
            abort(400, description=INCORRECT_MATRIX_MSG)

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
            abort(400, description=INCORRECT_MATRIX_MSG)

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
            'heuristic': heuristic
        })

    except KeyError as e:
        logging.error(f"Missing key: {e}")
        abort(400, description=f"Missing key: {e}")
    except Exception as e:
        logging.error(f"Error in greedy task scheduling: {e}")
        abort(500, description=str(e))

@app.route('/scheduling/task-sequence/ida_star', methods=['POST'])
def task_sequence_ida_star() -> Any:
    """IDA* para sequenciamento de tarefas com setups"""
    data = get_json_data()
    try:
        search = TaskSchedulingSearch()

        tasks = data['tasks']
        setup_costs = data['setup_matrix']
        heuristic = data.get('heuristic', 'h1')
        family_data = data.get('families')

        setup_matrix = SetupMatrix(tasks, setup_costs)
        if not setup_matrix.validate_matrix():
            abort(400, description=INCORRECT_MATRIX_MSG)

        families = TaskFamily(family_data) if family_data else None

        sequence, cost = search.ida_star_scheduling(tasks, setup_matrix, heuristic, families)

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
            'heuristic': heuristic
        })

    except KeyError as e:
        logging.error(f"Missing key: {e}")
        abort(400, description=f"Missing key: {e}")
    except Exception as e:
        logging.error(f"Error in IDA* task scheduling: {e}")
        abort(500, description=str(e))

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    logging.error(f"404 Error: {error}")
    return jsonify({'error': 'Not Found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
