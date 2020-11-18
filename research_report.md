<center> <h1> Area Coverage with Unmanned Aerial Vehicles Using Reinforcement Learning</h1> </center>

<center> <h5> By </h5> </center>

<center> <h3> Charles Zhang </h3> </center>

<center> <h4> 25 May - 31 July, 2020 </h4> </center>


## Abstract

In this summer research, I work with professor Esra Kadioglu-Urtis, and students Aaron Gould, Elisabeth Land- gren, and Fan Zhang at Macalester College. In this project, we first implement the hexagonal tessellation area coverage approach which Esra previously published. Secondly, we develop and implement Q learning reinforce- ment learning algorithms in a non-Markov Decision Process(NMDP) and Markov Decision Process(MDP) for the area coverage where, instead of mathematically generating a route, the drone itself will learn an efficient path to cover an entire given area and return back to its launch position. We successfully generate the shortest paths that cover a large regular or irregular field in terms of the limited drone’s battery life, and finally extend the problem to include multiple drones to considerably widen the coverage area, using the Q learning and Actor Critic using Kronecker-Factored Trust Region (ACKTR) deep reinforcement learning method, built in the Gym environment in Python or by graph. My code is available at https://github.com/zcczhang/UAV_Coverage.

## 1 Introduction

The coverage path planning(CPP) for Unmanned Aerial Vehicles (a.k.a drones) are increasingly being used for many applications such as search/rescue, agriculture, package delivery, inspection, etc.[1][2][3]. Using UAVs for the coverage provides several benefits, and UAVs with a high degree of mobility needs to cooperatively work as a team to provide effective coverage in a relative large are, in consideration of the limited battery life for drones[4].

Many existed work have already addressed the coverage problem by both theoretically methods or learning- based algorithms[5][6][7]. However, drones in those methods are either static for coverage in terms of drones’ field of view(FOV), or only complete one-way coverage paths where the cost for the drones’ recovery is not under the consideration. Therefore, in this work, we not only consider how to generate the shortest coverage paths, but also include letting the UAV return back to the launch position, which will be addressed in this work using reinforcement learning algorithms illustrated in detail in the overview sections in this report.

The main contribution of this work is to demonstrate approaches to the reinforcement learning algorithms, named Q-learning and d Actor Critic using Kronecker-Factored Trust Region (ACKTR) deep reinforcement learning, to perform the CPP of an regular or irregular environment with known obstacles, visiting only once each center of the FOV and returning(for single drone so far), resulting in an optimized path.


## 2 Implementation of Hexagonal Tessellation


Professor Esra Kadioglu shows that a coverage path can be obtained by using polygon tessellation of a given area, and hexagonal tessellation produces a shorter coverage path than a square tessellation, in the paper *UAV Coverage Using Hexagonal Tessellation*[6]. This paper provides the algorithm to generate the Hamiltonian circuit in a rectangular field, and I implemented this algorithm to get GPS way-points given diagonal coordinates of the field and the radius of the field of view(FOV) of the UAV(code). To improve the accuracy of the translation between longitude, latitude, and meter, I transform the coordinates to the radian first and calculate the distance showing below, with two diagonal points: (top, left), (bottom, right):

<center><img src="https://github.com/zcczhang/UAV_Coverage/blob/master/Research_Report/eq1.png?raw=true" width=610" height="50"/></center>

so that: longitude per meter = (right - left) / width, and latitude per meter = (top-bottom)/height.

Figures below show two circumstances of GPS way-points for drone covering a rectangular field using hexagonal tessellation. The radius of the FOV in the left figure is 7m while 8m for the right one.

