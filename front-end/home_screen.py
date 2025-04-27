import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import urllib.request
import io

class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#121212")
        
        # Create the main content
        self.create_home_content()
    
    def create_home_content(self):
        """Create the main content for the home screen"""
        # Main container
        main_container = tk.Frame(self, bg="#1E1E1E", padx=30, pady=30)
        main_container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.7)
        
        # Apply shadow effect
        self.apply_shadow(main_container)
        
        # Header
        header = tk.Label(main_container, text="Welcome to WORKOUT TRACKER from Group 8", 
                         font=("Arial", 25, "bold"), bg="#1E1E1E", fg="#4CAF50")
        header.pack(pady=(20, 30))
        
        # Description text
        description = tk.Label(main_container, 
                             text="WORKOUT TRACKER is a program that monitors and keeps track of exercises\n"
                                  "done using Ultralytics YOLO11 technology.",
                             font=("Arial BOLD", 18), bg="#1E1E1E", fg="white", justify="center")
        description.pack(pady=(0, 20))
        
        # Try to add an image
        try:
            # Create a frame for the image and description
            content_frame = tk.Frame(main_container, bg="#1E1E1E")
            content_frame.pack(fill="both", expand=True, pady=20)
            
            image = Image.open("gym_background.jpg")  # No full path needed
    
            # Resize image to fit in the frame
            image = image.resize((400, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            # Create image label
            img_label = tk.Label(content_frame, image=photo, bg="#1E1E1E", bd=0)
            img_label.image = photo  # Keep a reference to avoid garbage collection
            img_label.pack(side="left", padx=20)
            
            # Additional information
            info_frame = tk.Frame(content_frame, bg="#1E1E1E")
            info_frame.pack(side="left", fill="both", expand=True, padx=20)
            
            info_text = (
                "Track your workouts with advanced AI technology!\n\n"
                "• Monitor your form\n"
                "• Count repetitions\n"
                "• Track progress over time\n\n"
                "Get started by navigating to the Profile section."
            )
            
            info_label = tk.Label(info_frame, text=info_text, font=("Arial Bold", 16),
                                 bg="#1E1E1E", fg="white", justify="left", anchor="w")
            info_label.pack(fill="both", expand=True)
            
        except Exception as e:
            # If image loading fails, show a message
            error_msg = tk.Label(main_container, 
                               text=f"Could not load image. Click Profile to continue.",
                               font=("Arial", 11), bg="#1E1E1E", fg="#f44336")
            error_msg.pack(pady=20)
    
    def apply_shadow(self, widget):
        """Apply a shadow effect to a widget"""
        # In Tkinter we can't directly add shadows, so we'll use a border effect
        border_frame = tk.Frame(self, bg="#0a0a0a", padx=2, pady=2)
        border_frame.place(relx=0.5, rely=0.5, anchor="center", 
                           relwidth=0.8+0.01, relheight=0.7+0.01)
        
        # Ensure the main widget is above the border
        widget.lift()