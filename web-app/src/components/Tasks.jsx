import React, { useState } from 'react';
import './Tasks.css';

export function ActiveTasks({ tasks, onAddTask, onFinishTask, activeTaskId, setActiveTaskId }) {
    const [newTaskName, setNewTaskName] = useState('');
    const [estPoms, setEstPoms] = useState(1);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!newTaskName.trim()) return;
        onAddTask(newTaskName, estPoms);
        setNewTaskName('');
        setEstPoms(1);
    };

    const activeList = tasks.filter(t => !t.isFinished);

    return (
        <div className="task-view-container">
            <h2>Add a New Task</h2>
            <form className="add-task-form" onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Task description..."
                    value={newTaskName}
                    onChange={(e) => setNewTaskName(e.target.value)}
                    required
                />
                <div className="est-input">
                    <label>Est. Pomodoros:</label>
                    <input
                        type="number"
                        min="1"
                        max="10"
                        value={estPoms}
                        onChange={(e) => setEstPoms(parseInt(e.target.value))}
                    />
                </div>
                <button type="submit" className="add-btn">Add Task</button>
            </form>

            <h2 style={{ marginTop: '40px' }}>Up Next</h2>
            {activeList.length === 0 ? (
                <p className="empty-state">No tasks available. Add some to get started!</p>
            ) : (
                <ul className="task-list">
                    {activeList.map(task => (
                        <li
                            key={task.id}
                            className={`task-item ${task.id === activeTaskId ? 'selected' : ''}`}
                        >
                            <div
                                className="task-info"
                                onClick={() => setActiveTaskId(task.id)}
                            >
                                <span className="task-name">{task.name}</span>
                                <span className="task-progress">
                                    {task.completedPoms} / {task.estPoms} 🍅
                                </span>
                            </div>
                            <button
                                className="finish-btn"
                                onClick={() => onFinishTask(task.id)}
                            >
                                Done
                            </button>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export function FinishedTasks({ tasks }) {
    const finishedList = tasks.filter(t => t.isFinished);

    return (
        <div className="task-view-container">
            <h2>Finished Tasks</h2>
            {finishedList.length === 0 ? (
                <p className="empty-state">Nothing finished yet. Get to work!</p>
            ) : (
                <ul className="task-list finished-list">
                    {finishedList.map(task => (
                        <li key={task.id} className="task-item finished">
                            <span className="task-name"><s>{task.name}</s></span>
                            <span className="task-progress muted">
                                {task.completedPoms} 🍅
                            </span>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}
