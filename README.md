# 2020Fall_projects

# Title: Localization-Sequential Monte Carlo Method

### Authors: Shiqi Liu & Hui Xue
### Contribution: 

Shiqi took charge of the first class, including drawing the map, the car, ect, and cooperated with Hui to edited the README. 

Hui took the second part of the distance, emstimated weights,resample the estimates, ect.

(Errors encountered in the final test, so Shiqi committed the whole file in the end.)

# Introduction

Given a robot with sensor, it can constantly estimate the position and orientation of itself as it moves and sense the unknown environment by taking advantages of *Monte Carlo Localization*, i.e. particle filter localization. 

The particles can be considered as the possible locations and orientations of the robots, in other words, they are collected number of hypothesis state that the robot could be there in the future.The system will calculate the probability or the weight of the particle. Particles that closely match the observations are weighted higher than particles which don't match the observations very well. Then the particles will update its location based on its own heading and velocity. 

Then the system will discard particles inconsistent with the and generate new sample around particles with non-zero weight with gaussian distribution. The sampling strategy is that the higher the weight of the particle, the more likely it will be selected to be the center for the said gaussian distribution. It keeps updating the particles to more accurately reflect where it is while moving. 

Ultimately, the particles should converge towards the actual position of the robot. 


# Hypotheses
- The robot could start anywhere on the map randomly
- The particles are generated randomly on the map
- The sensor is noisy
- In the generated map, the robot can use the particle filters combined with the sensor to understand where it is

# Needed Models
- Map generator:

  The whole environment is represented as a randomly generated 2-D map with walls.
- Robot Model

# Changeable Variables:
- world_width: the width of the map
- world_height: the height of the map
- row_num: the number of the grid (x-axis)
- col_num: the number of the grid (y-axis)
# Key Ideas
- Initialize the system by generating the environment and robot
- The true measurement of the sensors for the estimated particles are computed and compared against the noisy (gaussian) sensor data
- The system will calculate the probability or the weight of the particle and keep updating the particles to more accurately reflect where it is while moving. 
- The particles should converge towards the actual position of the robot. 

# Demo
- Green arrow: the real robot (move constantly)
- Red arrows: randomly generated particles
- Blue arrows(predicted): the weight of all the state of red arrows


![](https://github.com/huixue719/2020Fall_projects/blob/main/demo.png)

# References:
https://en.wikipedia.org/wiki/Monte_Carlo_localization

https://www.cnblogs.com/21207-iHome/p/5237701.html

Video: 1-D localization https://youtu.be/JhkxtSn9eo8 

Related github topics: monte-carlo-localization: https://www.cs.hmc.edu/~dodds/projects/RobS03/Daniel/proj3.html 