![](https://github.com/zcczhang/UAV_Coverage/blob/master/Research_Report/fig1.png?raw=true)
<center> <h7> Figure 1: Two circumstances of GPS way-points for drone covering a rectangular field using hexagonal tessellation </h7> </center>

## 3 Single Agent Area Coverage

### 3.1 Overview

In comparison with the hexagon tessellation which is calculated and proved mathematically that generates the shorter coverage path than the square tessellation, we want to figure out if it is possible to implement the reinforcement learning to find the shortest coverage path in a given field. To begin with, the environment is set to be the rectangular grid world, and the start point is the same with the end point. Specifically, the graph below gives a simple example of the rectangular 4x5 grid world where the agent starts at the (0, 0) at the upper left corner. And the drone will ideally pass through every center of the FOV, and take photos or make some other actions along with the coverage each step. Then our problem becomes to implement the reinforcement learning looking for the shortest path where the drone visits all grids(squares) and returns back to the launch position in the environment grid world.

<center><img src="https://github.com/zcczhang/UAV_Coverage/blob/master/Research_Report/3.png?raw=true" width=320" height="130" /></center>
<center> <h7> Figure 2: The example of a projected area of a UAV and a simple 4x5 gridworld starting at (0,0)</h7> </center>

In this section, the whole field will be covered by one agent(a drone), using the reinforcement learning by tabular Q learning. We can define a quantity Q(s,a) that equals the total reward got by executing action a in state s. The agent will receive a huge global reward when finish the task visiting all cells and returning back to the launch position, and will receive a small penalty when revisit a cell in the gridworld, shown in the equation below.

<center><img src="https://github.com/zcczhang/UAV_Coverage/blob/master/Research_Report/eq2.png?raw=true" width=370" height="55" /></center>

where r is a relatively large constant reward and $f_{i}$ : {S} → {0,1} shows whether the state is visited, where 0 for unvisited while 1 for visited. The value function can be defined via the value V (s) as an expected total reward (optionally discounted) that is obtainable from the state. This quantity gave a name to the whole family of methods called Q-learning[8]. Applying the bellman equation and temporal difference method, the tabular Q learning updates the Q value Q(S, A) corresponding with the state s and action a after each step, showing following:

<center><img src="https://github.com/zcczhang/UAV_Coverage/blob/master/Research_Report/eq3.png?raw=true" width=350" height="36" /></center>

where S and S′ are the current and next (potential) states respectively; R is the reward based on the current state s and action a; α is the learning rate; and γ is the discount factor[8]. In our research, the state is set to be the waypoint of the environment—the gridworld in this section.

### 3.2 NMDP Tabular Q Learning

Since in each step in each episode, the agent has to observe if the current state is visited or not in order to get the reward, instead of only observing the current state, the process is the non-Markov Decision Process(NMDP). In order to let the agent ”learn” faster, I assume that they will visit the unvisited grid first. I also implement the decaying epsilon-greedy method to maximize the numerical reward for the action policy π(s) for each state s, shown below,

<center><img src="https://github.com/zcczhang/UAV_Coverage/blob/master/Research_Report/eq4.png?raw=true" width=300" height="43" /></center>

where ε decreases over time proportionally. Since the agent has to finish two task for each episode: visit all grids and complete the loop back to the origin, the agent will randomly move and receive the reward when visit the unvisited grid, and will receive a much larger global reward for both finishing visit and coming back. Instead of terminating the episode once the agent re-visit a state where leads to a ”fail” for the shortest coverage task like most reinforcement learning algorithms, my algorithm allows the repetition of visits but the agent will receive a negative reward for the penalty, in order to make the agent ”learn” and distinguish faster both from the good decisions and bad decisions[9]. The algorithm below shows the tabular Q learning for one agent looking for the optimal path.

<center><img src="https://github.com/zcczhang/UAV_Coverage/blob/master/Research_Report/al1.png?raw=true" width=600" height="400"/></center>

where S and S′ are the current and next states respectively; R is the reward based on the action a referring to S, which is dependant on whether the agent visit unvisited states, and finish the coverage task as well as flying back; α is the learning rate; and γ is the discount factor.

During the training, 4 values corresponding with four available directions up, down, right, and left at each entry of the ROWS×COLS table of Q values will be updated. The policy for the greedy method will choose the direction with the largest value at each state in the gridworld. After training, optimal path could be derived by choosing the direction with the largest Q value among all directions each state from the Q table. Since the movements at the beginning are random, and there are more than one ”optimal paths” which go through all grids exactly once and get back to the origin, we could get different Q tables and paths after training(code). Then, two different results of coverage path in a simple 4×5 gridworld are illustrated in figure 3 and figure 4. The table of directions corresponding with the largest Q values in the Q table is shown at the left, while the derived coverage path is shown at the right by dotted arrows. In conclusion, the minimum steps which is equivalent to the shortest coverage distance is supposed to be 20 steps in 4 × 5 gridworld, which is consistent with results derived by this reinforcement learning algorithm shown below.

<center><img src="https://github.com/zcczhang/UAV_Coverage/blob/master/Research_Report/5.png?raw=true" width=390" height="160"/></center>
<center> <h7> Figure 3: The first coverage path generated by NMDP tabular Q learning in 4x5 gridworld </h7> </center>

<center><img src="https://github.com/zcczhang/UAV_Coverage/blob/master/Research_Report/7.png?raw=true" width=390" height="160"/></center>
<center> <h7> Figure 4: The second coverage path generated by NMDP tabular Q learning in 4x5 gridworld </h7> </center>


The convergence means that the policy for shortest coverage path planning from Q values will not be changed, and the steps equal to the shortest distance for visiting all states and return back, which is the number of grids in the gridworld. From figure 5 and figure 6 represented the number of steps each episode, steps will converge around 350 episodes in the 4 × 5 gridworld. Using the decaying epsilon-greedy method can make sure that the agent will converge to only one optimal path for each training, and this is also the reason why multiple different results would be generated for each training. The steps vibrate a lot at the beginning and after the convergence, since a random state in the environment will be chosen to be the start state each episode. This random start state will make sure the agent looking for an optimal direction at any state for visiting all cells and getting back. The number of steps is increasing at first because the agent is sticking to a path that cover some but not all grids and the agent has less and less probabilities due to the decaying ε-greedy policy to be broken away from the current local optimum, but the number of cells for these repeatedly visited loops is actually increasing while training. And once the visited grids for the loop that the agent is sticking on each episode equal to the number of all grids in the grid world, the step will converge “suddenly” to the optimal steps, the number of grids in the gridworld, showing as the steep decrease just before the convergence around 200 to 300 episodes in this case.

![](https://github.com/zcczhang/UAV_Coverage/blob/master/Research_Report/fg5&6.png?raw=true)

This naive tabular Q learning could also be implemented in the hexagon tessellation environment by allowing six directions up, upper left, upper right, down, bottom left, and bottom right. Then, it requires a larger dimension of action space and Q table, and many out-of-bound directions need to be considered. Besides, as the size of the gridworld becomes large, it is unstable to find the coverage solution. Therefore, in the next section, a graph based algorithm will be introduced to reduce the computation and be available for more complicated environment like irregular field with obstacles.

### 3.3 Graph Based MDP Q Learning

In this section, I set the environment as a graph, where the vertices are the state that need to be covered and edges are available directions that the agent drone can fly through. Then, using adjacency matrices, only attainable vertices will have corresponding values for Q values, rewards, and actions. In this way, more complicated real world environment beyond the gridworld can be transformed to the graph to implement reinforcement learning[10]. Assume the environment has V vertices, then R and Q are V × V matrices. Specifically, R is an adjacency matrix except R[i,j] where j is the end(start) state and i,j are connected. In this way, each step of exploration will get a small reward except reaching the end state with a much larger reward. Unlike the NMDP naive Q learning in the previous section, the agent will first find shortest paths from any state in the environment to the launch position, and then store the Q values in Q matrix. This process is MDP, and is straightforward to implement the Q learning. As actions for the agent in this MDP are fully random without greedy move, the simple bellman equation is better to use to update Q values recursively[11].

<center><img src="https://github.com/zcczhang/UAV_Coverage/blob/master/Research_Report/eq5.png?raw=true" width=220" height="30"/></center>

To get the solution for coverage path planning, I consider that if the agent is supposed to to cover all grids, or in other words visit more states, it is equivalent to avoid the shortest path and minimize the overlapping states, by choosing the minimum Q value for the policy. The algorithm of this Q learning with graph-based state representation is shown below,

<center><img src="https://github.com/zcczhang/UAV_Coverage/blob/master/Pictures/Learning%20with%20Graph-Based%20State%20Representations.png?raw=true" width=600" height="400"/></center>


