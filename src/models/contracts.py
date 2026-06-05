from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal


# Type definitions for stronger type safety
ValidFieldTypes = Literal["uuid", "text", "integer", "boolean", "timestamp", "float", "date", "json", "array"]
ValidHTTPMethods = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]


# -----------------------------
# Risk Analysis
# -----------------------------

class RiskReport(BaseModel):
    ambiguity_score: float
    conflict_score: float
    completeness_score: float
    issues: List[str] = Field(default_factory=list)


# -----------------------------
# Intent Extraction with Deep Attributes
# -----------------------------

class AttributeModel(BaseModel):
    """Deep attribute model with type information"""
    name: str
    type: ValidFieldTypes = "text"
    nullable: bool = False
    is_primary: bool = False
    description: str = ""

class EntityModel(BaseModel):
    """Structured entity with full attribute definitions"""
    name: str
    description: str = ""
    attributes: List[AttributeModel] = Field(default_factory=list)

class IntentModel(BaseModel):
    """Enhanced intent model capturing full app structure"""
    app_name: str
    description: str = ""
    entities: List[EntityModel] = Field(default_factory=list)
    roles: List[str] = Field(default_factory=list)
    features: List[str] = Field(default_factory=list)
    integrations: List[str] = Field(default_factory=list)


# -----------------------------
# Assumptions
# -----------------------------

class Assumption(BaseModel):
    reason: str
    assumption: str


class AssumptionReport(BaseModel):
    assumptions: List[Assumption] = Field(default_factory=list)


# -----------------------------
# IR Models (Enhanced)
# -----------------------------

class AttributeIR(BaseModel):
    name: str
    type: ValidFieldTypes = "text"
    nullable: bool = False
    is_primary: bool = False
    description: str = ""

class EntityIR(BaseModel):
    name: str
    description: str = ""
    attributes: List[AttributeIR] = Field(default_factory=list)

class WorkflowIR(BaseModel):
    name: str
    description: str
    steps: List[str] = Field(default_factory=list)

class PermissionIR(BaseModel):
    role: str
    permissions: List[str] = Field(default_factory=list)

class IntegrationIR(BaseModel):
    name: str
    config: Dict = Field(default_factory=dict)

class ApplicationIR(BaseModel):
    version: int = 1
    app_name: str
    description: str = ""
    entities: List[EntityIR] = Field(default_factory=list)
    roles: List[str] = Field(default_factory=list)
    features: List[str] = Field(default_factory=list)
    workflows: List[WorkflowIR] = Field(default_factory=list)
    permissions: List[PermissionIR] = Field(default_factory=list)
    integrations: List[IntegrationIR] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)


# -----------------------------
# Database Schema (Enhanced)
# -----------------------------

class ColumnSchema(BaseModel):
    name: str
    type: ValidFieldTypes = "text"
    nullable: bool = False
    is_primary: bool = False
    is_foreign: bool = False
    foreign_table: Optional[str] = None
    default_value: Optional[str] = None

class TableSchema(BaseModel):
    name: str
    description: str = ""
    columns: List[ColumnSchema] = Field(default_factory=list)

class DatabaseSchema(BaseModel):
    tables: List[TableSchema] = Field(default_factory=list)


# -----------------------------
# API Schema (Enhanced)
# -----------------------------

class ParameterSchema(BaseModel):
    name: str
    type: ValidFieldTypes = "text"
    required: bool = True
    description: str = ""

class EndpointSchema(BaseModel):
    path: str
    method: ValidHTTPMethods = "GET"
    entity_name: str
    description: str = ""
    parameters: List[ParameterSchema] = Field(default_factory=list)
    response_fields: List[str] = Field(default_factory=list)
    requires_auth: bool = False
    required_roles: List[str] = Field(default_factory=list)

class APISchema(BaseModel):
    endpoints: List[EndpointSchema] = Field(default_factory=list)


# -----------------------------
# UI Schema (Enhanced)
# -----------------------------

class ComponentSchema(BaseModel):
    name: str
    type: str
    entity_binding: Optional[str] = None
    properties: Dict = Field(default_factory=dict)

class PageSchema(BaseModel):
    name: str
    description: str = ""
    route: str = ""
    components: List[ComponentSchema] = Field(default_factory=list)
    requires_auth: bool = False
    required_roles: List[str] = Field(default_factory=list)

class UISchema(BaseModel):
    pages: List[PageSchema] = Field(default_factory=list)


# -----------------------------
# Auth Schema (Enhanced)
# -----------------------------

class PermissionSchema(BaseModel):
    name: str
    description: str = ""
    resource: str
    action: str

class RoleSchema(BaseModel):
    name: str
    description: str = ""
    permissions: List[PermissionSchema] = Field(default_factory=list)

class AuthSchema(BaseModel):
    roles: List[RoleSchema] = Field(default_factory=list)


# -----------------------------
# Validation (Enhanced)
# -----------------------------

class ValidationError(BaseModel):
    type: str
    message: str
    severity: Literal["error", "warning"] = "error"
    component: str = ""
    path: str = ""

class ValidationReport(BaseModel):
    status: Literal["PASS", "FAIL", "WARN"] = "PASS"
    errors: List[ValidationError] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    total_issues: int = 0


# -----------------------------
# Repair (Enhanced)
# -----------------------------

class RepairAction(BaseModel):
    action: str
    target: str
    details: str = ""
    success: bool = True

class RepairReport(BaseModel):
    repairs: List[RepairAction] = Field(default_factory=list)
    total_repairs: int = 0


# -----------------------------
# Runtime (Enhanced)
# -----------------------------

class RuntimeReport(BaseModel):
    status: Literal["PASS", "FAIL"] = "PASS"
    registered_tables: int = 0
    registered_endpoints: int = 0
    registered_pages: int = 0
    errors: List[str] = Field(default_factory=list)


# -----------------------------
# Diagnostics (Enhanced)
# -----------------------------

class DiagnosticsReport(BaseModel):
    warnings: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    repairs: List[str] = Field(default_factory=list)
    confidence: float = 1.0
    rules_version: str = "2.0"
    template_version: str = "2.0"
    generation_time_ms: float = 0.0
    llm_calls: int = 0


class ConflictReport(BaseModel):
    conflict_score: float
    issues: List[str] = Field(default_factory=list)


# -----------------------------
# Intent Extraction Result
# -----------------------------

class IntentExtractionResult(BaseModel):
    intent: IntentModel
    confidence: float
    raw_response: str


class IntentValidationError(BaseModel):
    message: str


class IntentValidationReport(BaseModel):
    status: str
    errors: List[IntentValidationError] = Field(default_factory=list)
