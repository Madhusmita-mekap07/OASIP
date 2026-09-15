import tkinter as tk
from tkinter import messagebox
import requests

# NOTE: You will need to replace this with your free API key from openweathermap.org
API_KEY = "YOUR_API_KEY_HERE" 

def get_weather():
    city = entry_city.get().strip()
    if not city:
        messagebox.showerror("Input Error", "Please enter a city name.")
        return
    
    if API_KEY == "YOUR_API_KEY_HERE":
        messagebox.showwarning("API Key Missing", "Please replace 'YOUR_API_KEY_HERE' in the code with a real OpenWeatherMap API key.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get("cod") == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"].title()
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            
            result_text = (
                f"🌡️ Temperature: {temp}°C\n"
                f"☁️ Condition: {desc}\n"
                f"💧 Humidity: {humidity}%\n"
                f"💨 Wind Speed: {wind_speed} m/s"
            )
            lbl_result.config(text=result_text, fg="#0f172a")
        else:
            messagebox.showerror("Error", "City not found! Please check the spelling.")
            
    except requests.exceptions.RequestException:
        messagebox.showerror("Network Error", "Failed to connect to the weather service.")

# GUI Setup
root = tk.Tk()
root.title("Weather App - Oasis Infobyte")
root.geometry("350x350")
root.resizable(False, False)

tk.Label(root, text="Live Weather App", font=("Arial", 16, "bold"), fg="#0284c7").pack(pady=15)

tk.Label(root, text="Enter City Name:").pack()
entry_city = tk.Entry(root, font=("Arial", 12), justify="center")
entry_city.pack(pady=5)

btn_get = tk.Button(root, text="Get Weather", command=get_weather, bg="#10b981", fg="white", font=("Arial", 10, "bold"))
btn_get.pack(pady=10)

lbl_result = tk.Label(root, text="", font=("Arial", 12), justify="left")
lbl_result.pack(pady=15)

root.mainloop()