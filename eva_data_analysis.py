import datetime as dt
import json
import matplotlib.pyplot as plt
import csv

# https://data.nasa.gov/resource/eva.json (with modifications)
input_file = open('./eva-data.json', 'r')
output_file = open('./eva-data.csv','w')
graph_file = './cumulative_eva_graph.png'

fieldnames = ("EVA #", "Country", "Crew    ", "Vehicle", "Date", "Duration", "Purpose")

data=[]

for i in range(374):
    line = input_file.readline()
    print(line)
    data.append(json.loads(line[1:-1]))
#data.pop(0)
## Comment out this bit if you don't want the spreadsheet

write = csv.writer(output_file)

time = []
date =[]

j=0
for i in data:
    print(data[j])
    # and this bit
    write.writerow(data[j].values())

    if 'duration' in data[j].keys():
        duration = data[j]['duration']

        if duration == '':
            pass
        else:
            hours_mins = dt.datetime.strptime(duration, '%H:%M')
            ttt = dt.timedelta(hours=hours_mins.hour, minutes=hours_mins.minute, seconds=hours_mins.second).total_seconds()/(60*60)

            print(hours_mins, ttt)
            time.append(ttt)
            if 'date' in data[j].keys():
                date.append(dt.datetime.strptime(data[j]['date'][0:10], '%Y-%m-%d'))
                #date.append(data[j]['date'][0:10])

            else:
                time.pop(0)
    j+=1

hours_mins=[0]

for i in time:
    hours_mins.append(hours_mins[-1]+i)

date,time = zip(*sorted(zip(date, time)))

plt.plot(date,hours_mins[1:], 'ko-')
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(graph_file)
plt.show()
