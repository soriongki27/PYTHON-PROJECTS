import tkinter as tk
from tkinter import messagebox as mb

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("380x580")
        self.root.resizable(False, False)
        
        # Color scheme - Modern dark theme with blue accent
        self.bg_color = "#1e1e2e"
        self.display_bg = "#2d2d44"
        self.display_fg = "#ffffff"
        self.num_button_bg = "#3d3d5c"
        self.num_button_fg = "#ffffff"
        self.op_button_bg = "#5865f2"
        self.op_button_fg = "#ffffff"
        self.equal_button_bg = "#57f287"
        self.equal_button_fg = "#1e1e2e"
        self.clear_button_bg = "#ed4245"
        self.clear_button_fg = "#ffffff"
        
        self.root.configure(bg=self.bg_color)
        
        # Create display frame with padding
        display_frame = tk.Frame(root, bg=self.bg_color)
        display_frame.grid(row=0, column=0, columnspan=4, padx=15, pady=15, sticky="nsew")
        
        # Entry widget for showing numbers and results
        self.entry = tk.Entry(
            display_frame, 
            width=14, 
            font=('Segoe UI', 32, 'bold'), 
            borderwidth=0,
            relief="flat",
            bg=self.display_bg,
            fg=self.display_fg,
            justify='right',
            insertbackground=self.display_fg
        )
        self.entry.pack(fill='both', expand=True, ipady=20, ipadx=10)
        
        # Button configuration
        buttons = [
            ('7', 1, 0, 'num'), ('8', 1, 1, 'num'), ('9', 1, 2, 'num'), ('/', 1, 3, 'op'),
            ('4', 2, 0, 'num'), ('5', 2, 1, 'num'), ('6', 2, 2, 'num'), ('*', 2, 3, 'op'),
            ('1', 3, 0, 'num'), ('2', 3, 1, 'num'), ('3', 3, 2, 'num'), ('-', 3, 3, 'op'),
            ('0', 4, 0, 'num'), ('.', 4, 1, 'num'), ('=', 4, 2, 'equal'), ('+', 4, 3, 'op'),
        ]
        
        # Create number and operator buttons
        for (text, row, col, btn_type) in buttons:
            self.create_button(text, row, col, btn_type)
        
        # Clear button (spans full width)
        clear_btn = tk.Button(
            root, 
            text='CLEAR', 
            font=('Segoe UI', 16, 'bold'),
            bg=self.clear_button_bg,
            fg=self.clear_button_fg,
            activebackground='#c03537',
            activeforeground=self.clear_button_fg,
            borderwidth=0,
            relief="flat",
            cursor="hand2",
            command=self.button_clear
        )
        clear_btn.grid(row=5, column=0, columnspan=4, padx=15, pady=(5, 15), sticky="ew", ipady=15)
        self.add_hover_effect(clear_btn, self.clear_button_bg, '#c03537')
        
        # Configure grid weights for responsiveness
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)
    
    def create_button(self, text, row, col, btn_type):
        """Create a styled button based on its type"""
        if btn_type == 'num':
            bg = self.num_button_bg
            fg = self.num_button_fg
            hover_bg = '#4d4d6c'
            command = lambda t=text: self.button_click(t)
        elif btn_type == 'op':
            bg = self.op_button_bg
            fg = self.op_button_fg
            hover_bg = '#4752c4'
            command = lambda t=text: self.button_click(t)
        else:  # equal
            bg = self.equal_button_bg
            fg = self.equal_button_fg
            hover_bg = '#42d869'
            command = self.button_equal
        
        btn = tk.Button(
            self.root,
            text=text,
            font=('Segoe UI', 20, 'bold'),
            bg=bg,
            fg=fg,
            activebackground=hover_bg,
            activeforeground=fg,
            borderwidth=0,
            relief="flat",
            cursor="hand2",
            command=command
        )
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew", ipady=20)
        
        # Add hover effect
        self.add_hover_effect(btn, bg, hover_bg)
    
    def add_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to buttons"""
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))
    
    def button_click(self, number):
        """Handle number/operator button clicks"""
        current = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, current + str(number))
    
    def button_clear(self):
        """Clear the display"""
        self.entry.delete(0, tk.END)
    
    def button_equal(self):
        """Calculate and display result"""
        try:
            result = eval(self.entry.get())
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(result))
        except Exception as e:
            mb.showerror("Error", "Invalid Input")
            self.entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCalculator(root)
    root.mainloop()