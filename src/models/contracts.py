from pydantic import BaseModel, Field
from typing import List, Optional, Dict


# -----------------------------
# Risk Analysis
# -----------------------------

class RiskReport(BaseModel):
    ambiguity_score: float
    conflict_score: float
    completeness_score: float
    issues: List[str] = Field(default_factory=list)


# -----------------------------
# Intent Extraction
# -----------------------------

class IntentModel(BaseModel):
    app_name: str
    entities: List[str]= Field(default_factory=list)
    roles: List[str]= Field(default_factory=list)
    features: List[str]= Field(default_factory=list)


# -----------------------------
# Assumptions
# -----------------------------

class Assumption(BaseModel):
    reason: str
    assumption: str


class AssumptionReport(BaseModel):
    assumptions: List[Assumption]= Field(default_factory=list)


# -----------------------------
# IR Models
# -----------------------------

class AttributeIR(BaseModel):
    name: str
    type: str = "string"


class EntityIR(BaseModel):
    name: str
    attributes: List[AttributeIR] = Field(default_factory=list)


class WorkflowIR(BaseModel):
    name: str
    description: str


class PermissionIR(BaseModel):
    role: str
    permissions: List[str]= Field(default_factory=list)


class ApplicationIR(BaseModel):
    version: int = 1

    app_name: str

    entities: List[EntityIR] = Field(default_factory=list)

    roles: List[str] = Field(default_factory=list)

    features: List[str] = Field(default_factory=list)

    workflows: List[WorkflowIR] = Field(default_factory=list)

    permissions: List[PermissionIR] = Field(default_factory=list)

    integrations: List[str] = Field(default_factory=list)

    assumptions: List[str] = Field(default_factory=list)


# -----------------------------
# Database Schema
# -----------------------------

class ColumnSchema(BaseModel):
    name: str
    type: str


class TableSchema(BaseModel):
    name: str
    columns: List[ColumnSchema]= Field(default_factory=list)


class DatabaseSchema(BaseModel):
    tables: List[TableSchema]= Field(default_factory=list)


# -----------------------------
# API Schema
# -----------------------------

class EndpointSchema(BaseModel):
    path: str
    method: str
    entity_name: str
    description: str = ""


class APISchema(BaseModel):
    endpoints: List[EndpointSchema]= Field(default_factory=list)


# -----------------------------
# UI Schema
# -----------------------------

class PageSchema(BaseModel):
    name: str
    components: List[str]= Field(default_factory=list)


class UISchema(BaseModel):
    pages: List[PageSchema]= Field(default_factory=list)


# -----------------------------
# Auth Schema
# -----------------------------

class RoleSchema(BaseModel):
    name: str
    permissions: List[str]= Field(default_factory=list)


class AuthSchema(BaseModel):
    roles: List[RoleSchema]= Field(default_factory=list)


# -----------------------------
# Validation
# -----------------------------

class ValidationError(BaseModel):
    type: str
    message: str


class ValidationReport(BaseModel):
    status: str
    errors: List[ValidationError] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


# -----------------------------
# Repair
# -----------------------------

class RepairReport(BaseModel):
    repair_action: str
    target: str
    details: str = ""


# -----------------------------
# Runtime
# -----------------------------

class RuntimeReport(BaseModel):
    status: str

    registered_tables: int = 0

    registered_endpoints: int = 0

    registered_pages: int = 0


# -----------------------------
# Diagnostics
# -----------------------------

class DiagnosticsReport(BaseModel):
    warnings: List[str] = Field(default_factory=list)

    assumptions: List[str] = Field(default_factory=list)

    repairs: List[str] = Field(default_factory=list)

    confidence: float = 1.0

    rules_version: str = "1.0"

    template_version: str = "1.0"



class ConflictReport(BaseModel):

    conflict_score: float

    issues: List[str] = Field(
        default_factory=list
    )
class IntentExtractionResult(BaseModel):

    intent: IntentModel

    confidence: float

    raw_response: str
class IntentValidationError(BaseModel):
    message: str


class IntentValidationReport(BaseModel):

    status: str

    errors: List[IntentValidationError] = Field(
        default_factory=list
    )