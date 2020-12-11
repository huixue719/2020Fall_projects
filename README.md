# 2020Fall_projects

# Title: Localization-Sequential Monte Carlo Method

### Author: Shiqi Liu & Hui Xue
### Contribution: 

Shiqi mostly takes charge of the first class, including drawing the map, the car, ect.

Hui takes the second part of the distance, emstimated weights,resample the estimates, ect.
# Introduction

Given a robot with sensor, it can constantly estimate the position and orientation of itself as it moves and sense the unknown environment by taking advantages of *Monte Carlo Localization*, i.e. particle filter localization.

# Hypothesis
- The map is given
- The robot could start anywhere on the map randomly
- The particles are generated randomly on the map
- The sensor is noisy

# Key Idea
- Initialize the system by generating the environment and robot
- The true measurement of the sensors for the estimated particles are computed and compared against the noisy (gaussian) sensor data
- The system will calculate the probability or the weight of the particle and keep updating the particles to more accurately reflect where it is while moving. 
- The particles should converge towards the actual position of the robot. 

# Demo
- Red arrows: randomly generated particles
- Blue arrows(predicted): the weight of all the state of red arrows
- Green arrow: the real robot


# References:
https://en.wikipedia.org/wiki/Monte_Carlo_localization

https://www.cnblogs.com/21207-iHome/p/5237701.html

Video: 1-D localization https://youtu.be/JhkxtSn9eo8 

Related github topics: monte-carlo-localization: https://www.cs.hmc.edu/~dodds/projects/RobS03/Daniel/proj3.html 
