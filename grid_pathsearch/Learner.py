__author__ = 'Charles Zhang'
import World
import threading
import time
import random
import csv

random.seed(0)

discount = 0.95
epsilon = 0.25
e_decay = 0.7
alpha = 0.6

log = []

actions = World.actions
states = []
Q = {}
E = {}
for i in range(World.x):
    for j in range(World.y):
        states.append((i, j))

for state in states:
    temp = {}
    temp_e = {}
    for action in actions:
        temp[action] = 0.0 # Set to 0.1 if following greedy policy
        temp_e[action] = 0.0
        World.set_cell_score(state, action, temp[action])
    Q[state] = temp
    E[state] = temp_e

for (i, j, c, w) in World.specials:
    for action in actions:
        Q[(i, j)][action] = w
        World.set_cell_score((i, j), action, w)


def do_action(action):
    s = World.player
    r = -World.score
    if action == actions[0]:
        World.try_move(0, -1)
    elif action == actions[1]:
        World.try_move(0, 1)
    elif action == actions[2]:
        World.try_move(-1, 0)
    elif action == actions[3]:
        World.try_move(1, 0)
    else:
        return
    s2 = World.player
    r += World.score
    return s, action, r, s2


def reset_E():
    for state in states:
        for action in actions:
            E[state][action] = 0

def max_Q(s):
    val = None
    act = None
    for a, q in Q[s].items():
        if val is None or (q > val):
            val = q
            act = a
    return act, val


def policy(s, eps=epsilon):
    if random.random() > eps:
        return max_Q(s)
    else:
        l = [(a, q) for a, q in Q[s].items()]
        random.shuffle(l)
        return random.choice(l)


def inc_Q(s, a, alpha, inc):
    Q[s][a] += alpha * inc * E[s][a]
    World.set_cell_score(s, a, Q[s][a])


def run():
    global discount
    global epsilon
    global alpha
    global log
    score = 0
    time.sleep(1)
    s1 = World.player
    a1, q_val1 = policy(s1)  
    for episode_num in range(100):
        steps = 0
        score = 0
        path=[]
        path.append(s1)
        while not World.has_restarted():
            # Do the action
            (s1, a1, r1, s2) = do_action(a1)
            
            if s2 in path:
                if s2==(0,0) and len(path)==World.x*World.y:
                    score += r1+1            
                
                    World.restart_game()
            else:
                path.append(s2)
                score += r1
                print(path)
            
            

                # Update Q
                a2, q_val2 = policy(s2) # Change to max_Q(s2) if following Greedy policy
                a_best, q_best = max_Q(s2)
                delta = r1 + discount * q_best - Q[s1][a1]
                E[s1][a1] = 1


                for state in states:
                    for action in actions:
                        inc_Q(state, action, alpha, delta)
                        if a_best == a2:
                            E[state][action] *= discount * e_decay
                        else:
                            E[state][action] = 0
                # print('new q:', Q[s1][a1])
                s1 = s2
                a1 = a2
                q_val1 = q_val2
    
                steps += 1
    
                # Update the learning rate
    
                # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
                time.sleep(0.005)

        World.restart_game()
        reset_E()
        log.append({'episode': episode_num, 'score': score, 'steps': steps, 'alpha': alpha, 'epsilon': 0})
        time.sleep(0.01)
        alpha = max(0.1, pow(episode_num+1, -0.4))
        epsilon = min(0.3, pow(episode_num+1, -1.2))

    with open('data/log_eps-greedy_traces_0.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['episode', 'score', 'steps', 'alpha', 'epsilon'])
        writer.writeheader()
        for episode in log:
            writer.writerow(episode)
    print('Logged')


t = threading.Thread(target=run)
t.daemon = True
t.start()
World.start_game()
