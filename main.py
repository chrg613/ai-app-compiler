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
CONVERSATIONS = {}  # conversation_id -> {messages: [], current_intent: {}, status: 'active'}
import uuid
import zipfile
import io
import json


def serialize_result(obj):
    """JSON serializer for complex objects"""
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    return str(obj)


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
# Conversation Endpoints (Turn-by-Turn)
# ============================

@app.route('/api/conversation', methods=['POST'])
def start_conversation():
    """Start a new turn-by-turn conversation"""
    try:
        conv_id = str(uuid.uuid4())
        CONVERSATIONS[conv_id] = {
            'messages': [],
            'current_intent': None,
            'status': 'active',
            'created_at': datetime.utcnow().isoformat()
        }
        logger.info(f"[Conversation] Started new conversation: {conv_id}")
        return jsonify({
            'status': 'success',
            'conversation_id': conv_id
        }), 201

    except Exception as e:
        logger.error(f"[Conversation] Error starting conversation: {e}")
        return jsonify({'error': 'Failed to start conversation'}), 500


@app.route('/api/conversation/<conv_id>/message', methods=['POST'])
def add_message(conv_id):
    """Add a message to conversation and get AI response with assumptions"""
    try:
        if conv_id not in CONVERSATIONS:
            return jsonify({'error': 'Conversation not found'}), 404

        data = request.get_json() or {}
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({'error': 'Message is required'}), 400

        conv = CONVERSATIONS[conv_id]
        
        # Add user message
        conv['messages'].append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.utcnow().isoformat()
        })

        # Build conversation context
        full_prompt = "\n".join([
            m['content'] for m in conv['messages'] if m['role'] == 'user'
        ])

        logger.info(f"[Conversation] Processing message for {conv_id}")

        # Get AI response with assumptions
        try:
            result = compiler_pipeline.compile(full_prompt)
            intent = result['intent']
            
            # Extract assumptions from intent
            entities = [e.name for e in intent.entities] if hasattr(intent, 'entities') and intent.entities else []
            roles = intent.roles if hasattr(intent, 'roles') and intent.roles else ['user', 'admin']
            features = intent.features if hasattr(intent, 'features') and intent.features else []
            integrations = intent.integrations if hasattr(intent, 'integrations') and intent.integrations else []
            
            assumptions = {
                'entities': entities,
                'roles': roles,
                'features': features[:5],  # Limit to first 5
                'integrations': integrations
            }

            # Generate clarification question based on extracted data
            confidence = len(entities) > 0 and len(roles) > 0
            if not confidence:
                next_question = "I need more details. Can you tell me: what entities (data objects) does your app need? And who are the different user roles?"
            else:
                next_question = f"I've identified {len(entities)} entities and {len(roles)} user roles. Does this match your vision? Any changes?"

            ai_response = {
                'type': 'assumptions',
                'message': f"Based on your requirements, I've identified: {', '.join(entities)} entities",
                'assumptions': assumptions,
                'confidence': 0.9 if confidence else 0.6,
                'next_question': next_question
            }

            conv['messages'].append({
                'role': 'assistant',
                'content': ai_response['message'],
                'type': 'assumptions',
                'assumptions': assumptions,
                'timestamp': datetime.utcnow().isoformat()
            })

            conv['current_intent'] = result

            return jsonify({
                'status': 'success',
                'conversation_id': conv_id,
                'response': ai_response,
                'messages': conv['messages']
            }), 200

        except Exception as compile_error:
            logger.error(f"[Conversation] Compilation error: {compile_error}")
            error_response = f"I need clarification: {str(compile_error)}"
            conv['messages'].append({
                'role': 'assistant',
                'content': error_response,
                'type': 'clarification',
                'timestamp': datetime.utcnow().isoformat()
            })
            return jsonify({
                'status': 'clarification_needed',
                'conversation_id': conv_id,
                'response': {
                    'type': 'clarification',
                    'message': error_response
                },
                'messages': conv['messages']
            }), 200

    except Exception as e:
        logger.error(f"[Conversation] Error processing message: {e}", exc_info=True)
        return jsonify({'error': 'Failed to process message'}), 500


