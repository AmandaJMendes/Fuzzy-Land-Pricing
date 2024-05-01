import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

area          = ctrl.Antecedent(np.arange(100, 2000, 1), 'area') 
dist_to_av    = ctrl.Antecedent(np.arange(0, 5000, 1),   'dist_to_av')
dist_to_beach = ctrl.Antecedent(np.arange(0, 5000, 1),   'dist_to_beach')
price         = ctrl.Consequent(np.arange(20, 2000, 1),  'price') 

area['small']      = fuzz.trimf(area.universe, [100, 100, 200])
area['average']    = fuzz.trimf(area.universe, [100, 300, 500])
area['large']      = fuzz.trimf(area.universe, [400, 700, 1200])
area['very large'] = fuzz.trimf(area.universe, [1100, 2000, 2000])
# area.view()

dist_to_av['close']   = fuzz.trimf(dist_to_av.universe, [0, 0, 600])
dist_to_av['average'] = fuzz.trimf(dist_to_av.universe, [200, 1000, 1500])
dist_to_av['far']     = fuzz.trimf(dist_to_av.universe, [1400, 5000, 5000])
#dist_to_av.view()

dist_to_beach['close']   = fuzz.trimf(dist_to_beach.universe, [0, 0, 600])
dist_to_beach['average'] = fuzz.trimf(dist_to_beach.universe, [200, 1000, 1500])
dist_to_beach['far']     = fuzz.trimf(dist_to_beach.universe, [1400, 5000, 5000])
#dist_to_beach.view()

price['low']       = fuzz.trimf(price.universe, [20 , 20 , 150])
price['average']   = fuzz.trimf(price.universe, [100, 300, 400])
price['high']      = fuzz.trimf(price.universe, [300, 600, 1000])
price['very high'] = fuzz.trimf(price.universe, [800, 2000, 2000])
#price.view()

rules = []

rules.append(ctrl.Rule(area['small'], price['low']))
rules.append(ctrl.Rule(area['average'] & dist_to_av['far'], price['low']))
rules.append(ctrl.Rule(area['average'] & (dist_to_av['average'] | dist_to_beach['far']), price['low']))
rules.append(ctrl.Rule(dist_to_av['average'] & dist_to_beach['far'], price['low']))

rules.append(ctrl.Rule(area['large'], price['average'])) 
rules.append(ctrl.Rule(area['average'] & (dist_to_av['close'] | dist_to_beach['close']), price['average']))
rules.append(ctrl.Rule(area['average'] & dist_to_av['average'] & dist_to_beach['far'], price['average']))

rules.append(ctrl.Rule(area['average']    & (dist_to_av['close'] & dist_to_beach['close']), price['high'])) 
rules.append(ctrl.Rule(area['large']      & (dist_to_av['close'] | dist_to_beach['average']), price['high']))
rules.append(ctrl.Rule(area['very large'] & dist_to_av['far'], price['high']))

rules.append(ctrl.Rule(area['very large'], price['very high']))


pricing_ctrl = ctrl.ControlSystem(rules)
pricing = ctrl.ControlSystemSimulation(pricing_ctrl)

# Examples from https://www.procuraseimovel.com.br/portal/imoveis/rs/rio-grande/praia/cassino/venda?tipo=terreno
# Attributes: [area, dist_to_av, dist_to_beach, real price]

condos = [[270, 2800, 4400, 135000],
          [262, 1600, 600 , 212000]]

lands = [[220 , 2000, 1400, 95000],
         [300 , 1500, 2500, 120000],
         [360 , 700 , 2400, 130000],
         [375 , 1300, 2600, 138000],
         [360 , 700 , 2300, 140000],
         [180 , 500 , 1100, 140000],
         [300 , 1100, 450 , 170000],
         [220 , 2000, 1500, 75000],
         [225 , 2100, 1900, 55000],
         [250 , 3600, 1200, 85000],
         [250 , 1000, 500 , 180000],
         [300 , 1600, 600 , 180000],
         [360 , 1600, 1200, 190000],
         [300 , 1300, 2500, 200000],
         [400 , 1600, 500 , 215000],
         [360 , 1100, 2700, 220000],
         [600 , 1400, 200 , 250000],
         [250 , 200 , 1300, 265000],
         [300 , 800 , 1900, 300000],
         [250 , 200 , 1300, 318000],
         [250 , 100 , 1300, 320000],
         [375 , 400 , 1200, 350000],
         [750 , 1800, 800 , 550000],
         [493 , 1000, 500 , 600000],
         [1200, 1800, 100 , 850000],
         [750 , 300 , 850 , 1050000]] 

errors = []
for land in lands:
    pricing.input['area']          = land[0]
    pricing.input['dist_to_av']    = land[1]
    pricing.input['dist_to_beach'] = land[2]
    try:
        pricing.compute()
        error = ((pricing.output['price']*1000-land[3])/land[3])*100
        errors.append(abs(error))
        print("Predicted: ", round(pricing.output['price'])*1000, end = "  |  ")
        print("Real price: ", land[3], end = "  |  ")
        print(f"Error: {round(error,2)}%")
    except:
        print("Prediction failed for ", land)

print(f"\nAverage error: {round(sum(errors)/len(errors), 2)}%")
print(f"Maximum error: {round(max(errors), 2)}%")
print(f"Minimum error: {round(min(errors), 2)}%")
# price.view(sim=pricing)
# plt.show()
