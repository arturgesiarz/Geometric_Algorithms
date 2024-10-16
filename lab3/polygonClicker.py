import matplotlib.pyplot as plt
import matplotlib
import pickle
matplotlib.use('macosx')

from matplotlib.patches import Polygon
from copy import deepcopy


class PolygonDrawer:
    def __init__(self,OXRange=(0,10),OYRange=(0,10)):

        self.fig, self.ax = plt.subplots()
        self.ax.set_title('Polygons select')

        self.ax.set_xlim(OXRange[0], OXRange[1])
        self.ax.set_ylim(OYRange[0], OYRange[1])

        self.points = []
        self.current_polygon = []
        self.draw_enabled = True  # Flag to enable/disable drawing

        self.cid_press = self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def on_click(self, event):
        if event.button == 1 and self.draw_enabled:
            self.points.append((event.xdata, event.ydata))
            self.current_polygon.append((event.xdata, event.ydata))
            self.ax.plot(event.xdata, event.ydata, 'co')
            self.fig.canvas.draw()

        elif event.button == 3:
            if self.draw_enabled:
                self.draw_enabled = False
                polygon = Polygon(self.current_polygon, closed=True, fill=None, edgecolor='g')
                self.ax.add_patch(polygon)
                plt.draw()
            else: plt.close()

def render(polygons, no_of_polygons_to_render):

    for i in range(no_of_polygons_to_render):
        objectCreated = PolygonDrawer()
        plt.grid()
        plt.show(block=True)
        plt.close('all')
        polygons.append(deepcopy(objectCreated.points))

def start(polygons):
    no_of_polygons_to_render = int(input("Please, write a number of polygons to render ->  "))
    render(polygons,no_of_polygons_to_render)

    with open('polygons.pkl', 'wb') as file:
        pickle.dump(polygons, file)

    return polygons

if __name__ == '__main__':
    polygons = start([])
    print(polygons)

    poly = [[(1.9556451612903225, 1.9805194805194808), (8.024193548387096, 1.9264069264069263), (7.993951612903226, 8.000541125541126), (6.512096774193548, 4.889069264069264), (5.191532258064516, 3.2521645021645025), (3.1048387096774195, 2.3051948051948052)]]