@app.route('/api/conversation/<conv_id>/refine', methods=['POST'])
def refine_requirements(conv_id):
    """User modifies requirements mid-conversation"""
    try:
        if conv_id not in CONVERSATIONS:
            return jsonify({'error': 'Conversation not found'}), 404

        data = request.get_json() or {}
        refinement = data.get('changes', '').strip()

        if not refinement:
            return jsonify({'error': 'No changes provided'}), 400

        conv = CONVERSATIONS[conv_id]
        if not conv['current_intent']:
            return jsonify({'error': 'No active compilation'}), 400

        # Add refinement as new user message
        conv['messages'].append({
            'role': 'user',
            'content': refinement,
            'timestamp': datetime.utcnow().isoformat()
        })

        # Rebuild full context from all messages
        full_prompt = "\n".join([
            m['content'] for m in conv['messages'] if m['role'] == 'user'
        ])

        logger.info(f"[Refine] Recompiling for {conv_id} with refinement: {refinement[:50]}...")

        # Recompile with accumulated context
        try:
            result = compiler_pipeline.compile(full_prompt)
            intent = result['intent']
            
            # Extract updated assumptions
            entities = [e.name for e in intent.entities] if hasattr(intent, 'entities') and intent.entities else []
            roles = intent.roles if hasattr(intent, 'roles') and intent.roles else ['user', 'admin']
            features = intent.features if hasattr(intent, 'features') and intent.features else []
            integrations = intent.integrations if hasattr(intent, 'integrations') and intent.integrations else []
            
            updated_assumptions = {
                'entities': entities,
                'roles': roles,
                'features': features[:5],
                'integrations': integrations
            }

            # Store the updated result
            conv['current_intent'] = result

            # Add AI response with updated assumptions
            next_question = f"Updated! Now I see {len(entities)} entities and {len(roles)} roles. Anything else to adjust?"
            
            ai_response = {
                'type': 'assumptions',
                'message': f"Requirements updated. New structure: {', '.join(entities)}",
                'assumptions': updated_assumptions,
                'confidence': 0.9 if entities else 0.6,
                'next_question': next_question
            }

            conv['messages'].append({
                'role': 'assistant',
                'content': ai_response['message'],
                'type': 'assumptions',
                'assumptions': updated_assumptions,
                'timestamp': datetime.utcnow().isoformat()
            })

            logger.info(f"[Refine] Recompilation successful for {conv_id}")

            return jsonify({
                'status': 'success',
                'conversation_id': conv_id,
                'response': ai_response,
                'messages': conv['messages']
            }), 200

        except Exception as compile_error:
            logger.error(f"[Refine] Recompilation failed: {compile_error}")
            error_msg = f"Clarification needed: {str(compile_error)[:100]}"
            conv['messages'].append({
                'role': 'assistant',
                'content': error_msg,
                'type': 'clarification',
                'timestamp': datetime.utcnow().isoformat()
            })
            return jsonify({
                'status': 'clarification_needed',
                'conversation_id': conv_id,
                'response': {
                    'type': 'clarification',
                    'message': error_msg
                },
                'messages': conv['messages']
            }), 200

    except Exception as e:
        logger.error(f"[Refine] Error refining requirements: {e}", exc_info=True)
        return jsonify({'error': f'Failed to refine requirements: {str(e)}'}), 500


@app.route('/api/conversation/<conv_id>/generate-app', methods=['POST'])
def generate_app(conv_id):
    """Generate downloadable app from final requirements"""
    try:
        if conv_id not in CONVERSATIONS:
            return jsonify({'error': 'Conversation not found'}), 404

        conv = CONVERSATIONS[conv_id]
        if not conv['current_intent']:
            return jsonify({'error': 'No active compilation'}), 400

        # Extract intent from result dict
        result = conv['current_intent']
        intent = result['intent'] if isinstance(result, dict) else result
        ir = result['ir'] if isinstance(result, dict) else getattr(result, 'ir', None)
        
        app_name = intent.app_name if hasattr(intent, 'app_name') else 'GeneratedApp'
        description = intent.description if hasattr(intent, 'description') else 'Generated Application'

        # Create in-memory ZIP
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add app code
            app_py = "# Generated Flask Application\n# See main compilation for full code\n"
            zf.writestr('app.py', app_py)

            # Add requirements
            zf.writestr('requirements.txt', 'flask>=3.0.0\nflask-cors>=4.0.0\n')

            # Add README
            readme = f"# {app_name}\n\n{description}\n\n## Generated from AI Compiler\n"
            if ir and hasattr(ir, 'entities'):
                readme += f"\nEntities: {', '.join(e.name for e in ir.entities)}\n"
            zf.writestr('README.md', readme)

            # Add conversation history
            history_json = json.dumps(conv['messages'], indent=2, default=serialize_result)
            zf.writestr('conversation_history.json', history_json)

        zip_buffer.seek(0)
        
        logger.info(f"[Generate] Generated app download for conversation {conv_id}")

        return zip_buffer.getvalue(), 200, {
            'Content-Type': 'application/zip',
            'Content-Disposition': f"attachment; filename=app_{conv_id[:8]}.zip"
        }

    except Exception as e:
        logger.error(f"[Generate] Error generating app: {e}", exc_info=True)
        return jsonify({'error': f'Failed to generate app: {str(e)}'}), 500


@app.route('/api/conversation/<conv_id>', methods=['GET'])
def get_conversation(conv_id):
    """Get conversation history and current state"""
    try:
        if conv_id not in CONVERSATIONS:
            return jsonify({'error': 'Conversation not found'}), 404

        conv = CONVERSATIONS[conv_id]
        return jsonify({
            'status': 'success',
            'conversation_id': conv_id,
            'messages': conv['messages'],
            'current_intent': json.loads(json.dumps(conv['current_intent'], default=serialize_result)) if conv['current_intent'] else None,
            'conversation_status': conv['status']
        }), 200

    except Exception as e:
        logger.error(f"[Get] Error getting conversation: {e}")
        return jsonify({'error': 'Failed to get conversation'}), 500


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
