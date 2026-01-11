def find_weak_concepts(activities):
    """
    Rule:
    Same concept + score < 40 at least 3 times = weak concept
    """
    concept_counts = {}

    for activity in activities:
        if activity.score < 40:
            if activity.concept not in concept_counts:
                concept_counts[activity.concept] = 0
            concept_counts[activity.concept] += 1

    weak_concepts = []
    for concept, count in concept_counts.items():
        if count >= 3:
            weak_concepts.append(concept)

    return weak_concepts
