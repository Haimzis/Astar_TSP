from pytictoc import TicToc
from my_utils import init_distance_matrix
from search import Problem
import graph


class TravelingSalesmanProblem(Problem):
    """ The problem of finding the shortest
        way to perform Hemilton Circle between the cities"""

    def __init__(self, all_cities, initial, goal=None): # initial = (0), goal = some state that its first and last values are 0
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)
        self.cities_matrix = init_distance_matrix(all_cities)
        self.cities_identifiers = set(all_cities.keys())
        self.cities_amount = len(self.cities_identifiers)
        self.trees_evaluation_hash = {}
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
        h = 0.0
        visited_set = set(node.state)
        hashed_visited_set = hash(str(visited_set))
        unvisited_cities = self.get_unvisited_cities(node.state)
        # min edge from visited to unvisited
        #h += self.evaluate_visited_mst_connection_edge(node.state, node.state[-1], unvisited_cities)

        # MST evaluation
        if hashed_visited_set in self.trees_evaluation_hash.keys():
            h += self.trees_evaluation_hash[hashed_visited_set]
        else:
            mst_evaluation = self.eval_unvisited_mst_edges_sum_improved(unvisited_cities)
            self.trees_evaluation_hash[hashed_visited_set] = mst_evaluation
            h += mst_evaluation

        # min edge from unvisited to visited
        #h += self.evaluate_visited_mst_connection_edge(node.state, node.state[0], unvisited_cities)
        return h

    def eval_unvisited_mst_edges_sum_improved(self, unvisited_nodes):
        if int(self.t.tocvalue()) >= 600:
            self.t.toc('mst hash has been reset', True)
            self.reset_mst_eval_hash()
        if not unvisited_nodes:
            return 0.0
        return self.tsp_kruskal(unvisited_nodes)

    def path_cost(self, c, state1, action, state2):
        return c + self.cities_matrix[state1[-1]][state2[-1]]

    def evaluate_visited_mst_connection_edge(self, state, visited_city, unvisited_cities):
        min_connected_edge_weight = float('Inf')
        if not unvisited_cities:
            if state[-1] == state[0]:
                return 0.0
            else:
                return self.cities_matrix[state[-1]][visited_city]
        for unvisited_city in unvisited_cities:
            connected_edge_weight = self.cities_matrix[visited_city][unvisited_city]
            if connected_edge_weight < min_connected_edge_weight:
                min_connected_edge_weight = connected_edge_weight
        return min_connected_edge_weight

    def tsp_kruskal(self, unvisited_nodes):
        forest_value = 0.0
        disjoint_sets = graph.DisjointSets()
        non_sorted_edges_list = []
        for vertex_x in unvisited_nodes:
            disjoint_sets.make_set(vertex_x)
            for vertex_y in unvisited_nodes:
                if vertex_x < vertex_y:
                    non_sorted_edges_list.append((vertex_x, vertex_y))
        edges_list = sorted(non_sorted_edges_list, key=lambda edge: self.cities_matrix[edge[0]][edge[1]], reverse=False)
        for vertex_u, vertex_v in edges_list:
            if disjoint_sets.find(vertex_v) != disjoint_sets.find(vertex_u):
                forest_value += self.cities_matrix[vertex_u][vertex_v]
                disjoint_sets.union(vertex_v, vertex_u)
        return forest_value

    def reset_mst_eval_hash(self):
        self.trees_evaluation_hash = {}

