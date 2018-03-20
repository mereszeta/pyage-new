import matplotlib.pyplot as plt

x_ax = []
y_ax = []
filename = "result_evol_0.2_1.txt"
with open(filename) as f:
    for line in f:
        zz = str(line).split(";")
        x_ax.append(int(zz[0]))
        y_ax.append(float(zz[1].rstrip()))
        if int(zz[0]) == 499: break

plt.title(filename)
plt.axes().set_ylim([-5, 5])
plt.plot(x_ax, y_ax)
plt.show()
