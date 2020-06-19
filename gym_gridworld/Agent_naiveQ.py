__author__ = "Charles Zhang"
__time__ = "2020-06-18 17:28"

import gym
import gym_gridworld
import numpy as np
env = gym.make('gridworld-3x4-v0')




print(env.action_space.n)

print(env.action_space.contains(0))

print(env.moves[env.action_space.sample()])

print(env.past_all)