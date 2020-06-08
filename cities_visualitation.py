from matplotlib import pyplot as plt
import numpy as np
import params
from IPython.display import clear_output


def get_normalized_cities_identification(state):
    state_after_addition = [x+1 for x in state]
    return tuple(state_after_addition)


class CitiesMap:
    def __init__(self, all_cities):
        self.edges = []
        self.all_cities = all_cities
        coords = all_cities.values()
        x_coords = [x[0] for x in coords]
        y_coords = [x[1] for x in coords]
        self.x_coords = np.array(x_coords)
        self.y_coords = np.array(y_coords)
        self.fig = plt.figure()
        self.graph = self.fig.add_subplot()

    def show_map(self, state):
        plt.close(self.fig)
        self.fig = plt.figure()
        self.graph = self.fig.add_subplot()
        self.graph.scatter(self.x_coords, self.y_coords)
        self.show_cities_id()
        if state is not None:
            self.update_edges(state=state)
            self.fig.canvas.draw()
        self.fig.show()

    def update_edges(self, state):
        circle = state.copy()
        x_circle_coords = [self.x_coords[city] for city in circle]
        y_circle_coords = [self.y_coords[city] for city in circle]
        if params.show_distances:
            self.show_distances(x_circle_coords, y_circle_coords)
        ordered_x_coords = np.array(x_circle_coords)
        ordered_y_coords = np.array(y_circle_coords)
        self.graph.plot(ordered_x_coords, ordered_y_coords, 'r')

    def show_distances(self, x_circle_coords, y_circle_coords):
        circle_len = len(x_circle_coords)
        if params.show_distances:
            for ind in range(0, circle_len+1):
                p1 = (x_circle_coords[ind % circle_len], y_circle_coords[ind % circle_len])
                p2 = (x_circle_coords[(ind + 1) % circle_len], y_circle_coords[(ind + 1) % circle_len])
                self.graph.annotate(my_utils.distance(p1, p2), ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2))

    def show_cities_id(self):
        for city_id, (x, y) in self.all_cities.items():
            if params.show_coords:
                self.graph.annotate(s=str(city_id + 1) + " " + str((x, y)), xy=(x - 0.5, y + 1))
            else:
                self.graph.annotate(s=city_id + 1, xy=(x - 0.5, y + 1))

    def save_plot(self, file_name):
        self.fig.savefig('./final_result/' + file_name + '.png')


if __name__ == '__main__':
    import my_utils, tsp_problem

    all_cities = my_utils.generate_cities_dict('big')
    citiesMap = CitiesMap(all_cities)
    final_state = [0, 10, 3, 5, 7, 9, 13, 11, 2, 6, 4, 8, 14, 1, 12]
    print(get_normalized_cities_identification(final_state))
    citiesMap.show_map(final_state)
