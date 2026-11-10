def learn(memory, condition, action):
    """Apprentissage supervisé · la discipline de mémoire refuse
    toute règle contenant un secret (lève MemoryRefused)."""
    memory.add_rule(condition, action)