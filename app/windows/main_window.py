"""Main window for the SGDK character creator."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import os
import json
from ..utils.style import apply_style
from ..core.generator import CharacterGenerator
from ..core.exporter import SGDKExporter


class CharacterCreatorWindow:
    """Main window for creating SGDK characters."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SGDK Character Creator")
        self.root.geometry("1200x800")
        
        # Apply Mega Drive theme
        apply_style(self.root)
        
        # Character generator
        self.generator = CharacterGenerator()
        self.exporter = SGDKExporter()
        
        # Current character data
        self.character_data = {
            "head_type": "round",
            "body_type": "normal",
            "arm_type": "normal", 
            "leg_type": "normal",
            "head_color": "#FFDDAA",
            "body_color": "#0066CC",
            "arm_color": "#FFDDAA",
            "leg_color": "#0066CC",
            "size": 32,
            "animation_frames": 4
        }
        
        self.setup_ui()
        self.update_preview()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Controls
        control_frame = ttk.LabelFrame(main_frame, text="Character Editor", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Right panel - Preview
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding=10)
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.setup_controls(control_frame)
        self.setup_preview(preview_frame)
    
    def setup_controls(self, parent):
        """Set up the control panel."""
        # Body parts section
        parts_frame = ttk.LabelFrame(parent, text="Body Parts", padding=5)
        parts_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Head type
        ttk.Label(parts_frame, text="Head Type:").pack(anchor=tk.W)
        head_frame = ttk.Frame(parts_frame)
        head_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.head_var = tk.StringVar(value=self.character_data["head_type"])
        for head_type in ["round", "square", "oval", "triangle"]:
            ttk.Radiobutton(head_frame, text=head_type.title(), 
                          variable=self.head_var, value=head_type,
                          command=self.on_part_change).pack(side=tk.LEFT, padx=(0, 10))
        
        # Body type
        ttk.Label(parts_frame, text="Body Type:").pack(anchor=tk.W)
        body_frame = ttk.Frame(parts_frame)
        body_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.body_var = tk.StringVar(value=self.character_data["body_type"])
        for body_type in ["normal", "muscular", "slim", "round"]:
            ttk.Radiobutton(body_frame, text=body_type.title(),
                          variable=self.body_var, value=body_type,
                          command=self.on_part_change).pack(side=tk.LEFT, padx=(0, 10))
        
        # Arm type
        ttk.Label(parts_frame, text="Arm Type:").pack(anchor=tk.W)
        arm_frame = ttk.Frame(parts_frame)
        arm_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.arm_var = tk.StringVar(value=self.character_data["arm_type"])
        for arm_type in ["normal", "muscular", "thin", "long"]:
            ttk.Radiobutton(arm_frame, text=arm_type.title(),
                          variable=self.arm_var, value=arm_type,
                          command=self.on_part_change).pack(side=tk.LEFT, padx=(0, 10))
        
        # Leg type
        ttk.Label(parts_frame, text="Leg Type:").pack(anchor=tk.W)
        leg_frame = ttk.Frame(parts_frame)
        leg_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.leg_var = tk.StringVar(value=self.character_data["leg_type"])
        for leg_type in ["normal", "muscular", "thin", "long"]:
            ttk.Radiobutton(leg_frame, text=leg_type.title(),
                          variable=self.leg_var, value=leg_type,
                          command=self.on_part_change).pack(side=tk.LEFT, padx=(0, 10))
        
        # Colors section
        colors_frame = ttk.LabelFrame(parent, text="Colors", padding=5)
        colors_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.setup_color_controls(colors_frame)
        
        # Size section
        size_frame = ttk.LabelFrame(parent, text="Size & Animation", padding=5)
        size_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(size_frame, text="Sprite Size:").pack(anchor=tk.W)
        self.size_var = tk.IntVar(value=self.character_data["size"])
        size_scale = ttk.Scale(size_frame, from_=16, to=64, variable=self.size_var,
                              orient=tk.HORIZONTAL, command=self.on_size_change)
        size_scale.pack(fill=tk.X, pady=(0, 5))
        
        self.size_label = ttk.Label(size_frame, text=f"Size: {self.character_data['size']}px")
        self.size_label.pack(anchor=tk.W)
        
        ttk.Label(size_frame, text="Animation Frames:").pack(anchor=tk.W, pady=(10, 0))
        self.frames_var = tk.IntVar(value=self.character_data["animation_frames"])
        frames_scale = ttk.Scale(size_frame, from_=1, to=8, variable=self.frames_var,
                               orient=tk.HORIZONTAL, command=self.on_frames_change)
        frames_scale.pack(fill=tk.X, pady=(0, 5))
        
        self.frames_label = ttk.Label(size_frame, text=f"Frames: {self.character_data['animation_frames']}")
        self.frames_label.pack(anchor=tk.W)
        
        # Action buttons
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(action_frame, text="Random Character", 
                  command=self.generate_random).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(action_frame, text="Save Character", 
                  command=self.save_character).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(action_frame, text="Load Character", 
                  command=self.load_character).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(action_frame, text="Export to SGDK", 
                  command=self.export_sgdk).pack(fill=tk.X, pady=(0, 5))
    
    def setup_color_controls(self, parent):
        """Set up color selection controls."""
        color_parts = [
            ("Head Color", "head_color"),
            ("Body Color", "body_color"), 
            ("Arm Color", "arm_color"),
            ("Leg Color", "leg_color")
        ]
        
        self.color_vars = {}
        self.color_buttons = {}
        
        for label, key in color_parts:
            frame = ttk.Frame(parent)
            frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(frame, text=label + ":").pack(side=tk.LEFT)
            
            self.color_vars[key] = tk.StringVar(value=self.character_data[key])
            color_button = tk.Button(frame, text="  ", width=3,
                                   bg=self.character_data[key],
                                   command=lambda k=key: self.choose_color(k))
            color_button.pack(side=tk.RIGHT)
            self.color_buttons[key] = color_button
    
    def setup_preview(self, parent):
        """Set up the preview panel."""
        # Preview canvas
        self.canvas = tk.Canvas(parent, width=400, height=400, bg="#222222")
        self.canvas.pack(pady=10)
        
        # Animation controls
        anim_frame = ttk.Frame(parent)
        anim_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.play_var = tk.BooleanVar()
        ttk.Checkbutton(anim_frame, text="Play Animation", 
                       variable=self.play_var, command=self.toggle_animation).pack(side=tk.LEFT)
        
        self.frame_label = ttk.Label(anim_frame, text="Frame: 1/1")
        self.frame_label.pack(side=tk.RIGHT)
        
        # Animation state
        self.current_frame = 0
        self.animation_job = None
    
    def on_part_change(self):
        """Handle body part selection changes."""
        self.character_data["head_type"] = self.head_var.get()
        self.character_data["body_type"] = self.body_var.get()
        self.character_data["arm_type"] = self.arm_var.get()
        self.character_data["leg_type"] = self.leg_var.get()
        self.update_preview()
    
    def on_size_change(self, value):
        """Handle size slider changes."""
        size = int(float(value))
        self.character_data["size"] = size
        self.size_label.config(text=f"Size: {size}px")
        self.update_preview()
    
    def on_frames_change(self, value):
        """Handle animation frames slider changes."""
        frames = int(float(value))
        self.character_data["animation_frames"] = frames
        self.frames_label.config(text=f"Frames: {frames}")
        self.update_preview()
    
    def choose_color(self, color_key):
        """Open color chooser dialog."""
        from tkinter import colorchooser
        color = colorchooser.askcolor(initialcolor=self.character_data[color_key])
        if color[1]:  # If user didn't cancel
            self.character_data[color_key] = color[1]
            self.color_vars[color_key].set(color[1])
            self.color_buttons[color_key].config(bg=color[1])
            self.update_preview()
    
    def update_preview(self):
        """Update the character preview."""
        # Generate character sprite
        sprite = self.generator.generate_character(self.character_data, self.current_frame)
        
        # Convert to PhotoImage for display
        sprite_resized = sprite.resize((200, 200), Image.NEAREST)
        self.photo = ImageTk.PhotoImage(sprite_resized)
        
        # Clear canvas and draw sprite
        self.canvas.delete("all")
        self.canvas.create_image(200, 200, image=self.photo)
        
        # Update frame label
        total_frames = self.character_data["animation_frames"]
        self.frame_label.config(text=f"Frame: {self.current_frame + 1}/{total_frames}")
    
    def toggle_animation(self):
        """Toggle animation playback."""
        if self.play_var.get():
            self.start_animation()
        else:
            self.stop_animation()
    
    def start_animation(self):
        """Start animation playback."""
        if self.animation_job:
            self.root.after_cancel(self.animation_job)
        self.animate_frame()
    
    def stop_animation(self):
        """Stop animation playback."""
        if self.animation_job:
            self.root.after_cancel(self.animation_job)
            self.animation_job = None
    
    def animate_frame(self):
        """Animate to next frame."""
        if self.play_var.get():
            self.current_frame = (self.current_frame + 1) % self.character_data["animation_frames"]
            self.update_preview()
            self.animation_job = self.root.after(200, self.animate_frame)
    
    def generate_random(self):
        """Generate a random character."""
        import random
        
        head_types = ["round", "square", "oval", "triangle"]
        body_types = ["normal", "muscular", "slim", "round"]
        arm_types = ["normal", "muscular", "thin", "long"]
        leg_types = ["normal", "muscular", "thin", "long"]
        
        colors = ["#FFDDAA", "#DDAA88", "#AA8866", "#886644", "#664422",
                 "#FF6666", "#66FF66", "#6666FF", "#FFFF66", "#FF66FF", "#66FFFF"]
        
        self.character_data.update({
            "head_type": random.choice(head_types),
            "body_type": random.choice(body_types),
            "arm_type": random.choice(arm_types),
            "leg_type": random.choice(leg_types),
            "head_color": random.choice(colors),
            "body_color": random.choice(colors),
            "arm_color": random.choice(colors),
            "leg_color": random.choice(colors),
            "size": random.randint(24, 48),
            "animation_frames": random.randint(2, 6)
        })
        
        # Update UI controls
        self.head_var.set(self.character_data["head_type"])
        self.body_var.set(self.character_data["body_type"])
        self.arm_var.set(self.character_data["arm_type"])
        self.leg_var.set(self.character_data["leg_type"])
        self.size_var.set(self.character_data["size"])
        self.frames_var.set(self.character_data["animation_frames"])
        
        # Update color buttons
        for key, button in self.color_buttons.items():
            button.config(bg=self.character_data[key])
            self.color_vars[key].set(self.character_data[key])
        
        self.update_preview()
    
    def save_character(self):
        """Save character to file."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.character_data, f, indent=2)
                messagebox.showinfo("Success", "Character saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save character: {e}")
    
    def load_character(self):
        """Load character from file."""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    self.character_data = json.load(f)
                
                # Update UI controls
                self.head_var.set(self.character_data["head_type"])
                self.body_var.set(self.character_data["body_type"])
                self.arm_var.set(self.character_data["arm_type"])
                self.leg_var.set(self.character_data["leg_type"])
                self.size_var.set(self.character_data["size"])
                self.frames_var.set(self.character_data["animation_frames"])
                
                # Update color buttons
                for key, button in self.color_buttons.items():
                    button.config(bg=self.character_data[key])
                    self.color_vars[key].set(self.character_data[key])
                
                self.update_preview()
                messagebox.showinfo("Success", "Character loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load character: {e}")
    
    def export_sgdk(self):
        """Export character to SGDK format."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".c",
            filetypes=[("C files", "*.c"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.exporter.export_character(self.character_data, filename)
                messagebox.showinfo("Success", "Character exported to SGDK format!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export character: {e}")
    
    def run(self):
        """Run the application."""
        self.root.mainloop()


def launch():
    """Launch the main application window."""
    app = CharacterCreatorWindow()
    app.run()

