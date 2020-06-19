__author__ = "Charles Zhang"
__time__ = "2020-06-18 17:21" 

from gym.envs.registration import register

register(
    id='gridworld-v0',
    entry_point='gym_gridworld.envs:GridWorldEnv',
)

register(
    id='gridworld-3x3-v0',
    entry_point='gym_gridworld.envs:GridWorld3x3',
)

register(
    id='gridworld-3x4-v0',
    entry_point='gym_gridworld.envs:GridWorld3x4',
)

register(
    id='gridworld-4x5-v0',
    entry_point='gym_gridworld.envs:GridWorld4x5',
)

register(
    id='gridworld-7x8-v0',
    entry_point='gym_gridworld.envs:GridWorld7x8',
)
