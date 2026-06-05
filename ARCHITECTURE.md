# AI Application Compiler - Architecture Document

## System Overview

The AI Application Compiler is a production-grade, multi-stage compiler system that transforms natural language application requirements into complete, validated, executable application specifications. Unlike simple LLM wrappers, this system implements compiler principles to ensure reliability, consistency, and determinism.

---

## Core Principles

### 1. **LLMs Generate, Systems Validate**
- LLM output is never trusted directly
- Every output is validated against strict schemas
- Consistency is verified across all layers
- Issues are repaired intelligently

### 2. **Single Source of Truth (IR)**
- Application Intermediate Representation (IR) is the authoritative spec
- All downstream generation derives from IR
- Changes propagate consistently
- Enables incremental compilation

### 3. **Compiler-Inspired Design**
- Multi-phase pipeline (like LLVM)
- Structured intermediate representation
- Targeted optimization and repair
- Deterministic transformations

### 4. **Fail-Safe Operations**
- Validation catches errors early
- Repair systems fix only broken components
- Runtime simulation proves executability
- Comprehensive diagnostics explain decisions

---

## Pipeline Stages

### Stage 1: Risk Analysis
**Input**: Raw user prompt
**Output**: RiskReport with ambiguity/conflict scores

- Analyzes prompt for vagueness
- Identifies conflicting requirements
- Scores completeness
- Determines confidence level

**Key Metrics**:
- `ambiguity_score`: 0-1 (how vague is the prompt)
- `conflict_score`: 0-1 (how many contradictions)
- `completeness_score`: 0-1 (how detailed)

### Stage 2: Intent Extraction
**Input**: User prompt
**Output**: IntentModel with structured entities

- Uses LLM with structured prompting
- Forces output to match strict schema
- Extracts entities with full attributes
- Identifies roles, features, integrations

**Key Outputs**:
- Entity names and descriptions
- Attribute types (uuid, text, integer, etc.)
- Nullability constraints
- Primary key indicators

**Structured Prompt Forces**:
```
Response must be ONLY valid JSON matching:
{
  "app_name": string,
  "description": string,
  "entities": [
    {
      "name": "CamelCase",
      "attributes": [
        {
          "name": "snake_case",
          "type": "uuid|text|integer|...",
          "nullable": boolean,
          "is_primary": boolean
        }
      ]
    }
  ],
  "roles": ["admin", "user"],
  "features": ["Feature1", "Feature2"],
  "integrations": ["Stripe", "SendGrid"]
}
```

### Stage 3: Assumption Engine
**Input**: Extracted intent, risk report
**Output**: AssumptionReport with documented assumptions

- Identifies missing information
- Makes reasonable defaults
- Documents all assumptions
- Provides reasoning

**Example Assumptions**:
- "Email login enabled" (auth not specified)
- "Admin role created" (roles not mentioned)
- "Stripe selected" (payments required but provider not specified)

### Stage 4: Application IR (Intermediate Representation)
**Input**: IntentModel + Assumptions
**Output**: ApplicationIR (single source of truth)

This is the most critical stage. The IR captures:

```python
class ApplicationIR(BaseModel):
    version: int                      # For versioning
    app_name: str                     # Application name
    description: str                  # What it does
    entities: List[EntityIR]          # Data models
    roles: List[str]                  # User roles
    features: List[str]               # Features/capabilities
    workflows: List[WorkflowIR]       # Business processes
    permissions: List[PermissionIR]   # Access control
    integrations: List[IntegrationIR] # External services
    assumptions: List[str]            # Documented guesses
```

Each entity includes full attribute metadata:
- Name (snake_case)
- Type (uuid, text, integer, etc.)
- Nullability
- Primary key flag
- Description

**Why IR Exists**:
- Single source of truth (no inconsistency)
- Enables incremental updates
- Supports dependency tracking
- Facilitates targeted repair
- Makes system deterministic

### Stage 5: Schema Generation

Four parallel generators consume IR:

#### 5a. Database Schema Generator
**Input**: ApplicationIR
**Output**: DatabaseSchema

Transformations:
- Entity names → table names (snake_case)
- Attributes → columns with SQL types
- Type mapping: uuid→UUID, integer→INTEGER, text→TEXT, etc.

```
User entity → users table
├── id (uuid, primary)
├── email (text, not null)
├── created_at (timestamp)
└── metadata (json)
```

#### 5b. API Schema Generator
**Input**: ApplicationIR
**Output**: APISchema

For each entity, generates CRUD endpoints:
- GET /entity (list)
- POST /entity (create)
- GET /entity/{id} (read)
- PUT /entity/{id} (update)
- DELETE /entity/{id} (delete)

