import numpy as np

from sys import argv



if __name__ == "__main__":
    if len(argv) < 3:
        raise ValueError('please specify at least one and the subdir to save to')

    contributions = np.loadtxt(argv[1], delimiter=",", ndmin=2)
    print(argv[1], " loaded")

    SUBDIR = argv[-1]

    for path in argv[2:-1]: # the last one is the subdir to save to
        print(path, " loaded")
        contributions = np.concatenate( (contributions, np.loadtxt(path, delimiter=",", ndmin=2)) )


    # sort them according to the first colum (index)
    ind = np.argsort( contributions[:,0] )
    contributions = contributions[ind]

    print("\nsaving to results/contributions.csv")
    np.savetxt("results/{}/contributions.csv".format(SUBDIR), contributions, delimiter = ",", fmt = ["%.18e", "%d"])
