import numpy as np
import time


class SelfDrivingCarEstimate(object):
    def __init__(self, init_position_x: float, init_position_y: float, heading: float, world: MonteCarloLocalization,
                 weight=1.0, velocity=0):
        """

        :param init_position_x: meters
        :param init_position_y: meters
        :param heading: degree
        :param world: generated world
        :param weight: the weight of the estimation
        """
        self.x = init_position_x % world.width
        self.y = init_position_y % world.height
        self.heading = heading % 360
        self.world = world
        self.weight = weight
        self.velocity = velocity

    def get_sensor_distances(self):
        """
        return the accurate distance measurements of the self driving car estimate
        :return: the dict of [left: , top: , down, right]
        """
        return self.world.distance_to_walls(self.x, self.y)

    def resample(self, velocity, duration=1.0):
        self.heading = np.random.normal(self.heading, 10) % 360

        new_x = self.x + duration * velocity * np.cos(np.radians(self.heading))
        new_y = self.y + duration * velocity * np.sin(np.radians(self.heading))
        self.x = np.random.normal(new_x, 5)
        self.y = np.random.normal(new_y, 5)

    def move(self, velocity, duration=1.0):
        """
        move in the direction of the heading with the velocity given. if a collision with wall is deteacted.
        then that direction of motion is inhibited.
        :param duration: time is default 1 second
        :param velocity: must be smaller than min( path_height, path_width)
        :return: nothing
        """

        if velocity > 0.9 * min(self.world.path_height, self.world.path_width):
            velocity = 0.9 * min(self.world.path_height, self.world.path_width)
            print("velocity greater than maximum allowed, reducing velocity.")

        # new_x and new_y are new location of the car if moving unrestricted
        new_x = self.x + duration * velocity * np.cos(np.radians(self.heading))
        new_y = self.y + duration * velocity * np.sin(np.radians(self.heading))

        # get (row, col) of current and new block  col <=> x
        current_block = self.world.get_block_index(self.x, self.y)
        new_block = self.world.get_block_index(new_x, new_y)

        current_block_wall = self.world.check_walls(current_block)

        # if still within current block, good
        if current_block == new_block:
            self.x = new_x
            self.y = new_y
            return

        # if no wall between current block and new block's row, accept change of y
        if (new_block[0] > current_block[0] and current_block_wall["top"] == False) or \
                (new_block[0] < current_block[0] and current_block_wall["down"] == False):
            self.y = new_y
        # else dont change y

        if (new_block[1] > current_block[1] and current_block_wall["right"] == False) or \
                (new_block[1] < current_block[1] and current_block_wall["left"] == False):
            self.x = new_x
        # else dont change x

        return

    def randomly_move(self):
        # randomly change the heading, random walk fashion
        self.heading = self.heading + np.random.normal(0, 10)
        # move the car
        self.move(self.velocity)

    def get_noisy_sensor_distances(self):
        distances = self.get_sensor_distances()

        # add noise, but must be greater than 0
        distances["top"] = max(0, distances["top"] + np.random.normal(0, distances["top"] * 0.02))
        distances["down"] = max(0, distances["down"] + np.random.normal(0, distances["down"] * 0.02))
        distances["left"] = max(0, distances["left"] + np.random.normal(0, distances["left"] * 0.02))
        distances["right"] = max(0, distances["right"] + np.random.normal(0, distances["right"] * 0.02))

        return distances

    def get_noisy_heading(self):
        return self.heading + np.random.normal(0, 10)


if __name__ == '__main__':

    world_width = 512
    world_height = 512
    col_num = 10
    row_num = 10

    demo = MonteCarloLocalization(world_height, world_width, row_num, col_num, 1000)
    demo.run()

