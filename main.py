"""
AI Application Compiler - Production Server
Main entry point for the application compiler backend and API
"""

import os
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
from datetime import datetime

from src.llm.providers.openrouter_provider import OpenRouterProvider
from src.pipeline.compiler_pipeline import CompilerPipeline
from src.intent.extractor import IntentExtractor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize LLM Provider
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    logger.warning(" OPENROUTER_API_KEY not set. Using fallback.")
    api_key = "test-key"

llm_provider = OpenRouterProvider(api_key)
intent_extractor = IntentExtractor(llm_provider)
compiler_pipeline = CompilerPipeline(intent_extractor)

# In-memory storage for demo (replace with database in production)
COMPILATION_CACHE = {}


@app.route('/')
def index():
    """Serve the main application UI"""
    return render_template('index.html')


@app.route('/api/compile', methods=['POST'])
def compile_app():
    """
    Main endpoint: compile a natural language prompt into an app specification
    """
    try:
        data = request.json
        prompt = data.get('prompt', '').strip()

        if not prompt:
            return jsonify({
                'error': 'Prompt is required',
                'status': 'FAIL'
            }), 400

        logger.info(f"[v0] Compiling prompt: {prompt[:100]}...")

        # Compile using the pipeline
        result = compiler_pipeline.compile(prompt)

        # Cache the result
        request_id = datetime.now().isoformat()
        COMPILATION_CACHE[request_id] = result

        return jsonify({
            'status': 'SUCCESS',
            'request_id': request_id,
            'app_name': result['ir'].app_name,
            'description': result['ir'].description,
            'entities': [
                {
                    'name': e.name,
                    'attributes': [
                        {
                            'name': a.name,
                            'type': a.type,
                            'nullable': a.nullable,
                            'is_primary': a.is_primary
                        }
                        for a in e.attributes
                    ]
                }
                for e in result['ir'].entities
            ],
            'roles': result['ir'].roles,
            'features': result['ir'].features,
            'integrations': [i.name for i in result['ir'].integrations],
            'database_schema': {
                'tables': [
                    {
                        'name': t.name,
                        'columns': [
                            {
                                'name': c.name,
                                'type': c.type,
                                'nullable': c.nullable,
                                'is_primary': c.is_primary
                            }
                            for c in t.columns
                        ]
                    }
                    for t in result['database'].tables
                ]
            },
            'api_schema': {
                'endpoints': [
                    {
                        'path': e.path,
                        'method': e.method,
                        'entity_name': e.entity_name,
                        'description': e.description,
                        'requires_auth': e.requires_auth
                    }
                    for e in result['api'].endpoints
                ]
            },
            'ui_schema': {
                'pages': [
                    {
                        'name': p.name,
                        'route': p.route,
                        'description': p.description,
                        'requires_auth': p.requires_auth
                    }
                    for p in result['ui'].pages
                ]
            },
            'auth_schema': {
                'roles': [
                    {
                        'name': r.name,
                        'permissions': [
                            {
                                'name': p.name,
                                'resource': p.resource,
                                'action': p.action
                            }
                            for p in r.permissions
                        ]
                    }
                    for r in result['auth'].roles
                ]
            },
            'diagnostics': {
                'warnings': result['diagnostics'].warnings,
                'assumptions': result['diagnostics'].assumptions,
                'repairs': result['diagnostics'].repairs,
                'confidence': result['diagnostics'].confidence,
                'generation_time_ms': result['diagnostics'].generation_time_ms
            }
        })

    except Exception as e:
        logger.error(f"[v0] Compilation error: {str(e)}", exc_info=True)
        return jsonify({
            'error': str(e),
            'status': 'FAIL'
        }), 500


@app.route('/api/schema/<request_id>', methods=['GET'])
def get_schema(request_id):
    """Retrieve cached compilation result"""
    if request_id not in COMPILATION_CACHE:
        return jsonify({'error': 'Request not found'}), 404

    result = COMPILATION_CACHE[request_id]
    return jsonify({
        'ir': result['ir'].dict(),
        'database': result['database'].dict(),
        'api': result['api'].dict(),
        'ui': result['ui'].dict(),
        'auth': result['auth'].dict(),
        'diagnostics': result['diagnostics'].dict()
    })


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'ai-app-compiler',
        'version': '2.0.0'
    })


@app.route('/api/models', methods=['GET'])
def list_models():
    """List available LLM models"""
    return jsonify({
        'models': [
            'deepseek/deepseek-chat-v3-0324',
            'openai/gpt-4',
            'anthropic/claude-3-opus'
        ],
        'current': 'deepseek/deepseek-chat-v3-0324'
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"[v0] Starting AI Application Compiler on port {port}")
    logger.info("[v0] Pipeline: Prompt → Intent → IR → Schemas → Validation → Runtime Simulator → Diagnostics")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
