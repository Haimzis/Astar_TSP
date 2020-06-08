from pytictoc import TicToc
from ChristofidesAlgorithm.christofides import cal_christofides_heurisric
from search import Problem
import math
import graph


def distance(coords1, coords2):
    return math.sqrt((coords1[0] - coords2[0])**2 + (coords1[1] - coords2[1])**2)


def init_distance_matrix(cities_dict):
    return {row_ind: {col_ind: distance(row_coords, col_coords) for col_ind, col_coords in cities_dict.items()}
            for row_ind, row_coords in cities_dict.items()}


class TravelingSalesmanProblem(Problem):
    """ The problem of finding the shortest
        way to perform Hemilton Circle between the cities"""

    def __init__(self, all_cities, initial, goal=None): # initial = (0), goal = some state that its first and last values are 0
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)
        self.cities_matrix = init_distance_matrix(all_cities)
        self.cities_identifiers = set(all_cities.keys())
        self.cities_amount = len(self.cities_identifiers)
        self.cristofides_heurisrics_hash = {}
        self.t = TicToc()
        self.t.tic()

    def value(self, state):
        overall_distance = 0.0
        state_max_ind = len(state) - 1
        for ind, city in enumerate(state):
            if ind != state_max_ind:
                overall_distance += self.cities_matrix[state[ind]][state[ind + 1]]
        return overall_distance

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list"""
        if len(state) == self.cities_amount:
            return [0]
        return self.get_unvisited_cities(state)

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        new_state = list(state)
        new_state.append(action)
        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise"""
        return len(state) == (self.cities_amount + 1) and state[0] == state[self.cities_amount]

    def get_unvisited_cities(self, state):
        return self.cities_identifiers.difference(state)

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """
        visited_set = set(node.state)
        hashed_visited_set = hash(str(visited_set))
        unvisited_cities = self.get_unvisited_cities(node.state)
        # Christofides Heuristic Evaluation
        if hashed_visited_set in self.cristofides_heurisrics_hash.keys():
            return self.cristofides_heurisrics_hash[hashed_visited_set]
        else:
            christofides_h = 0.0
            if len(unvisited_cities) <= 1:
                christofides_h = self.value(tuple(unvisited_cities))
            else:
                christofides_h = cal_christofides_heurisric(self.build_graph(unvisited_cities))[0]
            self.cristofides_heurisrics_hash[hashed_visited_set] = (2/3)*christofides_h  # <= optimal_tsp
            return (2/3)*christofides_h

    def build_graph(self, unvisited_cities):
        cities_dict= {}
        for city_a in unvisited_cities:
            cities_dict[city_a] = {}
            for city_b in unvisited_cities:
                if city_a != city_b:
                    cities_dict[city_a][city_b] = self.cities_matrix[city_a][city_b]
        return cities_dict

    def hashed_build_graph(self, unvisited_nodes):
        if int(self.t.tocvalue()) >= 600:
            self.t.toc('mst hash has been reset', True)
            self.reset_mst_eval_hash()
        if not unvisited_nodes:
            return 0.0
        return self.build_graph(unvisited_nodes)

    def path_cost(self, c, state1, action, state2):
        return c + self.cities_matrix[state1[-1]][state2[-1]]

    def reset_mst_eval_hash(self):
        self.cristofides_heurisrics_hash = {}

