"""
__author__ = "Charles Zhang"
__time__ = "2020-06-05 16:38"
"""
# references:
# https://cs.stanford.edu/people/karpathy/reinforcejs/gridworld_dp.html
# https://github.com/qqiang00/ReinforcemengLearningPractice/blob/master/reinforce/codes_for_book/c06/gridworld.py


import gym
from gym import spaces


class Grid(object):
    def __init__(self, x: int = None,
                 y: int = None,
                 reward: int = 0.0):
        self.x = x
        self.y = y
        self.reward = reward
        self.name = None
        self._update_name()

    def _update_name(self):
        self.name = "X{0}-Y{1}".format(self.x, self.y)

    def __str__(self):
        return "name:{3}, x:{0}, y:{1}, reward:{2}".format(self.x,
                                                           self.y,
                                                           self.reward,
                                                           self.name)


class GridMatrix(object):

    def __init__(self, n_width: int,  # horizontal number of grids
                 n_height: int,  # vertical num of grids
                 default_reward: int = 0,
                 ):
        self.grids = None
        self.n_height = n_height
        self.n_width = n_width
        self.default_reward = default_reward
        self.reset()

    def reset(self):
        self.grids = []
        for x in range(self.n_height):
            for y in range(self.n_width):
                self.grids.append(Grid(x, y, self.default_reward))

    def get_grid(self, x, y=None):
        xx, yy = None, None
        if isinstance(x, int):
            xx, yy = x, y
        elif isinstance(x, tuple):
            xx, yy = x[0], x[1]
        index = yy * self.n_width + xx
        return self.grids[index]

    def set_reward(self, x, y, reward):
        grid = self.get_grid(x, y)
        if grid is not None:
            grid.reward = reward

    def get_reward(self, x, y):
        grid = self.get_grid(x, y)
        if grid is None:
            return None
        return grid.reward


class GridWorldEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 30
    }

    def __init__(self, n_width: int = 10,
                 n_height: int = 10,
                 u_size=40,
                 default_reward: int = 0):
        self.u_size = u_size
        self.n_width = n_width
        self.n_height = n_height
        self.width = u_size * n_width
        self.height = u_size * n_height
        self.default_reward = default_reward

        self.grids = GridMatrix(n_width=self.n_width,
                                n_height=self.n_height,
                                default_reward=self.default_reward)
        self.reward = 0  # for rendering
        self.action = None  # for rendering
        # 0,1,2,3,4 represent left, right, up, down, -, five moves.
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Discrete(self.n_height * self.n_width)
        self.ends = [(9, 0)]  # ending grid(s)
        self.start = (0, 9)  # start grid
        self.rewards = []  # special awards, 0 for the end
        self.refresh_setting()
        self.viewer = None
        self.reset()

    def _action_effect(self, x, y, action):
        new_x, new_y = x, y
        if action == 0:
            new_x -= 1  # left
        elif action == 1:
            new_x += 1  # right
        elif action == 2:
            new_y += 1  # up
        elif action == 3:
            new_y -= 1  # down
        return new_x, new_y

    def _boundary_effect(self, x, y):
        new_x, new_y = x, y
        if new_x < 0:
            new_x = 0
        if new_x >= self.n_width:
            new_x = self.n_width - 1
        if new_y < 0:
            new_y = 0
        if new_y >= self.n_height:
            new_y = self.n_height - 1
        return new_x, new_y

    def step(self, action):
        assert self.action_space.contains(action), \
            "%r (%s) invalid" % (action, type(action))

        self.action = action  # action for rendering
        old_x, old_y = self._state_to_xy(self.state)
        new_x, new_y = old_x, old_y

        new_x, new_y = self._action_effect(new_x, new_y, action)
        # boundary effect
        new_x, new_y = self._boundary_effect(new_x, new_y)
        self.reward = self.grids.get_reward(new_x, new_y)

        done = self._is_end_state(new_x, new_y)
        self.state = self._xy_to_state(new_x, new_y)
        info = {"x": new_x, "y": new_y, "grids": self.grids}
        return self.state, self.reward, done, info

    def _state_to_xy(self, s):
        x = s % self.n_width
        y = int((s - x) / self.n_width)
        return x, y

    def _xy_to_state(self, x, y=None):
        if isinstance(x, int):
            assert (isinstance(y, int)), "incomplete Position info"
            return x + self.n_width * y
        elif isinstance(x, tuple):
            return x[0] + self.n_width * x[1]
        return -1

    def refresh_setting(self):
        for x, y, r in self.rewards:
            self.grids.set_reward(x, y, r)

    def reset(self):
        self.state = self._xy_to_state(self.start)
        return self.state

    def _is_end_state(self, x, y=None):
        if y is not None:
            xx, yy = x, y
        elif isinstance(x, int):
            xx, yy = self._state_to_xy(x)
        else:
            xx, yy = x[0], x[1]
        for end in self.ends:
            if xx == end[0] and yy == end[1]:
                return True
        return False

    # UI
    def render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return
        u_size = self.u_size
        m = 2  # gap between grids

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(self.width, self.height)

            for i in range(self.n_width+1):
                line = rendering.Line(start=(i*u_size, 0),
                                      end=(i*u_size, u_size*self.n_height))
                self.viewer.add_geom(line)
            for i in range(self.n_height):
                line = rendering.Line(start=(0, i*u_size),
                                      end=(u_size*self.n_width, i*u_size))
                self.viewer.add_geom(line)

            # draw grids
            for x in range(self.n_width):
                for y in range(self.n_height):
                    v = [(x * u_size + m, y * u_size + m),
                         ((x + 1) * u_size - m, y * u_size + m),
                         ((x + 1) * u_size - m, (y + 1) * u_size - m),
                         (x * u_size + m, (y + 1) * u_size - m)]

                    rect = rendering.FilledPolygon(v)
                    rect.set_color(1.0, 1.0, 1.0)
                    self.viewer.add_geom(rect)
                    # frame
                    v_outline = [(x * u_size + m, y * u_size + m),
                                 ((x + 1) * u_size - m, y * u_size + m),
                                 ((x + 1) * u_size - m, (y + 1) * u_size - m),
                                 (x * u_size + m, (y + 1) * u_size - m)]
                    outline = rendering.make_polygon(v_outline, False)
                    outline.set_linewidth(10)

                    if self._is_end_state(x, y):
                        self.viewer.add_geom(outline)
                    if self.start[0] == x and self.start[1] == y:
                        self.viewer.add_geom(outline)
            # agent
            self.agent = rendering.make_circle(u_size / 4, 30, True)
            self.viewer.add_geom(self.agent)
            self.agent_trans = rendering.Transform()
            self.agent.add_attr(self.agent_trans)

        x, y = self._state_to_xy(self.state)
        self.agent_trans.set_translation((x + 0.5) * u_size, (y + 0.5) * u_size)
        return self.viewer.render(return_rgb_array=mode == 'rgb_array')

    def close(self):
        if self.viewer:
            self.viewer.close()


def grid_world():
    env = GridWorldEnv(n_width=10,
                       n_height=10,
                       u_size=40,
                       default_reward=-1)
    env.start = (0, 9)
    env.ends = [(9, 0)]
    env.rewards = [(9, 0, 0)]
    env.refresh_setting()
    return env


if __name__ == "__main__":
    env = grid_world()
    env.reset()
    env.render()
    total_reward = 0
    total_steps = 0
    while True:
        env.render()
        action = env.action_space.sample()
        state, reward, is_done, info = env.step(action)
        total_reward += reward
        total_steps += 1
        print("{0}, {1}, {2}".format(action, reward, is_done))
        if is_done:
            env.close()
            break
    print("env closed")
    print("Episode done in %d steps, total reward %.2f" % (
        total_steps, total_reward))
