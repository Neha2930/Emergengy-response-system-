import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter
import os
import webbrowser
import datetime
import geocoder  # Added to fetch location

# -------------------- LOGIN WINDOW -------------------- #
class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("Login - Guard Emergency Response")
        master.geometry("500x600")

        # Load background image
        image_path = os.path.join(os.path.dirname(__file__), "car.jpg")

        try:
            bg_image = Image.open(image_path)
        except FileNotFoundError:
            print("⚠️ Warning: car.jpg not found! Using a plain background.")
            bg_image = Image.new("RGB", (500, 600), "gray")  # Fallback gray background

        # Apply blur effect
        bg_image = bg_image.resize((500, 600), Image.LANCZOS).filter(ImageFilter.GaussianBlur(8))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Background Label
        self.bg_label = tk.Label(master, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Create a Canvas to simulate transparency
        self.canvas = tk.Canvas(master, width=350, height=250, bg="white", highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.55, anchor="center")

        # Draw a semi-transparent rectangle
        self.canvas.create_rectangle(0, 0, 350, 250, fill="#ffffff", outline="", stipple="gray50")

        # Login Frame (placed on top of the canvas)
        self.login_frame = tk.Frame(master, bg="white", bd=5, relief="ridge")
        self.login_frame.place(relx=0.5, rely=0.55, anchor="center", width=350, height=250)

        # Title
        self.title_label = tk.Label(self.login_frame, text="User Login", font=("Helvetica", 18, "bold"), bg="white")
        self.title_label.pack(pady=10)

        # Username
        self.username_label = tk.Label(self.login_frame, text="Username:", font=("Helvetica", 12), bg="white")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.login_frame, font=("Helvetica", 12), width=30)
        self.username_entry.pack(pady=5)

        # Password
        self.password_label = tk.Label(self.login_frame, text="Password:", font=("Helvetica", 12), bg="white")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.login_frame, font=("Helvetica", 12), width=30, show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login, bg="#5cb85c", fg="white",
                                      font=("Helvetica", 14, "bold"), width=12)
        self.login_button.pack(pady=15)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Dummy credentials
        if username == "admin" and password == "1234":
            self.master.destroy()  # Close login window
            root = tk.Tk()
            app = GuardApp(root)  # Open the Guard Emergency Response App
            root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")


# -------------------- GUARD APP -------------------- #
class GuardApp:
    def __init__(self, master):
        self.master = master
        master.title("Guard Emergency Response")
        master.geometry("500x700")
        master.configure(bg="#ffffff")

        # Get current location using IP
        g = geocoder.ip('me')
        self.latitude = g.latlng[0] if g.ok else 0.0
        self.longitude = g.latlng[1] if g.ok else 0.0
        self.place = f"{g.city}, {g.state}" if g.ok else "Location not found"

        # Dummy user profiles for demonstration
        self.user_profiles = {}
        self.current_profile = None

        # Title Label
        self.title_label = tk.Label(master, text="Emergency Response App", font=("Helvetica", 22, "bold"), bg="#ffffff", fg="#333333")
        self.title_label.pack(pady=20)

        # Location and Place
        self.location_label = tk.Label(master, text=f"Location: {self.latitude:.6f}, {self.longitude:.6f}", bg="#ffffff", font=("Helvetica", 12))
        self.location_label.pack(pady=5)

        self.place_label = tk.Label(master, text=f"Place: {self.place}", bg="#ffffff", font=("Helvetica", 12))
        self.place_label.pack(pady=5)

        # Alert Button
        self.alert_button = self.create_button(master, "Send Alert", self.send_alert, "#ff4d4d")
        self.alert_button.pack(pady=20)

        # Emergency Contacts
        self.contact_label = tk.Label(master, text="Emergency Contacts:", bg="#ffffff", font=("Helvetica", 14, "bold"))
        self.contact_label.pack()

        self.contact_entry = tk.Entry(master, width=40, font=("Helvetica", 12))
        self.contact_entry.pack(pady=5)

        self.add_contact_button = self.create_button(master, "Add Contact", self.add_contact, "#5cb85c")
        self.add_contact_button.pack(pady=5)

        self.contact_list_display = tk.Listbox(master, width=50, height=6, font=("Helvetica", 12), bg="#f8f8f8")
        self.contact_list_display.pack(pady=10)

        # Profile Management
        self.profile_button = self.create_button(master, "Create Profile", self.create_profile, "#5bc0de")
        self.profile_button.pack(pady=10)

        # Settings Button
        self.settings_button = self.create_button(master, "Settings", self.open_settings, "#5bc0de")
        self.settings_button.pack(pady=10)

        # Help Button
        self.help_button = self.create_button(master, "Help", self.show_help, "#d9534f")
        self.help_button.pack(pady=10)

        # History Log
        self.history_button = self.create_button(master, "View History", self.view_history, "#5bc0de")
        self.history_button.pack(pady=10)

        # Footer
        self.footer_label = tk.Label(master, text="© 2024 Guard App. All Rights Reserved.", bg="#ffffff", font=("Helvetica", 10))
        self.footer_label.pack(pady=10)

        # History log
        self.history = []

    def create_button(self, parent, text, command, color):
        button = tk.Button(parent, text=text, command=command, bg=color, fg="white", font=("Helvetica", 12, "bold"), bd=0)
        return button

    def add_contact(self):
        contact = self.contact_entry.get()
        if contact:
            self.contact_list_display.insert(tk.END, contact)
            messagebox.showinfo("Success", f"Added {contact} to emergency contacts.")
            self.contact_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Contact cannot be empty!")

    def send_alert(self):
        contacts = self.contact_list_display.get(0, tk.END)
        if not contacts:
            messagebox.showerror("No Contacts", "No emergency contacts available to notify.")
            return

        alert_message = f"ALERT: Emergency at {self.place}\nCoordinates: {self.latitude:.6f}, {self.longitude:.6f}\nContacts Notified: {', '.join(contacts)}"
        self.history.append((datetime.datetime.now(), alert_message))  # Log the alert

        messagebox.showinfo("Alert Sent", f"Alert sent to: {', '.join(contacts)}")

        self.open_in_google_maps()

    def open_in_google_maps(self):
        url = f"https://www.google.com/maps/search/?api=1&query={self.latitude},{self.longitude}"
        webbrowser.open(url)


# -------------------- RUN THE APPLICATION -------------------- #
if __name__ == "__main__":
    login_root = tk.Tk()
    login_app = LoginWindow(login_root)
    login_root.mainloop()
