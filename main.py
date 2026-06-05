import argparse
import json
from pathlib import Path
from langgraph.graph import StateGraph, START, END
from src.env import USER_PRESET
from src.state import CorporateState
from src.agents.ceo import run_ceo
from src.agents.worker import run_generalized_worker
from config.schema import BusinessOnboardingProfile
from config.presets import get_preset

# ==========================================
# 1. The Polymorphic Wrapper
# ==========================================
def dynamic_department_node(state: CorporateState):
    """
    This wrapper intercepts the graph execution. It looks at what the CEO requested
    (state["next_action"]) and passes that name into our generalized worker.
    """
    target_department = state["next_action"]
    return run_generalized_worker(state, target_department)

# ==========================================
# 2. Graph Topology definition
# ==========================================
def route_from_ceo(state: CorporateState) -> str:
    """If the CEO says finish, end the graph. Otherwise, trigger the dynamic worker."""
    if state.get("task_complete"):
        return END
    return "dynamic_worker"

# Initialize the Graph with our State schema
workflow = StateGraph(CorporateState)

# Add our two core nodes
workflow.add_node("ceo", run_ceo)
workflow.add_node("dynamic_worker", dynamic_department_node)

# Flow: Start -> CEO
workflow.add_edge(START, "ceo")

# Flow: CEO -> (Decision) -> Worker OR End
workflow.add_conditional_edges(
    "ceo",
    route_from_ceo,
    {
        "dynamic_worker": "dynamic_worker",
        END: END
    }
)

# Flow: Worker -> CEO (Mandatory review loop)
workflow.add_edge("dynamic_worker", "ceo")

# Compile the engine!
app = workflow.compile()

# ==========================================
# 3. Configuration loading
# ==========================================

def load_profile(path: str | None = None, preset: str | None = None, raw_config: dict | None = None) -> dict:
    if raw_config is not None:
        try:
            return BusinessOnboardingProfile(**raw_config).model_dump()
        except Exception:
            if preset:
                raw_preset = get_preset(preset)
                return BusinessOnboardingProfile(**raw_preset).model_dump()
            raise

    if path:
        config_path = Path(path)
        with config_path.open("r", encoding="utf-8") as handle:
            raw = json.load(handle)
        return BusinessOnboardingProfile(**raw).model_dump()

    preset_name = preset or USER_PRESET
    raw_preset = get_preset(preset_name)
    return BusinessOnboardingProfile(**raw_preset).model_dump()


def build_initial_state(profile: dict, user_prompt: str) -> CorporateState:
    return {
        "messages": [{"role": "user", "parts": [user_prompt]}],
        "business_profile": profile,
        "active_departments": [dept["name"] for dept in profile.get("active_departments", [])],
        "current_task": user_prompt,
        "next_action": "",
        "task_complete": False
    }


def format_event_output(event: dict) -> str:
    output_lines = []
    for node, state_update in event.items():
        output_lines.append(f"⚙️  Node Completed: {node.upper()}")
        if node == "ceo":
            output_lines.append(f"   -> CEO delegated to: {state_update.get('next_action', 'finish')}")
        if node == "dynamic_worker":
            if state_update.get("messages"):
                output_lines.append(f"   -> Output: {state_update['messages'][-1]['parts'][0]}")
        output_lines.append("-" * 50)
    return "\n".join(output_lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the YOUR_OWN_BUSINESS_CREW automation engine.")
    parser.add_argument("--prompt", type=str, default="Create a clear plan for my next internship search.", help="The user task or request to automate.")
    parser.add_argument("--preset", type=str, default="student", help="Which user preset to load: student, founder, creator.")
    parser.add_argument("--config", type=str, default=None, help="Optional path to a JSON config file.")
    args = parser.parse_args()

    user_prompt = args.prompt
    validated_profile = load_profile(path=args.config, preset=args.preset)
    initial_state = build_initial_state(validated_profile, user_prompt)

    company_name = validated_profile.get("company_name") or validated_profile.get("organization_name") or validated_profile.get("user_profile", {}).get("name", "User")
    print(f"--- Booting {company_name} Environment ---\n")

    for event in app.stream(initial_state):
        print(format_event_output(event))

    print("\n✅ Task Fully Automated and Completed.")