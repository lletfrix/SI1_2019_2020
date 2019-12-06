import matplotlib.pyplot as plt

FILENAME = "month_cli_stats.txt"

def main(graphic_name=None):
    names = []
    data = []

    f = open(FILENAME, "r")

    line = f.readline()
    while line:
        line = line[:-1]
        lst = line.split(" ")
        names.append(lst[0])
        data.append(float(lst[1]))
        line = f.readline()

    if graphic_name:
        fig = plt.figure(graphic_name)
    else:
        fig = plt.figure(u'Graphic')
    ax = fig.add_subplot(111) # Axes

    size = range(len(data))
    ax.bar(size, data, width=0.8, align='center')
    ax.set_xticks(size)
    ax.set_xticklabels(names)

    plt.show()


if __name__ == "__main__":
    main("lista clientes mes - tiempos medios")
