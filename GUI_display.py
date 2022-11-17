import PySimpleGUI as sg
import random
import gestureFunctions


def make_graph():
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
        TF_array = gestureFunctions.pinch()
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
