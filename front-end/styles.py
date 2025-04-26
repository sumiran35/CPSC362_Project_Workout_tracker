import tkinter as tk
from tkinter import ttk

def apply_styles(style):
    """Apply custom styles to the application"""
    # Configure colors
    colors = {
        "primary": "#4CAF50",
        "primary_dark": "#45a049",
        "error": "#f44336",
        "error_dark": "#d32f2f",
        "dark_bg": "#121212",
        "card_bg": "#1E1E1E",
        "text": "white",
        "text_secondary": "#CCCCCC",
        "input_bg": "#333333"
    }
    
    # Configure styles for ttk widgets
    style.configure("TFrame", background=colors["dark_bg"])
    
    # Progressbar style
    style.configure("TProgressbar", 
                   thickness=15, 
                   background=colors["primary"],
                   troughcolor=colors["input_bg"],
                   borderwidth=0,
                   relief="flat")
    
    # Combobox style
    style.map('TCombobox', 
             fieldbackground=[('readonly', colors["input_bg"])],
             background=[('readonly', colors["input_bg"])],
             foreground=[('readonly', 'white')],
             selectbackground=[('readonly', colors["primary"])],
             selectforeground=[('readonly', 'white')])
    
    style.configure('TCombobox',
                   background=colors["input_bg"],
                   foreground='white',
                   fieldbackground=colors["input_bg"],
                   arrowcolor='white')
    
    # Scrollbar style
    style.configure("TScrollbar",
                   background=colors["input_bg"],
                   borderwidth=0,
                   arrowcolor="white",
                   troughcolor=colors["dark_bg"])
    
    # Enable dark theme for all ttk widgets
    style.theme_use('alt')  # Use 'alt' theme as base for customization
    
    return style

def create_tooltip(widget, text):
    """Create a tooltip for a widget"""
    def on_enter(event):
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        
        # Create a toplevel window
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(tooltip, text=text, background="#2A2A2A", foreground="white",
                        relief="solid", borderwidth=1, font=("Arial", "9", "normal"),
                        padx=5, pady=2)
        label.pack()
        
        # Store tooltip reference
        widget.tooltip = tooltip
        
    def on_leave(event):
        # Destroy tooltip on leave
        if hasattr(widget, "tooltip"):
            widget.tooltip.destroy()
            
    # Bind events
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)