from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import uvicorn
import uuid
import sqlite3
from typing import List, Optional
import os
from fastapi.responses import JSONResponse

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
    
    # Create skills table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id TEXT PRIMARY KEY,
            system TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create classes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            id TEXT PRIMARY KEY,
            system TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            class_ability_1 TEXT NOT NULL,
            class_ability_2 TEXT NOT NULL,
            hit_dice_1 TEXT NOT NULL,
            hit_dice_2 TEXT NOT NULL,
            hit_dice_3 TEXT NOT NULL,
            hit_dice_4 TEXT NOT NULL,
            hit_dice_5 TEXT NOT NULL,
            hit_dice_6 TEXT NOT NULL,
            hit_dice_7 TEXT NOT NULL,
            hit_dice_8 TEXT NOT NULL,
            hit_dice_9 TEXT NOT NULL,
            hit_dice_10 TEXT NOT NULL,
            attack_bonus_1 TEXT NOT NULL,
            attack_bonus_2 TEXT NOT NULL,
            attack_bonus_3 TEXT NOT NULL,
            attack_bonus_4 TEXT NOT NULL,
            attack_bonus_5 TEXT NOT NULL,
            attack_bonus_6 TEXT NOT NULL,
            attack_bonus_7 TEXT NOT NULL,
            attack_bonus_8 TEXT NOT NULL,
            attack_bonus_9 TEXT NOT NULL,
            attack_bonus_10 TEXT NOT NULL,
            focus_picks_1 TEXT NOT NULL,
            focus_picks_2 TEXT NOT NULL,
            focus_picks_3 TEXT NOT NULL,
            focus_picks_4 TEXT NOT NULL,
            focus_picks_5 TEXT NOT NULL,
            focus_picks_6 TEXT NOT NULL,
            focus_picks_7 TEXT NOT NULL,
            focus_picks_8 TEXT NOT NULL,
            focus_picks_9 TEXT NOT NULL,
            focus_picks_10 TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create foci table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS foci (
            id TEXT PRIMARY KEY,
            system TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            level_1 TEXT NOT NULL,
            level_2 TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create arts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS arts (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            class_name TEXT NOT NULL,
            system TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create adventure_gear table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS adventure_gear (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            system TEXT NOT NULL,
            description TEXT NOT NULL,
            cost TEXT NOT NULL,
            weight TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create weapons table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weapons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            system TEXT NOT NULL,
            damage TEXT NOT NULL,
            shock TEXT NOT NULL,
            attribute TEXT NOT NULL,
            range TEXT NOT NULL,
            traits TEXT NOT NULL,
            cost TEXT NOT NULL,
            weight TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create armor table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS armor (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            system TEXT NOT NULL,
            type TEXT NOT NULL,
            ac TEXT NOT NULL,
            cost TEXT NOT NULL,
            weight TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create beasts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS beasts (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            system TEXT NOT NULL,
            cost TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_all_backgrounds():
    """Retrieve all backgrounds from database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM backgrounds ORDER BY name ASC')
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

def get_all_skills():
    """Retrieve all skills from database in alphabetical order"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM skills ORDER BY name ASC')
    rows = cursor.fetchall()
    skills = []
    for row in rows:
        skill = {
            "id": row[0],
            "system": row[1],
            "name": row[2],
            "description": row[3]
        }
        skills.append(skill)
    conn.close()
    return skills

def add_skill_to_db(skill_data):
    """Add a new skill to the database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO skills (id, system, name, description)
        VALUES (?, ?, ?, ?)
    ''', (
        skill_data["id"],
        skill_data["system"],
        skill_data["name"],
        skill_data["description"]
    ))
    
    conn.commit()
    conn.close()

def get_all_classes():
    """Retrieve all classes from database in alphabetical order"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM classes ORDER BY name ASC')
    rows = cursor.fetchall()
    classes = []
    for row in rows:
        class_item = {
            "id": row[0],
            "system": row[1],
            "name": row[2],
            "description": row[3],
            "class_ability": [row[4], row[5]],
            "hit_dice": [row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15]],
            "attack_bonus": [row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25]],
            "focus_picks": [row[26], row[27], row[28], row[29], row[30], row[31], row[32], row[33], row[34], row[35]]
        }
        classes.append(class_item)
    conn.close()
    return classes

def add_class_to_db(class_data):
    """Add a new class to the database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO classes (
            id, system, name, description,
            class_ability_1, class_ability_2,
            hit_dice_1, hit_dice_2, hit_dice_3, hit_dice_4, hit_dice_5, hit_dice_6, hit_dice_7, hit_dice_8, hit_dice_9, hit_dice_10,
            attack_bonus_1, attack_bonus_2, attack_bonus_3, attack_bonus_4, attack_bonus_5, attack_bonus_6, attack_bonus_7, attack_bonus_8, attack_bonus_9, attack_bonus_10,
            focus_picks_1, focus_picks_2, focus_picks_3, focus_picks_4, focus_picks_5, focus_picks_6, focus_picks_7, focus_picks_8, focus_picks_9, focus_picks_10
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        class_data["id"],
        class_data["system"],
        class_data["name"],
        class_data["description"],
        class_data["class_ability"][0],
        class_data["class_ability"][1],
        class_data["hit_dice"][0],
        class_data["hit_dice"][1],
        class_data["hit_dice"][2],
        class_data["hit_dice"][3],
        class_data["hit_dice"][4],
        class_data["hit_dice"][5],
        class_data["hit_dice"][6],
        class_data["hit_dice"][7],
        class_data["hit_dice"][8],
        class_data["hit_dice"][9],
        class_data["attack_bonus"][0],
        class_data["attack_bonus"][1],
        class_data["attack_bonus"][2],
        class_data["attack_bonus"][3],
        class_data["attack_bonus"][4],
        class_data["attack_bonus"][5],
        class_data["attack_bonus"][6],
        class_data["attack_bonus"][7],
        class_data["attack_bonus"][8],
        class_data["attack_bonus"][9],
        class_data["focus_picks"][0],
        class_data["focus_picks"][1],
        class_data["focus_picks"][2],
        class_data["focus_picks"][3],
        class_data["focus_picks"][4],
        class_data["focus_picks"][5],
        class_data["focus_picks"][6],
        class_data["focus_picks"][7],
        class_data["focus_picks"][8],
        class_data["focus_picks"][9]
    ))
    
    conn.commit()
    conn.close()

def get_all_foci():
    """Retrieve all foci from database in alphabetical order"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM foci ORDER BY name ASC')
    rows = cursor.fetchall()
    foci = []
    for row in rows:
        focus = {
            "id": row[0],
            "system": row[1],
            "name": row[2],
            "description": row[3],
            "level_1": row[4],
            "level_2": row[5]
        }
        foci.append(focus)
    conn.close()
    return foci

def add_focus_to_db(focus_data):
    """Add a new focus to the database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO foci (id, system, name, description, level_1, level_2)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        focus_data["id"],
        focus_data["system"],
        focus_data["name"],
        focus_data["description"],
        focus_data["level_1"],
        focus_data["level_2"]
    ))
    
    conn.commit()
    conn.close()

def get_all_arts():
    """Retrieve all arts from database in alphabetical order"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM arts ORDER BY name ASC')
    rows = cursor.fetchall()
    arts = []
    for row in rows:
        art = {
            "id": row[0],
            "name": row[1],
            "class_name": row[2],
            "system": row[3]
        }
        arts.append(art)
    conn.close()
    return arts

def add_art_to_db(art_data):
    """Add a new art to the database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO arts (
            id, name, class_name, system
        ) VALUES (?, ?, ?, ?)
    ''', (
        art_data["id"],
        art_data["name"],
        art_data["class_name"],
        art_data["system"]
    ))
    conn.commit()
    conn.close()

def get_all_adventure_gear():
    """Retrieve all adventure gear from database in alphabetical order"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM adventure_gear ORDER BY name ASC')
    rows = cursor.fetchall()
    gear = []
    for row in rows:
        gear_item = {
            "id": row[0],
            "name": row[1],
            "system": row[2],
            "description": row[3],
            "cost": row[4],
            "weight": row[5]
        }
        gear.append(gear_item)
    conn.close()
    return gear

def add_adventure_gear_to_db(gear_data):
    """Add a new adventure gear item to the database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO adventure_gear (
            id, name, system, description, cost, weight
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        gear_data["id"],
        gear_data["name"],
        gear_data["system"],
        gear_data["description"],
        gear_data["cost"],
        gear_data["weight"]
    ))
    conn.commit()
    conn.close()

def get_all_weapons():
    """Retrieve all weapons from database in alphabetical order"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM weapons ORDER BY name ASC')
    rows = cursor.fetchall()
    weapons = []
    for row in rows:
        weapon = {
            "id": row[0],
            "name": row[1],
            "system": row[2],
            "damage": row[3],
            "shock": row[4],
            "attribute": row[5],
            "range": row[6],
            "traits": row[7],
            "cost": row[8],
            "weight": row[9]
        }
        weapons.append(weapon)
    conn.close()
    return weapons

def add_weapon_to_db(weapon_data):
    """Add a new weapon to the database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO weapons (
            id, name, system, damage, shock, attribute, range, traits, cost, weight
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        weapon_data["id"],
        weapon_data["name"],
        weapon_data["system"],
        weapon_data["damage"],
        weapon_data["shock"],
        weapon_data["attribute"],
        weapon_data["range"],
        weapon_data["traits"],
        weapon_data["cost"],
        weapon_data["weight"]
    ))
    conn.commit()
    conn.close()

def get_all_armor():
    """Retrieve all armor from database in alphabetical order"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM armor ORDER BY name ASC')
    rows = cursor.fetchall()
    armor = []
    for row in rows:
        armor_item = {
            "id": row[0],
            "name": row[1],
            "system": row[2],
            "type": row[3],
            "ac": row[4],
            "cost": row[5],
            "weight": row[6]
        }
        armor.append(armor_item)
    conn.close()
    return armor

def add_armor_to_db(armor_data):
    """Add a new armor item to the database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO armor (
            id, name, system, type, ac, cost, weight
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        armor_data["id"],
        armor_data["name"],
        armor_data["system"],
        armor_data["type"],
        armor_data["ac"],
        armor_data["cost"],
        armor_data["weight"]
    ))
    conn.commit()
    conn.close()

def get_all_beasts():
    """Retrieve all beasts from database in alphabetical order"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM beasts ORDER BY name ASC')
    rows = cursor.fetchall()
    beasts = []
    for row in rows:
        beast = {
            "id": row[0],
            "name": row[1],
            "system": row[2],
            "cost": row[3]
        }
        beasts.append(beast)
    conn.close()
    return beasts

def add_beast_to_db(beast_data):
    """Add a new beast to the database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO beasts (
            id, name, system, cost
        ) VALUES (?, ?, ?, ?)
    ''', (
        beast_data["id"],
        beast_data["name"],
        beast_data["system"],
        beast_data["cost"]
    ))
    conn.commit()
    conn.close()

def get_all_services():
    """Retrieve all services from database in alphabetical order"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM services ORDER BY name ASC')
    rows = cursor.fetchall()
    services = []
    for row in rows:
        service = {
            "id": row[0],
            "name": row[1],
            "system": row[2],
            "cost": row[3]
        }
        services.append(service)
    conn.close()
    return services

def add_service_to_db(service_data):
    """Add a new service to the database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO services (
            id, name, system, cost
        ) VALUES (?, ?, ?, ?)
    ''', (
        service_data["id"],
        service_data["name"],
        service_data["system"],
        service_data["cost"]
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
    skills_list = get_all_skills()
    return templates.TemplateResponse("skills.html", {"request": request, "skills": skills_list})

@app.post("/skills")
async def add_skill(
    request: Request,
    system: str = Form(...),
    name: str = Form(...),
    description: str = Form(...)
):
    # Generate unique ID
    unique_id = str(uuid.uuid4())
    
    # Create skill object
    skill = {
        "id": unique_id,
        "system": system,
        "name": name,
        "description": description
    }
    
    # Add to database
    add_skill_to_db(skill)
    
    return RedirectResponse(url="/skills", status_code=303)

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

@app.get("/api/backgrounds/worlds-without-number")
async def backgrounds_wwn():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, description FROM backgrounds WHERE system = ?', ("Worlds Without Number",))
    rows = cursor.fetchall()
    conn.close()
    backgrounds = [{"id": row[0], "name": row[1], "description": row[2]} for row in rows]
    return JSONResponse(content=backgrounds)

@app.get("/character-creation")
async def character_creation(request: Request):
    return templates.TemplateResponse("character-creation.html", {"request": request})

@app.get("/class")
async def class_page(request: Request):
    classes_list = get_all_classes()
    return templates.TemplateResponse("class.html", {"request": request, "classes": classes_list})

@app.post("/class")
async def add_class(
    request: Request,
    system: str = Form(...),
    name: str = Form(...),
    description: str = Form(...),
    class_ability_1: str = Form(...),
    class_ability_2: str = Form(...),
    hit_dice_1: str = Form(...),
    hit_dice_2: str = Form(...),
    hit_dice_3: str = Form(...),
    hit_dice_4: str = Form(...),
    hit_dice_5: str = Form(...),
    hit_dice_6: str = Form(...),
    hit_dice_7: str = Form(...),
    hit_dice_8: str = Form(...),
    hit_dice_9: str = Form(...),
    hit_dice_10: str = Form(...),
    attack_bonus_1: str = Form(...),
    attack_bonus_2: str = Form(...),
    attack_bonus_3: str = Form(...),
    attack_bonus_4: str = Form(...),
    attack_bonus_5: str = Form(...),
    attack_bonus_6: str = Form(...),
    attack_bonus_7: str = Form(...),
    attack_bonus_8: str = Form(...),
    attack_bonus_9: str = Form(...),
    attack_bonus_10: str = Form(...),
    focus_picks_1: str = Form(...),
    focus_picks_2: str = Form(...),
    focus_picks_3: str = Form(...),
    focus_picks_4: str = Form(...),
    focus_picks_5: str = Form(...),
    focus_picks_6: str = Form(...),
    focus_picks_7: str = Form(...),
    focus_picks_8: str = Form(...),
    focus_picks_9: str = Form(...),
    focus_picks_10: str = Form(...)
):
    # Generate unique ID
    unique_id = str(uuid.uuid4())
    
    # Create class object
    class_item = {
        "id": unique_id,
        "system": system,
        "name": name,
        "description": description,
        "class_ability": [class_ability_1, class_ability_2],
        "hit_dice": [hit_dice_1, hit_dice_2, hit_dice_3, hit_dice_4, hit_dice_5, hit_dice_6, hit_dice_7, hit_dice_8, hit_dice_9, hit_dice_10],
        "attack_bonus": [attack_bonus_1, attack_bonus_2, attack_bonus_3, attack_bonus_4, attack_bonus_5, attack_bonus_6, attack_bonus_7, attack_bonus_8, attack_bonus_9, attack_bonus_10],
        "focus_picks": [focus_picks_1, focus_picks_2, focus_picks_3, focus_picks_4, focus_picks_5, focus_picks_6, focus_picks_7, focus_picks_8, focus_picks_9, focus_picks_10]
    }
    
    # Add to database
    add_class_to_db(class_item)
    
    return RedirectResponse(url="/class", status_code=303)

@app.get("/foci")
async def foci_page(request: Request):
    foci_list = get_all_foci()
    return templates.TemplateResponse("foci.html", {"request": request, "foci": foci_list})

@app.post("/foci")
async def add_focus(
    request: Request,
    system: str = Form(...),
    focus_name: str = Form(...),
    focus_description: str = Form(...),
    level_1: str = Form(...),
    level_2: str = Form(...)
):
    # Generate unique ID
    unique_id = str(uuid.uuid4())
    
    # Create focus object
    focus = {
        "id": unique_id,
        "system": system,
        "name": focus_name,
        "description": focus_description,
        "level_1": level_1,
        "level_2": level_2
    }
    
    # Add to database
    add_focus_to_db(focus)
    
    return RedirectResponse(url="/foci", status_code=303)

@app.get("/arts")
async def arts_page(request: Request):
    arts_list = get_all_arts()
    return templates.TemplateResponse("arts.html", {"request": request, "arts": arts_list})

@app.post("/arts")
async def add_art(
    request: Request,
    name: str = Form(...),
    class_name: str = Form(...),
    system: str = Form(...)
):
    unique_id = str(uuid.uuid4())
    art = {
        "id": unique_id,
        "name": name,
        "class_name": class_name,
        "system": system
    }
    add_art_to_db(art)
    return RedirectResponse(url="/arts", status_code=303)

@app.get("/adventure")
async def adventure(request: Request):
    gear_list = get_all_adventure_gear()
    return templates.TemplateResponse("adventure.html", {"request": request, "adventure_gear": gear_list})

@app.post("/adventure")
async def add_adventure_gear(
    request: Request,
    gearName: str = Form(...),
    system: str = Form(...),
    gearDescription: str = Form(...),
    gearCost: str = Form(...),
    gearWeight: str = Form(...)
):
    unique_id = str(uuid.uuid4())
    gear = {
        "id": unique_id,
        "name": gearName,
        "system": system,
        "description": gearDescription,
        "cost": gearCost,
        "weight": gearWeight
    }
    add_adventure_gear_to_db(gear)
    return RedirectResponse(url="/adventure", status_code=303)

@app.get("/world")
async def world(request: Request):
    return templates.TemplateResponse("world.html", {"request": request})

@app.get("/items")
async def items(request: Request):
    return templates.TemplateResponse("items.html", {"request": request})

@app.get("/weapons")
async def weapons(request: Request):
    weapons_list = get_all_weapons()
    return templates.TemplateResponse("weapons.html", {"request": request, "weapons": weapons_list})

@app.post("/weapons")
async def add_weapon(
    request: Request,
    name: str = Form(...),
    system: str = Form(...),
    damage: str = Form(...),
    shock: str = Form(...),
    attribute: str = Form(...),
    range: str = Form(...),
    traits: str = Form(...),
    cost: str = Form(...),
    weight: str = Form(...)
):
    # Generate unique ID
    unique_id = str(uuid.uuid4())
    
    # Create weapon object
    weapon = {
        "id": unique_id,
        "name": name,
        "system": system,
        "damage": damage,
        "shock": shock,
        "attribute": attribute,
        "range": range,
        "traits": traits,
        "cost": cost,
        "weight": weight
    }
    
    # Add to database
    add_weapon_to_db(weapon)
    
    return RedirectResponse(url="/weapons", status_code=303)

@app.get("/armor")
async def armor(request: Request):
    armor_list = get_all_armor()
    return templates.TemplateResponse("armor.html", {"request": request, "armor": armor_list})

@app.post("/armor")
async def add_armor(
    request: Request,
    name: str = Form(...),
    system: str = Form(...),
    type: str = Form(...),
    ac: str = Form(...),
    cost: str = Form(...),
    weight: str = Form(...)
):
    # Generate unique ID
    unique_id = str(uuid.uuid4())
    
    # Create armor object
    armor_item = {
        "id": unique_id,
        "name": name,
        "system": system,
        "type": type,
        "ac": ac,
        "cost": cost,
        "weight": weight
    }
    
    # Add to database
    add_armor_to_db(armor_item)
    
    return RedirectResponse(url="/armor", status_code=303)

@app.get("/beast-transport")
async def beast_transport(request: Request):
    beasts_list = get_all_beasts()
    return templates.TemplateResponse("beast-transport.html", {"request": request, "beasts": beasts_list})

@app.post("/beast-transport")
async def add_beast(
    request: Request,
    name: str = Form(...),
    system: str = Form(...),
    cost: str = Form(...)
):
    # Generate unique ID
    unique_id = str(uuid.uuid4())
    
    # Create beast object
    beast = {
        "id": unique_id,
        "name": name,
        "system": system,
        "cost": cost
    }
    
    # Add to database
    add_beast_to_db(beast)
    
    return RedirectResponse(url="/beast-transport", status_code=303)

@app.get("/service-living")
async def service_living(request: Request):
    services_list = get_all_services()
    return templates.TemplateResponse("service-living.html", {"request": request, "services": services_list})

@app.post("/service-living")
async def add_service(
    request: Request,
    name: str = Form(...),
    system: str = Form(...),
    cost: str = Form(...)
):
    # Generate unique ID
    unique_id = str(uuid.uuid4())
    
    # Create service object
    service = {
        "id": unique_id,
        "name": name,
        "system": system,
        "cost": cost
    }
    
    # Add to database
    add_service_to_db(service)
    
    return RedirectResponse(url="/service-living", status_code=303)

@app.get("/hirelings")
async def hirelings(request: Request):
    return templates.TemplateResponse("hirelings.html", {"request": request})

@app.get("/gear")
async def gear(request: Request):
    return templates.TemplateResponse("gear.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True) 