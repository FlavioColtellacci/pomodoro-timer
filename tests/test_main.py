import pytest
from unittest.mock import MagicMock, patch
import tkinter as tk
from main import Pomodoro

@pytest.fixture
def mock_root():
    root = MagicMock(spec=tk.Tk)
    return root

@pytest.fixture
def pomodoro(mock_root):
    # Prevent setup_ui from creating real Tkinter widgets which need a real Tk instance
    with patch("tkinter.Frame"), patch("tkinter.Label"), patch("tkinter.Button"), \
         patch("tkinter.Entry"), patch("tkinter.StringVar"):
        app = Pomodoro(mock_root)
        return app

def test_initial_state(pomodoro):
    assert pomodoro.current_phase == Pomodoro.WORK
    assert pomodoro.pomodoros_completed == 0
    assert pomodoro.running is False
    assert pomodoro.durations[Pomodoro.WORK] == 25.0

def test_start_timer(pomodoro):
    pomodoro.start_timer()
    assert pomodoro.running is True
    assert pomodoro.status_label.config.called

def test_stop_timer(pomodoro):
    pomodoro.start_timer()
    pomodoro.stop_timer()
    assert pomodoro.running is False

def test_reset_timer(pomodoro):
    pomodoro.current_phase = Pomodoro.SHORT_BREAK
    pomodoro.pomodoros_completed = 2
    pomodoro.reset_timer()
    assert pomodoro.current_phase == Pomodoro.WORK
    assert pomodoro.pomodoros_completed == 0
    assert pomodoro.running is False

def test_phase_transition_work_to_short_break(pomodoro):
    pomodoro.current_phase = Pomodoro.WORK
    pomodoro.pomodoros_completed = 0
    
    with patch("tkinter.messagebox.showinfo") as mock_info:
        pomodoro.handle_phase_transition()
        
    assert pomodoro.pomodoros_completed == 1
    assert pomodoro.current_phase == Pomodoro.SHORT_BREAK

def test_phase_transition_short_break_to_work(pomodoro):
    pomodoro.current_phase = Pomodoro.SHORT_BREAK
    
    with patch("tkinter.messagebox.showinfo") as mock_info:
        pomodoro.handle_phase_transition()
        
    assert pomodoro.current_phase == Pomodoro.WORK

def test_phase_transition_work_to_long_break(pomodoro):
    pomodoro.current_phase = Pomodoro.WORK
    pomodoro.pomodoros_completed = 3  # Next completion will be 4
    
    with patch("tkinter.messagebox.showinfo") as mock_info:
        pomodoro.handle_phase_transition()
        
    assert pomodoro.pomodoros_completed == 4
    assert pomodoro.current_phase == Pomodoro.LONG_BREAK

def test_save_settings_valid(pomodoro):
    pomodoro.work_var = MagicMock()
    pomodoro.short_var = MagicMock()
    pomodoro.long_var = MagicMock()
    pomodoro.work_var.get.return_value = "30"
    pomodoro.short_var.get.return_value = "10"
    pomodoro.long_var.get.return_value = "20"
    
    with patch("tkinter.messagebox.showinfo"):
        pomodoro.save_settings()
        
    assert pomodoro.durations[Pomodoro.WORK] == 30.0
    assert pomodoro.durations[Pomodoro.SHORT_BREAK] == 10.0
    assert pomodoro.durations[Pomodoro.LONG_BREAK] == 20.0

def test_save_settings_invalid(pomodoro):
    pomodoro.work_var = MagicMock()
    pomodoro.work_var.get.return_value = "-5"
    
    with patch("tkinter.messagebox.showerror") as mock_error:
        pomodoro.save_settings()
        mock_error.assert_called()
    
    # Should not have changed
    assert pomodoro.durations[Pomodoro.WORK] == 25.0
