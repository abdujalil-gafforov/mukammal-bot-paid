def list_to_matrix(data_list, cols=3):
    matrix = [data_list[i:i + cols] for i in range(0, len(data_list), cols)]
    return matrix
