import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec as grid
import constants as c

class Recorder:
    def __init__(self, evolution_metrics = None, process_times = None):
        
        if evolution_metrics is not None:
            self.evolution_data = pd.DataFrame(evolution_metrics)
        else:
            self.evolution_data = {
                'fitness':[],
                'vertical': [],
                'x rot':[],
                'y rot': [],
                'airtime': [],
                'gen': [],
                'light': []
            }
            self.process_times = {
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
        
    def archive_data(self):
        evolution_file_name = input("Evolution Data FileName: ")
        if c.evolution_alg =='apfo':
            pop_data_file_name = input("Population FileName: ")
            population_data = pd.DataFrame(self.evolution_data['pop_fitness'].copy())
            del self.evolution_data['pop_fitness']
            population_data.to_csv("data/" + str(pop_data_file_name) + ".csv")
        self.evolution_frame = pd.DataFrame(self.evolution_data)
        self.evolution_frame.to_csv("data/" + str(evolution_file_name) + ".csv")

    def add_metrics(self, ind, g):
        self.evolution_data["fitness"].append(ind.fitness)
        self.evolution_data['vertical'].append(ind.max_z)
        self.evolution_data['x rot'].append(ind.x_rotation)
        self.evolution_data['y rot'].append(ind.y_rotation)
        self.evolution_data['airtime'].append(ind.airtime)
        self.evolution_data['light'].append(ind.light_dist)
        self.evolution_data['gen'].append(g)
    
    def plotTimes(self):
        values = {"Gen": self.process_times['generations'], \
            "Start": self.process_times['startTimes'], \
                "Eval": self.process_times['evalTimes']\
            , "Copy": self.process_times['copyTimes'],\
                 "Fill": self.process_times['fillTimes'],\
                    #  "EF": self.process_times['entireFill']
                     }
        data = pd.DataFrame(values)
        data.plot(x = "Gen", y = ["Start", "Eval", "Copy", "Fill"])
        # plt.show()

        # panel = f.add_subplot(111)
        # plt.plot(self.data, label = "x")
        # plt.plot(y, label = "y")
        # plt.plot(z, label = "z")
        # plt.legend()
        # #panel.set_ylim(-2, +1.5)
        # plt.show()
    
    def present(self):
        plt.show()

    def plot_evolution(self):
        f2 = plt.figure(figsize=(48, 24))
        fitness = f2.add_subplot(4,1, 1)
        plt.plot(self.process_times['generations'], self.evolution_data['fitness'], label = 'fitness')
        fitness.set_title("Fitness over generations", y = 0.5)
        vert = f2.add_subplot(4,1, 2)
        plt.plot(self.process_times['generations'], self.evolution_data['vertical'], label = 'vert')
        vert.set_title("Vertcial Distance over generations", y = 0.5)
        # f2.add_subplot(5,1, 3)
        # plt.plot(self.process_times['generations'], self.evolution_data['x rot'], label = 'x')
        # plt.plot(self.process_times['generations'], self.evolution_data['y rot'], label = 'y')
        # plt.legend()
        light = f2.add_subplot(4,1,3)
        plt.plot(self.process_times['generations'], self.evolution_data['light'], label = 'light')
        light.set_title("Distance from blue box over generations", y = 0.5)
        airtime = f2.add_subplot(4,1, 4)
        # plt.plot(self.process_times['generations'], self.evolution_data['y rot'])
        # f2.add_subplot(5,1, 5)
        plt.plot(self.process_times['generations'], self.evolution_data['airtime'], label = 'airtime')
        airtime.set_title("Airtime over generations", y = 0.5)
        airtime.set_title
        f2.subplots_adjust(top = 0.95, bottom = 0.05)
        f2.show()

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
        if len(ind.complete_data['LightDist']) == 1:
            ind_fig = plt.figure(figsize=(48, 24))
            ray_contact = ind_fig.add_subplot(2,2,1)
            ray_contact.set_title("Ray Contact (Blue)")
            leg_touch = ind_fig.add_subplot(2,2,3)
            leg_touch.set_title("Touch Sensors on feet")
            color_values = []
            for r in range(c.numOfLegs):
                y_values = [r] * len(self.touch_data['Index'])
                ray_contact_inverted = [1 - ind.complete_data['Ray Contact'][0][r][term] \
                    for term in range(len(ind.complete_data['Ray Contact'][0][r]))]
                touch_values_inverted = [1 - ind.complete_data['TouchValues'][0][r][term] \
                    for term in range(len(ind.complete_data['TouchValues'][0][r]))]
                ray_contact.scatter(self.touch_data["Index"], y_values, c = ray_contact_inverted,\
                    s = 0.5, cmap = 'gray')
                leg_touch.scatter(self.touch_data["Index"], y_values, c = touch_values_inverted,\
                    s = 0.5, cmap = 'gray')
                # leg_touch.plot(self.touch_data["Index"], ind.complete_data['TouchValues'][0][r])
            light_dist = ind_fig.add_subplot(2,2,2)
            light_dist.set_title("Distance from Blue Box")
            light_dist.plot(self.touch_data["Index"], ind.complete_data['LightDist'][0])
            position = ind_fig.add_subplot(2,2,4)
            position.plot(ind.complete_data['XPos'][0], ind.complete_data['YPos'][0])
            ind_fig.subplots_adjust(top = 0.95, bottom = 0.05)
            position.set_title("Robots Position")
            ind_fig.show()
            return True
        fig = plt.figure(figsize=(48, 24))
        main_plt = grid.GridSpec(2,2)
        ul = grid.GridSpecFromSubplotSpec(2,2, subplot_spec = main_plt[0])
        ur = grid.GridSpecFromSubplotSpec(2,2, subplot_spec = main_plt[1])
        ll = grid.GridSpecFromSubplotSpec(2,2, subplot_spec = main_plt[2])
        lr = grid.GridSpecFromSubplotSpec(2,2, subplot_spec = main_plt[3])
        for x in range(2):
            for y in range(2):
                try:
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
                except IndexError:
                    continue
        fig.subplots_adjust(top = 0.95, bottom = 0.05)
        print("Graph not exited")
        # plt.show()

    def contact_plots(self):
        pass

    def record_times(self, g, evaluateTime, copyTime, fillTime, starttime):
        self.process_times['generations'].append(g)
        self.process_times['evalTimes'].append(evaluateTime)
        self.process_times['startTimes'].append(starttime)
        self.process_times['copyTimes'].append(copyTime)
        self.process_times['fillTimes'].append(fillTime)
        # self.process_times['entireFill'].append(entire_fill_time)

    def record_population_fitness(self, generation_fitness, ages, IDs, best):
        if self.evolution_data.get('pop_fitness') is None:
            self.evolution_data['pop_fitness'] = []
        self.evolution_data['pop_fitness'].append({
            'age':ages,
            'fitness':generation_fitness,
            "IDs": IDs, 
            'best_index':best
        })

    def plot_fitness_values(self):
        # temp = pd.DataFrame(self.evolution_data)
        # incrementor = self.set_increment_values()
        incrementor = 1
        for n in range(len(self.evolution_data['pop_fitness'])):
            if n % incrementor == 0:
                for gen, fitness, ID in zip(self.evolution_data['pop_fitness'][n]['age'],\
                    self.evolution_data['pop_fitness'][n]['fitness'], self.evolution_data['pop_fitness'][n]['IDs']):
                    # plt.scatter([gen] * len(fitness), fitness)
                    plt.scatter(gen, fitness)
                    plt.annotate(ID, (gen, fitness))
                plt.savefig("figures/" + str(n) + ".png")
                plt.clf()

    def set_increment_values(self):
        if c.numGens >= 1000:
            return 50
        elif c.numGens >= 500:
            return 20
        elif c.numGens >= 200:
            return 10
        elif c.numGens >=100:
            return 5
        elif c.numGens >=50:
            return 2
        else:
            return 1
