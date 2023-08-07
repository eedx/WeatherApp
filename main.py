# =======================================================================================
# LIBRARIES AND VARIABLES NEEDED

import datetime

import customtkinter as ctk
import requests
from PIL import Image
from urllib.request import urlopen

week = {
    0: 'Mon',
    1: 'Tue',
    2: 'Wed',
    3: 'Thu',
    4: 'Fri',
    5: 'Sat',
    6: 'Sun'
}

api_key = 'abb1e2d8f5df4b13b6304758230708'

url = 'http://api.weatherapi.com/v1/forecast.json'

# =======================================================================================
# CTK WINDOW SETTINGS

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

root = ctk.CTk()
root.geometry('800x500')
root.title('Weather App by @eedx')

# =======================================================================================
# FORECASTED VARIABLES AND FIRST API CALL

var = {
    'current': [ctk.StringVar() for i in range(5)],
    'date': [ctk.StringVar() for i in range(5)],
    'icon': [ctk.StringVar() for i in range(5)],
    'avg_t': [ctk.StringVar() for i in range(5)]
}


def forecast(q='London'):
    
    params = {
        'key': api_key,
        'q': q,
        'days': 5
    }

    with requests.get(url, params=params) as response:
        r = response.json()
    
    var['current'][0].set(r['location']['name'])
    var['current'][1].set(r['location']['country'])
    var['current'][2].set(str(r['current']['temp_c']) + '°C')
    var['current'][3].set(r['current']['condition']['text'])
    var['current'][4].set('https:' + r['current']['condition']['icon'])
    
    for i, (d, c, t) in enumerate(zip(var['date'], var['icon'], var['avg_t'])):
        d.set(r['forecast']['forecastday'][i]['date'])
        c.set(f"https:{r['forecast']['forecastday'][i]['day']['condition']['icon']}")
        t.set(f"{r['forecast']['forecastday'][i]['day']['avgtemp_c']}°C")
        
    
forecast()

# =======================================================================================
# CTK FRAMES CONFIGURATION WITH FORECAST DAYS, AVERAGE TEMP AND ICON

top_frame = ctk.CTkFrame(master=root, 
                         width=720, 
                         height=72, 
                         border_width=2, 
                         fg_color=('gray90', 'gray13'))
top_frame.pack(pady=(30,5),
           padx=40, 
           fill='both',
           expand=False)

bottom_frame = ctk.CTkFrame(master=root, 
                            width=720, 
                            height=360, 
                            border_width=2, 
                            fg_color=('#278dbd', 'gray13'))
bottom_frame.pack(pady=(5, 30),
           padx=40, 
           fill='both', 
           expand=True)

forecast_frame = ctk.CTkFrame(master=bottom_frame,
                              width=720,
                              height=180,
                              fg_color='transparent')
forecast_frame.grid(row=2, 
                    column=0, 
                    columnspan=5, 
                    rowspan=3, 
                    padx=20, 
                    pady=(20, 20))


days_frame = [None] * 5
df_icon = [None] * 5
def set_df():
    for i, (df, dfi) in enumerate(zip(days_frame, df_icon)):
        df = ctk.CTkFrame(master=forecast_frame,
                        fg_color=('#bbdefb', 'gray40'),
                        width=123.5,
                        height=160,
                        border_width=2)
        df.grid(row=0, column=i, padx=6)
        
        wday = var['date'][i].get()
        wday = datetime.datetime.strptime(wday, "%Y-%m-%d")
        wday = week[datetime.date.weekday(wday)]
        
        df_date = ctk.CTkLabel(master=df,
                      text=wday,
                      font=('Roboto', 18),
                      compound='center',
                      text_color=('gray10', 'white'),
                      width=118)
        df_date.grid(row=0, column=0, padx=2, pady=10)

        df_img = ctk.CTkImage(Image.open(
            urlopen(var['icon'][i].get())),
                            size=(50, 50))
        dfi = ctk.CTkLabel(master=df,
                            text='',
                            image=df_img,
                            compound='right')
        
        dfi.grid(row=1, column=0, rowspan=2, padx=0, pady=5)
        
        df_icon[i] = dfi

        df_temp = ctk.CTkLabel(master=df,
                    textvariable=var['avg_t'][i],
                    font=('Roboto', 24),
                    compound='center',
                    text_color=('gray10', 'white'))
        df_temp.grid(row=3, column=0, padx=0, pady=10)
        

set_df()

# =======================================================================================
# SEARCH BUTTON FUNCTIONALITY

def on_click():
    
    forecast(search_str.get())
    update_img()
    
    current_time = datetime.datetime.now()
    time = current_time.strftime('%a %d %b %Y, %I:%M%p')
    c_date.configure(text=time)