Each endpoint includes:
- Parameters with types
- Required/optional fields
- Response fields
- Auth requirements
- Required roles

#### 5c. UI Schema Generator
**Input**: ApplicationIR
**Output**: UISchema

Generates pages:
- Home/landing page
- Dashboard (if feature mentioned)
- List pages for each entity
- Form pages for create/edit
- Feature-specific pages
- Admin panel (if admin role exists)

Each page includes:
- Route
- Components
- Entity binding
- Auth requirements
- Access control

#### 5d. Auth Schema Generator
**Input**: ApplicationIR
**Output**: AuthSchema

Generates roles with permissions:
- Admin role: full access + admin-specific permissions
- User role: standard CRUD permissions on own records
- Custom roles: feature-specific permissions

Permissions are granular:
- manage_users (admin only)
- view_contacts (role-based)
- edit_own_records (user-level)

### Stage 6: Guardrails & Validators

Parallel validation checks:

#### Schema Guard
- Valid JSON structure
- Required fields present
- Correct types
- No extra fields

#### Content Guard
- API paths start with /
- Entity names are valid identifiers
- Roles have permissions
- Features are described

#### Logic Guard
- Payments feature requires integration
- Dashboard references entities
- Roles are used in permissions
- Auth aligns with features

#### Consistency Guard
- API fields exist in DB schema
- UI components bind to valid APIs
- Roles match permission subjects
- Auth routes exist in API schema

### Stage 7: Validation Engine

Multi-layer validation rules:

```python
Validation Rules:
├── Structure
│   ├── All required fields present
│   ├── Types match schema
│   └── No forbidden fields
├── Consistency
│   ├── UI↔API alignment
│   ├── API↔DB alignment
│   ├── DB↔Auth alignment
│   └── Circular dependency check
├── Business Logic
│   ├── Feature coverage (payments → integration)
│   ├── Role completeness
│   ├── Permission validity
│   └── Workflow consistency
└── Completeness
    ├── All entities have IDs
    ├── All pages have routes
    ├── All endpoints documented
    └── All roles defined
```

Output: ValidationReport with:
- Status (PASS/FAIL/WARN)
- List of errors
- List of warnings
- Component causing issues

### Stage 8: Repair Engine

Intelligent, targeted repairs:

**Traditional Approach**:
```
Validation Error
    ↓
Regenerate Entire App
    ↓
Re-validate
    ↓
Repeat
```

**Our Approach**:
```
Validation Error
    ↓
Identify Failing Component
    ↓
Regenerate Only That Component
    ↓
Re-validate That Component
    ↓
Success (avoids full regen)
```

Repair Types:
- AddTable: Missing entity table
- AddColumn: Missing field
- AddEndpoint: Missing API route
- AddPermission: Missing role permission
- AddPage: Missing UI page

Each repair is logged in diagnostics.

### Stage 9: Runtime Simulator

Simulates application execution to validate specs:

```python
Simulation Steps:
1. Register all database tables
2. Register all API endpoints
3. Register all UI pages
4. Verify endpoint→table references
5. Verify page→endpoint references
6. Verify role permissions
7. Attempt dummy transactions
8. Check all validations pass
```

Output: RuntimeReport with:
- Execution status (PASS/FAIL)
- Registered tables count
- Registered endpoints count
- Registered pages count
- Errors if any

**Why This Matters**:
Proves the spec is actually deployable. Not theoretical validation, but actual execution simulation.

### Stage 10: Diagnostics Engine

Comprehensive reporting:

```python
class DiagnosticsReport:
    warnings: List[str]        # Potential issues
    assumptions: List[str]     # Documented guesses
    repairs: List[str]         # Applied fixes
    confidence: float          # 0-1 confidence score
    generation_time_ms: float  # Performance metric
    llm_calls: int            # API calls made
```

Confidence Calculation:
```
Base: 0.5

+ 0.1 if app_name present
+ 0.1 if description present
+ 0.1 if entities extracted (>0)
+ 0.1 if entities have attributes (>1)
+ 0.1 if roles specified
+ 0.1 if features specified

Deductions:
- 0.05 per unresolved warning
- 0.02 per assumption
- 0.01 per repair

Final: min(0.99, score)
```

---

## Data Contracts (Type Safety)

All data flows through strictly-typed Pydantic models:

### Input Contracts

**IntentModel**: User intent extraction output
- app_name: str
- description: str
- entities: List[EntityModel] (with full attributes)
- roles: List[str]
- features: List[str]
- integrations: List[str]

### Intermediate Contracts

