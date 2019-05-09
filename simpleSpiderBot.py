import constants as c
from simplSpiderDims import SimpleSpiderDims
from math import pi
class SimpleSpiderBot:
    def __init__(self, sim, wts):
        self.z_origin = c.spiderRadius + c.vertical_displacement + 5
        self.y_origin = 0
        self.x_origin = 0
        self.numOfLegs = c.numOfLegs
        self.radi = c.spiderRadius
        # self.dims = SpiderDims(self.radi, self.x_origin, self.y_origin, self.z_origin)
        self.dims = SimpleSpiderDims(self.radi, self.x_origin, self.y_origin, self.z_origin)
        self.leg_radi = self.radi * 0.1
        # self.body = sim.send_sphere(x = 0, y = 0, z = self.z_origin, radius=self.radi)
        self.body = sim.send_sphere(position = (self.dims.body['x'],self.dims.body['y'],self.dims.body['z']), radius= self.radi, collision_group = "body")
        self.build_legs(sim)
        self.add_jump_sensors(sim)
        self.add_sensors(sim)
        self.add_motors(sim)
        self.add_hiddens(sim)
        self.add_snapses(sim, wts)

    def build_legs(self, sim):
        self.build_leg_segment1(sim)
        self.build_leg_segment2(sim)
        self.build_joint0(sim)
        self.build_joint(sim) 

    def build_leg_segment1(self, sim):
        self.leg1s = {}
        for n in range(self.numOfLegs):
            self.leg1s[n] = sim.send_cylinder(
                position= (
                    self.dims.leg1[n]['x'], 
                    self.dims.leg1[n]['y'], 
                    self.dims.leg1_z, 
                ),
                length = self.dims.leg1_length, 
                radius=self.dims.leg_radi, 
                orientation= (
                    self.dims.position_normals['leg1']['r1'][n], 
                    self.dims.position_normals['leg1']['r2'][n], 
                    self.dims.leg1_r3,     
                ),
                color = (
                    self.dims.colors['red'][n], 
                    self.dims.colors['green'][n], 
                    self.dims.colors['blue'][n]    
                ),
                collision_group = "robot"
            )


    def build_joint(self, sim):
        self.j1s = {}
        self.spring1 = {}
        for n in range(self.numOfLegs):
            self.j1s[n] = sim.send_hinge_spring_joint(
                body1 = self.leg1s[n],
                body2 = self.leg2s[n],
                axis1 = (
                    self.dims.joint_normals['n1'][n], 
                    self.dims.joint_normals['n2'][n], 
                    0 
                ), 
                axis2 = (
                    self.dims.joint_normals['n1.2'][n],
                    self.dims.joint_normals['n2.2'][n],
                    0
                ),
                anchor = (
                    self.dims.j1[n]['x'], 
                    self.dims.j1[n]['y'],
                    self.dims.j1_z,    
                ),
                stiffness= c.springStrength,
                damping= 0
            )
            self.all_joints[1][n] = self.j1s[n]

    def build_leg_segment2(self, sim):
        self.leg2s = {}
        for n in range(self.numOfLegs):
            self.leg2s[n] = sim.send_cylinder(
                position = (
                    self.dims.leg2[n]['x'], 
                    self.dims.leg2[n]['y'],
                    self.dims.leg2_z,     
                ),
                radius= self.dims.leg_radi, 
                length = self.dims.leg2_length, 
                orientation=(
                    self.dims.position_normals['leg2']['r1'][n], 
                    self.dims.position_normals['leg2']['r2'][n], 
                    self.dims.leg2_r3, 
                ),
                color=(
                    self.dims.colors['red'][n], 
                    self.dims.colors['green'][n], 
                    self.dims.colors['blue'][n]),
                collision_group = "robot"    
                )

    def build_joint0(self, sim):
        self.j0s = {}
        self.all_joints = {
            0: {},
            1: {}
        }
        self.j0springs = {}
        for n in range(self.numOfLegs):
            self.j0s[n] = sim.send_hinge_spring_joint(
                body1 = self.body, 
                body2 = self.leg1s[n],
                anchor = (
                    self.dims.j0[n]['x'], 
                    self.dims.j0[n]['y'], 
                    self.dims.j0_z, 
                ),
                axis1= (
                    self.dims.joint_normals['n1'][n], 
                    self.dims.joint_normals['n2'][n], 
                    0 
                ), 
                axis2= (
                    self.dims.joint_normals['n1.2'][n],
                    self.dims.joint_normals['n2.2'][n],
                    0
                ), 
                stiffness=c.springStrength, 
                damping=0, 
                joint_range = (-pi/2, (3*pi)/4)
            )
            self.all_joints[0][n] = self.j0s[n]
    
    def add_sensors(self, sim):
        self.sensors = {}
        self.sensorNeurons = {}
        self.add_touch_sensor(sim)
        # # Position along the z axis 
        self.position = sim.send_position_sensor(body_id= self.body, which_dimension = 'z')
        # self.sensors[self.numOfLegs] = self.position
        # self.sensorNeurons[self.numOfLegs] = sim.send_sensor_neuron(sensor_id= self.sensors[self.numOfLegs])
        # #Quaternion sensors along the x axis and the sensors and sensorNuerons attached  
        self.x_rotation_sensor = sim.send_quaternion_sensor(body_id = self.body, which_sense = 'x')
        # self.sensors[self.numOfLegs + 1] = self.x_rotation_sensor
        # self.sensorNeurons[self.numOfLegs + 1] = sim.send_sensor_neuron(sensor_id = self.sensors[self.numOfLegs + 1])
        # # Quaternion sensors along the y axis and the sensors and sensorNuerons attached 
        self.y_rotation_sensor = sim.send_quaternion_sensor(body_id = self.body, which_sense = 'y')
        # self.sensors[self.numOfLegs + 2] = self.y_rotation_sensor
        # self.sensorNeurons[self.numOfLegs + 2] = sim.send_sensor_neuron(sensor_id = self.sensors[self.numOfLegs + 2])
        # # Touch values of the body and attached sensors 
        self.body_touch = sim.send_touch_sensor(body_id = self.body)
        self.sensors[len(self.sensors)] = self.body_touch
        self.sensorNeurons[len(self.sensorNeurons)] = sim.send_sensor_neuron(sensor_id = self.sensors[len(self.sensors) - 1])
        # Light sensors and the attached bodies 

        # self.light_sensor = sim.send_light_sensor(body_id = self.body)
        # # self.sensors[self.numOfLegs + 4] = self.light_sensor
        # # self.sensorNeurons[self.numOfLegs + 4] = sim.send_sensor_neuron(sensor_id = self.sensors[self.numOfLegs + 4])
        # self.sensors[self.numOfLegs] = self.light_sensor
        # self.sensorNeurons[self.numOfLegs] = sim.send_sensor_neuron(sensor_id = self.sensors[self.numOfLegs])
        self.connect_ray_sensors(sim)

        self.y_position_sensor = sim.send_position_y_sensor(body_id = self.body)
        self.x_position_sensor = sim.send_position_x_sensor(body_id = self.body)

    def connect_ray_sensors(self, sim):
        index = len(self.sensors)
        for s in range(8):
            self.sensors[index + s] = self.ray_sensors[s]
            self.sensorNeurons[index + s] = sim.send_sensor_neuron(sensor_id = self.sensors[index + s])
        


    def add_touch_sensor(self, sim):
        self.touchSensors = {}
        #Adding touch sensors
        for n in range(self.numOfLegs):
            # self.sensors[n] = sim.send_touch_sensor(body_id = self.leg2s[n])
            # self.sensorNeurons[n] = sim.send_sensor_neuron(sensor_id= self.sensors[n])
            # self.touchSensors[n] = self.sensors[n]
            self.touchSensors[n] = sim.send_touch_sensor(body_id = self.leg2s[n])
            self.sensors[n] = self.touchSensors[n]
            self.sensorNeurons[n] = sim.send_sensor_neuron(sensor_id= self.sensors[n])
            # self.touchSensors[n] = self.sensors[n]

    def add_jump_sensors(self, sim):
        self.ray_sensors = {}
        self.rays = {}
        for r in range(8):
            # self.ray_sensors[r] = sim.send_ray_sensor(
            #     position = [
            #         self.x_origin, 
            #     ]
            # )
            self.rays[r] = sim.send_ray(body_id = self.body, 
                position = [
                    self.dims.ray_sensors[r]['x'],
                    self.dims.ray_sensors[r]['y'],
                    self.dims.body['z']
                ],
                direction = [
                    self.dims.ray_directions['x'][r],
                    self.dims.ray_directions['y'][r],
                    0
                ],
                max_length = 50 )
            self.ray_sensors[r] = sim.send_ray_sensor(
                ray_id = self.rays[r],
                which_sense = 'b'
            )

    # def add_light_sensors(self):
    
    def add_motors(self, sim):
        self.motors = {
            0:{},
            1:{}
        }
        self.motorNuerons = {
            0:{},
            1:{}
        }
        for j in self.all_joints:
            for j2 in self.all_joints[j]:
                self.motors[j][j2] = sim.send_rotary_actuator(joint_id= self.all_joints[j][j2], max_force= c.maxJointForce) 
                self.motorNuerons[j][j2] = sim.send_motor_neuron(motor_id = self.motors[j][j2])


    def add_hiddens(self, sim):
        self.hiddens = {}
        for n in range(c.num_of_hidden):
            self.hiddens[n] = sim.send_hidden_neuron()

    def add_snapses(self, sim, wts):
        if len(self.hiddens) < 1:
             for s in self.sensorNeurons:
            # for h in self.hiddens:
                for l in self.all_joints:
                    for k in self.all_joints[l]:
                        sim.send_synapse(
                            source_neuron_id = self.sensorNeurons[s], 
                            target_neuron_id = self.motorNuerons[l][k], 
                            weight = wts[0][s][k][l]
                        )
        else:
            for j in self.sensorNeurons:
                for h in self.hiddens:
                    sim.send_synapse(source_neuron_id = self.sensorNeurons[j], target_neuron_id = self.hiddens[h], weight = wts[0][j][h])
            for h in self.hiddens:
                for h2 in self.hiddens:
                    if h == h2:
                        continue
                    sim.send_synapse(source_neuron_id = self.hiddens[h], target_neuron_id = self.hiddens[h2], weight = wts[1][h][h2])
            for h in self.hiddens:
                for l in self.all_joints:
                    for k in self.all_joints[l]:
                        try:
                            sim.send_synapse(source_neuron_id = self.hiddens[h], target_neuron_id = self.motorNuerons[l][k], weight = wts[2][h][k][l])
                        except TypeError:
                            print(self.hiddens)
                            print(self.motorNuerons[l])
                            print(wts[2][h][l])
                            exit()
                        except IndexError:
                            print("Index")
                            print(self.hiddens)
                            print(self.motorNuerons[l])
                            print(wts[2][h][k][1])
                            exit()
            # for j in self.sensorNeurons:
            #     # for h in self.hiddens:
            #         for i in self.motors:
            #             sim.send_synapse(
            #                 source_neuron_id = self.sensorNeurons[j], 
            #                 target_neuron_id = self.motorNueron[i], 
            #                 weight = wts[j, i]
            #             )

    def assign_target(self, sim, target_id, wts):
        self.target_sensor = sim.send_distance_to_sensor(body1_id = self.body, body2_id = target_id)
        position = len(self.sensors)
        self.sensors[position] =  self.target_sensor
        self.sensorNeurons[position] = sim.send_sensor_neuron(sensor_id = self.sensors[position])
        self.add_snapses(sim, wts)
        self.delete_data()

    def delete_data(self):
        del self.j1s
        del self.j0s
        del self.leg1s
        del self.leg2s
        del self.sensorNeurons
        del self.sensors
        del self.motors
        del self.all_joints
        del self.motorNuerons