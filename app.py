"""
from fastapi import FastAPI
app=FastAPI()
@app.get("/")
def home():
    return{"message":"Hello! My Python FastAPI web application is running successful."}
"""
#fastapi webpage by the python code
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Manoj's Advanced FastAPI App", version="1.0")

# 1. Pydantic Model for incoming data validation
class TaskItem(BaseModel):
    title: str
    description: str
    priority: int = 1

# Temporary in-memory database list
fake_db: List[TaskItem] = [
    TaskItem(title="Learn FastAPI", description="Master routes, Pydantic, and HTML responses", priority=5),
    TaskItem(title="Build Portfolio", description="Create an AI analytics platform", priority=4)
]

# 2. HTML Frontend Route served right at the root
@app.get("/", response_class=HTMLResponse)
def home_page():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Manoj's FastAPI Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f6f9; color: #333; margin: 40px; }
            .container { max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .task-card { background: #eef2f3; padding: 15px; margin: 10px 0; border-radius: 6px; border-left: 5px solid #3498db; }
            input, button { width: 100%; padding: 10px; margin: 5px 0 15px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
            button { background-color: #3498db; color: white; border: none; font-weight: bold; cursor: pointer; }
            button:hover { background-color: #2980b9; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Manoj's FastAPI App</h1>
            <p style="text-align: center; color: #7f8c8d;">Powered by Python, Uvicorn, and FastAPI</p>
            
            <h3>Add a New Task</h3>
            <input type="text" id="title" placeholder="Task Title">
            <input type="text" id="description" placeholder="Task Description">
            <input type="number" id="priority" placeholder="Priority (1-5)" value="3">
            <button onclick="addTask()">Submit Task</button>

            <h2>📋 Task Database</h2>
            <div id="taskList">Loading tasks...</div>
        </div>

        <script>
            async function fetchTasks() {
                const response = await fetch('/api/tasks');
                const tasks = await response.json();
                let html = '';
                tasks.forEach(t => {
                    html += `<div class="task-card">
                        <strong>${t.title}</strong> (Priority: ${t.priority})<br>
                        <small>${t.description}</small>
                    </div>`;
                });
                document.getElementById('taskList').innerHTML = html;
            }

            async function addTask() {
                const title = document.getElementById('title').value;
                const description = document.getElementById('description').value;
                const priority = parseInt(document.getElementById('priority').value);

                await fetch('/api/tasks', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ title, description, priority })
                });

                document.getElementById('title').value = '';
                document.getElementById('description').value = '';
                fetchTasks();
            }

            fetchTasks();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/tasks", response_model=List[TaskItem])
def get_tasks():
    return fake_db
@app.post("/api/tasks")
def create_task(task: TaskItem):
    fake_db.append(task)
    return {"message": "Task successfully created!", "task": task}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
