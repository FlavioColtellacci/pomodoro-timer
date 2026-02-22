import React from 'react';
import './TomatoProgress.css';
import TomatoImage from '../assets/tomato.png';

function TomatoProgress({ progressPercentage = 0, isRunning = false }) {
    // We cap progress at 100
    const width = Math.min(Math.max(progressPercentage, 0), 100);

    return (
        <div className="tomato-progress-wrapper">
            <div className="tomato-dialogue">
                <p>Time to be productive.</p>
                <p>Let's start! <span className="arrow-down">⤵</span></p>
            </div>

            <div className="progress-track">
                <div
                    className="progress-fill"
                    style={{ width: `${width}%` }}
                >
                    <img
                        src={TomatoImage}
                        alt="Productive Tomato"
                        className={`tomato-character ${isRunning ? 'moving' : ''}`}
                    />
                </div>
            </div>
        </div>
    );
}

export default TomatoProgress;
