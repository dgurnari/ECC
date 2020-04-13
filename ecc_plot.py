from sys import argv
import numpy as np
from matplotlib import pyplot as plt

# given the ordered list of local contributions
# returns a list of tuples (filtration, euler characteristic)



def euler_characteristic_list(local_contributions):

    euler_characteristic = []

    current_characteristic = 0
    old_f = 0

    for filtration, contribution in local_contributions:
        if filtration > old_f:
            euler_characteristic.append([old_f, current_characteristic])
            old_f = filtration

        current_characteristic += contribution

    # add last contribution
    euler_characteristic.append([filtration, current_characteristic])

    return np.array(euler_characteristic)


# In[6]:


# WARNING
# when plotting a lot of points, drawing the lines can take some time

def plot_euler_curve(e_list, with_lines=False, title = None):
    plt.figure()
    plt.scatter([f[0] for f in e_list], [f[1] for f in e_list])

    # draw horizontal and vertical lines b/w points

    if with_lines:
        plt.hlines(y = e_list[0][1], xmin=0, xmax=e_list[0][0])

        for i in range(len(e_list) - 1):
            plt.vlines(x=e_list[i][0], ymin=min(e_list[i][1], e_list[i+1][1]),ymax=max(e_list[i][1], e_list[i+1][1]))

            plt.hlines(y=e_list[i+1][1], xmin=e_list[i][0], xmax=e_list[i+1][0])

    plt.xlabel("filtration")
    plt.ylabel("euler characteristic")
    plt.title(title)
    plt.savefig("ECC.png")
    print("plot saved in ECC.png")



if __name__ == "__main__":
    if len(argv) < 4:
        raise ValueError('please specify a csv file,  if you want a png and lines with 0/1')
    FILE_PATH = argv[1]
    DRAW = int(argv[2])
    LINES = int(argv[3])

    lc_list = np.loadtxt(FILE_PATH, delimiter=',', ndmin=2)

    e = euler_characteristic_list(lc_list)

    if DRAW:
        plot_euler_curve(e, with_lines=LINES)
