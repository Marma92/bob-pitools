import tkinter as tk
from gpiozero import CPUTemperature
import psutil
import requests
import datetime
from PIL import Image, ImageTk

# Dictionary mapping weather conditions to icon filenames
#    Clear, Clouds, Drizzle, Rain, Thunderstorm, Snow, Mist, Smoke, Haze, Dust, Fog, Sand, Ash, Squall, Tornado

weather_icons = {
    "Clear": "sun.png",
    "Clouds": "cloud.png",
    "Drizzle": "drizzle.png",
    "Rain": "rain.png",
    "Thunderstorm": "thunder.png",
    "Snow": "snow.png",
    "Tornado": "tornado.png"
}
current_time = datetime.datetime.now().strftime('%H:%M')

# Function to get the current date in French format
def get_french_date():
    # Define French names for days and months
    french_days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    french_months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

    # Get current date
    current_date = datetime.datetime.now()

    # Get French day and month names
    french_day = french_days[current_date.weekday()]
    french_month = french_months[current_date.month - 1]  # Month index starts from 1

    # Format date string
    french_date = f"{french_day} {current_date.day} {french_month} {current_date.year}"
    return french_date


def toggle_colon():
    global current_time
    if ":" in current_time:
        current_time = datetime.datetime.now().strftime('%H %M')
    else:
        current_time = datetime.datetime.now().strftime('%H:%M')
    time_label.config(text=current_time, font=('Helvetica', 13), fg="#444")

# Function to update the French date and time display
def update_french_date_and_time():
    toggle_colon()
    #time_label.config(text="", font=('Helvetica', 13), fg="#444")
    french_date_label.config(text=get_french_date(), font=('Helvetica', 18), fg="#333")
    # Schedule the update_french_datetime function to run again every second
    root.after(1000, update_french_date_and_time)


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
        city_label.config(text=f"{city}", font=('Helvetica', 20, 'bold'), fg="#333")
        weather_label.config(text=f"{weather_info}", font=('Helvetica', 14), fg="#666")
        temperature_label.config(text=f"{temperature_info}", font=('Helvetica', 18), fg="#444")
        # Get weather condition
        weather_condition = weather_data["weather"][0]["main"]
        # Load and display corresponding icon
        if weather_condition in weather_icons:
            icon_filename = weather_icons[weather_condition]
            icon_image = Image.open(icon_filename)
            # Resize the image to desired dimensions
            icon_image = icon_image.resize((32, 32), Image.ANTIALIAS)  # Adjust size as needed
            # Ensure transparency is preserved
            icon_image = icon_image.convert("RGBA")
            icon_photo = ImageTk.PhotoImage(icon_image)
            weather_icon_label.config(image=icon_photo)
            weather_icon_label.image = icon_photo  # Keep reference to prevent garbage collection
        else:
            print(f"Icon for weather condition '{weather_condition}' not found.")
            weather_icon_label.config(image=None)
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
    cpu_temp = round(CPUTemperature().temperature, 1)
    ram_load = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    return cpu_load, cpu_temp, ram_load, disk_usage

# Function to update the system information display
def update_system_info():
    cpu_load, cpu_temp, ram_load, disk_usage = get_system_info()
    disk_usage_label.config(text=f"💿 Disk : {disk_usage}%", font=('Helvetica', 12), fg="#444")
    cpu_load_label.config(text=f"💻 CPU : {cpu_load}%", font=('Helvetica', 12), fg="#444")
    cpu_temp_label.config(text=f"🌡 Temp: {cpu_temp}°C", font=('Helvetica', 12), fg="#444")
    ram_load_label.config(text=f"🖲 RAM : {ram_load}%", font=('Helvetica', 12), fg="#444")

    # Schedule the update_system_info function to run again after 1 second
    root.after( 1000, update_system_info)

###########################################
# Display
###########################################

# Function to make the window full-screen
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))
    root.after(10000, hide_pointer)

# Function to hide the mouse pointer
def hide_pointer():
    root.config(cursor="none")  # Hide the mouse pointer

# Function to show the mouse pointer
def show_pointer(event=None):
    root.config(cursor="")  # Show the mouse pointer

# Function to reset the timer for hiding the mouse pointer
def reset_timer(event=None):
    global timer_id  # Declare timer_id as global
    root.after_cancel(timer_id)  # Cancel previous timer
    timer_id = root.after(10000, hide_pointer)  # Schedule hiding the mouse pointer after 10 seconds


###########################################
# Main
###########################################



# Create Tkinter window
root = tk.Tk()
root.title("Bob-tools")

# Handling pointer disappearance
# Initialize timer_id
timer_id = None
# Bind mouse movement and keypress events to reset the timer
root.bind("<Motion>", reset_timer)
root.bind("<Key>", reset_timer)
# Schedule hiding the mouse pointer after 10 seconds
timer_id = root.after(10000, hide_pointer)
# Show the mouse pointer when the window loses focus
root.bind("<FocusIn>", show_pointer)
# Hide the mouse pointer initially
hide_pointer()


# Create and configure frames

#weather
weather_frame = tk.Frame(root)
weather_frame.grid(row=0, column=0, padx=5, pady=5)

# Create and place widgets in the weather frame
city_label = tk.Label(weather_frame, text="")  # Set font size to 20
city_label.grid(row=0, column=0)

# Add a label for weather icon
weather_icon_label = tk.Label(weather_frame)
weather_icon_label.grid(row=1, column=0)

weather_label = tk.Label(weather_frame, text="")
weather_label.grid(row=2, column=0)

temperature_label = tk.Label(weather_frame, text="")
temperature_label.grid(row=3, column=0)

# Create and configure system info frame
system_info_frame = tk.Frame(root)
system_info_frame.grid(row=0, column=2, padx=5, pady=5)

# Create and place labels for system information
cpu_load_label = tk.Label(system_info_frame, text="")
cpu_load_label.grid(sticky="W", row=0, column=0)

cpu_temp_label = tk.Label(system_info_frame, text="")
cpu_temp_label.grid(sticky="W", row=1, column=0)

ram_load_label = tk.Label(system_info_frame, text="")
ram_load_label.grid(sticky="W", row=2, column=0)

disk_usage_label = tk.Label(system_info_frame, text="")
disk_usage_label.grid(sticky="W", row=3, column=0)


# Create and place French date frame in the center of the window
french_date_frame = tk.Frame(root)
french_date_frame.grid(row=1, column=1, pady=10)
french_date_frame.lift()

# Create and place label for French date in the center of the window
french_date_label = tk.Label(french_date_frame, text="", font=("Arial", 20))
french_date_label.grid(row=0, column=0)

time_label = tk.Label(french_date_frame, text="", font=("Arial", 15))
time_label.grid(row=1, column=0)

# Call update_system_info function to fetch and display system information initially
update_system_info()

# Call update_weather function to fetch and display weather data
update_weather()

# Call update_french_datetime function to fetch and display French date and time information initially
update_french_date_and_time()

# Bind F11 key to toggle full-screen
root.bind("<F11>", toggle_fullscreen)

# Bind Escape key to exit full-screen
root.bind("<Escape>", toggle_fullscreen)

# Start the application
root.mainloop()