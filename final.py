"""
Team: Hui Xue & Shiqi Liu
"""

import numpy as np
import turtle



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
