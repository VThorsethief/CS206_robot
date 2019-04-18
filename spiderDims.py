from math import sin, cos, pi, sqrt
class SpiderDims:
    def __init__(self, radius, x, y, z):
        self.z_origin = radius * 3
        self.y_origin = 0
        self.x_origin = 0
        self.radi = radius
        self.leg_radi = self.radi * 0.1
        self.build_leg_dims()

    def build_leg_dims(self):
        self.build_rotation_normals()
        self.build_leg1_dims()
        self.build_j1_dims()
        self.build_leg2_dims()
        self.build_j2_dims()
        self.build_leg3_dims()
        self.build_j3_dims()
        self.build_leg4_dims()
        self.build_j0_dims()
        self.add_colors()

    def build_j0_dims(self):
        self.j0_z = self.z_origin - (self.radi * 1) * sin((pi)/6)
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
        self.leg1_length = self.radi * .7
        self.leg1_z = self.z_origin - (self.radi * 1.1) * sin((pi)/6)
        self.leg1_r3 = -0.4
        self.leg1_x = {}
        self.leg1_y = {}
        self.leg1_r1 = {}
        self.leg1_r2 = {}
        axis_offset = (self.radi * 1.1) * cos((pi/6))
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
        self.j1_z = self.z_origin - (self.radi * 1 + self.leg1_length/2) * sin((pi)/6)
        self.j1_radi = self.radi * 0.112
        axis_offset = (self.radi * 1.11 + self.leg1_length/2) * cos((pi/6))
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
        self.leg2_length = self.radi * 2.5
        self.leg2_r3 = 2
        self.leg2_z = self.j1_z + ((self.leg2_length/2) * sin(pi/3))
        axis_offset = ((self.leg2_length/2) * cos(pi/3))
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
        
    def build_j2_dims(self):
        self.j2_z = self.j1_z + ((self.leg2_length) * sin(pi/3))
        axis_offset = ((self.leg2_length*0.95) * cos(pi/3))
        diagonal_offset = get_diagonal_offset(axis_offset)
        self.j2 = {
            # Joint 2 x+ axis
            0:{
                'x': self.j1[0]['x'] + axis_offset,
                'y': 0 
            },
            # Joint 2 y+ axis 
            1:{
                'x': 0, 
                'y': self.j1[1]['y'] + axis_offset
            }, 
            # Joint 2 x- axis 
            2:{
                'x': self.j1[2]['x'] - axis_offset,
                'y': 0
            }, 
            # Joint 2 y- axis 
            3:{
                'x': 0, 
                'y': self.j1[3]['y'] - axis_offset
            }, 
            # Joint 2 xy+ axis 
            4:{
                'x': self.j1[4]['x'] + diagonal_offset,
                'y': self.j1[4]['y'] + diagonal_offset
            },
            # Joint 2 xy- axis 
            5:{
                'x': self.j1[5]['x'] - diagonal_offset,
                'y': self.j1[5]['y'] - diagonal_offset
            }, 
            # Joint 2 x+y- axis 
            6:{
                'x': self.j1[6]['x'] + diagonal_offset,
                'y': self.j1[6]['y'] - diagonal_offset
            },
            # Joint 2 x-y+ axis 
            7:{
                'x': self.j1[7]['x'] - diagonal_offset,
                'y': self.j1[7]['y'] + diagonal_offset,
            }
        }

    def build_leg3_dims(self):
        self.leg3_length = self.radi * 3
        self.leg3_z = self.j2_z - ((self.leg3_length/2) * sin(pi/3))
        self.leg3_r3 = -2
        axis_offset = ((self.leg3_length/2)* .95 * cos(pi/3))
        diagonal_offset = get_diagonal_offset(axis_offset)
        self.leg3 = {
            # Third Leg Segment x+ axis 
            0:{
                'x': self.j2[0]['x'] + axis_offset,
                'y': 0
            }, 
            # Third Leg Segment y+ axis 
            1:{
                'x': 0, 
                'y': self.j2[1]['y'] + axis_offset
            },
            # Third Leg Segment x- axis 
            2:{
                'x': self.j2[2]['x'] - axis_offset,
                'y': 0
            },
            # Third Leg Segment y- axis 
            3:{
                'x': 0, 
                'y': self.j2[3]['y'] - axis_offset
            }, 
            # Third Leg Segment xy+ axis 
            4:{
                'x': self.j2[4]['x'] + diagonal_offset,
                'y': self.j2[4]['y'] + diagonal_offset 
            }, 
            # Third Leg Segment xy- axis 
            5:{
                'x': self.j2[5]['x'] - diagonal_offset, 
                'y': self.j2[5]['y'] - diagonal_offset
            },
            # Third Leg Segment x+y- axis 
            6:{
                'x': self.j2[6]['x'] + diagonal_offset,
                'y': self.j2[6]['y'] - diagonal_offset
            }, 
            # Third Leg Segment x-y+ axis 
            7:{
                'x': self.j2[7]['x'] - diagonal_offset,
                'y': self.j2[7]['y'] + diagonal_offset
            }
        }

    def build_j3_dims(self):
        self.j3_z = self.j2_z - ((self.leg3_length) *1.01* sin(pi/3))
        self.j3_radi = self.j1_radi
        axis_offset = ((self.leg3_length)* .92 * cos(pi/3))
        diagonal_offset = get_diagonal_offset(axis_offset) 
        self.j3 = {
            # Joint 3 x+ axis 
            0:{
                'x': self.j2[0]['x'] + axis_offset,
                'y': 0
            },
            # Joint 3 y+ axis 
            1:{
                'x': 0,
                'y': self.j2[1]['y'] + axis_offset
            }, 
            # Joint 3 x- axis 
            2:{
                'x': self.j2[2]['x'] - axis_offset,
                'y': 0
            }, 
            # Joint 3 y- axis 
            3:{
                'x': 0, 
                'y': self.j2[3]['y'] - axis_offset
            }, 
            # Joint 3 xy+ axis 
            4:{
                'x': self.j2[4]['x'] + diagonal_offset,
                'y': self.j2[4]['y'] + diagonal_offset
            }, 
            # Joint 3 xy- axis 
            5:{
                'x': self.j2[5]['x'] - diagonal_offset, 
                'y': self.j2[5]['y'] - diagonal_offset
            }, 
            # Joint 3 x+y- axis 
            6:{
                'x': self.j2[6]['x'] + diagonal_offset, 
                'y': self.j2[6]['y'] - diagonal_offset
            },
            # Joint 3 x-y+ axis 
            7:{
                'x': self.j2[7]['x'] - diagonal_offset, 
                'y': self.j2[7]['y'] + diagonal_offset
            }

        }

    def build_leg4_dims(self):
        self.leg4_length = self.radi * 1.8
        self.leg4_z = self.j3_z - ((self.leg4_length/2) *1.01* sin(pi/3))
        self.leg4_r3 = 2
        axis_offset = ((self.leg4_length/2)* .90 * cos(pi/3))
        diagonal_offset = get_diagonal_offset(axis_offset)
        self.leg4 = {
            # Fourth Leg Segment x+ axis 
            0:{
                'x': self.j3[0]['x'] - axis_offset, 
                'y': 0
            }, 
            # Fourth Leg Segment y+ axis 
            1:{
                'x': 0, 
                'y': self.j3[1]['y'] - axis_offset
            }, 
            # Fourth Leg Segment x- axis 
            2:{
                'x': self.j3[2]['x'] + axis_offset, 
                'y': 0
            }, 
            # Fourth Leg Segment y- axis 
            3:{
                'x': 0, 
                'y': self.j3[3]['y'] + axis_offset
            }, 
            # Fourth Leg Segment xy+ axis 
            4:{
                'x': self.j3[4]['x'] - diagonal_offset, 
                'y': self.j3[4]['y'] - diagonal_offset
            }, 
            # Fourth Leg Segment xy- axis 
            5:{
                'x': self.j3[5]['x'] + diagonal_offset, 
                'y': self.j3[5]['y'] + diagonal_offset
            }, 
            # Fourth Leg Segment x+y- axis 
            6:{
                'x': self.j3[6]['x'] - diagonal_offset, 
                'y': self.j3[6]['y'] + diagonal_offset
            }, 
            #Fourth Leg Segment x-y+ axis 
            7:{
                'x': self.j3[7]['x'] + diagonal_offset, 
                'y': self.j3[7]['y'] - diagonal_offset
            }
        }

    def build_j4_dims(self):
        self.j4_z = self.j3_z - ((self.leg4_length) *1.01* sin(pi/3))
        axis_offset = ((self.leg4_length)* .90 * cos(pi/3))
        diagonal_offset = get_diagonal_offset(axis_offset)
        self.j4 = {
            # Joint 4 x+ axis 
            0:{
                'x': self.j3[0]['x'] + axis_offset, 
                'y': 0
            }, 
            # Joint 4 y+ axis 
            1:{
                'x': 0, 
                'y': self.j3[1]['y'] + axis_offset
            }, 
            # Joint 4 x- axis 
            2:{
                'x': self.j3[2]['x'] - axis_offset, 
                'y': 0
            }, 
            # Joint 4 y- axis 
            3:{
                'x': 0, 
                'y': self.j3[3]['y'] - axis_offset
            }, 
            # Joint 4 xy+ axis 
            4:{
                'x': self.j3[4]['x'] + diagonal_offset, 
                'y': self.j3[4]['y'] + diagonal_offset
            }, 
            # Joint 4 xy- axis 
            5:{
                'x': self.j3[5]['x'] - diagonal_offset, 
                'y': self.j3[5]['y'] - diagonal_offset
            }, 
            # Joint 4 x+y- axis 
            6:{
                'x': self.j3[6]['x'] + diagonal_offset, 
                'y': self.j3[6]['x'] - diagonal_offset
            }, 
            # Joint 4 x-y+ axis 
            7:{
                'x': self.j3[7]['x'] - diagonal_offset, 
                'y': self.j3[7]['y'] + diagonal_offset
            }
        }

    def build_rotation_normals(self):
        self.joint_normals = {
            "n1": [0, -1, 0, 1, -1, 1, 1, -1],
            'n2': [1, 0, -1, 0, 1, -1, 1, -1], 
            'n1.2' : [-1, 0, 1, 0, -1, 1, -1, 1],
            'n2.2' : [0, -1, 0, 1, -1, 1, 1, -1]
        }
        self.position_normals = {
            # "r1": [1, 0, -1, 0, 1, -1, 1, -1],
            # "r2": [0, 1, 0, -1, 1, -1, -1, 1]
            "r1": [1, 0, -1, 0, sqrt(2)/2, -sqrt(2)/2, sqrt(2)/2, -sqrt(2)/2],
            "r2": [0, 1, 0, -1, sqrt(2)/2, -sqrt(2)/2, -sqrt(2)/2, sqrt(2)/2]
        }

    def add_colors(self):
        self.colors = {
            'red':[1, 0, 1, 0, 0, 0, 1, 1],
            'green': [0, 1, 0, 1, 0, 0, 0, 0], 
            "blue": [0, 0, 0, 0, 1, 1, 1, 1]
        }
def get_diagonal_offset(axis_offset):
    return axis_offset * (sqrt(2)/2)


