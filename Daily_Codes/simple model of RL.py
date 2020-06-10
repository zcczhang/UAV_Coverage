import random
from typing import List

# simple model of reinforcement learning
# an environment that will give the agent random rewards
# for a limited number of steps, regardless of the agent's actions


class Environment:
    """
    providing observations and giving rewards.
    The environment changes its state based on the agent's actions.
    """
    # initialize its internal state.
    def __init__(self):
        self.steps_left = 10

    # return the current environment's observation to the agent.
    def get_observation(self) -> List[float]:
        return [0.0, 0.0, 0.0]      # environment basically has no internal state in this case.

    # query the set of actions it can execute.
    def get_actions(self) -> List[int]:
        return [0, 1]       # two possible actions in this case

    # signaled the end of the episode to the agent
    def is_done(self) -> bool:
        return self.steps_left == 0

    # handles an agent's action and returns the reward for this action
    def action(self, action: int) -> float:
        if self.is_done():
            raise Exception("Game is over")
        self.steps_left -= 1
        return random.random()


class Agent:
    def __init__(self):
        self.total_reward = 0.0

    def step(self, env: Environment):
        current_obs = env.get_observation()
        actions = env.get_actions()
        reward = env.action(random.choice(actions))
        self.total_reward += reward


if __name__ == "__main__":
    env = Environment()
    agent = Agent()

    while not env.is_done():
        agent.step(env)

    print("Total reward got: %.4f" % agent.total_reward)

