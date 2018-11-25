import matplotlib.pyplot as plt

lines = []
with open('h2.csv', 'r') as file:
    for l in file:
        lines.append(l)

sliding_window = []
x = []
y = []
avg_x = []
avg_y = []
min_x = []
min_y = []
for line in lines:
    l = line.split(',')
    sliding_window.append(float(l[1]))
    y.append(float(l[1]))
    x.append(int(l[0]))
    avg_x.append(int(l[0])+10)
    if len(sliding_window) < 10:
        avg_y.append(0)
    elif len(sliding_window) == 10:
        avg=sum(sliding_window)/10.0
        q=float(min(sliding_window))/float(avg)
        if (q)<0.985:
            min_x.append(int(l[0]))
            min_y.append(min(sliding_window))

        avg_y.append(avg)
        sliding_window.remove(sliding_window[0])

plt.plot(x, y, 'y', label='real')
plt.plot(avg_x, avg_y, 'b', label='avg')
plt.plot(min_x, min_y, 'go', markersize=2, label='min')
plt.legend(loc='best')
plt.show()

plt.plot(x, y, 'y', label='real')
plt.legend(loc='best')
plt.show()

plt.plot(avg_x, avg_y, 'b', label='avg')
plt.legend(loc='best')
plt.show()

plt.plot(min_x, min_y, 'go', label='avg')
plt.legend(loc='best')
plt.show()