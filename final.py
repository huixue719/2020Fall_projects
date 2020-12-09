import numpy as np
import turtle
import bisect
import time


class MonteCarloLocalization(object):
    def __init__(self, height, width, row_num_, col_num_, num_of_estimates=256):
        """
        initialize the turtle world.
        THE MAIN FUNCTION IS run()
        :param world_height:
        :param world_width:
        :param row_num:
        :param col_num:
        """
        self.path_height = height / row_num
        self.path_width = width / col_num
        self.height = height
        self.width = width
        self.row_num = row_num_
        self.col_num = col_num_
        self.down_wall_probability = 1 - 0.35
        self.left_wall_probability = 1 - 0.35

        # initialization of the matrix for world storage, world[row, col]
        self.world_down_wall = None
        self.world_left_wall = None
        self.create_map()

        # create where the real car is at randomly
        self.car = SelfDrivingCarEstimate(init_position_x=np.random.uniform(0, (self.width - self.path_width)),
                                          init_position_y=np.random.uniform(0, (self.height - self.path_height)),
                                          heading=np.random.uniform(0, 360),
                                          world=self,
                                          velocity=np.random.uniform(1, 5))

        # create the estimations of the cars whereabouts
        self.max_num_of_estimates = num_of_estimates
        self.current_estimates = self.create_estimates(num_of_estimates)

    def draw_estimated_location_of_the_car(self, estimates=None):
        if estimates is None:
            estimates = self.current_estimates

        sum_x = 0
        sum_y = 0
        sum_heading = 0
        total_weight = 0

        for est in estimates:
            sum_x = est.x * est.weight + sum_x
            sum_y = est.y * est.weight + sum_y
            sum_heading = est.heading * est.weight + sum_heading
            total_weight = total_weight + est.weight

        if total_weight == 0:
            print("no estimate found")
            return

        estimate_x = sum_x / total_weight
        estimate_y = sum_y / total_weight
        estimate_heading = sum_heading / total_weight

        turtle.penup()
        turtle.shape("arrow")
        turtle.shapesize(0.5, 2, 1)
        turtle.color("blue")
        turtle.setposition((estimate_x, estimate_y))
        turtle.setheading(estimate_heading)
        turtle.stamp()

    def draw_estimates(self, estimates=None):
        if estimates is None:
            estimates = self.current_estimates

        for i, est in enumerate(estimates):
            turtle.shape("arrow")
            turtle.shapesize(0.5, 2, 1)
            turtle.penup()
            turtle.setposition((est.x, est.y))
            turtle.setheading(est.heading)
            turtle.fillcolor("red")
            turtle.stamp()

        turtle.update()

    def draw_car(self):
        turtle.shape("arrow")
        turtle.shapesize(0.7, 2.8, 1)
        turtle.penup()
        turtle.setposition((self.car.x, self.car.y))
        turtle.setheading(self.car.heading)
        turtle.fillcolor("green")
        turtle.stamp()

    def create_estimates(self, estimate_count: int):
        car_estimates = list()
        for i in range(estimate_count):
            x = np.random.uniform(0, self.width - self.path_width)
            y = np.random.uniform(0, self.height - self.path_height)
            car_estimates.append(SelfDrivingCarEstimate(init_position_x=x, init_position_y=y,
                                                        heading=np.random.uniform(0, 360), world=self))
        return car_estimates

    def create_map(self):
        """

        :return:
        """
        assert self.row_num > 0 and self.col_num > 0 and "row and col number must be greater than 0"
        self.world_down_wall = np.zeros((self.row_num, self.col_num), dtype=np.uint8)
        self.world_left_wall = np.zeros((self.row_num, self.col_num), dtype=np.uint8)

        down_wall_probability = np.random.random((self.row_num, self.col_num))
        left_wall_probability = np.random.random((self.row_num, self.col_num))

        for i in range(self.row_num):
            for j in range(self.col_num):
                # set down wall based on down wall generation threshold
                if down_wall_probability[i, j] > self.down_wall_probability:
                    self.world_down_wall[i, j] = 1

                # set left wall based on left wall generation threshold
                if left_wall_probability[i, j] > self.left_wall_probability:
                    self.world_left_wall[i, j] = 1

                # left most column must have a left wall
                if j == 0:
                    self.world_left_wall[i, j] = 1

                # right most column must only have a left wall
                if j == self.col_num - 1:
                    self.world_left_wall[i, j] = 1
                    self.world_down_wall[i, j] = 0

                # bottom most column must have down wall
                if i == 0:
                    self.world_down_wall[i, j] = 1

                # top most column must only have down wall
                if i == self.row_num - 1:
                    self.world_down_wall[i, j] = 1
                    self.world_left_wall[i, j] = 0

                # top right most block have nothing.
                if i == self.row_num - 1 and j == self.col_num - 1:
                    self.world_down_wall[i, j] = 0
                    self.world_left_wall[i, j] = 0
        print("finished creating the world.")

    def draw_map(self):
        '''

        :return:
        '''
        turtle.setworldcoordinates(0, 0, self.width, self.height)

        cursor = turtle.Turtle()
        cursor.hideturtle()
        cursor.speed(0)
        cursor.width(1)
        turtle.tracer(0, 0)

        right_heading = 0
        up_heading = 90
        left_heading = 180
        down_heading = 270

        for i in range(self.row_num):
            for j in range(self.col_num):
                wall_existence = self.check_walls(block=(i, j))

                cursor.up()
                cursor.setposition(j * self.path_width, (i + 1) * self.path_height)
                cursor.setheading(down_heading)
                # draw left wall if exists
                if wall_existence["left"]:
                    cursor.pendown()
                else:
                    cursor.penup()
                cursor.forward(self.path_height)

                # down wall
                cursor.setheading(right_heading)
                if wall_existence["down"]:
                    cursor.pendown()
                else:
                    cursor.penup()
                cursor.forward(self.path_width)

                # right wall
                cursor.setheading(up_heading)
                if wall_existence["right"]:
                    cursor.pendown()
                else:
                    cursor.penup()
                cursor.forward(self.path_height)

                # top wall
                cursor.setheading(left_heading)
                if wall_existence["top"]:
                    cursor.pendown()
                else:
                    cursor.penup()
                cursor.forward(self.path_width)
                cursor.penup()
        turtle.update()

    def check_walls(self, block: (int, int)):
        """
        check existence of walls.
        :param block: the block's index (row, col)
        :return: (top,lef,down,right). true if wall exists, false otherwise.
        """
        return_val = dict()

        current_cell_left_value = self.world_left_wall[block[0], block[1]]
        current_cell_down_value = self.world_down_wall[block[0], block[1]]

        if block[1] == self.col_num - 1:
            right_side_cell_left_value = 0
            # right_side_cell_down_value = 0 # not used
        else:
            right_side_cell_left_value = self.world_left_wall[block[0], block[1] + 1]
            # right_side_cell_down_value = self.world_down_wall[block[0], block[1] + 1]

        if block[0] == self.row_num - 1:
            # top_side_cell_left_value = 0 # not used
            top_side_cell_down_value = 0
        else:
            # top_side_cell_left_value = self.world_left_wall[block[0] + 1, block[1]] # not used
            top_side_cell_down_value = self.world_down_wall[block[0] + 1, block[1]]

        return_val["top"] = top_side_cell_down_value
        return_val["left"] = current_cell_left_value
        return_val["down"] = current_cell_down_value
        return_val["right"] = right_side_cell_left_value
        return return_val

    def get_block_index(self, position_x: float, position_y: float) -> (int, int):
        """

        :param position_x: location within map
        :param position_y: location within map
        :return: the block that contains the the position, (row, col)
        """
        col = int(position_x / self.path_width)
        row = int(position_y / self.path_height)
        return row, col

    def distance_to_walls(self, position_x: float, position_y: float):
        """
        ^
        |
         ---- x/col/width
        find the distance to top/left/down/right walls
        :param position_x: location x
        :param position_y: location y
        :return: dict = [top: ,left: ,down: ,right: ] distance
        """
        ret_val = dict()
        col = int(position_x / self.path_width)
        row = int(position_y / self.path_height)

        for i in range(col, -1, -1):
            walls = self.check_walls((row, i))
            if walls["left"]:
                # hit a wall on left.
                ret_val["left"] = position_x - self.path_width * i
                break
            # if i == 0:
            #     ret_val["left"] = 100  # there's no left wall, give a max dist

        for i in range(row, -1, -1):
            walls = self.check_walls((i, col))
            if walls["down"]:
                # hit a wall below.
                ret_val["down"] = position_y - self.path_height * i
                break
            # if i == 0:
            #     ret_val["down"] = 100  # there's no down wall, give a maximum dist

        for i in range(col, self.col_num, 1):
            walls = self.check_walls((row, i))
            if walls["right"]:
                # hit a wall on the right.
                ret_val["right"] = self.path_width * (i + 1) - position_x
                break
            # if i == self.col_num - 1:
            #     ret_val["right"] = 100  # there's no right wall, give a maximum dist

        for i in range(row, self.row_num, 1):
            walls = self.check_walls((i, col))
            if walls["top"]:
                ret_val["top"] = self.path_height * (i + 1) - position_y
                break
            # if i == self.row_num - 1:
            #     ret_val["top"] = 100  # there's no top wall, give a maximum dist

        return ret_val

    def sensor_error_norm(self, sensor_reading_1, sensor_reading_2, heading_1, heading_2):
        diff_top = sensor_reading_1["top"] - sensor_reading_2["top"]
        diff_left = sensor_reading_1["left"] - sensor_reading_2["left"]
        diff_down = sensor_reading_1["down"] - sensor_reading_2["down"]
        diff_right = sensor_reading_1["right"] - sensor_reading_2["right"]
        diff_heading = np.radians(180 - abs(abs(heading_1 - heading_2) % 360 - 180)) * 5

        squared_sum = diff_top * diff_top + diff_left * diff_left + diff_down * diff_down + diff_right * diff_right + diff_heading * diff_heading

        return np.sqrt(squared_sum)

    def update_estimates_weight(self, noisy_distance_measurement_from_vehicle, noisy_vehicle_heading,
                                estimage_sigma=100):
        """
        update vehicle estimate's weight
        :param noisy_distance_measurement_from_vehicle:
        :return:
        """
        sum_weight = 0  # prevent division by zero

        for est in self.current_estimates:
            measurement_from_est = est.get_sensor_distances()  # dict of [left: , top: , down, right]
            error_norm = self.sensor_error_norm(noisy_distance_measurement_from_vehicle, measurement_from_est,
                                                noisy_vehicle_heading, est.heading)
            est.weight = np.exp((-error_norm ** 2) / np.sqrt(2 * estimage_sigma)) # pdf of normal distribution.
            sum_weight += est.weight

        if sum_weight < 1e-15:
            sum_weight = 0

        # normalize the weight
        for est in self.current_estimates:
            # with the exception of when sum is equal to zero
            if sum_weight is 0:
                est.weight = 0
            else:
                est.weight /= sum_weight

    def resample_estimates(self):
        # build a cumulative distribution of weights
        current_accumulation = 0
        cumulative_distribution = list()

        # sum of the weight is 1
        for est in self.current_estimates:
            current_accumulation = current_accumulation + est.weight
            cumulative_distribution.append(current_accumulation)

        # randomly select based on weights, higher the weight, more the likely
        # keep 1/5th of the original samples
        kept_estimates = list()
        for i in range(0, int(self.max_num_of_estimates)):
            random_val = np.random.uniform(0, 1)
            the_chosen_one = bisect.bisect_left(cumulative_distribution,
                                                random_val)  # sum of the weight is 1
            try:
                # move the chosen estimate at the same speed of the real car
                est = SelfDrivingCarEstimate(init_position_x=self.current_estimates[the_chosen_one].x,
                                             init_position_y=self.current_estimates[the_chosen_one].y,
                                             heading=self.current_estimates[the_chosen_one].heading,
                                             world=self)

                est.move(self.car.velocity)
                est.resample(self.car.velocity)

                # if estimate x and y exceed the outside bound of the map then skip the append process
                if est.x < 0 or est.x > self.width - self.path_width:
                    continue
                if est.y < 0 or est.y > self.height - self.path_height:
                    continue

                # keep the estimate
                kept_estimates.append(est)
            except IndexError:
                # this happens when weights are all zero
                x = np.random.uniform(0, self.width - self.path_width)
                y = np.random.uniform(0, self.height - self.path_height)
                kept_estimates.append(SelfDrivingCarEstimate(init_position_x=x, init_position_y=y,
                                                             heading=np.random.uniform(0, 360), world=self))

        self.current_estimates = kept_estimates

    def run(self):
        """
        main function with a infinite loop.
        BLUE IS THE final ESTIMATE, which is the weighted sum of all estimates
        GREEN is the true location of the car.
        RED are all the estimates currently alive.

        :return:
        """
        # check out __init__ for variables initialized for this class.

        # create a turtle window
        window = turtle.Screen()
        window.setup(width=self.width, height=self.height)
        self.draw_map()

        # draw the estimates
        self.draw_estimates()
        self.draw_estimated_location_of_the_car()
        self.draw_car()

        while True:
            # the vehicle only gives a noisy measurement of the up/down/left/right wall distance
            vehicle_measurement = self.car.get_noisy_sensor_distances()
            vehicle_heading = self.car.get_noisy_heading()

            # check which estimate's measurement is closest to vehicle's measurements
            # the higher the weight, the closer the estimate is to the vehicle's measurement.
            self.update_estimates_weight(vehicle_measurement, vehicle_heading)

            # draw stuff
            turtle.clearstamps()
            self.draw_estimates()
            self.draw_car()
            self.draw_estimated_location_of_the_car()
            turtle.update()

            # resampling
            self.resample_estimates()

            # move the car
            self.car.randomly_move()
            time.sleep(0.1)


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

