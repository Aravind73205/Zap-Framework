from typing import Dict, Any

from engine.orchestrator import WorkflowStep

# These agents are placeholders for now, real implementations coming later


# adapter fns

def pass_validated_input(prev_output: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Adapter btwn Input validator agent -> Audience analyzer agent
    just pass the validated stuff to nxt agent
    """

    return prev_output.get("validated_input", {})


def prepare_value_prop_input(prev_output: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    
    # same for AudienceAnalyzer -> ValueProposition
    # Combines validated input (from contxt memory) + audience insights (from previous agent)

    validated = context.get("marketing.input_validator", {}).get("validated_input", {})
    return {
        "product_description": validated.get("product_description"),
        "goal": validated.get("goal"),
        "audience_insights": prev_output.get("audience_insights"),
    }


def prepare_content_outline_input(prev_output: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    validated = context.get("marketing.input_validator", {}).get("validated_input", {})
    
    #Value prop -> Content outline

    return {
        "core_message": prev_output.get("core_message"),
        "key_benefits": prev_output.get("key_benefits"),
        "goal": validated.get("goal"),
    }



# Workflow factory

def create_marketing_workflow(
    input_validator,
    audience_analyzer,
    value_proposition_agent,
    content_outline_generator,
):
    """
    Builds the sequence of steps for marketing content generation.
    Agents are passed in so we can swap/mock them easily.
    """

    steps = [
        WorkflowStep(
            agent=input_validator
        ),

        WorkflowStep(
            agent=audience_analyzer,
            input_transformer=pass_validated_input
        ),

        WorkflowStep(
            agent=value_proposition_agent,
            input_transformer=prepare_value_prop_input
        ),

        WorkflowStep(
            agent=content_outline_generator,
            input_transformer=prepare_content_outline_input
        ),
    ]

    return steps
