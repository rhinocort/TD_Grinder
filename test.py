import numpy as np

rozsah = [-2.0,2.0]

data = [-3,0,5,1,0,1,2]
data_x = range(len(data))

#data_v_rozsahu = np.where(data < rozsah[1])


data_v_rozsahu = [ j for (i,j) in zip(data_x,data) if data >= 4 ]

print(data_v_rozsahu)