from individual import INDIVIDUAL
import pickle
from environments import ENVIORNMENTS
from population import POPULATION
from recorder import Recorder

envs = ENVIORNMENTS()
f = open('saved_files/weirdSpin2019-04-15.p', 'rb')
best = pickle.load(f)
f.close()
best_pop = POPULATION(1)
best_pop.Initialize()
best_pop.pop[0] = best
best_pop.Evaluate_Best(envs, pb = False, pp = True, retain_data = True)

recorder = Recorder(best_pop.pop[0])
recorder.plot_touch_values(best_pop.pop[0])