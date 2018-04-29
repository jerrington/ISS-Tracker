from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import requests
import datetime
import time

ISS_URL="http://api.open-notify.org/iss-now.json"


# Function to get ISS position from NASA API
def get_iss_location():
    raw_data = ''
    while not raw_data:
        try:
            raw_data=requests.get(ISS_URL, timeout=30)
        except requests.ConnectionError as e:
            print(str(e))
            time.wait(10)
        except requests.Timeout as e:
            print(str(e))
            time.wait(10)
        except requests.RequestException as e:
            print(str(e))
            time.wait(10)

    json_data=raw_data.json()
    lat=json_data['iss_position']['latitude']
    lon=json_data['iss_position']['longitude']
    position=[float(lon), float(lat)]
    return position

# Setup the figure for the animation
f = plt.figure(figsize=(14, 8))
m = Basemap(projection='cyl')
#m.bluemarble(scale=.75)
m.drawcoastlines(color='#000000', linewidth=1) 
m.drawcountries()
m.drawstates()
m.drawmapboundary(fill_color='xkcd:ocean')
m.fillcontinents(color='xkcd:dirt brown',lake_color='xkcd:lightblue')

# Set plot styles
x,y = m(0, 0)
x1, y1 = m(0, 0)
x2, y2 = m(0, 0)
# 0 - 180
line1 = m.plot(x, y, linestyle='-', color='xkcd:black')[0]
# -180 - 0
line2 = m.plot(x1, y1, linestyle='-', color='xkcd:red')[0]
# Marker
point = m.plot(x2, y2, marker='o', color='xkcd:black', markersize=5)[0]


# Set blank canvas for anaimation init
def init():
    point.set_data([], [])
    line1.set_data([], [])
    line2.set_data([], [])
    return point, line1, line2,

# Red Array
array1_1=[]
# Blue Array
array2_1=[]

# animation function.  This is called sequentially
def animate(i):
    global array1_1
    global array2_1

    current_location=get_iss_location()

    if 179.900 <= current_location[0] < 180:
            array1_1.append(current_location)
            time.sleep(1)
            current_location=get_iss_location()
            if current_location[0] < 0:
                array2_1 = array1_1
                array1_1 = []
            else:
                time.sleep(2)
                current_location=get_iss_location()
                array2_1 = array1_1
                array1_1 = []
    else:
        array1_1.append(current_location)

    # Load array1_1 data
    if array1_1:
        lons, lats = zip(*array1_1)
        x1, y1 = m(lons, lats)
        line1.set_data(x1, y1)
    # Load array1_2 data
    if array2_1:
        lons2, lats2 = zip(*array2_1)
        x2, y2 = m(lons2, lats2)
        line2.set_data(x2, y2)

    # Set marker
    lons_point, lats_point = zip(current_location)
    x_point, y_point = m(lons_point, lats_point)
    point.set_data(x_point, y_point)

    return point, line1, line2,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(plt.gcf(), animate, init_func=init,
                               frames=None, interval=2000, blit=False)

plt.show()
