class Table:
    def __init__(self, sim, center, width, height):
        top = sim.send_box(position = [center[0], center[1], height], sides = [width, width, 0.1], color = [0,1,0], collision_group = "env")
        side_length = width/4
        legs = {}
        anchors = {}
        anchors[0] = [center[0] + side_length, center[1] + side_length]
        anchors[1] = [center[0] + side_length, center[1] - side_length]
        anchors[2] = [center[0] - side_length, center[1] + side_length]
        anchors[3] = [center[0] - side_length, center[1] - side_length] 

        for x in range(4):
            legs[x] = sim.send_box(position = [anchors[x][0], anchors[x][1], height/2], sides = [1, 1, height], collision_group = "env")
            joints = {}
            joints[x] = sim.send_hinge_joint(body1 = top, body2 = legs[x], anchor = [anchors[x][0], anchors[x][1], height])
            sim.send_hinge_joint(body1 = legs[x], body2 = -1, anchor = [anchors[x][0], anchors[x][1], 0])



