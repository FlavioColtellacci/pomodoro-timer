import React from 'react';
import './Timer.css';

function Timer({ currentPhase, timeLeft, isRunning, onPhaseChange, onToggleTimer, phases }) {
    // Format seconds to MM:SS
    const formatTime = (seconds) => {
        const m = Math.floor(seconds / 60).toString().padStart(2, '0');
        const s = (seconds % 60).toString().padStart(2, '0');
        return `${m}:${s}`;
    };

    return (
        <div className="timer-card">
            <div className="phase-selectors">
                <button
                    className={`phase-btn ${currentPhase === phases.WORK ? 'active' : ''}`}
                    onClick={() => onPhaseChange(phases.WORK)}
                >
                    {phases.WORK}
                </button>
                <button
                    className={`phase-btn ${currentPhase === phases.SHORT_BREAK ? 'active' : ''}`}
                    onClick={() => onPhaseChange(phases.SHORT_BREAK)}
                >
                    {phases.SHORT_BREAK}
                </button>
                <button
                    className={`phase-btn ${currentPhase === phases.LONG_BREAK ? 'active' : ''}`}
                    onClick={() => onPhaseChange(phases.LONG_BREAK)}
                >
                    {phases.LONG_BREAK}
                </button>
            </div>

            <div className="time-display">
                {formatTime(timeLeft)}
            </div>

            <button className="start-btn" onClick={onToggleTimer}>
                {isRunning ? 'PAUSE' : 'START'}
            </button>
        </div>
    );
}

export default Timer;
