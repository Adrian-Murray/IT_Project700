# test_adjective_mapping.py

def test_get_factor():
    adjectives = {
        "assertive": "Dominance",
        "sociable": "Extraversion",
        "calm": "Patience",
        "structured": "Formality",
        "assertive": "Dominance", "confident": "Dominance", "decisive": "Dominance",
        "ambitious": "Dominance", "bold": "Dominance", "commanding": "Dominance",
        "competitive": "Dominance", "determined": "Dominance", "independent": "Dominance",
        "sociable": "Extraversion", "outgoing": "Extraversion", "friendly": "Extraversion",
        "communicative": "Extraversion", "enthusiastic": "Extraversion", "persuasive": "Extraversion",
        "lively": "Extraversion", "talkative": "Extraversion", "engaging": "Extraversion",
        "calm": "Patience", "steady": "Patience", "patient": "Patience",
        "consistent": "Patience", "reliable": "Patience", "composed": "Patience",
        "accommodating": "Patience", "predictable": "Patience", "supportive": "Patience",
        "structured": "Formality", "precise": "Formality", "detail-oriented": "Formality",
        "methodical": "Formality", "organized": "Formality", "careful": "Formality",
        "disciplined": "Formality", "conscientious": "Formality", "rule-following": "Formality"
    }

    for adjective, expected_factor in adjectives.items():
        factor = get_factor(adjective)
        assert factor == expected_factor, f"Error: {adjective} -> Expected {expected_factor}, got {factor}"

    print("All tests passed.")

if __name__ == "__main__":
    from app import get_factor
    test_get_factor()
