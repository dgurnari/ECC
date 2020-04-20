import numpy as np
from sys import argv


def create_grid(dim, lenght):
    # creates #dim arrays each of #lenght numbers at 0.1 distance
    # then staks them together

    return np.stack(np.meshgrid( *[[x/10 for x in range(lenght)] for i in range(dim)]  ), -1).reshape(-1, dim)

if __name__ == "__main__":
    if len(argv) < 3:
        raise ValueError('please specify the dimension and lenght of the grid')

    DIM = int(argv[1])
    LENGHT = int(argv[2])

    print("grid {} {} created".format(DIM, LENGHT))
    grid = create_grid(DIM, LENGHT)

    np.savetxt("datasets/grid_{}_{}.csv".format(DIM, LENGHT), grid, delimiter = ",", fmt='%1.1f')
    print("grid saved in datasets/grid_{}_{}.csv".format(DIM, LENGHT))
