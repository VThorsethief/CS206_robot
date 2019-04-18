from math import sin, cos, sqrt, pi

class SimpleSpiderDims:
    def __init__(self, radius, x, y, z):
        self.z_origin = radius * 4
        self.y_origin = 0
        self.x_origin = 0
        self.body = {
            'x': self.x_origin, 
            'y': self.y_origin, 
            'z': self.z_origin
        }
        self.radi = radius
        self.leg_radi = self.radi * 0.1
        self.build_leg_dims()
        self.set_ray_sensors()
        self.get_ray_directions()

    def build_leg_dims(self):
        self.build_leg1_dims()
        self.build_j1_dims()
        self.build_leg2_dims()
        self.build_j0_dims()
        self.add_colors()
        self.build_rotation_normals()

    def build_j0_dims(self):
        self.j0_z = self.z_origin
        axis_offset = self.radi * cos(pi/6)
        diagonal_offset = get_diagonal_offset(axis_offset)
        # self.j0 = {}
        # Joint 0 x+ axis
        self.j0 = {
            0:{
            'x': self.x_origin + axis_offset,
            'y': 0,
            },
            # Joint 0 y+ axis
            1:{
                'x': 0,
                'y': self.y_origin + axis_offset
            },
            # Joint 0 x- axis 
            2:{
                'x': self.x_origin - axis_offset,
                'y': 0
            },
            # Joint 0 y- axis 
            3:{
                'x': 0,
                'y': self.y_origin - axis_offset
            },
            # Joint 0 xy+ axis 
            4:{
                'x': self.x_origin + diagonal_offset, 
                'y': self.y_origin + diagonal_offset
            },
            # Joint xy- axis 
            5:{
                'x': self.x_origin - diagonal_offset,
                'y': self.y_origin - diagonal_offset
            },
            # Joint x+y- axis 
            6:{
                'x': self.x_origin + diagonal_offset,
                'y': self.y_origin - diagonal_offset
            },
            # Joint x-y- axis 
            7:{
                'x': self.x_origin - diagonal_offset,
                'y': self.y_origin + diagonal_offset

            }
            }
    def build_leg1_dims(self):
        self.leg1_length = self.radi * 4
        self.leg1_r3 = self.leg1_length * cos(pi/3)
        self.leg1_z = self.z_origin + ((self.leg1_length/2) * sin(pi/6))
        self.leg1_x = {}
        self.leg1_y = {}
        self.leg1_r1 = {}
        self.leg1_r2 = {}
        axis_offset = (self.leg1_length/2) * cos(pi/6) + self.radi
        diagonal_offset = get_diagonal_offset(axis_offset)
        self.leg1 = {
            # First Leg Segment, x+ axis 
            0:{
                'x': self.x_origin + axis_offset,
                'y': 0
            },
            # First Leg Segment y+ axis
            1:{
                'x': 0,
                'y': self.y_origin + axis_offset
            },
            # First Leg Segment x- axis
            2:{
                'x': self.x_origin - axis_offset,
                'y': 0
            },
            # First Leg Segment y- axis
            3:{
                'x': 0, 
                'y': self.y_origin - axis_offset
            },
            # First Leg Segment xy+ axis 
            4:{
                'x': self.x_origin + diagonal_offset,
                'y': self.y_origin + diagonal_offset,
                'r1': 1, 
                'r2': 1
            },
            # First Leg Segment xy- axis 
            5:{
                'x': self.x_origin - diagonal_offset,
                'y': self.y_origin - diagonal_offset,
                'r1': -1,
                'r2': -1
            },
            # First Leg Segment x+y- axis 
            6:{
                'x': self.x_origin + diagonal_offset,
                'y': self.y_origin - diagonal_offset,
                'r1': 1,
                'r2': -1
            },
            # First eg Segment x-y+ axis 
            7:{
                'x': self.x_origin - diagonal_offset,
                'y': self.y_origin + diagonal_offset
            }
        }        

    def build_j1_dims(self):
        self.j1_z = self.z_origin + ((self.leg1_length) * sin(pi/6))
        self.j1_radi = self.radi * 0.112
        axis_offset = ((self.leg1_length) * cos(pi/6)) + self.radi
        diagonal_offset = get_diagonal_offset(axis_offset)
        self.j1 = {
            # Joint 1 x+ axis
            0:{
                'x': self.x_origin + axis_offset,
                'y': 0
            },
            # Joint 1 y+ axis 
            1:{
                'x': 0, 
                'y': self.y_origin + axis_offset
            },
            # Joint 1 x- axis 
            2:{
                'x': self.x_origin - axis_offset,
                'y': 0
            },
            # Joint 1 y- axis  
            3:{
                'x': 0,
                'y': self.y_origin - axis_offset
            }, 
            # Joint 1 xy+ axis 
            4:{
                'x': self.y_origin + diagonal_offset,
                'y': self.y_origin + diagonal_offset
            },
            # Joint 1 xy- axis 
            5:{
                'x': self.y_origin - diagonal_offset,
                'y': self.y_origin - diagonal_offset
            },
            # Joint 1 x+y- axis 
            6:{
                'x': self.y_origin + diagonal_offset,
                'y': self.y_origin - diagonal_offset 
            }, 
            # Joint 1 x-y+ axis 
            7:{
                'x': self.y_origin - diagonal_offset,
                'y': self.y_origin + diagonal_offset
            }    
        }

    def build_leg2_dims(self):
        self.leg2_length = self.radi * 6
        self.leg2_angle = ((-2*pi)/5)
        self.leg2_r3 = self.leg2_length * sin(-self.leg2_angle)
        # self.leg2_r3 = 0
        self.leg2_z = self.j1_z + ((self.leg2_length/2) * sin(((-2*pi)/5)))
        axis_offset = ((self.leg2_length/2) * cos(self.leg2_angle))
        diagonal_offset = get_diagonal_offset(axis_offset)
        self.leg2 = {
            # Second Leg Segment x+ axis 
            0:{
                'x': self.j1[0]['x'] + axis_offset, 
                'y': 0
            },
            #Second Leg Segment y+ axis 
            1:{
                'x': 0, 
                'y': self.j1[1]['y'] + axis_offset
            }, 
            # Second Leg Segment x- axis 
            2:{
                'x': self.j1[2]['x'] - axis_offset,
                'y': 0
            }, 
            # Second Leg Segment y- axis 
            3:{
                'x': 0, 
                'y': self.j1[3]['y'] - axis_offset
            }, 
            # Second Leg Segment xy+ axis 
            4:{
                'x': self.j1[4]['x'] + diagonal_offset,
                'y': self.j1[4]['y'] + diagonal_offset
            }, 
            # Second Leg Segment xy- axis 
            5:{
                'x': self.j1[5]['x'] - diagonal_offset,
                'y': self.j1[5]['y'] - diagonal_offset
            }, 
            # Second Leg Segment x+y- axis 
            6:{
                'x': self.j1[6]['x'] + diagonal_offset,
                'y': self.j1[6]['y'] - diagonal_offset
            }, 
            # Second Leg x-y+ axis 
            7:{
                'x': self.j1[7]['x'] - diagonal_offset,
                'y': self.j1[7]['y'] + diagonal_offset 
            }
        }

    def build_rotation_normals(self):
        axis_normal = self.leg1_length * sin(pi/3)
        axis_normal2 = self.leg2_length * -sin(pi/10)
        diagonal_normal1 = get_diagonal_offset(axis_normal)
        diagonal_normal12 = get_diagonal_offset(axis_normal2)

        self.joint_normals = {
            "n1": [0, -1, 0, 1, -1, 1, 1, -1],
            'n2': [1, 0, -1, 0, 1, -1, 1, -1], 
            'n1.2' : [-1, 0, 1, 0, -1, 1, -1, 1],
            'n2.2' : [0, -1, 0, 1, -1, 1, 1, -1]
        }
        self.position_normals = {
            "leg1":{
                "r1": [axis_normal, 0, -axis_normal, 0, diagonal_normal1, -diagonal_normal1, diagonal_normal1, -diagonal_normal1],
                "r2": [0, axis_normal, 0, -axis_normal, diagonal_normal1, -diagonal_normal1, -diagonal_normal1, diagonal_normal1]
            },
            "leg2": {
                "r1": [axis_normal2, 0, -axis_normal2, 0, diagonal_normal12, -diagonal_normal12, diagonal_normal12, -diagonal_normal12],
                "r2": [0, axis_normal2, 0, -axis_normal2, diagonal_normal12, -diagonal_normal12, -diagonal_normal12, diagonal_normal12]
            }
            
            
        }

    def add_colors(self):
        self.colors = {
            'red':[1, 0, 1, 0, 0, 0, 1, 1],
            'green': [0, 1, 0, 1, 0, 0, 0, 0], 
            "blue": [0, 0, 0, 0, 1, 1, 1, 1]
        }

    def set_ray_sensors(self):
        self.rad3_over2 = (self.radi * sqrt(3))/2
        self.ray_sensors = {
            0: {
                'x': self.rad3_over2,
                'y': self.radi * 0.5
            },
            1: {
                'x': self.radi * 0.5,
                'y': self.rad3_over2,
            },
            2:{
                'x': self.radi * -0.5,
                'y': self.rad3_over2
            },
            3:{
                'x': self.rad3_over2 * -1,
                'y': self.radi * 0.5,
            },
            4:{
                'x': self.rad3_over2 * -1,
                'y': self.radi * -0.5
            },
            5:{
                'x': self.radi * -0.5,
                'y': self.rad3_over2 * -1
            },
            6:{
                'x': self.radi * 0.5,
                'y': self.rad3_over2 * -1
            },
            7:{
                'x': self.rad3_over2,
                'y': self.radi -0.5
            }
        }

    def get_ray_directions(self):
        large_angle = sqrt(3)/2
        small_angle = 0.5
        self.ray_directions = {
            'x': [large_angle, small_angle, -small_angle, -large_angle, -large_angle, -small_angle, small_angle, large_angle],
            'y': [small_angle, large_angle, large_angle, small_angle, -small_angle, -large_angle, -large_angle, -small_angle]
        }

def get_diagonal_offset(axis_offset):
    return axis_offset * (sqrt(2)/2)
