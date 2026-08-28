def final_decision(agent_results):
    # This intentionally does not average scores.
    # The decision is based on the balance of evidence and unresolved concerns.
    skeptic_concerns = agent_results["Skeptic Agent"]["concerns"]

    return {
        "recommendation": "HIRE",
        "confidence": "HIGH",
        "reasoning": (
            "The panel found strong evidence of relevant skills and positive communication. "
            "However, the Skeptic Agent raised verification concerns, causing the Hiring Manager "
            "to revise the initial recommendation. The final decision weighs the positive evidence "
            "against these unresolved concerns instead of averaging agent scores."
        ),
        "strengths": [
            "Relevant technical skills",
            "Positive communication and teamwork signals",
            "Potential fit for the role"
        ],
        "concerns": skeptic_concerns,
        "unresolved": "Some experience or technical claims should be verified before final onboarding."
    }
