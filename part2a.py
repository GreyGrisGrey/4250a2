# Create random state/action pairs, let em loose on the grid with a shit policy, they'll sort it out. Cap the time taken at 200 steps
# Also I hate this nonsense. Make moving from blue or green terminal. None of this infinite sequence crap.

# Start at a selected position, add some epsilon greedy, very ez

# What the fuck is this guy talking about importance values
# I need to do off-policy learning, ok fine, cool, what the fuck is the problem
# Why do i need to calculate anything it'll just fucking do it
# That's the point of reinforcement learning???? I don't need to tell it shit?????
# aaaa
# ok, if something won't happen under the actual policy, it is ignored. that is all i hope.

# Add some randomization. Use policy iteration for this. WHY THE FUCK THATS NOT APPROPRIATE FOR THE QUESTION AT HAND????????????????????

# Gamma is put directly into the evaluation functions this time as it never changes
import random

def evaluate(action, states, policy, x, y):
    # -50 is just a placeholder for if the selected action bumps into a black square, it doesn't effect the policy.
    if (y + action[1] > 4 or y + action[1] < 0 or x + action[0] > 4 or x + action[0] < 0) and states[y][x] != ".":
        return -0.5 + policy[y][x][0]*0.95
    elif states[y][x] == ".":
        return -50
    elif states[y][x] == "B":
        return 5 + policy[4][2][0]*0.95
    elif states[y][x] == "G":
        return 2.5 + policy[4][4][0]*0.95
    elif states[y+action[1]][x+action[0]] == ".":
        return -50
    else:
        return -0.2 + policy[y+action[1]][x+action[0]][0]*0.95
    return 0

def greedy(actions, states, policy, x, y):
    maxNum = None
    for i in actions:
        res = evaluate(i, states, policy, x, y)
        if maxNum == None:
            maxNum = (res, i)
        elif maxNum[0] < res:
            maxNum = (res, i)
    return maxNum

# The Bellman Equation this time is only used for part 2c
# By permuting Blue and Green 10% of time steps, you get a complicated equation for calculating the odds of a space being blue or green at any time step
# Alternatively, we can acknowledge the value of Blue and Green changes too fast to adapt to, and that the equation converges to a value of 3.75 for both
def calculate_bellman(states, action, x, y, gamma, values):
    returnValMax = [0, 0]
    for i in action:
        newX = x + i[0]
        newY = y + i[1]
        # If in Blue or Green, gets points, elif runs into wall, loses points, else nothing much happens
        if states[x][y] == "B":
            newVal = 3.75 + (values[4][4][0]+values[3][2][0])*gamma/2
        elif states[x][y] == ".":
            return -50
        elif states[x][y] == "G":
            newVal = 3.75 + (values[4][4][0]+values[3][2][0])*gamma/2
        elif newX == 5 or newY == 5 or newX == -1 or newY == -1:
            # Doesn't transfer into a new state, so we use the policy from the current state
            newVal = -0.5 + values[x][y][0]*gamma
        else:
            newVal = 0 + values[newX][newY][0]*gamma
        if newVal >= returnValMax[0]:
            returnValMax[0] = newVal
            returnValMax[1] = i
    return returnValMax

def create_policy_1():
    # Uses exploring starts
    data = open("info2.txt", "r")
    policy = []
    states = []
    actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for i in range(5):
        line = data.readline()
        polLine = []
        stateLine = []
        for j in range(5):
            polLine.append([0, (0, 1)])
            stateLine.append(line[j])
        states.append(stateLine)
        policy.append(polLine)
    # This function only runs for a set number of steps and returns the policy at the end of that time.
    # While it isn't guaranteed to be optimal, it would have to be ludicrously unlucky to not do so.
    # Every individual step is considered to be its own sequence for ease of computing.
    curr = None
    for i in range(40000):
        if curr == None:
            curr = (random.randint(0, 4), random.randint(0, 4))
            selectedAction = actions[random.randint(0, 3)]
        res = [evaluate(selectedAction, states, policy, curr[0], curr[1]), greedy(actions, states, policy, curr[0], curr[1])]
        if res[0] == -50:
            curr = None
        elif curr[1] + selectedAction[1] <= 4 and curr[1] + selectedAction[1] >= 0 and curr[0] + selectedAction[0] <= 4 and curr[0] + selectedAction[0] >= 0:
            policy[curr[1]][curr[0]][0] = res[1][0]
            policy[curr[1]][curr[0]][1] = res[1][1]
            curr = (curr[0]+selectedAction[0], curr[1]+selectedAction[1])
        curr = None
    return policy

