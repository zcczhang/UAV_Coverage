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

![](https://github.com/zcczhang/UAV_Coverage/blob/master/Research_Report/eq1.png?raw=true)

so that: longitude per meter = (right - left) / width, and latitude per meter = (top-bottom)/height.

Figures below show two circumstances of GPS way-points for drone covering a rectangular field using hexagonal tessellation. The radius of the FOV in the left figure is 7m while 8m for the right one.

![](https://github.com/zcczhang/UAV_Coverage/blob/master/Research_Report/1.png?raw=true)


