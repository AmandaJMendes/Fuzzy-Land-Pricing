import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


area          = ctrl.Antecedent(np.arange(2, 60, 1),  'area') #*100
dist_to_av    = ctrl.Antecedent(np.arange(0, 13, 1),  'dist_to_av')
dist_to_beach = ctrl.Antecedent(np.arange(0, 5, 1),   'dist_to_beach')
price         = ctrl.Consequent(np.arange(2, 400, 1), 'price') #*10.000

# area['very small'] = fuzz.trimf(tip.universe, [0, 0, 13])
# area['small']      = fuzz.trimf(tip.universe, [0, 0, 13])
# area['average']     = fuzz.trimf(tip.universe, [0, 13, 25])
# area['large']      = fuzz.trimf(tip.universe, [13, 25, 25])
# area['very large'] = fuzz.trimf(tip.universe, [13, 25, 25])
area.automf(5, names = ['very small', 'small', 'average', 'large', 'very large'])
area.view()
# dist_to_av['close']    = fuzz.trimf(tip.universe, [0, 0, 13])
# dist_to_av['average'] = fuzz.trimf(tip.universe, [0, 13, 25])
# dist_to_av['far']   = fuzz.trimf(tip.universe, [13, 25, 25])
dist_to_av.automf(3, names = ['close', 'average', 'far'])
dist_to_av.view()
# dist_to_beach['close']    = fuzz.trimf(tip.universe, [0, 0, 13])
# dist_to_beach['average'] = fuzz.trimf(tip.universe, [0, 13, 25])
# dist_to_beach['far']   = fuzz.trimf(tip.universe, [13, 25, 25])
dist_to_beach.automf(3, names = ['close', 'average', 'far'])
dist_to_beach.view()
# price['very low']    = fuzz.trimf(tip.universe, [0, 0, 13])
# price['low']    = fuzz.trimf(tip.universe, [0, 0, 13])
# price['average'] = fuzz.trimf(tip.universe, [0, 13, 25])
# price['high']   = fuzz.trimf(tip.universe, [13, 25, 25])
# price['very high']    = fuzz.trimf(tip.universe, [0, 0, 13])
price.automf(5, names = ['very low', 'low', 'average', 'high', 'very high'])
price.view()

rule1 = ctrl.Rule(area['very small'] | dist_to_av['far']   | dist_to_beach['far']  , price['very low'])
rule2 = ctrl.Rule(area['very large'] | dist_to_av['close'] | dist_to_beach['close'], price['very high'])

pricing_ctrl = ctrl.ControlSystem([rule1, rule2])
pricing = ctrl.ControlSystemSimulation(pricing_ctrl)

pricing.input['area']          = 6000.0
pricing.input['dist_to_av']    = 0.0
pricing.input['dist_to_beach'] = 0.0

pricing.compute()

print(pricing.output['price'])
price.view(sim=pricing)
plt.show()
