import time
import tkinter as tk
from datetime import date
from tkinter import TOP, BOTH, BOTTOM, Label
import matplotlib as mpl
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import requests
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.basemap import Basemap

mpl.rcParams['toolbar'] = 'None'
ISS_URL="http://api.open-notify.org/iss-now.json"
time1 = ''
date1 = ''

def tick():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%H:%M')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    clock.after(1000, tick)

def get_date():
    global date1 
    #get current date
    date2 = date.today().strftime('%b, %d %Y')
    # compare
    if date2 != date1:
        date1 = date2 
        day.config(text=date2)

    day.after(20000000, get_date)


# Function to get ISS position from NASA API
def get_iss_location():
    json_data=''
    while not json_data:
        try:
            json_data=requests.get(ISS_URL, timeout=30).json()
        except requests.ConnectionError as e:
            print(str(e))
            time.sleep(10)
        except requests.Timeout as e:
            print(str(e))
            time.sleep(10)
        except requests.RequestException as e:
            print(str(e))
            time.sleep(10)

    position=[float(json_data['iss_position']['longitude']), float(json_data['iss_position']['latitude'])]
    return position

# Setup the figure for the animation
f = plt.figure(figsize=(8, 4.8), frameon=False, tight_layout={ "pad": 0.0 })
m = Basemap(projection='cyl', resolution='c')
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
line1 = m.plot(x, y, linestyle='-', color='xkcd:red')[0]

# -180 - 0
line2 = m.plot(x1, y1, linestyle='-', color='xkcd:black')[0]

# Marker
point = m.plot(x2, y2, marker='o', color='xkcd:red', markersize=5)[0]

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

    if 179.950 <= current_location[0] < 180:
            array1_1.append(current_location)
            time.sleep(2)
            current_location=get_iss_location()
            if current_location[0] < 0:
                array2_1 = array1_1
                array1_1 = []
                array1_1.append(current_location)
            else:
                time.sleep(2)
                current_location=get_iss_location()
                array2_1 = array1_1
                array1_1 = []
                array1_1.append(current_location)
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


root = tk.Tk()
root.configure(background='grey')
root.geometry('800x480+0+0')
root.overrideredirect(1)

canvas = FigureCanvasTkAgg(f, master=root)
canvas.get_tk_widget().configure(background='grey')
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

clock = Label(canvas.get_tk_widget(), font=('courier', 22, 'bold'), bg='grey')
clock.pack(side=BOTTOM, pady=1)

day = Label(canvas.get_tk_widget(),font=('courier', 22, 'bold'), bg='grey')
day.pack(side=TOP)
canvas.draw()

get_date()
tick()

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(f, animate, init_func=init,
                               frames=None, interval=2000, blit=False)

root.update()

root.mainloop()