from individual import INDIVIDUAL
import copy
import random
import constants as c
import time
class POPULATION:
    def __init__(self, popSize):
        self.pop = {}
        self.popSize = popSize
        
    # Age-Fitness Perito front optimization for populations. 
    def apfo(self, other):
        fill_start = time.clock()
        keep = []
        pop_fitness = []
        ages = []
        IDs = []
        removed = []
        # Adds age and IDs for plotting pngs at the end of evolution to track the peritofront.
        for x in range(len(other.pop)):
            keep.append(True)
            IDs.append(other.pop[x].ID)
            ages.append(other.pop[x].age)
            pop_fitness.append(other.pop[x].fitness)
            for y in range(len(other.pop)):
                # If the indivudual is older and has a lower performance than a younger individual, 
                # than that individual is marked for removal. All individuals in the first population 
                # are excempt to allow them another mutation to imporve. 
                if other.pop[y].fitness > other.pop[x].fitness and \
                    other.pop[y].age <= other.pop[x].age and other.pop[x].age > 0:
                    keep[x] = False
        # Retrieves the index of the best indivdual from the population. I don't want to move their 
        # position in the population, only flag their ID for later.  
        best_index = self.retrieve_best_index(other)
        pop_limit = len(other.pop)

        # If there is a saturation of the peritofront, I want to add some more individuals, once I 
        # reach a max of 20, then remove the lagging 10% according to fitness.
        #TODO: Change this, if I remove the bottom 10% in the event of a saturation, then it's 
        # counter to the idea of the afpo. Maybe choose 10% at random to remove?
        if sum(keep) > len(other.pop) * 0.8:
            if len(other.pop) < 20:
                pop_limit = len(other.pop) + 2
                self.popSize = pop_limit
                keep.extend([False, False])
            else:
                other.replace()
        for n in range(pop_limit):
            if keep[n]:
                self.pop[n] = copy.deepcopy(other.pop[n])
                # Don't mutate the best individual
                #TODO: Should this change so all best-performers within each age group are kept?
                if n != best_index:
                    self.pop[n].Mutate()
                self.pop[n].increment_age()
            else:
                self.pop[n] = INDIVIDUAL(n)
                self.pop[n].age = 0
                removed.append(n)
            self.pop[n].fitness = 0
        print("Removed: ", removed)
        return pop_fitness, ages, IDs, best_index

    # Copies and returns the best performing individual in the population by iterating through the population            
    def Copy_Best_From(self, other):
        maxIndex = 0
        for i in range(len(other.pop)):
            if other.pop[i].fitness > other.pop[maxIndex].fitness:
                maxIndex = i
        
        best = copy.deepcopy(other.pop[maxIndex])
        return best

    # Collects the rest of the children from the population excluding the best, and chooses bwteen two based on 
    # tournament selection. Mutates the winner and adds to the population.
    def Collect_Children_From(self, other):
        for i in range(1, self.popSize):
            # self.pop[i] = copy.deepcopy(other.pop[i])
            winner = copy.deepcopy(other.Winner_Of_Tournament_Selection())
            winner.Mutate()
            # winner.cppn.mutate()
            self.pop[i] = winner

    # To part evalution method which allows you to run sumulations in parllel. 
    # Starts the simulation for all the robots in the population, then completes the evaluation. 
    # Calls Start_Evaluation() and Complete_Evaluation()
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
 
    # Evaluates the pest in the population, this method is for playing the simulation of 
    # the best individual unblinded at the end of evolution. 
    def Evaluate_Best(self, envs, pb = False, pp = True, retain_data = True):
        for e in range(c.numEnvs):
            if (e > 0):
                pp = False
            self.pop[0].Start_Evaluation(envs.envs[e], pb, pp)
            self.pop[0].Complete_Fitness(retain_data)
  
    # Allows you to select the individuals you want to view in simulation based on the 
    # indices provided. Used in the playback.py program to play saved robots. 
    def Evaluate_Select(self,pb, indices):
        for i in indices:
            self.pop[i].Evaluate(pb)

    def Fill_From(self, other):
        fill_start = time.clock()
        self.pop[0] = self.Copy_Best_From(other)
        self.Collect_Children_From(other)
        for x in self.pop:
            self.pop[x].fitness = 0
        entire_fill = time.clock() - fill_start
        return entire_fill
            # print("Fill From fitness:",self.pop[x].fitness)
    
    def Initialize(self, genome = None, cppn = None):
        for i in range(self.popSize):
            self.pop[i] = INDIVIDUAL(i, genome, cppn)

    def Mutate(self):
        for i in self.pop:
            self.pop[i].Mutate()
            # self.pop[i].cppn.mutate()

    def Print(self):
        for i in self.pop:
            if(i in self.pop):
                self.pop[i].Print()
        print()

    def replace(self):
        temp_class = []
        for person in self.pop:
            print(self.pop[person].ID, self.pop[person].fitness)
            temp_class.append(self.pop[person])
        # Takes the worst performing 10% by their fitness values 
        bad_hombres = sorted(temp_class, reverse = True)[-int(self.popSize * .1):]
        # Replaces them with new random individuals 
        for hombre in bad_hombres:
            hombre = int(hombre.ID)
            self.pop[hombre] = INDIVIDUAL(hombre)
            self.pop[hombre].age = 0

    def ReplaceWith(self, other):
        for i in self.pop:
            if self.pop[i].fitness < other.pop[i].fitness:
                self.pop[i] = other.pop[i]

    def retrieve_best_index(self, other):
        maxIndex = 0
        for i in range(len(other.pop)):
            if other.pop[i].fitness > other.pop[maxIndex].fitness:
                maxIndex = i
        return maxIndex

    def Winner_Of_Tournament_Selection(other):
        p1 = random.randint(0,other.popSize - 1)
        p2 = random.randint(0,other.popSize - 1)
        while(p1 == p2):
            p2 = random.randint(0,other.popSize - 1)
        if other.pop[p1].fitness > other.pop[p2].fitness:
            return other.pop[p1]
        else:
            return other.pop[p2]

      

