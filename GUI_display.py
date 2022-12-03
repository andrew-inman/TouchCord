import PySimpleGUI as sg
import random
import gestureFunctions
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation


# indices = np.array([1,2,3,4,5,6,7,8,9])
# fig = plt.figure(figsize = (10, 5))
# TF_array = [0]*indices
# plt.bar(indices, TF_array, color =['black','red'], width = 0.4)
# plt.xlabel("Beads")
# plt.ylabel("Current State")
# plt.title('Touched Beads in the I/O Beads')

# #     (df.pivot(index='cake',columns='has_chocolate',values='sales')
# #    .plot.bar(stacked=True)
# #)

# def animate(TF_array):
#     TF_array.append(TF_array)

# ani = animation.FuncAnimation(fig,
#     animate,
#     fargs=(TF_array),
#     interval=50,
#     blit=True)
# plt.show(block=False)


def make_graph(data, baseline, beadCount = 5):
    BAR_WIDTH = 50      # width of each bar
    BAR_SPACING = 75    # space between each bar
    EDGE_OFFSET = 3     # offset from the left edge for first bar
    GRAPH_SIZE= DATA_SIZE = (500,500)       # size in pixels

    sg.theme('Light brown')

    layout = [[sg.Text('Touched Beads in the I/O Beads',font='Calibri 20')],
            [sg.Graph(GRAPH_SIZE, (0,0), DATA_SIZE, k='-GRAPH-')]]

    window = sg.Window('Bar Graph', layout, finalize=True)

    graph = window['-GRAPH-']       # type: sg.Graph

    while True:
        TF_array = gestureFunctions.pinchDetect(data, baseline, beadCount)
        graph.erase()
        for i in range(5):
            if TF_array[i]:
                graph_value = 250
            else:
                graph_value = 10
            graph.draw_rectangle(top_left=(i * BAR_SPACING + EDGE_OFFSET, graph_value),
                                bottom_right=(i * BAR_SPACING + EDGE_OFFSET + BAR_WIDTH, 0),
                                fill_color='light blue')
                                # fill_color=sg.theme_button_color()[1])

            graph.draw_text(text=graph_value, location=(i*BAR_SPACING+EDGE_OFFSET+25, graph_value+10), font='Calibri 14')

        # Normally at the top of the loop, but because we're drawing the graph first, making it at the bottom
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break


    window.close()