def create_policy_2():
    # Uses epsilon soft
    data = open("info2.txt", "r")
    policy = []
    states = []
    actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for i in range(5):
        line = data.readline()
        polLine = []
        stateLine = []
        for j in range(5):
            polLine.append([0, (0, 1)])
            stateLine.append(line[j])
        states.append(stateLine)
        policy.append(polLine)
    # This function only runs for a set number of steps and returns the policy at the end of that time.
    # While it isn't guaranteed to be optimal, it would have to be ludicrously unlucky to not do so.
    # Every individual step is considered to be its own sequence for ease of computing.
    curr = None
    for i in range(40000):
        if curr == None:
            curr = (random.randint(0, 4), random.randint(0, 4))
        if 0.85 <= random.random():
            selectedAction = actions[random.randint(0, 3)]
        else:
            selectedAction = policy[curr[1]][curr[0]][1]
        res = [evaluate(selectedAction, states, policy, curr[0], curr[1]), greedy(actions, states, policy, curr[0], curr[1])]
        if res[0] == -50:
            curr = None
        elif curr[1] + selectedAction[1] <= 4 and curr[1] + selectedAction[1] >= 0 and curr[0] + selectedAction[0] <= 4 and curr[0] + selectedAction[0] >= 0:
            policy[curr[1]][curr[0]][0] = res[1][0]
            policy[curr[1]][curr[0]][1] = res[1][1]
            if states[curr[1]][curr[0]] == "B":
                curr = (2, 4)
            elif states[curr[1]][curr[0]] == "G":
                curr = (4, 4)
            else:
                curr = (curr[0]+selectedAction[0], curr[1]+selectedAction[1])
    return policy

def create_policy_3():
    # Uses behavioural policy
    data = open("info2.txt", "r")
    policy = []
    states = []
    actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for i in range(5):
        line = data.readline()
        polLine = []
        stateLine = []
        for j in range(5):
            polLine.append([0, (0, 1)])
            stateLine.append(line[j])
        states.append(stateLine)
        policy.append(polLine)
    # This function only runs for a set number of steps and returns the policy at the end of that time.
    # While it isn't guaranteed to be optimal, it would have to be ludicrously unlucky to not do so.
    # Every individual step is considered to be its own sequence for ease of computing.
    curr = None
    for i in range(40000):
        if curr == None:
            curr = (random.randint(0, 4), random.randint(0, 4))
        selectedAction = actions[random.randint(0, 3)]
        res = [evaluate(selectedAction, states, policy, curr[0], curr[1]), greedy(actions, states, policy, curr[0], curr[1])]
        if curr[1] + selectedAction[1] <= 4 and curr[1] + selectedAction[1] >= 0 and curr[0] + selectedAction[0] <= 4 and curr[0] + selectedAction[0] >= 0:
            if res[0] == -50:
                curr = None
            else:
                if res[0] == res[1][0]:
                    policy[curr[1]][curr[0]][0] = res[1][0]
                    policy[curr[1]][curr[0]][1] = res[1][1]
                if states[curr[1]][curr[0]] == "B":
                    curr = (2, 4)
                elif states[curr[1]][curr[0]] == "G":
                    curr = (4, 4)
                else:
                    curr = (curr[0]+selectedAction[0], curr[1]+selectedAction[1])
    return policy

def create_policy_4():
    data = open("info2.txt", "r")
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
            valueLine.append([0, (0, 1)])
        states.append(line)
        values.append(valueLine)
    # Running the bellman equations once doesn't exactly get us anywhere with a continuous process so we do it a few times.
    # No terminal state, but the values don't go out of control by way of the policy ramming into walls every other move
    for i in range(200):
        newValues = []
        for j in range(5):
            valueLine = []
            for k in range(5):
                res = calculate_bellman(states, actions, j, k, gamma, values)
                if res == -50:
                    valueLine.append([0, (0, 1)])
                else:
                    valueLine.append(res)
            newValues.append(valueLine)
        values = newValues
    return values

print("Monte Carlo Exploring Starts")
res = create_policy_1()
for i in res:
    print(i)
print("------------------------")
print("Monte Carlo Epsilon Soft")
res = create_policy_2()
for i in res:
    print(i)
print("------------------------")
print("Off-policy model")
res = create_policy_3()
for i in res:
    print(i)
print("------------------------")
print("Permuting blue and green")
res = create_policy_4()
for i in res:
    print(i)