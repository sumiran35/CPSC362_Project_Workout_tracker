import tkinter as tk
from tkinter import ttk
from login_screen import LoginScreen
from home_screen import HomeScreen
from profile_screen import ProfileScreen
from styles import apply_styles

class WorkoutTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configure the main window
        self.title("Workout Tracker")
        self.geometry("900x700")
        self.minsize(800, 600)
        
        # Apply styles to the application
        self.style = ttk.Style()
        apply_styles(self.style)
        
        # Set up the container for all frames
        self.container = tk.Frame(self)
        self.container.pack(side="bottom", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Dictionary to store the frames
        self.frames = {}
        
        # Create the navigation bar
        self.create_navbar()
        
        # Initialize user authentication state
        self.is_logged_in = False
        
        # Show the login screen initially
        self.show_frame("login")
        
    def create_navbar(self):
        """Create the navigation bar at the top of the application"""
        self.navbar = tk.Frame(self, bg="#000000", height=50)
        self.navbar.pack(side="top", fill="x")
        
        # Home button
        self.home_btn = tk.Button(self.navbar, text="HOME", bg="#000000", fg="white", 
                                  activebackground="#4CAF50", activeforeground="white",
                                  bd=0, padx=20, pady=10, font=("Arial Bold", 11),
                                  command=lambda: self.show_frame("home"))
        self.home_btn.pack(side="left", padx=10)
        
        # Profile button
        self.profile_btn = tk.Button(self.navbar, text="PROFILE", bg="#000000", fg="white", 
                                     activebackground="#4CAF50", activeforeground="white",
                                     bd=0, padx=20, pady=10, font=("Arial Bold", 11),
                                     command=lambda: self.show_frame("profile"))
        self.profile_btn.pack(side="left", padx=10)
        
        # Logout button (initially hidden)
        self.logout_btn = tk.Button(self.navbar, text="Logout", bg="#f44336", fg="white", 
                                   activebackground="#d32f2f", activeforeground="white",
                                   bd=0, padx=15, pady=8, font=("Arial Bold", 10),
                                   command=self.logout)
        self.logout_btn.pack(side="right", padx=15, pady=8)
        self.logout_btn.pack_forget()  # Hide initially
    
    def setup_frames(self):
        """Set up all the frames for the application"""
        # Initialize frames
        for F, page_name in [
            (LoginScreen, "login"),
            (HomeScreen, "home"),
            (ProfileScreen, "profile")
        ]:
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
    
    def show_frame(self, page_name):
        """Show the specified frame"""
        # Check if user is logged in
        if page_name != "login" and not self.is_logged_in:
            page_name = "login"
        
        # Create frames if they don't exist yet
        if not self.frames:
            self.setup_frames()
            
        frame = self.frames[page_name]
        frame.tkraise()
        
        # Update UI based on login state
        if self.is_logged_in:
            self.logout_btn.pack(side="right", padx=15, pady=8)
        else:
            self.logout_btn.pack_forget()
    
    def login(self, username):
        """Handle user login"""
        self.is_logged_in = True
        self.username = username
        self.show_frame("home")
        
    def logout(self):
        """Handle user logout"""
        self.is_logged_in = False
        self.show_frame("login")
        # Reset the login form
        self.frames["login"].reset_form()

if __name__ == "__main__":
    app = WorkoutTrackerApp()
    app.mainloop()