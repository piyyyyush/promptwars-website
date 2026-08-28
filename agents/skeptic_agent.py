def analyze(resume, transcript, job_description):
    return {
        "name": "Skeptic Agent",
        "icon": "🕵️",
        "verdict": "CONCERNED",
        "confidence": 70,
        "strengths": ["Some relevant claims are supported."],
        "concerns": [
            "Some experience claims may require verification.",
            "Transcript evidence may not fully support every resume claim."
        ],
        "evidence": '"The candidate describes experience, but some details are not clearly explained in the interview."',
        "initial_opinion": "Further verification is required before a final decision."
    }
