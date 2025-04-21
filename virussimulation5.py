import random
import matplotlib.pyplot as plt
import math
from matplotlib.animation import FuncAnimation


People = 1500
Masks = 3
Vaccines = 500
distance_infectivity = 60
chance_of_infection = 0.9  # 0-1
days = 100
Vaccine_effectiveness = 0.8  # 0-1


Points = []
ListOfPeople = list(range(People))
infected = {0}  
infected_with_vaccines = set()
colors = ["green"] * People  
colors[0] = "red"  

for person in ListOfPeople:
    x = random.randint(0, People)
    y = random.randint(0, People)
    Points.append((x, y))

PeopleAndPointsdict = dict(zip(ListOfPeople, Points))
PeopleAndPointsdictWithVACCINES = {key: PeopleAndPointsdict[key] for key in random.sample(ListOfPeople, Vaccines)}


fig, ax = plt.subplots()
sc = ax.scatter(
    [p[0] for p in Points],
    [p[1] for p in Points],
    c=colors,
    s=10
)


vaccinated_sc = ax.scatter(
    [PeopleAndPointsdict[key][0] for key in PeopleAndPointsdictWithVACCINES],
    [PeopleAndPointsdict[key][1] for key in PeopleAndPointsdictWithVACCINES],
    c="yellow",
    s=5,
    label="Vaccinated"
)

ax.scatter(PeopleAndPointsdict[0][0], PeopleAndPointsdict[0][1], s=40, color="black", label="Patient Zero")  # Patient zero

#actual infection simulation
def update(frame):
    global infected, colors
    new_infected = set()
    for key in infected:
        for key2, (x, y) in PeopleAndPointsdict.items():
            if key2 not in infected:
                distance = math.sqrt(
                    (PeopleAndPointsdict[key][0] - x) ** 2 + (PeopleAndPointsdict[key][1] - y) ** 2
                )
                if distance <= distance_infectivity:
                    if random.random() <= chance_of_infection:
                        if key2 in PeopleAndPointsdictWithVACCINES:
                            if random.random() <= 1 - Vaccine_effectiveness:
                                new_infected.add(key2)
                                colors[key2] = "red"  
                        else:
                            new_infected.add(key2)
                            colors[key2] = "red" 
    infected.update(new_infected)
    sc.set_color(colors)  
    return sc, vaccinated_sc


ani = FuncAnimation(fig, update, frames=days, interval=50, repeat=False)


ax.legend()
plt.show()