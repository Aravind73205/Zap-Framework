class GuardrailViolation(Exception):
    """
    Raised when a guardrail rule is violated.
    This is a control-flow exception that stops execution.
    """
    pass
