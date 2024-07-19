# The optimal policy given by different runs may be different from other runs, this is just because there are multiple optimal policies

def eval_state(states, action, x, y, gamma, policy):
    newX = x + action[0]
    newY = y + action[1]
    # If in Blue or Green, gets points, elif runs into wall, loses points, else nothing much happens
    if states[x][y] == "B":
        return 5 + policy[3][2]*gamma
    elif states[x][y] == "G":
        return 2.5 + (policy[4][4]+policy[3][2])*gamma*0.5
    elif newX == 5 or newY == 5 or newX == -1 or newY == -1:
        # Doesn't transfer into a new state, so we use the policy from the current state
        return -0.5 + policy[x][y]*gamma
    return 0 + policy[newX][newY]*gamma

def calculate_bellman(states, action, x, y, gamma, values):
    returnValAvg = 0
    returnValMax = [0, 0]
    for i in action:
        newX = x + i[0]
        newY = y + i[1]
        # If in Blue or Green, gets points, elif runs into wall, loses points, else nothing much happens
        if states[x][y] == "B":
            newVal = 5 + values[3][2]*gamma
        elif states[x][y] == "G":
            newVal = 2.5 + (values[4][4]+values[3][2])*gamma
        elif newX == 5 or newY == 5 or newX == -1 or newY == -1:
            # Doesn't transfer into a new state, so we use the policy from the current state
            newVal = -0.5 + values[x][y]*gamma
        else:
            newVal = 0 + values[newX][newY]*gamma
        if newVal >= returnValMax[0]:
            returnValMax[0] = newVal
            returnValMax[1] = i
        returnValAvg += newVal
    return returnValAvg*0.25

def value_iteration():
    data = open("info.txt", "r")
    states = []
    policy = []
    values = []
    actions = ((0, 1), (1, 0), (0, -1), (-1, 0))
    gamma = 0.95
    for i in data:
        i = i.strip()
        line = []
        policyLine = []
        valueLine = []
        for j in i:
            line.append(j)
            policyLine.append(0)
            valueLine.append(0)
        states.append(line)
        policy.append(policyLine)
        values.append(valueLine)
    # Converges to roughly where it needs to be after ~100 iterations, but I feel more secure with 200 iterations. Small inefficiency.
    # It is very close to the code for the bellman equation, but this time it uses a max function.
    for i in range(200):
        newValues = []
        for j in range(5):
            valueLine = []
            for k in range(5):
                # Ugly line, but nicer than extending it
                valueLine.append(max(eval_state(states, actions[0], j, k, gamma, values), eval_state(states, actions[1], j, k, gamma, values), eval_state(states, actions[2], j, k, gamma, values), eval_state(states, actions[3], j, k, gamma, values)))
            newValues.append(valueLine)
        values = newValues
    return values

def iterative_policy_evaluation():
    # Sum of successor states, Sum of rewards, sum of actions 
    # (actions given state)(reward + (gamma)(value of being in successor state))
    data = open("info.txt", "r")
    states = []
    values = []
    actions = ((0, 1), (1, 0), (0, -1), (-1, 0))
    gamma = 0.95
    for i in data:
        i = i.strip()
        line = []
        valueLine = []
        for j in i:
            line.append(j)
            valueLine.append(0)
        states.append(line)
        values.append(valueLine)
    # Running the bellman equations once doesn't exactly get us anywhere with a continuous process so we do it a few times.
    # No terminal state, but the values don't go out of control by way of the policy ramming into walls every other move
    for i in range(200):
        newValues = []
        for j in range(5):
            valueLine = []
            for k in range(5):
                valueLine.append(calculate_bellman(states, actions, j, k, gamma, values))
            newValues.append(valueLine)
        values = newValues
    return values

print("Value Iteration")
res = value_iteration()
for i in res:
    print(i)
print("---------------")
print("Iterative Policy Evaluation")
res = iterative_policy_evaluation()
for i in res:
    print(i)