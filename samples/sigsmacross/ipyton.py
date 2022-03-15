import matplotlib.pyplot as plt

x = [1,2,3]
y = [1,7,5]

plt.ion()               # interactive mode on
fig,ax = plt.subplots()
line, = ax.plot(x,y)
fig.show()