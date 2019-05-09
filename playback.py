from individual import INDIVIDUAL
import pickle
from environments import ENVIORNMENTS
from platforms import PLATFORMS
from population import POPULATION
from recorder import Recorder
import os
import constants as c
from archive import Archive

envs = PLATFORMS()
# f = open('saved_files/bestJumpEver2019-04-27.p', 'rb')
# f = open('saved_files/4hidden_500gen_apfo_thruwall2019-05-02.p', 'rb')
# f = open('saved_files/2019-05-02.p', 'rb')
# f = open('saved_files/samplesave2019-05-01.p', 'rb')
# f = open('saved_files/4hidden_6legs_apfo_500gen_ind.p', 'rb')
f = open('saved_files/1env_500gens_genetic_6legs_4hidden_trial32019-05-05.p', 'rb')
best_genome = pickle.load(f)
f.close()
best_pop = POPULATION(1)

if isinstance(best_genome, Archive):
    best_pop.Initialize(best_genome.genome, best_genome.cppn)
elif isinstance(best_genome, list):
    best_pop.Initialize(best_genome)
else:
    print("Could not determine class")
    exit()
    
# best_pop.Initialize(best_genome)
best_pop.Evaluate_Best(envs, pb = False, pp = True, retain_data = True)

recorder = Recorder()
recorder.plot_touch_values(best_pop.pop[0])

newSave = input("New Save? (y/n)")
if (newSave == 'y'):
    label = input("New Label: ") + '.p'
    manSav = open(os.path.join(c.save_file_folder,label), "wb")
    saved_ind = Archive(best_pop.pop[0].genome, best_pop.pop[0].cppn.save())
    pickle.dump(saved_ind, manSav)