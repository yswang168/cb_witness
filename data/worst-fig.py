import matplotlib.pyplot as plt


# get the time 
fs = "worst-50-400"
suff=[".txt", "-MUS.txt", "-mc.txt"]
legend=["cb", "cb-MUS", "mmc"]
style=["-", "-.",":"]
time=[ [], [], [] ]

x=range(50, 401, 10)
for i in range(3):
    fn = open(fs + suff[i], "r")
    line = fn.readline()
    while (line):
        time[i].append(float(line.split(" ")[1]))
        line = fn.readline()
    fn.close()
    plt.plot(x, time[i], style[i], label=legend[i])
plt.legend()                   
plt.ylabel('Time (s)')        
plt.xlabel('Number of variables (n)')      # 设置y轴的label;
plt.savefig("worst-50-400.png")
