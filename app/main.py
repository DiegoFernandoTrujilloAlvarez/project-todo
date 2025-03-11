from fastapi import FastAPI
from app.routers.users_router import users
from app.routers.tasks_router import tasks
from app.config.dbconfig import Base, engine, get_db
import time
from datetime import datetime, date
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
import ssl
import smtplib
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.models.task_model import Tasks

from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "port": 465,
    "username": "repbloodgamer@gmail.com",
    "password": os.getenv("KEY_GMAIL")
}

async def send_email(to: str, subject: str, body: str):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_CONFIG['username']
    msg['To'] = to

    try:
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['port'], context=context) as smtp:
            smtp.login(EMAIL_CONFIG['username'], EMAIL_CONFIG["password"])
            smtp.sendmail(EMAIL_CONFIG["username"], to,msg.as_string())
    except Exception as e:
        print("Error al enviar el correo")

async def check_daily_tasks():
    with next(get_db()) as db:
        today = date.today()
        tasks = db.query(Tasks).filter(Tasks.date_to_do == today).all()

        user_tasks = {}
        for task in tasks:
            if task.user_id not in user_tasks:
                user_tasks[task.user_id] = []
            user_tasks[task.user_id].append(task)

        for user_id, tasks in user_tasks.items():
            task_list = "\n".join([f"- {task.description}" for task in tasks])
            name = tasks[0].owner.firt_name
            to = tasks[0].owner.email
            body = f"Hola {name}, \n\nTienes las siguientes tareas para hoy:\n{task_list}"
            await send_email(to=to, subject="Recodatorio de tareas diarias", body=body)
            
print("Crear db")
Base.metadata.create_all(bind=engine)
print("Terminó de crear")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Iniciar el scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_daily_tasks, 'cron', hour=8, minute=0)  # Ejecutar diario a las 8 AM
    scheduler.start()
    yield
    # Detener al cerrar
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan, title="Proyecto TODO", version="1.0", debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # URL de tu frontend en desarrollo
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar los routers
app.include_router(users)
app.include_router(tasks)

@app.get("/{number}")
async def root(number: int):
    print(f"ROOT {number}")
    time.sleep(5)
    print(f"despues {number}")
    return "Bievenido a la aplicación TODO"