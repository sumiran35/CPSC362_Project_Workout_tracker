import tkinter as tk
from tkinter import ttk, messagebox

class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#121212")
        self.controller = controller
        
        # Database Implementation
        self.users = {"user1": "password1"}
        
        # Create the login container
        self.create_login_container()
    
    def create_login_container(self):
        """Create the login form container"""
        # Main container
        login_container = tk.Frame(self, bg="#1E1E1E", padx=30, pady=30)
        login_container.place(relx=0.5, rely=0.4, anchor="center", width=400, height=500)
        
        # Create rounded corners effect with canvas
        self.create_rounded_frame(login_container)
        
        # Login header
        header = tk.Label(login_container, text="Welcome Back!", 
                          font=("Arial", 18, "bold"), bg="#1E1E1E", fg="white")
        header.pack(pady=(20, 30))
        
        # Username field
        username_frame = tk.Frame(login_container, bg="#1E1E1E")
        username_frame.pack(fill="x", pady=5)
        
        self.username_var = tk.StringVar()
        username_entry = tk.Entry(username_frame, textvariable=self.username_var,
                                 font=("Arial Bold", 12), bg="#333333", fg="white",
                                 insertbackground="white", bd=0)
        username_entry.insert(0, "Username")
        username_entry.pack(fill="x", ipady=8)
        username_entry.bind("<FocusIn>", lambda e: self.on_entry_click(e, "Username"))
        username_entry.bind("<FocusOut>", lambda e: self.on_focus_out(e, "Username"))
        
        # Password field
        password_frame = tk.Frame(login_container, bg="#1E1E1E")
        password_frame.pack(fill="x", pady=15)
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(password_frame, textvariable=self.password_var,
                                      font=("Arial Bold", 12), bg="#333333", fg="white",
                                      insertbackground="white", bd=0, show="")
        self.password_entry.insert(0, "Password")
        self.password_entry.pack(fill="x", ipady=8)
        self.password_entry.bind("<FocusIn>", lambda e: self.on_entry_click(e, "Password"))
        self.password_entry.bind("<FocusOut>", lambda e: self.on_focus_out(e, "Password"))
        self.password_entry.bind("<Return>", lambda e: self.validate_login())
        
        # Login button
        login_button = tk.Button(login_container, text="Login", bg="#4CAF50", fg="white",
                                 activebackground="#45a049", activeforeground="white",
                                 font=("Arial", 12, "bold"), bd=0, cursor="hand2",
                                 command=self.validate_login)
        login_button.pack(fill="x", pady=20, ipady=8)
        
        # Or separator
        separator_frame = tk.Frame(login_container, bg="#1E1E1E")
        separator_frame.pack(fill="x", pady=15)
        
        left_line = tk.Frame(separator_frame, bg="#333333", height=1)
        left_line.pack(side="left", fill="x", expand=True, padx=5)
        
        or_label = tk.Label(separator_frame, text="OR", bg="#1E1E1E", fg="#666666",
                           font=("Arial", 10))
        or_label.pack(side="left", padx=10)
        
        right_line = tk.Frame(separator_frame, bg="#333333", height=1)
        right_line.pack(side="left", fill="x", expand=True, padx=5)
        
        # Create Profile button
        create_profile_button = tk.Button(login_container, text="Create New Profile", 
                                        bg="#333333", fg="white",
                                        activebackground="#404040", activeforeground="white",
                                        font=("Arial", 12), bd=0, cursor="hand2",
                                        command=self.show_create_profile)
        create_profile_button.pack(fill="x", pady=10, ipady=8)
        
        # Error message label
        self.error_label = tk.Label(login_container, text="", fg="#f44336", 
                                   bg="#1E1E1E", font=("Arial", 10))
        self.error_label.pack(pady=10)
        
        # Profile creation section (initially hidden)
        self.profile_container = tk.Frame(login_container, bg="#1E1E1E")
        
        profile_header = tk.Label(self.profile_container, text="Create Profile", 
                                font=("Arial", 16, "bold"), bg="#1E1E1E", fg="white")
        profile_header.pack(pady=(0, 20))
        
        # Profile fields
        fields = [
            ("Name/Username", "name_var"),
            ("Age", "age_var"),
            ("Weight (lb)", "weight_var"),
            ("Height (ft)", "height_var"),
            ("New Password", "new_password_var")
        ]
        
        for field_name, var_name in fields:
            frame = tk.Frame(self.profile_container, bg="#1E1E1E")
            frame.pack(fill="x", pady=5)
            
            setattr(self, var_name, tk.StringVar())
            entry = tk.Entry(frame, textvariable=getattr(self, var_name),
                           font=("Arial", 12), bg="#333333", fg="white",
                           insertbackground="white", bd=0)
            entry.insert(0, field_name)
            entry.pack(fill="x", ipady=8)
            entry.bind("<FocusIn>", lambda e, text=field_name: self.on_entry_click(e, text))
            entry.bind("<FocusOut>", lambda e, text=field_name: self.on_focus_out(e, text))
            
            if "Password" in field_name:
                entry.config(show="")
                setattr(self, f"{var_name}_entry", entry)
        
        # Save Profile button
        save_profile_button = tk.Button(self.profile_container, text="Save Profile", 
                                      bg="#4CAF50", fg="white",
                                      activebackground="#45a049", activeforeground="white",
                                      font=("Arial", 12, "bold"), bd=0, cursor="hand2",
                                      command=self.save_profile)
        save_profile_button.pack(fill="x", pady=20, ipady=8)
        
        # Back to Login button
        back_button = tk.Button(self.profile_container, text="Back to Login", 
                               bg="#333333", fg="white",
                               activebackground="#404040", activeforeground="white",
                               font=("Arial", 12), bd=0, cursor="hand2",
                               command=self.show_login)
        back_button.pack(fill="x", pady=(0, 10), ipady=8)
    
    def create_rounded_frame(self, container):
        """Create an effect of rounded corners for the container"""
        canvas = tk.Canvas(container, bg="#1E1E1E", highlightthickness=0)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
    def on_entry_click(self, event, default_text):
        """Handle click on entry field"""
        widget = event.widget
        if widget.get() == default_text:
            widget.delete(0, "end")
            if "Password" in default_text:
                widget.config(show="*")
    
    def on_focus_out(self, event, default_text):
        """Handle focus out from entry field"""
        widget = event.widget
        if widget.get() == "":
            widget.insert(0, default_text)
            if "Password" in default_text:
                widget.config(show="")
    
    def show_create_profile(self):
        """Switch to profile creation view"""
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if child != self.profile_container:
                        child.pack_forget()
                self.profile_container.pack(fill="both", expand=True)
    
    def show_login(self):
        """Switch back to login view"""
        self.profile_container.pack_forget()
        self.create_login_container()
        self.reset_form()
    
    def validate_login(self):
        """Validate login credentials"""
        username = self.username_var.get()
        password = self.password_var.get()
        
        # Check if credentials are valid
        if username in self.users and self.users[username] == password:
            self.error_label.config(text="")
            self.controller.login(username)
        else:
            self.error_label.config(text="Invalid username or password")
    
    def save_profile(self):
        """Save the new profile"""
        try:
            # Validate inputs
            name = self.name_var.get()
            age = self.age_var.get()
            weight = self.weight_var.get()
            height = self.height_var.get()
            password = self.new_password_var.get()
            
            # Basic validation
            if any(val in ["Name", "Age", "Weight (kg)", "Height (cm)", "New Password"] 
                   for val in [name, age, weight, height, password]):
                raise ValueError("Please fill in all fields")
            
            # Convert numeric values
            age = int(age)
            weight = float(weight)
            height = float(height)
            

            #DATABASE IMPLEMENTATION
            self.users[name] = password
            
            messagebox.showinfo("Success", "Profile created successfully!")
            self.show_login()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def reset_form(self):
        """Reset the login form"""
        self.username_var.set("Username")
        self.password_var.set("Password")
        self.password_entry.config(show="")
        self.error_label.config(text="")