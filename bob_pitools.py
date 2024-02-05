import tkinter as tk
import requests

# Function to fetch weather data from OpenWeatherMap API
def get_weather(city):
    api_key = "YOUR_API_KEY_HERE"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    return weather_data

# Function to update the weather display
def update_weather():
    city = city_entry.get()
    weather_data = get_weather(city)
    if weather_data["cod"] != "404":
        weather_info = weather_data["weather"][0]["description"].capitalize()
        temperature_info = f"{weather_data['main']['temp']}°C"
        weather_label.config(text=f"Weather: {weather_info}")
        temperature_label.config(text=f"Temperature: {temperature_info}")
    else:
        weather_label.config(text="City not found")
        temperature_label.config(text="")

# Create Tkinter window
root = tk.Tk()
root.title("Weather Forecast")

# Create and configure frames
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Create and place widgets
city_label = tk.Label(frame, text="Enter City:")
city_label.pack()

city_entry = tk.Entry(frame)
city_entry.pack()

update_button = tk.Button(frame, text="Update Weather", command=update_weather)
update_button.pack()

weather_label = tk.Label(frame, text="")
weather_label.pack()

temperature_label = tk.Label(frame, text="")
temperature_label.pack()

# Function to make the window full-screen
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

# Bind F11 key to toggle full-screen
root.bind("<F11>", toggle_fullscreen)

# Bind Escape key to exit full-screen
root.bind("<Escape>", toggle_fullscreen)

# Start the application
root.mainloop()
