import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image, ImageTk

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
        description = tk.Label(scrollable_frame, text="Upload your workout video for analysis:", 
                              font=("Arial", 12), bg="#1E1E1E", fg="white")
        description.pack(pady=(0, 20), anchor="w")
        
        # Workout type selection
        workout_frame = tk.Frame(scrollable_frame, bg="#1E1E1E")
        workout_frame.pack(fill="x", pady=10)
        
        workout_label = tk.Label(workout_frame, text="Select Workout Type:", 
                                font=("Arial", 11), bg="#1E1E1E", fg="white")
        workout_label.pack(side="left", padx=(0, 10))
        
        workout_options = ["", "Pushups", "Squats", "Leg Extension", "Leg Press", "Pullups", "Abs"]
        workout_menu = ttk.Combobox(workout_frame, textvariable=self.workout_type, 
                                   values=workout_options, width=20, state="readonly")
        workout_menu.set("-- Select a workout --")
        workout_menu.pack(side="left")
        
        # File upload section
        upload_frame = tk.Frame(scrollable_frame, bg="#1E1E1E", pady=20)
        upload_frame.pack(fill="x")
        
        upload_label = tk.Label(upload_frame, text="Upload your workout video (MP4 format):", 
                               font=("Arial", 11), bg="#1E1E1E", fg="white")
        upload_label.pack(anchor="w", pady=(0, 10))
        
        file_frame = tk.Frame(upload_frame, bg="#1E1E1E")
        file_frame.pack(fill="x")
        
        self.file_path_entry = tk.Entry(file_frame, textvariable=self.video_file_path, 
                                      font=("Arial", 10), bg="#333333", fg="white",
                                      width=50, readonlybackground="#333333")
        self.file_path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=5)
        self.file_path_entry.config(state="readonly")
        
        browse_button = tk.Button(file_frame, text="Browse", bg="#333333", fg="white",
                                 activebackground="#4CAF50", activeforeground="white",
                                 font=("Arial", 10), bd=0, padx=15, pady=5,
                                 command=self.browse_file)
        browse_button.pack(side="left")
        
        # Analyze button
        analyze_button = tk.Button(upload_frame, text="Analyze Workout", bg="#4CAF50", fg="white",
                                  activebackground="#45a049", activeforeground="white",
                                  font=("Arial", 11, "bold"), bd=0, padx=20, pady=8,
                                  command=self.analyze_workout)
        analyze_button.pack(pady=20)
        
        # Results container (initially hidden)
        self.results_container = tk.Frame(scrollable_frame, bg="#2A2A2A", padx=20, pady=20)
        
        # Results header
        results_header = tk.Label(self.results_container, text="Workout Analysis Results", 
                                 font=("Arial", 14, "bold"), bg="#2A2A2A", fg="white")
        results_header.pack(pady=(0, 20))
        
        # Progress bar
        progress_frame = tk.Frame(self.results_container, bg="#2A2A2A")
        progress_frame.pack(fill="x", pady=10)
        
        self.progress = ttk.Progressbar(progress_frame, orient="horizontal", length=400, 
                                       mode="determinate", value=75)
        self.progress.pack()
        
        # Stats frame
        stats_frame = tk.Frame(self.results_container, bg="#2A2A2A")
        stats_frame.pack(fill="x", pady=20)
        
        # Rep count stat
        rep_frame = tk.Frame(stats_frame, bg="#2A2A2A", padx=10, pady=10)
        rep_frame.pack(side="left", expand=True)
        
        self.rep_count = tk.Label(rep_frame, text="0", font=("Arial", 24, "bold"), 
                                 bg="#2A2A2A", fg="#4CAF50")
        self.rep_count.pack()
        
        rep_label = tk.Label(rep_frame, text="Reps Completed", font=("Arial", 10), 
                            bg="#2A2A2A", fg="white")
        rep_label.pack()
        
        # Accuracy stat
        accuracy_frame = tk.Frame(stats_frame, bg="#2A2A2A", padx=10, pady=10)
        accuracy_frame.pack(side="left", expand=True)
        
        self.accuracy = tk.Label(accuracy_frame, text="0%", font=("Arial", 24, "bold"), 
                                bg="#2A2A2A", fg="#4CAF50")
        self.accuracy.pack()
        
        accuracy_label = tk.Label(accuracy_frame, text="Form Accuracy", font=("Arial", 10), 
                                 bg="#2A2A2A", fg="white")
        accuracy_label.pack()
        
        # Calories stat
        calories_frame = tk.Frame(stats_frame, bg="#2A2A2A", padx=10, pady=10)
        calories_frame.pack(side="left", expand=True)
        
        self.calories = tk.Label(calories_frame, text="0", font=("Arial", 24, "bold"), 
                                bg="#2A2A2A", fg="#4CAF50")
        self.calories.pack()
        
        calories_label = tk.Label(calories_frame, text="Calories Burned", font=("Arial", 10), 
                                 bg="#2A2A2A", fg="white")
        calories_label.pack()
        
        # Detailed results
        self.detailed_results = tk.Text(self.results_container, height=5, width=50, 
                                      bg="#333333", fg="white", font=("Arial", 10),
                                      padx=10, pady=10, bd=0)
        self.detailed_results.pack(fill="x", pady=10)
        self.detailed_results.insert("1.0", "Detailed analysis will appear here after processing.")
        self.detailed_results.config(state="disabled")
    
    def apply_shadow(self, widget):
        """Apply a shadow effect to a widget"""
        # In Tkinter we can't directly add shadows, so we'll use a border effect
        border_frame = tk.Frame(self, bg="#0a0a0a", padx=2, pady=2)
        border_frame.place(relx=0.5, rely=0.5, anchor="center", 
                           relwidth=0.8+0.01, relheight=0.7+0.01)
        
        # Ensure the main widget is above the border
        widget.lift()
    
    def browse_file(self):
        """Open file dialog to select a video file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Video Files", "*.mp4")]
        )
        
        if file_path:
            self.video_file_path.set(file_path)
    
    def analyze_workout(self):
        """Analyze the selected workout video"""
        if not self.workout_type.get() or self.workout_type.get() == "-- Select a workout --":
            messagebox.showerror("Error", "Please select a workout type")
            return
        
        if not self.video_file_path.get():
            messagebox.showerror("Error", "Please select a video file")
            return
        
        # In a real application, this would send the video for analysis
        # For now, we'll simulate the analysis with mock results
        
        # Show the results container if it's not already visible
        if not self.results_visible:
            self.results_container.pack(fill="x", pady=20)
            self.results_visible = True
        
        # Update the results with mock data
        workout_type = self.workout_type.get()
        
        # Set mock values based on workout type
        if workout_type == "Pushups":
            reps = "12"
            accuracy = "85%"
            cals = "45"
            details = "Good form detected. Keep your back straight during pushups for better results."
        elif workout_type == "Squats":
            reps = "15"
            accuracy = "92%"
            cals = "60"
            details = "Excellent squat depth. Try to maintain consistent tempo between repetitions."
        else:
            reps = "8"
            accuracy = "78%"
            cals = "35"
            details = f"Analysis complete for {workout_type}. Form is generally good but could use some improvements."
        
        # Update UI elements with the results
        self.rep_count.config(text=reps)
        self.accuracy.config(text=accuracy)
        self.calories.config(text=cals)
        
        self.detailed_results.config(state="normal")
        self.detailed_results.delete("1.0", "end")
        self.detailed_results.insert("1.0", details)
        self.detailed_results.config(state="disabled")
        
        # Set progress bar value
        accuracy_val = int(accuracy.strip('%'))
        self.progress.config(value=accuracy_val)
        
        messagebox.showinfo("Analysis Complete", f"Workout analysis for {workout_type} is complete!")