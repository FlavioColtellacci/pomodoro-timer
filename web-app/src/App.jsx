import React, { useState, useEffect } from 'react';
import Timer from './components/Timer';
import TomatoProgress from './components/TomatoProgress';
import { ActiveTasks, FinishedTasks } from './components/Tasks';

const PHASES = {
  WORK: 'Pomodoro',
  SHORT_BREAK: 'Short break',
  LONG_BREAK: 'Long break'
};

const DURATIONS = {
  [PHASES.WORK]: 25 * 60,
  [PHASES.SHORT_BREAK]: 5 * 60,
  [PHASES.LONG_BREAK]: 15 * 60
};

function App() {
  const [activeView, setActiveView] = useState('Timer');
  const [currentPhase, setCurrentPhase] = useState(PHASES.WORK);
  const [timeLeft, setTimeLeft] = useState(DURATIONS[PHASES.WORK]);
  const [isRunning, setIsRunning] = useState(false);
  const [pomodorosCompleted, setPomodorosCompleted] = useState(0);

  // Task State
  const [tasks, setTasks] = useState([]);
  const [activeTaskId, setActiveTaskId] = useState(null);

  const handleAddTask = (name, estPoms) => {
    const newTask = {
      id: Date.now(),
      name,
      estPoms,
      completedPoms: 0,
      isFinished: false
    };
    setTasks([...tasks, newTask]);
    if (!activeTaskId) setActiveTaskId(newTask.id);
  };

  const handleFinishTask = (id) => {
    setTasks(tasks.map(t => t.id === id ? { ...t, isFinished: true } : t));
    if (activeTaskId === id) setActiveTaskId(null);
  };

  // Handle the countdown timer
  useEffect(() => {
    let interval = null;
    if (isRunning && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft((time) => time - 1);
      }, 1000);
    } else if (timeLeft === 0) {
      handlePhaseTransition();
    }
    return () => clearInterval(interval);
  }, [isRunning, timeLeft]);

  const handlePhaseTransition = () => {
    setIsRunning(false);

    if (currentPhase === PHASES.WORK) {
      const newCompleted = pomodorosCompleted + 1;
      setPomodorosCompleted(newCompleted);

      // Credit the active task
      if (activeTaskId) {
        setTasks(prevTasks => prevTasks.map(t => {
          if (t.id === activeTaskId) {
            const updatedCompleted = t.completedPoms + 1;
            // Auto finish if they hit the target (optional, we leave it manual here but increment it)
            return { ...t, completedPoms: updatedCompleted };
          }
          return t;
        }));
      }

      // Every 4th pomodoro is a long break
      if (newCompleted % 4 === 0) {
        changePhase(PHASES.LONG_BREAK);
      } else {
        changePhase(PHASES.SHORT_BREAK);
      }
    } else {
      // If we were on a break, go back to work
      changePhase(PHASES.WORK);
    }
  };

  const changePhase = (newPhase) => {
    setCurrentPhase(newPhase);
    setTimeLeft(DURATIONS[newPhase]);
    setIsRunning(false);
  };

  const toggleTimer = () => {
    setIsRunning(!isRunning);
  };

  // Calculate percentage for the snail
  const currentDuration = DURATIONS[currentPhase];
  const progressPercentage = ((currentDuration - timeLeft) / currentDuration) * 100;

  return (
    <div className="layout">
      {/* Sidebar Navigation */}
      <nav className="sidebar">
        <ul>
          <li
            className={activeView === 'Timer' ? 'active' : ''}
            onClick={() => setActiveView('Timer')}
          >Timer</li>
          <li
            className={activeView === 'Add task' ? 'active' : ''}
            onClick={() => setActiveView('Add task')}
          >Add task</li>
          <li
            className={activeView === 'Finished tasks' ? 'active' : ''}
            onClick={() => setActiveView('Finished tasks')}
          >Finished tasks</li>
        </ul>
      </nav>

      {/* Main Content Area */}
      <main className="content">
        {activeView === 'Timer' && (
          <>
            <div className="timer-container">
              <Timer
                currentPhase={currentPhase}
                timeLeft={timeLeft}
                isRunning={isRunning}
                onPhaseChange={changePhase}
                onToggleTimer={toggleTimer}
                phases={PHASES}
              />
            </div>
            <div className="progress-container">
              <TomatoProgress progressPercentage={progressPercentage} isRunning={isRunning} />
            </div>
          </>
        )}

        {/* View Placeholders */}
        {activeView === 'Add task' && (
          <ActiveTasks
            tasks={tasks}
            onAddTask={handleAddTask}
            onFinishTask={handleFinishTask}
            activeTaskId={activeTaskId}
            setActiveTaskId={setActiveTaskId}
          />
        )}

        {activeView === 'Finished tasks' && (
          <FinishedTasks tasks={tasks} />
        )}
      </main>
    </div>
  );
}

export default App;
