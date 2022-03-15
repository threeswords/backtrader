# %% 
# first cell ------------------------------

import matplotlib.pyplot as plt

x = [1,2,3]
y = [1,7,5]

plt.ion()               # interactive mode on
fig,ax = plt.subplots()
line, = ax.plot(x,y)
fig.show()

# %% 
# second cell ------------------------------

x.append(4)
y.append(10)

line.set_data(x,y)   # set new data

ax.relim()           # recompute the data limits
ax.autoscale_view()  # automatic axis scaling

# %% 
# third cell: just a radom example to plot sequentially ---------------------

from random import randint

for i in range(5):
    x.append(x[-1]+1)
    y.append(randint(0,10))

    line.set_data(x,y)   # set new data

    ax.relim()           # recompute the data limits
    ax.autoscale_view()  # automatic axis scaling

    plt.pause(0.5)
# %%
