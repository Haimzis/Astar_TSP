import math

import params


def generate_data_from_file(data_file_path):
    cities_dict = {}
    with open(data_file_path) as data_file:
        content = data_file.readlines()
    for ind, line in enumerate(content):
        x = y = None
        for separated_str in line.split(' '):
            if separated_str is not None and len(separated_str) != 0 and separated_str != '\n':
                if x is None:
                    x = separated_str
                elif y is None:
                    y = separated_str.split('\n')[0]
        if x is not None and y is not None:
            cities_dict[ind] = (float(x), float(y))
        x = y = None
    return cities_dict


def generate_cities_dict(tsp_problem_difficulty):
    problems_dict = {'check': params.check_problem_data_path,
                     'small': params.small_problem_data_path,
                     'medium': params.medium_problem_data_path,
                     'big': params.hard_problem_data_path}

    cities_dict = generate_data_from_file(problems_dict[tsp_problem_difficulty])
    return cities_dict

def save_results(file_name, eval, state ,msg):
    output_file = open('./final_result/' + file_name + '.txt', 'w')
    output_file.write('final_evaluation: ' + str(eval) + '\n')
    output_file.write('final_state: ' + str(state) + '\n')
    output_file.write('message: ' + str(msg) + '\n')


def distance(coords1, coords2):
    return math.sqrt((coords1[0] - coords2[0])**2 + (coords1[1] - coords2[1])**2)


def init_distance_matrix(cities_dict):
    return {row_ind: {col_ind: distance(row_coords, col_coords) for col_ind, col_coords in cities_dict.items()}
            for row_ind, row_coords in cities_dict.items()}