import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec as grid

class Recorder:
    def __init__(self, generation, evolution_metrics = None, process_times = None):
        
        self.generation = generation
        if evolution_metrics is not None:
            self.evolution_data = pd.DataFrame(evolution_metrics)
        else:
            self.evolution_metrics = {
                'fitness':[],
                'vertical': [],
                'x rot':[],
                'y rot': [],
                'airtime': [],
                'gen': [],
                'light': []
            }
            self.process_timees = {
                'startTimes':[],
                'copyTimes' : [],
                'evalTimes' : [],
                'generations' : [],
                'fillTimes': [],
                "entireFill" : []
            }
        # print(self.data)

    def plot_ind(self, ind):
        self.plot_touch_values(ind)
        

    def add_metrics(self, ind):
        self.evolution_metrics['gen'].append(g)
        self.evolution_metrics["fitness"].append(children.pop[0].fitness)
        self.evolution_metrics['vertical'].append(children.pop[0].max_z)
        self.evolution_metrics['x rot'].append(children.pop[0].x_rotation)
        self.evolution_metrics['y rot'].append(children.pop[0].y_rotation)
        self.evolution_metrics['airtime'].append(children.pop[0].airtime)
        self.evolution_metrics['light'].append(children.pop[0].light_dist)

    
    def plotTimes(self, startTimes, evalTimes, copyTimes, fillTimes,entire_fill):
        values = {"Gen": self.generation, "Start": startTimes, "Eval": evalTimes, "Copy": copyTimes, "Fill": fillTimes,
        "EF": entire_fill}
        data = pd.DataFrame(values)
        data.plot(x = "Gen", y = ["Start", "Eval", "Copy", "Fill", "EF"])
        # plt.show()

        # panel = f.add_subplot(111)
        # plt.plot(self.data, label = "x")
        # plt.plot(y, label = "y")
        # plt.plot(z, label = "z")
        # plt.legend()
        # #panel.set_ylim(-2, +1.5)
        # plt.show()
    
    def plot_evolution(self):
        f2 = plt.figure()
        f2.add_subplot(5,1, 1)
        plt.plot(self.evolution_data['gen'], self.evolution_data['fitness'], label = 'fitness')
        f2.add_subplot(5,1, 2)
        plt.plot(self.evolution_data['gen'], self.evolution_data['vertical'], label = 'vert')
        f2.add_subplot(5,1, 3)
        plt.plot(self.evolution_data['gen'], self.evolution_data['x rot'], label = 'x')
        plt.plot(self.evolution_data['gen'], self.evolution_data['y rot'], label = 'y')
        plt.legend()
        f2.add_subplot(5,1,4)
        plt.plot(self.evolution_data['gen'], self.evolution_data['light'], label = 'light')
        f2.add_subplot(5,1, 5)
        # plt.plot(self.evolution_data['gen'], self.evolution_data['y rot'])
        # f2.add_subplot(5,1, 5)
        plt.plot(self.evolution_data['gen'], self.evolution_data['airtime'], label = 'airtime')

    def plot_touch_values(self, ind):
        touch_values = {}
        for t in range(len(ind.sensor_data)):
            # touch_values[t] = ind.sensor_data[t]
            touch_values[t] = ind.ray_data[t]
        touch_values["Index"] = list(range(len(ind.sensor_data[0])))
        touch_values["Z"] = ind.sensor_position_data
        self.touch_data = pd.DataFrame(touch_values)
        # f, ax = plt.subplots(2,2)
        # ax[0,0].subplot(3,1,1)
        # # self.touch_data.plot(x = "Index", y = list(range(len(ind.sensor_data))))
        # ax[0,0].plot(self.touch_data["Index"], self.touch_data[list(range(len(ind.sensor_data)))])
        # ax[0,0].title("Touch Values")
        # ax[0,0].subplot(3,1,2)
        # ax[0,0].plot(self.touch_data["Index"], self.touch_data["Z"])
        # ax[0,0].title("Vertical Distance")
        # ax[0,0].subplot(3,1,3)
        # ax[0,0].plot(self.touch_data["Index"], ind.light_data)
        # ax[0,0].title("Light Distance")
        # ax[0,0].show()
        fig = plt.figure(figsize=(48, 24))
        main_plt = grid.GridSpec(2,2)
        ul = grid.GridSpecFromSubplotSpec(2,2, subplot_spec = main_plt[0])
        ur = grid.GridSpecFromSubplotSpec(2,2, subplot_spec = main_plt[1])
        ll = grid.GridSpecFromSubplotSpec(2,2, subplot_spec = main_plt[2])
        lr = grid.GridSpecFromSubplotSpec(2,2, subplot_spec = main_plt[3])
        for x in range(2):
            for y in range(2):
                axul = fig.add_subplot(ul[x,y])
                axur = fig.add_subplot(ur[x,y])
                axll = fig.add_subplot(ll[x,y])
                axlr = fig.add_subplot(lr[x,y])
                if x <1 :
                    if y < 1:
                        print(list(range(len(ind.complete_data['Ray Contact'][0]))))
                        # axul.plot(self.touch_data["Index"], self.touch_data[list(range(len(ind.sensor_data)))])
                        for r in range(6):
                            axul.plot(self.touch_data["Index"], ind.complete_data['Ray Contact'][0][r])
                            axur.plot(self.touch_data["Index"], ind.complete_data['Ray Contact'][1][r])
                            axll.plot(self.touch_data["Index"], ind.complete_data['Ray Contact'][2][r])
                            axlr.plot(self.touch_data["Index"], ind.complete_data['Ray Contact'][3][r])
                        axul.set_title("Wall Ray Contact ENV" + str(1))
                        axur.set_title("Wall Ray Contact ENV" + str(2))
                        axll.set_title("Wall Ray Contact ENV" + str(3))
                        axlr.set_title("Wall Ray Contact ENV" + str(4))
                    else:
                        axul.plot(self.touch_data["Index"], ind.complete_data['Body Touch'][0])
                        axur.plot(self.touch_data["Index"], ind.complete_data['Body Touch'][1])
                        axll.plot(self.touch_data["Index"], ind.complete_data['Body Touch'][2])
                        axlr.plot(self.touch_data["Index"], ind.complete_data['Body Touch'][3])
                        axul.set_title("Body Touch" + str(1))
                        axur.set_title("Body Touch" + str(2))
                        axll.set_title("Body Touch" + str(3))
                        axlr.set_title("Body Touch" + str(4))
                else:
                    if y < 1:
                        axul.plot(self.touch_data["Index"], ind.complete_data['LightDist'][0])
                        axur.plot(self.touch_data["Index"], ind.complete_data['LightDist'][1])
                        axll.plot(self.touch_data["Index"], ind.complete_data['LightDist'][2])
                        axlr.plot(self.touch_data["Index"], ind.complete_data['LightDist'][3])
                        axul.set_title("Light Intensity ENV" + str(1), y = 0.5)
                        axur.set_title("Light Intensity ENV" + str(2), y = 0.5)
                        axll.set_title("Light Intensity ENV" + str(3), y = 0.5)
                        axlr.set_title("Light Intensity ENV" + str(4), y = 0.5)
                    else:
                        axul.plot(ind.complete_data['XPos'][0], ind.complete_data['YPos'][0])
                        axur.plot(ind.complete_data['XPos'][1], ind.complete_data['YPos'][1])
                        axll.plot(ind.complete_data['XPos'][2], ind.complete_data['YPos'][2])
                        axlr.plot(ind.complete_data['XPos'][3], ind.complete_data['YPos'][3])
                        axul.set_title("Position ENV" + str(1),y = 0.5)
                        axur.set_title("Position ENV" + str(2),y = 0.5)
                        axll.set_title("Position ENV" + str(3), y = 0.5)
                        axlr.set_title("Position ENV" + str(4), y = 0.5)
        fig.subplots_adjust(top = 0.95, bottom = 0.05)

        plt.show()






        
        

