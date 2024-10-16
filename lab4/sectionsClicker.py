import matplotlib.pyplot as plt
import matplotlib
import pickle
matplotlib.use('macosx')
from matplotlib.lines import Line2D
from copy import deepcopy
class LineDrawer:
    def __init__(self, OXRange=(0, 10), OYRange=(0, 10)):

        self.fig, self.ax = plt.subplots()
        self.ax.set_title('Lines select')

        self.ax.set_xlim(OXRange[0], OXRange[1])
        self.ax.set_ylim(OYRange[0], OYRange[1])

        self.lines = []
        self.current_line = []
        self.draw_enabled = True  # Flag to enable/disable drawing

        self.cid_press = self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def on_click(self, event):
        if event.button == 1 and self.draw_enabled:
            self.current_line.append((event.xdata, event.ydata))

            # Dodanie punktu od razu po kliknięciu lewym przyciskiem myszy
            self.ax.plot(event.xdata, event.ydata, 'ro')


            if len(self.current_line) == 2:
                line = Line2D([self.current_line[0][0], self.current_line[1][0]],
                              [self.current_line[0][1], self.current_line[1][1]], color='g')
                self.ax.add_line(line)

                # Dodanie punktów na końcach odcinka
                self.ax.plot(self.current_line[0][0], self.current_line[0][1], 'ro')  # Punkt początkowy
                self.ax.plot(self.current_line[1][0], self.current_line[1][1], 'ro')  # Punkt końcowy

                self.lines.append(deepcopy(self.current_line))
                self.current_line = []
                self.fig.canvas.draw()

        elif event.button == 3:
            if self.draw_enabled:
                self.draw_enabled = False
            else:
                plt.close()

def render():
    object_created = LineDrawer()
    plt.grid()
    plt.show(block=True)
    plt.close('all')
    lines = object_created.lines
    return lines
def start():
    lines = render()
    with open('lines.pkl', 'wb') as file:
        pickle.dump(lines, file)
    return lines

if __name__ == '__main__':
    lines = start()