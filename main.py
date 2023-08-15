from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation 
import time
import pandas as pd


# initializing a figure in 
# which the graph will be plotted
fig = plt.figure() 
x = []
y = []
   
# marking the x-axis and y-axis
axis = plt.axes(xlim =(0, 10), 
                ylim =(0, 100)) 
  
# initializing a line variable
line, = axis.plot([], [], "r*",lw = 3) 
   
# data which the line will 
# contain (x, y)
def init(): 
    line.set_data([], [])
    return line,
t0= time.time()

with open('k.csv','w') as f:
    f.write('x,y\n')   

x = []
y = []

def animate(i):
    # data = pd.read_csv('data.csv')
    # with open('k.csv','a') as f:
    #     f.write(f'{i/3},{i**2/9}\n')
        
    # x = data['x'].to_numpy()
    # y = data['y'].to_numpy()
    # x.append(i/10)
    # y.append(i**2)
    x.append(i)
    y.append(i**2)
    line.set_data(x, y)
    return line,
   
anim = FuncAnimation(fig, animate, init_func = init,
                     frames = 100, interval = 500, repeat=False)
  
   
# # anim.save('continuousSineWave.gif', 
# #           writer = 'ffmpeg', fps = 30)
plt.show()