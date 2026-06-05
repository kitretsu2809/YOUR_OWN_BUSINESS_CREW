from typing import TypedDict, List, Dict, Any

class MessageDict(TypedDict):
    role: str      # 'user', 'model', or 'system'
    parts: List[str]

class CorporateState(TypedDict, total=False):
    """
    The generalized corporate memory object. Holds the conversation history,
    the custom business metadata, and dynamic routing targets.
    """
    messages: List[MessageDict]       # The unfolding workspace conversation log
    business_profile: Dict[str, Any]  # The validated Pydantic onboarding data
    active_departments: List[str]     # Dynamically loaded departments (e.g. ['finance', 'legal', 'design'])
    next_action: str                 # The dynamic routing target chosen by the CEO
    task_complete: bool              # Termination toggle
    current_task: str                # User's primary task or request
    user_preferences: Dict[str, Any] # Optional user preferences for personalization
