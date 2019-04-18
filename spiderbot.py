# from pyrosim import pyrosim, Simulator as sim
from math import pi, cos, sin
from spiderDims import SpiderDims
import constants as c
# sim = pyrosim.Simulator
class Spiderbot:
    def __init__(self, sim, wts):
        
        self.z_origin = c.spiderRadius * 3
        self.y_origin = 0
        self.x_origin = 0
        self.numOfLegs = c.numOfLegs
        self.radi = c.spiderRadius
        self.dims = SpiderDims(self.radi, self.x_origin, self.y_origin, self.z_origin)
        self.leg_radi = self.radi * 0.1
        # self.body = sim.send_sphere(x = 0, y = 0, z = self.z_origin, radius=self.radi)
        self.body = sim.send_sphere(position = (0,0,self.z_origin), radius= self.radi)
        self.build_legs(sim)

        self.add_sensors(sim)
        self.add_motors(sim)
        self.add_snapses(sim, wts)

        del self.j1s
        del self.j2s
        del self.j3s
        del self.j0s
        del self.leg1s
        del self.leg2s
        del self.leg3s
        del self.leg4s
        del self.sensorNeurons
        del self.sensors
        del self.motors
        del self.all_joints
        del self.motorNueron

        
        

    def build_legs(self, sim):
        self.build_leg_segment1(sim)
        self.build_leg_segment2(sim)
        self.build_leg_segment3(sim)
        self.build_leg_segment4(sim)
        self.build_joint0(sim)
        self.build_joint(sim)
        self.build_joint2(sim)
        self.build_joint3(sim)


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
                    self.dims.position_normals['r1'][n], 
                    self.dims.position_normals['r2'][n], 
                    self.dims.leg1_r3,     
                ),
                color = (
                    self.dims.colors['red'][n], 
                    self.dims.colors['green'][n], 
                    self.dims.colors['blue'][n]    
                )
            )


    def build_joint(self, sim):
        self.j1s = {}
        self.spring1 = {}
        for n in range(self.numOfLegs):
            # self.j1s[n] = sim.send_hinge_joint(
            #     anchor = (
            #         self.dims.j1[n]['x'], 
            #         self.dims.j1[n]['y'],
            #         self.dims.j1_z,    
            #     ),
            #     body1 = self.leg1s[n],
            #     body2 = self.leg2s[n],
            #     axis = (
            #         self.dims.joint_normals['n1'][n], 
            #         self.dims.joint_normals['n2'][n], 
            #         0
            #     ) 
            #     )
            self.j1s[n] = sim.send_hinge_spring_joint(
                body1 = self.leg1s[n],
                body2 = self.leg2s[n],
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
                anchor = (
                    self.dims.j1[n]['x'], 
                    self.dims.j1[n]['y'],
                    self.dims.j1_z,    
                ),
                stiffness= c.springStrength,
                damping= 0
            )
            self.all_joints[n + self.numOfLegs] = self.j1s[n]
        
        


    def build_joint2(self, sim):
        
        # self.joint2 = sim.send_sphere(x = self.dimsj2A_x, z = self.j2_z, radius= self.j2_radi, r = 1, g = 0, b = 0)
        self.j2s = {}
        self.j2springs = {}

        for n in range(self.numOfLegs):
            # self.j2s[n] = sim.send_hinge_joint(
            #     anchor = (
            #         self.dims.j2[n]['x'], 
            #         self.dims.j2[n]['y'], 
            #         self.dims.j2_z    
            #     ),
            #     body1 = self.leg2s[n],                 
            #     body2 = self.leg3s[n],
            #     axis= (
            #         self.dims.joint_normals['n1'][n], 
            #         self.dims.joint_normals['n2'][n], 
            #         0    
            #     )
            #     )
            self.j2s[n] = sim.send_hinge_spring_joint(
                body1 = self.leg2s[n],
                body2 = self.leg3s[n],
                anchor = (
                    self.dims.j2[n]['x'], 
                    self.dims.j2[n]['y'], 
                    self.dims.j2_z    
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
                ), stiffness= c.springStrength, 
                damping = 0
            )
            
            self.all_joints[n + (self.numOfLegs * 2)] = self.j2s[n]

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
                    self.dims.position_normals['r1'][n], 
                    self.dims.position_normals['r2'][n], 
                    self.dims.leg2_r3, 
                ),
                color=(
                    self.dims.colors['red'][n], 
                    self.dims.colors['green'][n], 
                    self.dims.colors['blue'][n])    
                )


    def build_leg_segment3(self, sim):
        self.leg3s = {}
        for n in range(self.numOfLegs):
            self.leg3s[n] = sim.send_cylinder(
                position=(
                    self.dims.leg3[n]['x'], 
                    self.dims.leg3[n]['y'], 
                    self.dims.leg3_z    
                ),
                orientation=(
                    self.dims.position_normals['r1'][n], 
                    self.dims.position_normals['r2'][n],
                    self.dims.leg3_r3    
                ) ,
                length= self.dims.leg3_length,
                radius=self.dims.leg_radi,
                color = (
                    self.dims.colors['red'][n], 
                    self.dims.colors['green'][n], 
                    self.dims.colors['blue'][n]
                )
                ) 
    
    def build_joint3(self, sim):
        self.j3s = {}
        self.j3springs = {}
        for n in range(self.numOfLegs):
            # self.j3s[n] = sim.send_hinge_joint(
            #     anchor = (
            #         self.dims.j3[n]['x'], 
            #         self.dims.j3[n]['y'],
            #         self.dims.j3_z,     
            #     ),
            #     axis = (
            #         self.dims.joint_normals['n1'][n], 
            #         self.dims.joint_normals['n2'][n], 
            #         0    
            #     ), 
            #     body1 = self.leg3s[n],
            #     body2 = self.leg4s[n]
            #     )
            self.j3s[n] = sim.send_hinge_spring_joint(
                body1 = self.leg3s[n], 
                body2 = self.leg4s[n],
                anchor = (
                    self.dims.j3[n]['x'], 
                    self.dims.j3[n]['y'],
                    self.dims.j3_z,     
                ), 
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
                stiffness= c.springStrength,
                damping= 0  
            )
            self.all_joints[n + (self.numOfLegs * 3)] = self.j3s[n]
        
    def build_leg_segment4(self, sim):
        self.leg4s = {}
        for n in range(self.numOfLegs):
            self.leg4s[n] = sim.send_cylinder(
                position= (
                    self.dims.leg4[n]['x'], 
                    self.dims.leg4[n]['y'], 
                    self.dims.leg4_z,     
                ),
                length=self.dims.leg4_length, 
                radius = self.dims.leg_radi,
                orientation=(
                    self.dims.position_normals['r1'][n],
                    self.dims.position_normals['r2'][n], 
                    self.dims.leg4_r3,     
                ),
                color = (
                    self.dims.colors['red'][n], 
                    self.dims.colors['green'][n], 
                    self.dims.colors['blue'][n]
                )
                )

    def build_joint0(self, sim):
        self.j0s = {}
        self.all_joints = {}
        self.j0springs = {}
        for n in range(self.numOfLegs):
            # self.j0s[n] = sim.send_hinge_joint(
            #     anchor = (
            #         self.dims.j0[n]['x'], 
            #         self.dims.j0[n]['y'], 
            #         self.dims.j0_z, 
            #     ),
            #     axis = (
            #         self.dims.joint_normals['n1'][n], 
            #         self.dims.joint_normals['n2'][n], 
            #         0    
            #     ),
            #     body1 = self.body, 
            #     body2 = self.leg1s[n]
            #     )
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
            self.all_joints[n] = self.j0s[n]
    
    def add_sensors(self, sim):
        self.sensors = {}
        self.sensorNeurons = {}
        self.touchSensors = {}
        for n in range(self.numOfLegs):
            self.sensors[n] = sim.send_touch_sensor(body_id = self.leg4s[n])
            self.sensorNeurons[n] = sim.send_sensor_neuron(sensor_id= self.sensors[n])
            self.touchSensors[n] = self.sensors[n]
        self.position = sim.send_position_sensor(body_id= self.body, which_dimension = 'z')
        self.sensors[len(self.sensors) - 1] = self.position
        self.sensorNeurons[len(self.sensors) - 1] = sim.send_sensor_neuron(sensor_id= self.sensors[len(self.sensors) -1])
        self.x_rotation_sensor = sim.send_quaternion_sensor(body_id = self.body, which_sense = 'x')
        self.y_rotation_sensor = sim.send_quaternion_sensor(body_id = self.body, which_sense = 'y')
    
    def add_motors(self, sim):
        self.motors = {}
        self.motorNueron = {}
        for j in self.all_joints:
            self.motors[j] = sim.send_rotary_actuator(joint_id= self.all_joints[j]) 
            self.motorNueron[j] = sim.send_motor_neuron(motor_id = self.motors[j])
            

    def add_snapses(self, sim, wts):
        for j in self.sensorNeurons:
            for i in self.motors:
                sim.send_synapse(
                    source_neuron_id = self.sensorNeurons[j], 
                    target_neuron_id = self.motorNueron[i], 
                    weight = wts[j, i]
                )