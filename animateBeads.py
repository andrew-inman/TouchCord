import tkinter
import time

width = 1000
height = 400
beadPosition = [
    (100, 100),
    (200, 100),
    (300, 100),
    (400, 100),
    (500, 100),
    (600, 100),
    (700, 100),
    (800, 100),
    (900, 100)
]
maxRadius = 50

def createWindow():
    Window = tkinter.Tk()
    Window.title("I/O Beads")
    Window.geometry(f"{width}x{height}")
    return Window

def createCanvas(Window):
    canvas = tkinter.Canvas(Window)
    canvas.configure(bg = "#464646")
    canvas.pack(fill = "both", expand = True)
    return canvas

def drawBeads(Window, canvas, gestureDict):
    # Documentation for canvas shapes: https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html
    canvas.delete("all")
    untouchedRadius = 30
    touchRadius = 40
    beadCanvasObjects = []
    for i in range(len(beadPosition)):
        if gestureDict["touchState"][i]:
            radius = touchRadius
            color = "#8100D1"
        else:
            radius = untouchedRadius
            color = "Red"
        beadXPos = beadPosition[i][0]
        beadYPos = beadPosition[i][1]
        bead = canvas.create_oval(
            beadXPos - radius,
            beadYPos - radius,
            beadXPos + radius,
            beadYPos + radius,
            fill = color,
            outline = "Black",
            width = 4
        )
        beadCanvasObjects.append(bead)

    if gestureDict["slide"] != 0:
        if gestureDict["slide"] > 0:
            arrow = canvas.create_line(
                415, # X start
                300, # Y start
                585, # X end
                300, # Y end
                width = 20,
                arrow = tkinter.LAST,
                arrowshape = (30, 38, 20),
                fill = "#0072E2"
            )
        else:
            arrow = canvas.create_line(
                585, # X start
                300, # Y start
                415, # X end
                300, # Y end
                width = 20,
                arrow = tkinter.LAST,
                arrowshape = (30, 38, 20),
                fill = "#0072E2"
            )

    if gestureDict["twist"]:
        twistIcon_X = 325
        twistIcon_Y = 275
        twistIconRadius = 30
        arrowHeadLen = 15
        offset = 5
        arrow = canvas.create_line(
            twistIcon_X + offset, # X start
            twistIcon_Y, # Y start
            twistIcon_X, # X end
            twistIcon_Y, # Y end
            width = 15,
            arrow = tkinter.LAST,
            arrowshape = (15, 15, 10),
            fill = "#0072E2"
        )
        arrow2 = canvas.create_line(
            twistIcon_X + arrowHeadLen + offset, # X start
            twistIcon_Y + twistIconRadius * 2, # Y start
            twistIcon_X + + arrowHeadLen + offset * 2, # X end
            twistIcon_Y + twistIconRadius * 2, # Y end
            width = 15,
            arrow = tkinter.LAST,
            arrowshape = (arrowHeadLen, 15, 10),
            fill = "#0072E2"
        )

        arc1 = canvas.create_arc(
            twistIcon_X + twistIconRadius + arrowHeadLen, # X start
            twistIcon_Y + twistIconRadius * 2, # Y start
            twistIcon_X - twistIconRadius + arrowHeadLen, # X end
            twistIcon_Y, # Y end
            extent = 90,
            width = 10,
            style = "arc",
            outline = "#0072E2"
        )

        arc2 = canvas.create_arc(
            twistIcon_X + twistIconRadius + arrowHeadLen, # X start
            twistIcon_Y + twistIconRadius * 2, # Y start
            twistIcon_X - twistIconRadius + arrowHeadLen, # X end
            twistIcon_Y, # Y end
            extent = 90,
            start = 180,
            width = 10,
            style = "arc",
            outline = "#0072E2"
        )

    if gestureDict["grab"]:
        rect = canvas.create_rectangle(
            620,
            275,
            700,
            325,
            fill = "#0072E2",
            outline = "#0072E2"
        )

    Window.update()


# Sample Usage Code:
# window = createWindow()
# canvas = createCanvas(window)

# gestureState1 = {
#     "touchState": [True, False, True, False, False, False, True, True, False],
#     "slide": 1,
#     "twist": True,
#     "grab": True
# }

# gestureState2 = {
#     "touchState": [False, False, False, False, False, False, False, False, False],
#     "slide": 0,
#     "twist": False,
#     "grab": False
# }

# gestureState3 = {
#     "touchState": [False, False, False, True, False, False, False, False, True],
#     "slide": -1,
#     "twist": False,
#     "grab": False
# }

# while True:
#     drawBeads(window, canvas, gestureState1)
#     time.sleep(0.01)
   
#     drawBeads(window, canvas, gestureState2)
#     time.sleep(0.01)

#     drawBeads(window, canvas, gestureState3)
#     time.sleep(0.01)

#     drawBeads(window, canvas, gestureState1)
#     time.sleep(0.01)