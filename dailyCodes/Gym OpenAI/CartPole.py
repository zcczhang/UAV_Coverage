__author__ = "Charles Zhang"
__time__ = "2020-06-05 11:02" 
 
import gym

# random CartPole agent
if __name__ == "__main__":
    env = gym.make("CartPole-v0")

    total_reward = 0.0
    total_steps = 0
    obs = env.reset()       # four number: x coordinate of center,  speed, angle to platform, angular speed

    while True:
        action = env.action_space.sample()      # random sample from underlying space(0 for left, 1 for right)
        obs, reward, done, _ = env.step(action)
        total_reward += reward
        total_steps += 1
        if done:
            break

    print("Episode done in %d steps, total reward %.2f" % (
        total_steps, total_reward))

