import tkinter as tk
from tkinter import messagebox
import time
import random


class Pomodoro:
    WORK = "WORK"
    SHORT_BREAK = "SHORT_BREAK"
    LONG_BREAK = "LONG_BREAK"

    def __init__(self, root):
        """Initialize the Pomodoro Timer."""
        self.root = root
        self.root.title("Pomodoro Timer 🍅")
        self.root.geometry("450x450")
        self.running = False
        
        # Default Durations in minutes
        self.durations = {
            self.WORK: 25.0,
            self.SHORT_BREAK: 5.0,
            self.LONG_BREAK: 15.0
        }

        self.current_phase = self.WORK
        self.pomodoros_completed = 0
        self.remaining_time_ms = int(self.durations[self.WORK] * 60 * 1000)
        self.timer_job = None

        # UI Components
        self.setup_ui()

        # Background Colors
        self.colors = ["#2E8B57", "#6B8E23", "#556B2F", "#4682B4", "#5F9EA0", "#8FBC8F", "#708090"]
        self.background_job = None
        self.update_background_color()

    def setup_ui(self):
        """Set up the UI components."""
        self.frame = tk.Frame(self.root, width=450, height=450)
        self.frame.pack(fill="both", expand=True)

        # Settings Options
        settings_frame = tk.Frame(self.frame)
        settings_frame.pack(pady=10)

        tk.Label(settings_frame, text="Work (m):").grid(row=0, column=0, padx=5)
        self.work_var = tk.StringVar(value=str(self.durations[self.WORK]))
        tk.Entry(settings_frame, textvariable=self.work_var, width=5).grid(row=0, column=1)

        tk.Label(settings_frame, text="Short Brk:").grid(row=0, column=2, padx=5)
        self.short_var = tk.StringVar(value=str(self.durations[self.SHORT_BREAK]))
        tk.Entry(settings_frame, textvariable=self.short_var, width=5).grid(row=0, column=3)

        tk.Label(settings_frame, text="Long Brk:").grid(row=0, column=4, padx=5)
        self.long_var = tk.StringVar(value=str(self.durations[self.LONG_BREAK]))
        tk.Entry(settings_frame, textvariable=self.long_var, width=5).grid(row=0, column=5)

        tk.Button(settings_frame, text="Save Settings", command=self.save_settings).grid(row=1, column=0, columnspan=6, pady=5)

        self.timer_label = tk.Label(self.frame, text="", font=("Arial", 30))
        self.update_timer_display(self.remaining_time_ms)
        self.timer_label.pack(pady=20)

        self.start_button = tk.Button(self.frame, text="Start 🍎", command=self.start_timer, width=10)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.frame, text="Stop 🛑", command=self.stop_timer, width=10)
        self.stop_button.pack(pady=5)

        self.reset_button = tk.Button(self.frame, text="Reset 🍏", command=self.reset_timer, width=10)
        self.reset_button.pack(pady=5)

        self.quit_button = tk.Button(self.frame, text="Quit ❌", command=self.quit_application, width=10)
        self.quit_button.pack(pady=5)

        self.status_label = tk.Label(self.frame, text="Ready to grow apples! (WORK)", font=("Arial", 12), fg="green")
        self.status_label.pack(pady=10)

        self.progress_label = tk.Label(self.frame, text="Pomodoros Completed: 0", font=("Arial", 12), fg="blue")
        self.progress_label.pack(pady=5)

    def save_settings(self):
        try:
            w = float(self.work_var.get())
            s = float(self.short_var.get())
            l = float(self.long_var.get())
            if w <= 0 or s <= 0 or l <= 0:
                raise ValueError("Must be positive")
            self.durations[self.WORK] = w
            self.durations[self.SHORT_BREAK] = s
            self.durations[self.LONG_BREAK] = l
            
            if not self.running:
                self.remaining_time_ms = int(self.durations[self.current_phase] * 60 * 1000)
                self.update_timer_display(self.remaining_time_ms)
            
            messagebox.showinfo("Settings", "Durations saved successfully!")
        except Exception:
            messagebox.showerror("Error", "Please enter valid positive numbers for durations.")

    def update_background_color(self):
        """Update the background color at regular intervals."""
        random_color = random.choice(self.colors)
        self.frame.config(bg=random_color)
        self.background_job = self.root.after(5000, self.update_background_color)

    def start_timer(self):
        """Start the Pomodoro timer."""
        if not self.running:
            self.running = True
            self.status_label.config(text=f"Timer running... ({self.current_phase})", fg="blue")
            self.run_timer()

    def stop_timer(self):
        """Stop the Pomodoro timer."""
        if self.running:
            self.running = False
            self.status_label.config(text=f"Timer paused! ({self.current_phase})", fg="orange")
            if self.timer_job:
                self.root.after_cancel(self.timer_job)
                self.timer_job = None

    def reset_timer(self):
        """Reset the Pomodoro timer."""
        self.stop_timer()
        self.current_phase = self.WORK
        self.pomodoros_completed = 0
        self.remaining_time_ms = int(self.durations[self.WORK] * 60 * 1000)
        self.update_timer_display(self.remaining_time_ms)
        self.status_label.config(text="Apple tree reset! (WORK)", fg="green")
        self.progress_label.config(text="Pomodoros Completed: 0")

    def run_timer(self):
        """Run the timer logic using tkinter's after method."""
        if self.running and self.remaining_time_ms > 0:
            self.remaining_time_ms -= 10  # Decrease by 10ms
            self.update_timer_display(self.remaining_time_ms)
            self.timer_job = self.root.after(10, self.run_timer)  # Schedule next update
        elif self.remaining_time_ms <= 0:
             self.running = False
             self.update_timer_display(0)
             self.handle_phase_transition()

    def handle_phase_transition(self):
        """Handle the transition logic between pomodoro phases."""
        if self.current_phase == self.WORK:
            self.pomodoros_completed += 1
            self.progress_label.config(text=f"Pomodoros Completed: {self.pomodoros_completed}")
            
            if self.pomodoros_completed % 4 == 0:
                self.current_phase = self.LONG_BREAK
                messagebox.showinfo("Pomodoro Timer", "Work session complete! Take a long break.")
            else:
                self.current_phase = self.SHORT_BREAK
                messagebox.showinfo("Pomodoro Timer", "Work session complete! Take a short break.")
        else:
            self.current_phase = self.WORK
            messagebox.showinfo("Pomodoro Timer", "Break over! Back to work.")
            
        self.remaining_time_ms = int(self.durations[self.current_phase] * 60 * 1000)
        self.update_timer_display(self.remaining_time_ms)
        self.status_label.config(text=f"Ready to start ({self.current_phase})", fg="green")

    def update_timer_display(self, milliseconds):
        """Update the timer label with the current time."""
        if milliseconds <= 0:
            milliseconds = 0
        minutes = int(milliseconds // 60000)
        seconds = int((milliseconds % 60000) // 1000)
        millis = int(milliseconds % 1000)
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}.{millis:03d}")

    def quit_application(self):
        """Quit the application gracefully."""
        self.stop_timer()
        if self.background_job:
            self.root.after_cancel(self.background_job)
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        self.root.destroy()


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = Pomodoro(root)
    root.mainloop()