**ApplicationIR**: Single source of truth
- entities: List[EntityIR] (with attributes, types, constraints)
- roles: List[str]
- features: List[str]
- permissions: List[PermissionIR]

### Output Contracts

**DatabaseSchema**: SQL schema
**APISchema**: REST API spec
**UISchema**: UI/pages spec
**AuthSchema**: Auth/permissions spec

Each contract is validated at every stage.

---

## Type System

Restricted set of types ensures deterministic generation:

```
uuid        → UUID in DB, uuid in APIs
text        → TEXT in DB, string in APIs
integer     → INTEGER in DB, number in APIs
boolean     → BOOLEAN in DB, boolean in APIs
timestamp   → TIMESTAMP in DB, ISO-8601 in APIs
float       → NUMERIC in DB, number in APIs
date        → DATE in DB, ISO-8601 in APIs
json        → JSONB in DB, object in APIs
array       → TEXT[] in DB, array in APIs
```

No ambiguity in code generation.

---

## Dependency Graph

Tracks component dependencies for incremental updates:

```
Node: SubscriptionEntity
├── SubscriptionTable (depends on entity)
├── SubscriptionAPI (depends on entity)
└── SubscriptionPage (depends on API)

If entity removed:
  Only regen table, API, page
  Don't touch User, Contact, etc.
```

---

## Error Recovery Strategy

Multi-level recovery:

### Level 1: Validation Repair
- Identify specific error
- Regenerate only failed component
- Re-validate

### Level 2: Assumption Adjustment
- Loosen assumptions
- Try alternate interpretation
- Regenerate

### Level 3: Graceful Degradation
- Generate minimal spec
- Document what's missing
- Still provide partial output

### Level 4: Escalation
- Provide diagnostic
- Suggest improvements to prompt
- Let user refine

---

## Performance Considerations

### Latency vs. Quality Tradeoff

**Fast Mode** (~2s):
- Intent extraction
- Basic IR generation
- Schema generation
- No validation/repair/simulation

**Reliable Mode** (~5-10s):
- Full intent extraction with detailed parsing
- Complete IR generation
- Full validation
- Targeted repairs if needed
- Runtime simulation
- Comprehensive diagnostics

### Optimization Techniques

- Parallel schema generation (4 generators run simultaneously)
- Cached LLM responses for common patterns
- Minimal re-generation in repair
- Efficient dependency tracking

---

## Security Considerations

### Input Validation
- Prompt length limits
- Character encoding validation
- XSS prevention in UI
- SQL injection prevention (parameterized queries)

### Output Validation
- Schema injection checks
- Permission verification
- Role validation
- API path sanitization

### API Security
- CORS enabled for frontend
- Rate limiting (recommended for production)
- Request size limits
- HTTPS in production

---

## Monitoring & Observability

### Metrics Collected
- Success rate (% successful compilations)
- Confidence score distribution
- Validation failure rate
- Repair frequency
- Generation latency
- LLM call count

### Logging Strategy
- [v0] prefixed debug logs
- Structured logging for production
- Error tracking
- Performance telemetry

---

## Extensibility Points

### Add New Generator
1. Implement `generate(ir: ApplicationIR) → Schema`
2. Add to pipeline
3. Update validation rules

### Add New Validator
1. Implement validation logic
2. Return ValidationError list
3. Add to validator chain

### Add New Repair Type
1. Implement repair logic
2. Add condition to repair engine
3. Update diagnostics

---

## Testing Strategy

### Unit Tests
- Schema generation correctness
- Type mappings
- Case conversions
- Validation rules

### Integration Tests
- Full pipeline end-to-end
- Error recovery
- Repair application

### Evaluation Tests
- 10 normal prompts (diverse domains)
- 10 edge cases (conflicting, vague, incomplete)
- Metrics: success rate, confidence, latency

---

## Future Enhancements

### Phase 2
- Database relationships (foreign keys)
- Migration scripts
- Advanced permission models

### Phase 3
- Frontend code generation (React/Vue)
- Backend code generation (Python/Node)
- Full deployable projects

### Phase 4
- Interactive refinement UI
- Real-time collaboration
- Version control integration

---

## References

- LLVM IR Design: https://llvm.org/docs/LangRef/
- Compiler Design Principles: Dragon Book
- JSON Schema Validation: https://json-schema.org/
- OpenAI Structured Outputs: https://platform.openai.com/docs/guides/json-mode
- Pydantic Validation: https://docs.pydantic.dev/

---

**Version**: 2.0.0  
**Last Updated**: June 5, 2024  
**Maintainer**: AI Compiler Team
