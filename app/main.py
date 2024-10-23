from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

# Define paths for templates and static files
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/projects", StaticFiles(directory="app/projects"), name="projects")


# Path where projects are stored
PROJECTS_PATH = "app/projects"

# Helper function to get all project folders and images
def get_projects():
    projects = []
    for project in os.listdir(PROJECTS_PATH):
        project_path = os.path.join(PROJECTS_PATH, project)
        if os.path.isdir(project_path):
            images = [img for img in os.listdir(project_path) if img.endswith(('.jpg', '.jpeg', '.png', '.JPG'))]
            projects.append({"name": project, "images": images})
    return projects

# Main route to display the portfolio
@app.get("/", response_class=HTMLResponse)
async def portfolio(request: Request):
    projects = get_projects()
    return templates.TemplateResponse("index.html", {"request": request, "projects": projects})

# New route to display a specific project's images
@app.get("/project/{project_name}", response_class=HTMLResponse)
async def project_detail(request: Request, project_name: str):
    project_path = os.path.join(PROJECTS_PATH, project_name)
    if not os.path.exists(project_path):
        return HTMLResponse(content="Project not found", status_code=404)
    
    images = [img for img in os.listdir(project_path) if img.endswith(('.jpg', '.jpeg', '.png', '.JPG'))]
    return templates.TemplateResponse("project_detail.html", {
        "request": request, 
        "project_name": project_name, 
        "images": images
    })