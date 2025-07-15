from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import uvicorn
import uuid
import sqlite3
from typing import List, Optional
import os

app = FastAPI(title="TTRPG Tool Kit", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Database setup
DATABASE_FILE = "ttrpg_tools.db"

def init_database():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Create backgrounds table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS backgrounds (
            id TEXT PRIMARY KEY,
            system TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            free_skill TEXT NOT NULL,
            quick_skill_1 TEXT NOT NULL,
            quick_skill_2 TEXT NOT NULL,
            growth_1 TEXT NOT NULL,
            growth_2 TEXT NOT NULL,
            growth_3 TEXT NOT NULL,
            growth_4 TEXT NOT NULL,
            growth_5 TEXT NOT NULL,
            growth_6 TEXT NOT NULL,
            learning_1 TEXT NOT NULL,
            learning_2 TEXT NOT NULL,
            learning_3 TEXT NOT NULL,
            learning_4 TEXT NOT NULL,
            learning_5 TEXT NOT NULL,
            learning_6 TEXT NOT NULL,
            learning_7 TEXT NOT NULL,
            learning_8 TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_all_backgrounds():
    """Retrieve all backgrounds from database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM backgrounds ORDER BY created_at DESC')
    rows = cursor.fetchall()
    
    backgrounds = []
    for row in rows:
        background = {
            "id": row[0],
            "system": row[1],
            "name": row[2],
            "description": row[3],
            "free_skill": row[4],
            "quick_skills": [row[5], row[6]],
            "growth": [row[7], row[8], row[9], row[10], row[11], row[12]],
            "learning": [row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20]]
        }
        backgrounds.append(background)
    
    conn.close()
    return backgrounds

def add_background_to_db(background_data):
    """Add a new background to the database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO backgrounds (
            id, system, name, description, free_skill,
            quick_skill_1, quick_skill_2,
            growth_1, growth_2, growth_3, growth_4, growth_5, growth_6,
            learning_1, learning_2, learning_3, learning_4, learning_5, learning_6, learning_7, learning_8
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        background_data["id"],
        background_data["system"],
        background_data["name"],
        background_data["description"],
        background_data["free_skill"],
        background_data["quick_skills"][0],
        background_data["quick_skills"][1],
        background_data["growth"][0],
        background_data["growth"][1],
        background_data["growth"][2],
        background_data["growth"][3],
        background_data["growth"][4],
        background_data["growth"][5],
        background_data["learning"][0],
        background_data["learning"][1],
        background_data["learning"][2],
        background_data["learning"][3],
        background_data["learning"][4],
        background_data["learning"][5],
        background_data["learning"][6],
        background_data["learning"][7]
    ))
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_database()

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/character")
async def character(request: Request):
    return templates.TemplateResponse("character.html", {"request": request})

@app.get("/skills")
async def skills_page(request: Request):
    return templates.TemplateResponse("skills.html", {"request": request})

@app.get("/backgrounds")
async def backgrounds(request: Request):
    backgrounds_list = get_all_backgrounds()
    return templates.TemplateResponse("backgrounds.html", {"request": request, "backgrounds": backgrounds_list})

@app.post("/backgrounds")
async def add_background(
    request: Request,
    system: str = Form(...),
    name: str = Form(...),
    description: str = Form(...),
    free_skill: str = Form(...),
    quick_skill_1: str = Form(...),
    quick_skill_2: str = Form(...),
    growth_1: str = Form(...),
    growth_2: str = Form(...),
    growth_3: str = Form(...),
    growth_4: str = Form(...),
    growth_5: str = Form(...),
    growth_6: str = Form(...),
    learning_1: str = Form(...),
    learning_2: str = Form(...),
    learning_3: str = Form(...),
    learning_4: str = Form(...),
    learning_5: str = Form(...),
    learning_6: str = Form(...),
    learning_7: str = Form(...),
    learning_8: str = Form(...)
):
    # Generate unique ID
    unique_id = str(uuid.uuid4())
    
    # Create background object
    background = {
        "id": unique_id,
        "system": system,
        "name": name,
        "description": description,
        "free_skill": free_skill,
        "quick_skills": [quick_skill_1, quick_skill_2],
        "growth": [growth_1, growth_2, growth_3, growth_4, growth_5, growth_6],
        "learning": [learning_1, learning_2, learning_3, learning_4, learning_5, learning_6, learning_7, learning_8]
    }
    
    # Add to database
    add_background_to_db(background)
    
    return RedirectResponse(url="/backgrounds", status_code=303)

@app.get("/class")
async def class_page(request: Request):
    return templates.TemplateResponse("class.html", {"request": request})

@app.get("/foci")
async def foci_page(request: Request):
    return templates.TemplateResponse("foci.html", {"request": request})

@app.get("/world")
async def world(request: Request):
    return templates.TemplateResponse("world.html", {"request": request})

@app.get("/items")
async def items(request: Request):
    return templates.TemplateResponse("items.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=True) 