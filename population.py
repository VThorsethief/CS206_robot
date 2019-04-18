from individual import INDIVIDUAL
import copy
import random
import constants as c
import time
class POPULATION:
    def __init__(self, popSize):
        self.pop = {}
        self.popSize = popSize
        

    def Initialize(self):
        for i in range(self.popSize):
            self.pop[i] = INDIVIDUAL(i)


    def Print(self):
        for i in self.pop:
            if(i in self.pop):
                self.pop[i].Print()
        print()

    def Evaluate(self, env, pb, pp, retain_data = False):
        numOfEnv = len(env.envs)
        # for i in self.pop:
            # print("Pre Evaluation Fitness:", self.pop[i].fitness)
        for e in range(numOfEnv):
            for i in self.pop:
                # self.pop[i].fitness = 0
                if (len(self.pop) == 1 & e > 0):
                    pp = True
                self.pop[i].Start_Evaluation(env.envs[e], pb, pp)
            for i in self.pop:
                self.pop[i].Complete_Fitness(retain_data)
        
        for i in self.pop:
            # print("after eval",self.pop[i].fitness)
            self.pop[i].fitness /= numOfEnv
            # print("Evaluate Fitness:",self.pop[i].fitness)
            # print(self.pop[i].fitness)
        

    def Evaluate_Select(self,pb, indices):
        for i in indices:
            self.pop[i].Evaluate(pb)
    
    def Mutate(self):
        for i in self.pop:
            self.pop[i].Mutate()
            # self.pop[i].cppn.mutate()

    def ReplaceWith(self, other):
        for i in self.pop:
            if self.pop[i].fitness < other.pop[i].fitness:
                self.pop[i] = other.pop[i]

    def Fill_From(self, other):
        fill_start = time.clock()
        self.pop[0] = self.Copy_Best_From(other)
        self.Collect_Children_From(other)
        for x in self.pop:
            self.pop[x].fitness = 0
        entire_fill = time.clock() - fill_start
        return entire_fill
            # print("Fill From fitness:",self.pop[x].fitness)
    
    def Copy_Best_From(self, other):
        maxIndex = 0
        for i in range(len(other.pop)):
            if other.pop[i].fitness > other.pop[maxIndex].fitness:
                maxIndex = i
        best = copy.deepcopy(other.pop[maxIndex]) 
        return best

    def Collect_Children_From(self, other):
        for i in range(1, self.popSize):
            # self.pop[i] = copy.deepcopy(other.pop[i])
            winner = copy.deepcopy(other.Winner_Of_Tournament_Selection())
            winner.Mutate()
            # winner.cppn.mutate()
            self.pop[i] = winner

    def Winner_Of_Tournament_Selection(other):
        p1 = random.randint(0,other.popSize - 1)
        p2 = random.randint(0,other.popSize - 1)
        while(p1 == p2):
            p2 = random.randint(0,other.popSize - 1)
        if other.pop[p1].fitness > other.pop[p2].fitness:
            return other.pop[p1]
        else:
            return other.pop[p2]

    def Evaluate_Best(self, envs, pb = False, pp = True, retain_data = True):
        for e in range(c.numEnvs):
            if (e > 0):
                pp = False
            self.pop[0].Start_Evaluation(envs.envs[e], pb, pp)
            self.pop[0].Complete_Fitness(retain_data)
        

