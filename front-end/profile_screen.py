import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image, ImageTk
from workout_track import (
    track_pushups, track_squats, track_leg_extension,
    track_legpress, track_pullups, track_abs
)

class ProfileScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#121212")
        
        # Set up variables
        self.workout_type = tk.StringVar()
        self.video_file_path = tk.StringVar()
        self.results_visible = False
        
        # Create the profile content
        self.create_profile_content()
    
    def create_profile_content(self):
        """Create the main content for the profile screen"""
        # Main container
        self.main_container = tk.Frame(self, bg="#1E1E1E", padx=30, pady=30)
        self.main_container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.7)
        
        # Apply shadow effect
        self.apply_shadow(self.main_container)
        
        # Header
        header = tk.Label(self.main_container, text="Your Profile", 
                         font=("Arial", 22, "bold"), bg="#1E1E1E", fg="#4CAF50")
        header.pack(pady=(20, 30))
        
        # Create a Canvas with scrollbar for content
        canvas = tk.Canvas(self.main_container, bg="#1E1E1E", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1E1E1E")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Description
        description = tk.Label(scrollable_frame, text="Start your workout tracking session:", 
                              font=("Arial Bold", 12), bg="#1E1E1E", fg="white")
        description.pack(pady=(0, 20), anchor="w")
        
        # Workout type selection
        workout_frame = tk.Frame(scrollable_frame, bg="#1E1E1E")
        workout_frame.pack(fill="x", pady=10)
        
        workout_label = tk.Label(workout_frame, text="Select Workout Type:", 
                                font=("Arial Bold", 11), bg="#1E1E1E", fg="white")
        workout_label.pack(side="left", padx=(0, 10))
        
        workout_options = ["", "Pushups", "Squats", "Leg Extension", "Leg Press", "Pullups", "Abs"]
        workout_menu = ttk.Combobox(workout_frame, textvariable=self.workout_type, 
                                   values=workout_options, width=20, state="readonly")
        workout_menu.set("-- Select a workout --")
        workout_menu.pack(side="left")
        
        # Start tracking button
        start_button = tk.Button(scrollable_frame, text="Start Tracking", bg="#4CAF50", fg="white",
                                activebackground="#45a049", activeforeground="white",
                                font=("Arial", 11, "bold"), bd=0, padx=20, pady=8,
                                command=self.start_tracking)
        start_button.pack(pady=20)
        
        # Results container (initially hidden)
        self.results_container = tk.Frame(scrollable_frame, bg="#2A2A2A", padx=20, pady=20)
        
        # Results header
        results_header = tk.Label(self.results_container, text="Workout Results", 
                                 font=("Arial", 14, "bold"), bg="#2A2A2A", fg="white")
        results_header.pack(pady=(0, 20))
        
        # Rep count display
        self.rep_count_display = tk.Label(self.results_container, text="0", 
                                         font=("Arial", 36, "bold"), bg="#2A2A2A", fg="#4CAF50")
        self.rep_count_display.pack(pady=(0, 10))
        
        rep_label = tk.Label(self.results_container, text="Total Repetitions", 
                            font=("Arial Bold", 12), bg="#2A2A2A", fg="white")
        rep_label.pack()
        
        # Reset button
        self.reset_button = tk.Button(self.results_container, text="Start New Workout", 
                                     bg="#333333", fg="white",
                                     activebackground="#4CAF50", activeforeground="white",
                                     font=("Arial Bbold", 10), bd=0, padx=15, pady=5,
                                     command=self.reset_tracking)
        self.reset_button.pack(pady=20)
    
    def apply_shadow(self, widget):
        """Apply a shadow effect to a widget"""
        border_frame = tk.Frame(self, bg="#0a0a0a", padx=2, pady=2)
        border_frame.place(relx=0.5, rely=0.5, anchor="center", 
                           relwidth=0.8+0.01, relheight=0.7+0.01)
        widget.lift()
    
    def start_tracking(self):
        """Start tracking the selected workout"""
        workout = self.workout_type.get().lower()
        
        if not workout or workout == "-- select a workout --":
            messagebox.showerror("Error", "Please select a workout type")
            return
        
        # Show loading message
        self.rep_count_display.config(text="Tracking...")
        self.results_container.pack(fill="x", pady=20)
        self.results_visible = True
        self.update()
        
        try:
            # Call appropriate tracking function based on workout type
            rep_count = 0
            if workout == "pushups":
                rep_count = track_pushups()
            elif workout == "squats":
                rep_count = track_squats()
            elif workout == "leg extension":
                rep_count = track_leg_extension()
            elif workout == "leg press":
                rep_count = track_legpress()
            elif workout == "pullups":
                rep_count = track_pullups()
            elif workout == "abs":
                rep_count = track_abs()
            
            # Update results display
            self.rep_count_display.config(text=str(rep_count))
            messagebox.showinfo("Complete", f"Workout tracking complete!\nTotal repetitions: {rep_count}")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while tracking: {str(e)}")
            self.reset_tracking()
    
    def reset_tracking(self):
        """Reset the tracking interface"""
        self.workout_type.set("-- Select a workout --")
        if self.results_visible:
            self.results_container.pack_forget()
            self.results_visible = False