# AI Application Compiler

AI Application Compiler converts natural language requirements into structured application specifications.

Instead of generating code directly from a prompt, the system follows a compiler-style pipeline:

```
Natural Language
      ↓
Intent Extraction
      ↓
Application IR
      ↓
Schema Generation
      ↓
Validation & Repair
      ↓
Runtime Checks
```

## Features

- Natural language to application specification
- Intermediate Representation (IR) as a single source of truth
- Database, API, UI, and Authentication schema generation
- Validation and consistency checks
- Targeted repair of invalid components
- Runtime simulation and diagnostics
- Requirement refinement through conversation

## Tech Stack

- Python
- Flask
- OpenRouter API
- Docker

## Running Locally

```bash
git clone https://github.com/chrg613/ai-app-compiler.git
cd ai-app-compiler

pip install -r requirements.txt

export OPENROUTER_API_KEY=your_api_key

python main.py
```

The application will be available at:

```text
http://localhost:5000
```

## Example Prompt

```text
Build a CRM system with users, contacts, companies, and role-based access.

Admins can view analytics while users can only access their own records.
```

## Output

The compiler generates:

- Application Intent
- Database Schema
- API Schema
- UI Schema
- Authentication Schema
- Diagnostics Report

## Project Structure

```text
src/
├── intent/
├── ir/
├── generators/
├── validation/
├── repair/
├── runtime/
└── diagnostics/
```

## Deployment

The project can be deployed using:

- Vercel
- Railway
- Render
- Docker

## Future Improvements

- Database migrations
- Frontend code generation
- App integration
- Deployment advancements
- Integration templates
- Advanced permission models
- Multi-tenant support

## References
- https://faculty.sist.shanghaitech.edu.cn/faculty/songfu/cav/Dragon-book.pdf
- IR system in LLVM
- gaurdrail ai
