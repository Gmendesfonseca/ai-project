import logging
from typing import Any, Dict
from service.UninformedSearch import UninformedSearch
from flask_cors import CORS # type: ignore
from flask import Flask, request, jsonify, abort # type: ignore

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

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

@app.route('/search/breadth_first', methods=['POST'])
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
        
@app.route('/search/depth_first', methods=['POST'])
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

@app.route('/search/depth_limited', methods=['POST'])
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
        
@app.route('/search/iterative_deepening', methods=['POST'])
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

@app.route('/search/bidirectional', methods=['POST'])
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

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    logging.error(f"404 Error: {error}")
    return jsonify({'error': 'Not Found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
