from ChristofidesTSP import TravelingSalesmanProblem
import params
import cities_visualitation
import my_utils
import search
import sys
from pytictoc import TicToc


def run_tsp(difficulty, file_name):
    t = TicToc()
    all_cities = my_utils.generate_cities_dict(difficulty)
    cities_map = cities_visualitation.CitiesMap(all_cities)
    tsp = TravelingSalesmanProblem(all_cities, (0,), ())
    t.tic()
    best_known_solution_value = 0.0

    if difficulty == 'big':
        best_known_solution_value = params.big_best_known_solution
    elif difficulty == 'medium':
        best_known_solution_value = params.medium_best_known_solution
    elif difficulty == 'small':
        best_known_solution_value = params.small_best_known_solution
    tsp_result, msg = search.astar_search(tsp, best_known_solution_value, display=True)
    print(msg)
    t.toc()
    cities_list = cities_visualitation.get_normalized_cities_identification(tsp_result.state)
    cities_list_evaluation = (-1)*tsp.value(tsp_result.state)
    cities_map.show_map(list(tsp_result.state))
    cities_map.save_plot(file_name)
    my_utils.save_results(file_name, cities_list_evaluation, cities_list, msg)


if __name__ == '__main__':
    run_tsp(str(sys.argv[1]), str(sys.argv[2]))


