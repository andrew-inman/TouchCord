import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# Create figure for plotting
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
# bars = ax.plot([],[], width = 0.4)
indices = np.array([1,2,3,4,5,6,7,8,9])
fig = plt.figure(figsize = (10, 5))
TF_array = [0]*indices
bars = plt.bar(indices, [TF_array], color =['black','red'], width = 0.4)
plt.xlabel("Beads")
plt.ylabel("Current State")
plt.title('Touched Beads in the I/O Beads')

#     (df.pivot(index='cake',columns='has_chocolate',values='sales')
#    .plot.bar(stacked=True)
#)
def animate(TF_array, new_data): # first arg is frames, the rest are fargs =(..)
    global bars
    TF_array.append(new_data)
    bars.set_data()
    bars = plt.bar(indices, [TF_array], color =['black','red'], width = 0.4)
    #bars.__setattr__()
    return bars # if blit false then return val is unused 
# interval is amount of time to wait btwn calls to animate()
ani = animation.FuncAnimation(fig, # also init_func --> used to draw a clear frame (called once before first frame)
    animate,
    fargs=(new_data,), #additional args (has to be a tuple)
    frames = TF_array, #frames arg is the data to pass func
    interval=100,
    repeat=False, 
    blit=True) # think we want blit = false (default) bc 
plt.show(block=False) # this is similar to plt.ion() i read