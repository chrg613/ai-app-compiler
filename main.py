"""
AI Application Compiler - Production Server
Main entry point for the application compiler backend and API
"""

import os
import logging
import sys
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from src.config import Config
from src.llm.providers.openrouter_provider import OpenRouterProvider
from src.pipeline.compiler_pipeline import CompilerPipeline
from src.intent.extractor import IntentExtractor

# Setup configuration and logging early
Config.setup_logging()
logger = logging.getLogger(__name__)

# Validate configuration on startup
is_valid, errors = Config.validate()
if not is_valid:
    logger.error("Configuration validation failed:")
    for error in errors:
        logger.error(f"  - {error}")
    sys.exit(1)

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(Config)
CORS(app, origins=Config.CORS_ORIGINS)

# Initialize LLM provider and pipeline
try:
    logger.info("[Main] Initializing LLM provider...")
    llm_provider = OpenRouterProvider(Config.LLM_API_KEY)
    intent_extractor = IntentExtractor(llm_provider)
    compiler_pipeline = CompilerPipeline(intent_extractor)
    logger.info("[Main] Pipeline initialized successfully")
except Exception as e:
    logger.error(f"[Main] Failed to initialize pipeline: {e}")
    sys.exit(1)

# In-memory storage for demo (replace with database in production)
COMPILATION_CACHE = {}


# ============================
# UI Routes
# ============================

@app.route('/')
def index():
    """Serve the main application UI"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"[Main] Error serving index: {e}")
        return jsonify({'error': 'UI not available'}), 500


# ============================
# Health & Status Endpoints
# ============================

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'environment': Config.ENV
    }), 200


@app.route('/api/status')
def status():
    """Get system status and configuration (no secrets)"""
    return jsonify({
        'status': 'ready',
        'config': Config.to_dict(),
        'cache_size': len(COMPILATION_CACHE)
    }), 200


# ============================
# Compilation Endpoints
# ============================

@app.route('/api/compile', methods=['POST'])
def compile_app():
    """
    Main endpoint: compile a natural language prompt into an app specification
    
    Request body:
    {
        "prompt": "description of the app to build"
    }
    
    Response:
    {
        "status": "success",
        "id": "compilation_id",
        "result": {
            "intent": {...},
            "database_schema": {...},
            "api_schema": {...},
            "ui_schema": {...},
            "auth_schema": {...},
            "diagnostics": {...}
        }
    }
    """
    try:
        data = request.get_json() or {}
        prompt = data.get('prompt', '').strip()

        if not prompt:
            logger.warning("[Compile] Empty prompt received")
            return jsonify({'error': 'Prompt is required'}), 400

        if len(prompt) > 5000:
            logger.warning("[Compile] Prompt too long")
            return jsonify({'error': 'Prompt too long (max 5000 chars)'}), 400

        logger.info(f"[Compile] Processing prompt ({len(prompt)} chars)")

        # Run compilation pipeline
        result = compiler_pipeline.compile(prompt)

        # Cache result
        compilation_id = str(len(COMPILATION_CACHE))
        COMPILATION_CACHE[compilation_id] = {
            'prompt': prompt,
            'result': result,
            'timestamp': datetime.utcnow().isoformat()
        }

        logger.info(f"[Compile] Compilation #{compilation_id} successful")

        return jsonify({
            'status': 'success',
            'id': compilation_id,
            'result': result
        }), 200

    except ValueError as e:
        logger.error(f"[Compile] Validation error: {e}")
        return jsonify({'error': str(e)}), 400

    except Exception as e:
        logger.error(f"[Compile] Unexpected error: {e}", exc_info=True)
        return jsonify({'error': 'Compilation failed'}), 500


@app.route('/api/compile/<compilation_id>', methods=['GET'])
def get_compilation(compilation_id):
    """Retrieve a previously compiled specification"""
    try:
        if compilation_id not in COMPILATION_CACHE:
            return jsonify({'error': 'Compilation not found'}), 404

        cached = COMPILATION_CACHE[compilation_id]
        return jsonify({
            'status': 'found',
            'id': compilation_id,
            'timestamp': cached['timestamp'],
            'result': cached['result']
        }), 200

    except Exception as e:
        logger.error(f"[Get] Error retrieving compilation: {e}")
        return jsonify({'error': 'Failed to retrieve compilation'}), 500


@app.route('/api/compile', methods=['GET'])
def list_compilations():
    """List all cached compilations"""
    try:
        compilations = [
            {
                'id': cid,
                'timestamp': cached['timestamp'],
                'prompt_length': len(cached['prompt'])
            }
            for cid, cached in COMPILATION_CACHE.items()
        ]
        return jsonify({
            'status': 'success',
            'total': len(compilations),
            'compilations': compilations
        }), 200

    except Exception as e:
        logger.error(f"[List] Error listing compilations: {e}")
        return jsonify({'error': 'Failed to list compilations'}), 500


# ============================
# Export Endpoints
# ============================

@app.route('/api/compile/<compilation_id>/export', methods=['GET'])
def export_compilation(compilation_id):
    """Export compilation result as downloadable files"""
    try:
        if compilation_id not in COMPILATION_CACHE:
            return jsonify({'error': 'Compilation not found'}), 404

        result = COMPILATION_CACHE[compilation_id]['result']
        export_format = request.args.get('format', 'json')

        if export_format == 'json':
            return jsonify(result), 200

        elif export_format == 'yaml':
            # TODO: Implement YAML export
            return jsonify({'error': 'YAML export not yet implemented'}), 501

        else:
            return jsonify({'error': 'Unknown export format'}), 400

    except Exception as e:
        logger.error(f"[Export] Error exporting compilation: {e}")
        return jsonify({'error': 'Export failed'}), 500


# ============================
# Error Handlers
# ============================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"[Error] Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


# ============================
# Application Entry Point
# ============================

if __name__ == '__main__':
    port = Config.PORT
    debug = Config.DEBUG

    logger.info(f"[Main] Starting server on {Config.HOST}:{port}")
    logger.info(f"[Main] Debug mode: {debug}")
    logger.info(f"[Main] Configuration: {Config.to_dict()}")

    app.run(
        host=Config.HOST,
        port=port,
        debug=debug,
        use_reloader=False  # Important for Vercel deployment
    )
