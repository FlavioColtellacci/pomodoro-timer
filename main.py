import tkinter as tk
from tkinter import messagebox
import time
import random


class Pomodoro:
    DEFAULT_TIME_MS = 15 * 60 * 1000  # 15 minutes in milliseconds

    def __init__(self, root):
        """Initialize the Pomodoro Timer."""
        self.root = root
        self.root.title("Pomodoro Timer 🍅")
        self.root.geometry("400x250")
        self.running = False
        self.remaining_time_ms = self.DEFAULT_TIME_MS

        # UI Components
        self.setup_ui()

        # Background Colors
        self.colors = ["#2E8B57", "#6B8E23", "#556B2F", "#4682B4", "#5F9EA0", "#8FBC8F", "#708090"]
        self.update_background_color()

    def setup_ui(self):
        """Set up the UI components."""
        self.frame = tk.Frame(self.root, width=400, height=250)
        self.frame.pack(fill="both", expand=True)

        self.timer_label = tk.Label(self.frame, text="25:00.000", font=("Arial", 30))
        self.timer_label.pack(pady=20)

        self.start_button = tk.Button(self.frame, text="Start 🍎", command=self.start_timer, width=10)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.frame, text="Stop 🛑", command=self.stop_timer, width=10)
        self.stop_button.pack(pady=5)

        self.reset_button = tk.Button(self.frame, text="Reset 🍏", command=self.reset_timer, width=10)
        self.reset_button.pack(pady=5)

        self.quit_button = tk.Button(self.frame, text="Quit ❌", command=self.quit_application, width=10)
        self.quit_button.pack(pady=5)


        self.status_label = tk.Label(self.frame, text="Ready to grow apples!", font=("Arial", 12), fg="green")
        self.status_label.pack(pady=10)

    def update_background_color(self):
        """Update the background color at regular intervals."""
        random_color = random.choice(self.colors)
        self.frame.config(bg=random_color)
        self.root.after(5000, self.update_background_color)

    def start_timer(self):
        """Start the Pomodoro timer."""
        if not self.running:
            self.running = True
            self.status_label.config(text="Apples are growing... 🍎", fg="blue")
            self.run_timer()

    def stop_timer(self):
        """Stop the Pomodoro timer."""
        if self.running:
            self.running = False
            self.status_label.config(text="Apple growth paused! 🍏", fg="orange")

    def reset_timer(self):
        """Reset the Pomodoro timer."""
        self.running = False
        self.remaining_time_ms = self.DEFAULT_TIME_MS
        self.update_timer_display(self.remaining_time_ms)
        self.status_label.config(text="Apple tree reset! 🌳", fg="green")

    def run_timer(self):
        """Run the timer logic using tkinter's after method."""
        if self.running and self.remaining_time_ms > 0:
            self.remaining_time_ms -= 10  # Decrease by 10ms
            self.update_timer_display(self.remaining_time_ms)
            self.root.after(10, self.run_timer)  # Schedule next update
        elif self.remaining_time_ms <= 0:
            self.running = False
            self.update_timer_display(0)
            self.status_label.config(text="Apples are ready to harvest! 🍎", fg="red")
            messagebox.showinfo("Pomodoro Timer", "Time's up! Take a break or start a new session.")

    def update_timer_display(self, milliseconds):
        """Update the timer label with the current time."""
        if milliseconds <= 0:
            milliseconds = 0
        minutes = milliseconds // 60000
        seconds = (milliseconds % 60000) // 1000
        millis = milliseconds % 1000
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}.{millis:03d}")

    def quit_application(self):
        """Quit the application gracefully."""
        self.root.destroy()


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = Pomodoro(root)
    root.mainloop()