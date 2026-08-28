def run_debate(agent_results):
    """Demo debate. Replace later with sequential LLM calls."""
    return [
        {
            "agent": "Technical Agent",
            "icon": "💻",
            "type": "statement",
            "text": "The candidate demonstrates relevant technical knowledge and appears capable of handling the core technical responsibilities.",
            "evidence": agent_results["Technical Agent"]["evidence"]
        },
        {
            "agent": "Skeptic Agent",
            "icon": "🕵️",
            "type": "response",
            "text": "I disagree with treating the technical claims as fully verified. Some claims are mentioned, but the interview does not provide enough depth to validate all of them.",
            "evidence": agent_results["Skeptic Agent"]["evidence"]
        },
        {
            "agent": "HR / Culture Agent",
            "icon": "👥",
            "type": "agreement",
            "text": "I agree that missing information should not be treated as proof. However, the communication evidence remains positive.",
            "evidence": agent_results["HR / Culture Agent"]["evidence"]
        },
        {
            "agent": "Hiring Manager Agent",
            "icon": "💼",
            "type": "opinion_change",
            "before": "STRONG HIRE",
            "after": "HIRE WITH CONCERNS",
            "text": "After reviewing the Skeptic Agent's evidence, I am changing my recommendation. The candidate is still promising, but important claims should be verified."
        }
    ]
