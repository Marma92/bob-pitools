import tkinter as tk
from tkinter import ttk
from gpiozero import CPUTemperature
import psutil
import requests

###########################################
# WEATHER
###########################################

# Function to fetch weather data from OpenWeatherMap API
def get_weather(city):
    api_key = "4e86d3fafe06458f1bd7c3f8444845ac"  # OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    print (weather_data)
    return weather_data

# Function to update the weather display
def update_weather():
    city = "Clichy"
    weather_data = get_weather(city)
    if "cod" in weather_data and weather_data["cod"] != "404":
        weather_info = weather_data["weather"][0]["description"].capitalize()
        temperature_info = f"{weather_data['main']['temp']}°C"
        city_label.config(text=f"{city}")
        weather_label.config(text=f"{weather_info}")
        temperature_label.config(text=f"{temperature_info}")
    else:
        if "message" in weather_data:
            error_message = weather_data["message"]
            weather_label.config(text=f"Error: {error_message}")
            temperature_label.config(text="")
        else:
            weather_label.config(text="Unknown error")
            temperature_label.config(text="")
    # Schedule the update_weather function to run again after 30 minutes
    root.after(30 * 60 * 1000, update_weather)

###########################################
# System
###########################################

# Function to fetch system information
def get_system_info():
    cpu_load = psutil.cpu_percent(interval=1)
    ram_load = psutil.virtual_memory().percent
    cpu_temp = round(CPUTemperature().temperature, 1)
    return cpu_load, ram_load, cpu_temp

# Function to update the system information display
def update_system_info():
    cpu_load, ram_load, cpu_temp = get_system_info()
    cpu_load_label.config(text=f"CPU Load: {cpu_load}%")
    ram_load_label.config(text=f"RAM Load: {ram_load}%")
    cpu_temp_label.config(text=f"CPU Temperature: {cpu_temp}°C")
    # Schedule the update_system_info function to run again after 1 second
    root.after( 1000, update_system_info)




# Function to make the window full-screen
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))



# Create Tkinter window
root = tk.Tk()
root.title("Bob-tools")

# Create and configure frames
weather_frame = tk.Frame(root)
weather_frame.pack(anchor="nw", side="left", padx=10, pady=10)

# Create and place widgets
city_label = tk.Label(weather_frame, text="", font=("Arial", 20))  # Set font size to 20
city_label.pack()

weather_label = tk.Label(weather_frame, text="")
weather_label.pack()

temperature_label = tk.Label(weather_frame, text="", font=("Arial", 25))
temperature_label.pack()

# Create and place system information widgets
system_info_frame = tk.Frame(root)
system_info_frame.pack(anchor="ne", side="right", padx=10, pady=10)

# Create and place labels for system information
cpu_load_label = tk.Label(system_info_frame, text="")
cpu_load_label.pack()

ram_load_label = tk.Label(system_info_frame, text="")
ram_load_label.pack()

cpu_temp_label = tk.Label(system_info_frame, text="")
cpu_temp_label.pack()

# Call update_system_info function to fetch and display system information initially
update_system_info()

# Call update_weather function to fetch and display weather data
update_weather()

# Bind F11 key to toggle full-screen
root.bind("<F11>", toggle_fullscreen)

# Bind Escape key to exit full-screen
root.bind("<Escape>", toggle_fullscreen)

# Start the application
root.mainloop()



