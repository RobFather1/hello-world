import tkinter as tk
from datetime import datetime
import json
import os

# Target: March 31st 2031 (local time), if you want a specific time, set hour/minute/second.
TARGET = datetime(2031, 3, 31, 0, 0, 0)
# Config file for persistence
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".retirement_countdown_config.json")

class CountdownWidget(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Giganti's Retirement Countdown")
        self.overrideredirect(True)  # borderless
        self.attributes("-topmost", True)

        # Dark mode state (load from config)
        self.is_dark_mode = self._load_preferences()

        # Color schemes
        self.light_theme = {
            'bg': '#93C5FD',
            'frame_bg': '#19B0A8',
            'title_fg': '#A7F3D0',
            'time_fg': '#FBBF24',
            'sub_fg': '#93C5FD',
            'button_bg': '#0C7489',
            'button_fg': '#E0F2FE'
        }

        self.dark_theme = {
            'bg': '#1E2939',
            'frame_bg': '#0F172A',
            'title_fg': '#94A3B8',
            'time_fg': '#F59E0B',
            'sub_fg': '#64748B',
            'button_bg': '#334155',
            'button_fg': '#CBD5E1'
        }

        # Apply saved theme
        theme = self.dark_theme if self.is_dark_mode else self.light_theme
        self.configure(bg=theme['bg'])

        # Starting position (x, y)
        self.geometry("520x190+40+40")

        # Allow dragging the widget
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.do_move)

        # Right-click menu (close)
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Exit", command=self.destroy)
        self.bind("<Button-3>", self.show_menu)

        # Keyboard shortcut for dark mode
        self.bind("<KeyPress-d>", lambda e: self.toggle_dark_mode())
        self.bind("<KeyPress-D>", lambda e: self.toggle_dark_mode())

        # Main container
        self.frame = tk.Frame(self, bg=theme['frame_bg'], padx=14, pady=12)
        self.frame.pack(fill="both", expand=True)

        # Header label
        self.title_label = tk.Label(
            self.frame,
            text="Giganti's Retirement Countdown",
            fg=theme['title_fg'],
            bg=theme['frame_bg'],
            font=("Segoe UI", 14, "bold"),
        )
        self.title_label.pack(anchor="w")

        # Big countdown (days + HH:MM:SS)
        self.time_label = tk.Label(
            self.frame,
            text="--d --:--:--",
            fg=theme['time_fg'],
            bg=theme['frame_bg'],
            font=("Consolas", 34, "bold"),
        )
        self.time_label.pack(anchor="w", pady=(6, 0))

        # Small status
        self.sub_label = tk.Label(
            self.frame,
            text="(Right-click to exit | Press 'D' for dark mode)",
            fg=theme['sub_fg'],
            bg=theme['frame_bg'],
            font=("Segoe UI", 10),
        )
        self.sub_label.pack(anchor="w", pady=(6, 0))

        # Dark mode toggle button
        button_text = "🌙 Light Mode" if self.is_dark_mode else "💡 Dark Mode"
        self.dark_mode_btn = tk.Button(
            self.frame,
            text=button_text,
            command=self.toggle_dark_mode,
            bg=theme['button_bg'],
            fg=theme['button_fg'],
            font=("Segoe UI", 9),
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=4
        )
        self.dark_mode_btn.pack(anchor="w", pady=(8, 0))

        self.update_countdown()

    def toggle_dark_mode(self):
        """Toggle between light and dark mode"""
        self.is_dark_mode = not self.is_dark_mode
        theme = self.dark_theme if self.is_dark_mode else self.light_theme

        # Update window background
        self.configure(bg=theme['bg'])

        # Update frame
        self.frame.configure(bg=theme['frame_bg'])

        # Update labels
        self.title_label.config(fg=theme['title_fg'], bg=theme['frame_bg'])
        self.time_label.config(fg=theme['time_fg'], bg=theme['frame_bg'])
        self.sub_label.config(fg=theme['sub_fg'], bg=theme['frame_bg'])

        # Update button
        button_text = "🌙 Light Mode" if self.is_dark_mode else "💡 Dark Mode"
        self.dark_mode_btn.config(
            text=button_text,
            bg=theme['button_bg'],
            fg=theme['button_fg']
        )

        # Save preference
        self._save_preferences()

        self.update_countdown()

    def start_move(self, event):
        self._x = event.x
        self._y = event.y

    def do_move(self, event):
        x = self.winfo_pointerx() - self._x
        y = self.winfo_pointery() - self._y
        self.geometry(f"+{x}+{y}")

    def show_menu(self, event):
        self.menu.tk_popup(event.x_root, event.y_root)

    def _load_preferences(self):
        """Load dark mode preference from config file"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    return config.get('dark_mode', False)
        except Exception:
            pass
        return False

    def _save_preferences(self):
        """Save dark mode preference to config file"""
        try:
            config = {'dark_mode': self.is_dark_mode}
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f)
        except Exception:
            pass

    def update_countdown(self):
        now = datetime.now()
        delta = TARGET - now

        if delta.total_seconds() <= 0:
            self.time_label.config(text="🎊 00:00:00", fg="#340399")  # green
            self.sub_label.config(text="Congratulations!")
        else:
            total_seconds = int(delta.total_seconds())

            days = total_seconds // 86400
            remainder = total_seconds % 86400
            hours = remainder // 3600
            minutes = (remainder % 3600) // 60
            seconds = remainder % 60

            self.time_label.config(text=f"{days}d Days {hours:02d}:{minutes:02d}:{seconds:02d}")

        self.after(250, self.update_countdown)

if __name__ == "__main__":
    app = CountdownWidget()
    app.mainloop()