from pydantic import BaseModel, Field
from typing import List, Optional

class UserProfile(BaseModel):
    name: str = Field(..., description="User name, student name, founder name, or creator name")
    role: str = Field(..., description="The user's identity or role, e.g. student, founder, creator")
    specialization: Optional[str] = Field(None, description="Primary expertise or focus area")
    objective: str = Field(..., description="The main goal the user is trying to achieve")
    preferred_tone: str = Field(default="Professional", description="Preferred writing tone for generated output")
    about: Optional[str] = Field(None, description="Optional background context about the user")

class DepartmentConfig(BaseModel):
    name: str = Field(..., description="Name of the department (e.g., communication, research)")
    focus_areas: List[str] = Field(..., description="Specific goals or areas of execution")
    skills: List[str] = Field(default_factory=list, description="Skills or capabilities the department supports")
    allowed_tools: List[str] = Field(default_factory=list, description="List of functional tools assigned")

class BusinessOnboardingProfile(BaseModel):
    company_name: Optional[str] = Field(None, description="Optional company or organization name")
    organization_name: Optional[str] = Field(None, description="Optional startup or creator brand name")
    industry: Optional[str] = Field(None, description="Primary vertical or domain")
    target_audience: Optional[str] = Field(None, description="Main audience, customer, or stakeholder")
    brand_tone: str = Field(default="Professional", description="Communication style guideline for generated output")
    user_profile: UserProfile = Field(..., description="Profile metadata for the person using the system")
    active_departments: List[DepartmentConfig] = Field(..., description="Matrix of active operational departments")