# =======================================================================================
# MODE TOGGLER FUNCTIONALITY

def mode_switch():
    if switch_var.get() == 'light':
        ctk.set_appearance_mode('light')
    else:
        ctk.set_appearance_mode('dark')


switch_var = ctk.StringVar(value='dark')
    
# =======================================================================================
# TOP FRAME
    
search_str = ctk.StringVar(value='')

search_bar = ctk.CTkEntry(master=top_frame,
                          placeholder_text='Search by city or country',
                          width=250,
                          font=('Roboto', 12),
                          textvariable=search_str)
search_bar.grid(row=0, column=0, pady=(20, 2), padx=(20, 10))

search_text = ctk.CTkLabel(master=top_frame,
                           text='Powered by WeatherAPI.com',
                           font=('Roboto', 13))
search_text.grid(row=1, column=0, pady=(2, 15))
    
button = ctk.CTkButton(master=top_frame,
                       text='Search',
                       width=120,
                       command=on_click)
button.grid(row=0, column=1, pady=(20, 2), padx=0)

switch = ctk.CTkSwitch(master=top_frame,
                       width=80,
                       switch_width=70,
                       text='',
                       command=mode_switch,
                       variable=switch_var,
                       onvalue='light',
                       offvalue='dark',
                       button_color=('#306fd5', 'lightgrey'),
                       progress_color=('lightblue', 'grey'))
switch.grid(row=0, column=3, pady=(20, 2), padx=(200, 10))

moon_img = ctk.CTkImage(Image.open('moon_icon.png'),
                         size=(22, 22))

moon_icon = ctk.CTkLabel(master=top_frame,
                        image=moon_img,
                        text='',
                        width=22,
                        height=22,
                        compound='right')

sun_img = ctk.CTkImage(Image.open('sun_icon.png'),
                         size=(22, 22))

sun_icon = ctk.CTkLabel(master=top_frame,
                        image=sun_img,
                        text='',
                        width=22,
                        height=22,
                        compound='left',
                        anchor='w')

moon_icon.place(x=590, y=50)
sun_icon.place(x=660, y=50)

# =======================================================================================
# BOTTOM FRAME

city_name = ctk.CTkLabel(master=bottom_frame,
                      textvariable=var['current'][0],
                      font=('Roboto', 26),
                      compound='right',
                      text_color=('gray95', 'white'))
city_name.grid(row=0, column=0, padx=(10, 0), pady=(20, 5))

country_name = ctk.CTkLabel(master=bottom_frame,
                      textvariable=var['current'][1],
                      font=('Roboto', 16),
                      compound='left',
                      text_color=('gray95', 'white'))
country_name.grid(row=0, column=1, padx=(0, 0), pady=(20, 5))

current_time = datetime.datetime.now()
time = current_time.strftime('%a %d %b %Y, %I:%M%p')

c_date = ctk.CTkLabel(master=bottom_frame,
                      text=time,
                      font=('Roboto', 16),
                      compound='left',
                      text_color=('gray95', 'white'))
c_date.grid(row=0, column=2, padx=(0, 0), pady=(20, 5))

temperature = ctk.CTkLabel(master=bottom_frame,
                    textvariable=var['current'][2],
                    font=('Roboto', 34),
                    compound='center',
                    text_color=('gray95', 'white'))
temperature.grid(row=1, column=0, padx=(10, 0), pady=(5, 10))

current_img = ctk.CTkImage(Image.open(
            urlopen(var['current'][4].get())),
                           size=(50, 50))
current_icon = ctk.CTkLabel(master=bottom_frame,
                       text='',
                       image=current_img,
                       compound='right')
current_icon.grid(row=0, column=4, padx=10, pady=(30, 5))

current_weather = ctk.CTkLabel(master=bottom_frame,
                       textvariable=var['current'][3],
                       font=('Roboto', 25),
                       compound='right',
                       text_color=('gray95', 'white'))
current_weather.grid(row=1, 
                     column=3, 
                     columnspan=2, 
                     padx=(0, 10), 
                     pady=(5, 10))

# =======================================================================================
# IMAGES UPDATE FUNCTION

def update_img():        
    cw_img = ctk.CTkImage(Image.open(urlopen(var['current'][4].get())),
                      size=(50, 50))
    current_icon.configure(image=cw_img)
    current_icon.image = cw_img
    
    for i, dfi in enumerate(df_icon): 
        df_img = ctk.CTkImage(Image.open(urlopen(var['icon'][i].get())), size=(50, 50))   
        dfi.configure(image=df_img)
        dfi.image = df_img

# =======================================================================================
# MAIN LOOP DECLARATION

root.resizable(False, False)
root.mainloop()