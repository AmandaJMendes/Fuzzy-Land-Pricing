import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


area          = ctrl.Antecedent(np.arange(100, 2000, 1), 'area') 
dist_to_av    = ctrl.Antecedent(np.arange(0, 5000, 1), 'dist_to_av')
dist_to_beach = ctrl.Antecedent(np.arange(0, 5000, 1), 'dist_to_beach')
price         = ctrl.Consequent(np.arange(20, 4000, 1), 'price') 

area['very small'] = fuzz.trimf(area.universe, [100, 100, 200])
area['small']      = fuzz.trimf(area.universe, [100, 200, 300])
area['average']    = fuzz.trimf(area.universe, [200, 300, 400])
area['large']      = fuzz.trimf(area.universe, [300, 600, 900])
area['very large'] = fuzz.trimf(area.universe, [700, 2000, 2000])
#area.view()

dist_to_av['close']   = fuzz.trimf(dist_to_av.universe, [0, 0, 600])
dist_to_av['average'] = fuzz.trimf(dist_to_av.universe, [200, 1000, 1800])
dist_to_av['far']     = fuzz.trimf(dist_to_av.universe, [800, 5000, 5000])
#dist_to_av.view()

dist_to_beach['close']   = fuzz.trimf(dist_to_beach.universe, [0, 0, 600])
dist_to_beach['average'] = fuzz.trimf(dist_to_beach.universe, [200, 1000, 1800])
dist_to_beach['far']     = fuzz.trimf(dist_to_beach.universe, [800, 5000, 5000])
#dist_to_beach.view()

price['very low']  = fuzz.trimf(price.universe, [20 , 20    , 80])
price['low']       = fuzz.trimf(price.universe, [50 , 100 , 150])
price['average']   = fuzz.trimf(price.universe, [100, 200, 300])
price['high']      = fuzz.trimf(price.universe, [200, 600, 1000])
price['very high'] = fuzz.trimf(price.universe, [800, 4000, 4000])
#price.view()

rules = []
rules.append(ctrl.Rule(area['very small'] & (dist_to_av['far'] | dist_to_beach['far']),         price['very low']))
rules.append(ctrl.Rule(area['very small'] & (dist_to_av['average'] & dist_to_beach['average']), price['very low']))
rules.append(ctrl.Rule(area['small'] & dist_to_av['far'] & dist_to_beach['far'],                price['very low']))
rules.append(ctrl.Rule(area['average'] & dist_to_av['far'] & dist_to_beach['far'],              price['very low']))

rules.append(ctrl.Rule(area['very small'] & dist_to_av['close'] & dist_to_beach['close'], price['low']))
rules.append(ctrl.Rule(area['small'] & (dist_to_av['far'] | dist_to_beach['far']),        price['low']))
rules.append(ctrl.Rule(area['average'] & dist_to_av['far'] & dist_to_beach['far'],        price['low']))

rules.append(ctrl.Rule(area['very small'] & dist_to_av['close'] & dist_to_beach['close'],  price['average']))
rules.append(ctrl.Rule(area['small'] & (dist_to_av['close'] | dist_to_beach['close']),     price['average']))
rules.append(ctrl.Rule(area['average'] & dist_to_av['average'] & dist_to_beach['average'], price['average']))
rules.append(ctrl.Rule(area['average'] & (dist_to_av['close'] | dist_to_beach['average']), price['average']))
rules.append(ctrl.Rule(area['average'] & (dist_to_av['average'] | dist_to_beach['close']), price['average']))
rules.append(ctrl.Rule(area['large'] & (dist_to_av['close'] | dist_to_beach['far']),    price['average']))
rules.append(ctrl.Rule(area['large'] & (dist_to_av['far'] | dist_to_beach['close']),    price['average']))
rules.append(ctrl.Rule(area['large'] & (dist_to_av['far'] | dist_to_beach['far']), price['average']))

rules.append(ctrl.Rule(area['average'] & dist_to_av['average'] & dist_to_beach['average'], price['high']))
rules.append(ctrl.Rule(area['average'] & dist_to_av['average'] & dist_to_beach['close'],   price['high']))
rules.append(ctrl.Rule(area['average'] & dist_to_av['close'] & dist_to_beach['average'],   price['high']))
rules.append(ctrl.Rule(area['large'] & (dist_to_av['close'] & dist_to_beach['close']),    price['high']))
rules.append(ctrl.Rule(area['large'] & (dist_to_av['close'] & dist_to_beach['far']),    price['high']))
rules.append(ctrl.Rule(area['large'] & (dist_to_av['far'] & dist_to_beach['close']),    price['high']))
rules.append(ctrl.Rule(area['very large'] & (dist_to_av['close'] | dist_to_beach['close']), price['high']))

rules.append(ctrl.Rule(area['very large'] & dist_to_av['close'] & dist_to_beach['average'], price['very high']))
rules.append(ctrl.Rule(area['very large'] & dist_to_av['average'] & dist_to_beach['close'], price['very high']))
rules.append(ctrl.Rule(area['very large'] & dist_to_av['close'] & dist_to_beach['close'], price['very high']))

pricing_ctrl = ctrl.ControlSystem(rules)
pricing = ctrl.ControlSystemSimulation(pricing_ctrl)

pricing.input['area']          = 600
pricing.input['dist_to_av']    = 500
pricing.input['dist_to_beach'] = 100

pricing.compute()

print(pricing.output['price'])
price.view(sim=pricing)
plt.show()
