# 2020Fall_projects

  In our setup, we have 4 range sensors attached to the robot, each attached to one cardinal direction. (North East West South, or more commonly known as up right left down). 
  The sensor will return a detection for the distance to the closest wall in the direction its facing.
  
	For our simulation, first, we initialize the system by doing the following: Randomly generate the world map for the robot to traverse through; Randomly select the real     location of the robot, along with its heading and it velocity; Random select 256 uniformly distributed particles as estimate of the robot location.
 
  During the main loop of the operation, the true measurement of the sensors for the estimated particles are computed and compared against the noisy (gaussian) sensor data measured by the real robot to determine the weight of the particle. The higher the weight, the more likely the real robot is at or near the particle.
  
	The particles can be considered as the possible locations and orientations of the robots, in other words, they are collected number of hypothesis state that the robot could be there in the future.
  
	The system will calculate the probability or the weight of the particle. Particles that closely match the observations are weighted higher than particles which don't match the observations very well. Then the particles will update its location based on its own heading and velocity. Then the robot will discard particles inconsistent with the and generate new sample around particles with non-zero weight with gaussian distribution. The sampling strategy is that the higher the weight of the particle, the more likely it will be selected to be the center for the said gaussian distribution. It keeps updating the particles to more accurately reflect where it is while moving. Ultimately, the particles should converge towards the actual position of the robot. 

Task: Shiqi mostly takes charge of the first class, including drawing the map, the car, ect.
			Hui takes the second part of the distance, emstimated weights,resample the estimates, ect.

References:
https://en.wikipedia.org/wiki/Monte_Carlo_localization
https://www.cnblogs.com/21207-iHome/p/5237701.html
Video: 1-D localization https://youtu.be/JhkxtSn9eo8 
Related github topics: monte-carlo-localization · GitHub Topics · GitHub
https://www.cs.hmc.edu/~dodds/projects/RobS03/Daniel/proj3.html 
