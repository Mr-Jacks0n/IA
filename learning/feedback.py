def learn(memory, condition, action):
    memory.rules.append({
        "condition": condition,
        "action": action
    })
    memory.save_rules()