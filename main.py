import csv
import plotly.express as pe

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns


rows=[]

with open("data.csv","r") as f:
    data = csv.reader(f)

    for row in data:
        rows.append(row)

headers = rows[0]    

planet_data_rows = rows[1:]

# print(headers)
# print(planet_data_rows)

headers[0] = "row_num"

solar_system_planet_count ={}

for planet_data in planet_data_rows:
    
    if solar_system_planet_count.get(planet_data[11]):
        solar_system_planet_count[planet_data[11]] += 1

    else:
        solar_system_planet_count[planet_data[11]] = 1


max_solar_system = max(solar_system_planet_count, key = solar_system_planet_count.get)

print("Solar System That Has The Maximum Number Of The Planets-->",max_solar_system)
print("The Maximum Number Of The Planets-->",solar_system_planet_count[max_solar_system])



temp_planet_data_rows = list(planet_data_rows)

for planet_data in temp_planet_data_rows :
    
    # 1 Jupiter Mass = 317.8 Earth Mass
    # 1 Jupiter Radius = 11.2 Earth Radius

    planet_mass = planet_data[3]

    if planet_mass.lower() == "unknown" :
        planet_data_rows.remove(planet_data)
        continue

    else:
        planet_mass_value = planet_mass.split(" ")[0]  
        planet_mass_ref = planet_mass.split(" ")[1]

        if planet_mass_ref == "Jupiters":
            planet_mass_value = float(planet_mass_value)*317.8

            planet_data[3] = planet_mass_value
            
    planet_radius = planet_data[7]
    if planet_radius.lower() == "unknown" :
        planet_data_rows.remove(planet_data)
        continue
    
    else:
        planet_radius_value = planet_radius.split(" ")[0]
        planet_radius_ref = planet_radius.split(" ")[2]

        if planet_radius_ref == "Jupiters":
            planet_radius_value = float(planet_radius_value)*11.2

            planet_data[7] = planet_radius_value

print(len(planet_data_rows))


hd_10180_planets = []

for planet_data in planet_data_rows:
    if max_solar_system == planet_data[11]:
        hd_10180_planets.append(planet_data)


# print(hd_10180_planets)
# print(len(hd_10180_planets))

#------------------- BAR GRAPH ------------------------------

hd_10180_planets_mass =[]
hd_10180_planets_name =[]

for planet_data in hd_10180_planets:
    hd_10180_planets_mass.append(planet_data[3])
    hd_10180_planets_name.append(planet_data[1])


# fig = pe.bar(x=hd_10180_planets_mass , y = hd_10180_planets_name )    

# fig.show()

#------------------------------------------------------------------------------------

# g = (G + mass of Earth) / d2
 
#  G is a gravitational constant, which means that it will always be the same.

# M(earth) is the mass of Earth (or any other planet if we are calculating it for another planet)

# d is the radius of the planet!

# Our Earth’s gravity(g) is 9.8 m/s, and we as humans are accustomed to it

# Mars has a gravity of 3.711 m/s and Moon has a gravity of 1.62 m/s.



temp_planet_data_rows = list(planet_data_rows)

for planet_data in temp_planet_data_rows:
    if planet_data[1].lower() == "hd 100546 b":
        planet_data_rows.remove(planet_data)

planet_masses = []
planet_radiuses = []
planet_names = []

for planet_data in planet_data_rows:
    planet_masses.append(planet_data[3])
    planet_radiuses.append(planet_data[7])
    planet_names.append(planet_data[1])

planet_gravity = []

for index, name in enumerate(planet_names):
    gravity = (float(planet_masses[index])*5.972e+24) / (float(planet_radiuses[index])*float(planet_radiuses[index])*6371000*6371000) * 6.674e-11
    planet_gravity.append(gravity)

# fig = pe.scatter(x=planet_radiuses, y=planet_masses, size=planet_gravity, hover_data=[planet_names])
# fig.show()

# Mass of Earth = 5.972e+24  
# Radius of Earth = 6371000

# The value of G (Gravitational Constant) is 6.674e-11

low_gravity_planets = []

for index , gravity in enumerate(planet_gravity):
    if gravity < 10:
        low_gravity_planets.append(planet_data_rows[index])

print(len(low_gravity_planets))

low_gravity_planets = []
for index, gravity in enumerate(planet_gravity):
  if gravity < 100:
    low_gravity_planets.append(planet_data_rows[index])

print(len(low_gravity_planets))

print(headers)
planet_types_values = []
for planet_data in planet_data_rows:
  planet_types_values.append(planet_data[6])
print(list(set(planet_types_values)))

planet_masses =[]
planet_radiuses = []

for planet_data in planet_data_rows:
  planet_masses.append(planet_data[3])
  planet_radiuses.append(planet_data[7])

fig = pe.scatter(x=planet_radiuses,y = planet_masses)
fig.show()

X = []

for index, planet_mass in enumerate(planet_masses):
  temp_list = [
                  planet_radiuses[index],
                  planet_mass
              ]
  X.append(temp_list)


wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state = 42)
    kmeans.fit(X)
    # inertia method returns wcss for that model
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(10,5))
sns.lineplot(range(1, 11), wcss, marker='o', color='red')
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

planet_masses = []
planet_radiuses = []
planet_types = []

for planet_data in low_gravity_planets:
  planet_masses.append(planet_data[3])
  planet_radiuses.append(planet_data[7])
  planet_types.append(planet_data[6])

fig = pe.scatter(x = planet_radiuses,y = planet_masses , color = planet_types )
fig.show()

suitable_planets = []
for planet_data in low_gravity_planets:
  if planet_data[6].lower() == "terrestrial" or planet_data[6].lower() == "super earth":
    suitable_planets.append(planet_data)

print(len(suitable_planets))