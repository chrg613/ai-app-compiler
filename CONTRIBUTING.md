# Contributing to AI Application Compiler

We love your input! We want to make contributing to this project as easy and transparent as possible.

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you're expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots if possible**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Explain why this enhancement would be useful**

### Pull Requests

* Follow the Python PEP 8 code style
* Include appropriate test cases
* Update documentation as needed
* End all files with a newline

## Development Setup

### Prerequisites
- Python 3.11+
- Git
- OpenRouter API key (for testing)

### Local Development

```bash
# Clone the repository
git clone https://github.com/chrg613/ai-app-compiler.git
cd ai-app-compiler

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Set environment variables
export OPENROUTER_API_KEY=your_test_key

# Run the development server
python main.py

# In another terminal, run tests
pytest tests/
```

### Project Structure

```
ai-app-compiler/
├── main.py                 # Flask application entry point
├── requirements.txt        # Python dependencies
├── README.md              # Project overview
├── ARCHITECTURE.md        # Detailed architecture
├── QUICKSTART.md         # Quick start guide
├── CONTRIBUTING.md       # This file
│
├── src/
│   ├── pipeline/          # Main compilation pipeline
│   │   └── compiler_pipeline.py
│   │
│   ├── llm/              # LLM integrations
│   │   └── providers/
│   │       └── openrouter_provider.py
│   │
│   ├── models/           # Pydantic data models
│   │   └── contracts.py
│   │
│   ├── intent/           # Intent extraction stage
│   │   └── extractor.py
│   │
│   ├── ir/               # Intermediate representation
│   │   └── ir_builder.py
│   │
│   ├── generators/       # Schema generators
│   │   ├── db_generator.py
│   │   ├── api_generator.py
│   │   ├── ui_generator.py
│   │   └── auth_generator.py
│   │
│   ├── validation/       # Validation engines
│   │   └── validator.py
│   │
│   ├── repair/           # Repair engine
│   │   └── repair_engine.py
│   │
│   ├── runtime/          # Runtime simulator
│   │   └── simulator.py
│   │
│   └── diagnostics/      # Diagnostics engine
│       └── diagnostics_engine.py
│
├── templates/
│   └── index.html        # Frontend UI
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
└── tests/
    ├── test_intent_extraction.py
    ├── test_schema_generation.py
    ├── test_validation.py
    └── test_integration.py
```

## Making Changes

### Branch Naming
- `feature/description` for new features
- `fix/description` for bug fixes
- `docs/description` for documentation
- `refactor/description` for refactoring

### Commit Messages

Write clear, descriptive commit messages:

```
[CATEGORY] Brief description

More detailed explanation if needed.
Explain the why, not the what (code shows what).

Closes #123
```

Categories: FEATURE, FIX, DOCS, REFACTOR, TEST, PERF

Examples:
```
[FEATURE] Add support for foreign key relationships
[FIX] Fix repair engine not handling missing API routes
[DOCS] Update ARCHITECTURE.md with new validation rules
[REFACTOR] Simplify DatabaseSchema class
[TEST] Add test coverage for confidence scoring
```

### Code Style

Follow PEP 8. Use tools to help:

```bash
# Format code
black src/

# Check for style issues
flake8 src/

# Run type checking
mypy src/
```

### Testing

Write tests for new functionality:

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_validation.py::test_schema_guard
```

Test structure:

```python
# tests/test_my_feature.py
import pytest
from src.path.to.module import MyClass

class TestMyFeature:
    def setup_method(self):
        """Setup for each test"""
        self.obj = MyClass()
    
    def test_basic_functionality(self):
        """Test basic behavior"""
        result = self.obj.do_something()
        assert result == expected
    
    def test_error_handling(self):
        """Test error cases"""
        with pytest.raises(ValueError):
            self.obj.do_invalid_thing()
```

## Documentation

- Update README.md for user-facing changes
- Update ARCHITECTURE.md for technical changes
- Add docstrings to new functions
- Include examples for new features

Example docstring:

```python
def compile_application(prompt: str) -> ApplicationSpec:
    """
    Compile a natural language prompt into an application specification.
    
    This function orchestrates the multi-stage compiler pipeline:
    1. Risk Analysis
    2. Intent Extraction
    3. Application IR generation
    4. Schema generation (parallel)
    5. Validation and repair
    6. Runtime simulation
    7. Diagnostics
    
    Args:
        prompt: Natural language description of the application
        
    Returns:
        ApplicationSpec: Complete application specification
        
    Raises:
        ValueError: If prompt is empty or invalid
        RuntimeError: If compilation fails
        
    Example:
        >>> spec = compile_application("CRM with users and contacts")
        >>> spec.app_name
        'CRM System'
        >>> len(spec.entities)
        2
    """
```

## Performance Considerations

When contributing, keep these in mind:

- **Latency**: Aim for <10s total compilation time
- **Memory**: Keep peak memory usage reasonable (test with large prompts)
- **API Calls**: Minimize LLM calls (each is costly)
- **Parallelism**: Use parallel schema generation where possible

## Areas for Contribution

### High Priority
- [ ] Support for database relationships and foreign keys
- [ ] Migration script generation
- [ ] Advanced permission models (RBAC/ABAC)
- [ ] Performance optimizations

### Medium Priority
- [ ] Frontend code generation (React/Vue)
- [ ] Backend code generation (Python/Node)
- [ ] Integration templates (Stripe, SendGrid, etc.)
- [ ] Interactive refinement UI

### Lower Priority
- [ ] Multi-tenant support patterns
- [ ] Cost estimation engine
- [ ] Batch compilation API
- [ ] Real-time collaboration

## Review Process

1. Submit a Pull Request with a clear description
2. Ensure all tests pass and code is formatted
3. Wait for review from maintainers
4. Address any feedback or suggestions
5. Merge once approved

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- Check existing issues and discussions
- Review ARCHITECTURE.md for technical details
- Ask in GitHub Discussions

---

**Thank you for contributing! 🙏**
