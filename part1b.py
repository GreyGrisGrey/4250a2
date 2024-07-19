
def eval_state(states, action, x, y, gamma, policy):
    newX = x + action[0]
    newY = y + action[1]
    # If in Blue or Green, gets points, elif runs into wall, loses points, else nothing much happens
    if states[x][y] == "B":
        return [5 + policy[3][2][0]*gamma, action]
    elif states[x][y] == "G":
        return [2.5 + (policy[4][4][0]+policy[3][2][0])*0.5*gamma, action]
    elif newX == 5 or newY == 5 or newX == -1 or newY == -1:
        # Doesn't transfer into a new state, so we use the policy from the current state
        return [-0.5 + policy[x][y][0]*gamma, action]
    return [0 + policy[newX][newY][0]*gamma, action]

def calculate_bellman(states, action, x, y, gamma, values):
    returnValAvg = 0
    returnValMax = [0, 0]
    for i in action:
        newX = x + i[0]
        newY = y + i[1]
        # If in Blue or Green, gets points, elif runs into wall, loses points, else nothing much happens
        if states[x][y] == "B":
            newVal = 5 + values[3][2][0]*gamma
        elif states[x][y] == "G":
            newVal = 2.5 + (values[4][4][0]+values[3][2][0])*gamma*0.5
        elif newX == 5 or newY == 5 or newX == -1 or newY == -1:
            newVal = -0.5 + values[x][y][0]*gamma
        else:
            newVal = 0 + values[newX][newY][0]*gamma
        if newVal >= returnValMax[0]:
            returnValMax[0] = newVal
            returnValMax[1] = i
        returnValAvg += newVal
    return returnValMax

def value_iteration():
    data = open("info.txt", "r")
    states = []
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
            valueLine.append([0, 0])
        states.append(line)
        values.append(valueLine)
    # Converges to roughly where it needs to be after ~100 iterations, but I feel more secure with 200 iterations. Small inefficiency.
    # It is very close to the code for the bellman equation, but this time it uses a max function.
    # We use policy improvement by having a policy that improves each time we iterate the values
    # I don't know what else to do with this. I am baffled. What on god's green earth
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
            valueLine.append([0, 1])
        states.append(line)
        values.append(valueLine)
    # Running the bellman equations once doesn't exactly get us anywhere with a continuous process so we do it a few times.
    # No terminal state, but the values don't go out of control by way of the policy ramming into walls every other move
    # Evaluate every possible action under the current values, update policy and values so that the value is the max.
    # values contains [Vk, Pik]
    # values is a bit of a misnomer, each state is a two length list containing the expected value of the state at index 0 and the best action at index 1.
    for i in range(200):
        newValues = []
        for j in range(5):
            valueLine = []
            for k in range(5):
                valueLine.append(calculate_bellman(states, actions, j, k, gamma, values))
            newValues.append(valueLine)
        values = newValues
    return values

# Values of x and y are backwards in iterative policy evaluation
# They're right, but they're backwards
# how and why
print("--------------")
print("Value iteration")
res = value_iteration()
for i in res:
    print(i)
print("--------------")
print("Policy iteration")
res = iterative_policy_evaluation()
for i in res:
    print(i)