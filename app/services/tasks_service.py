from ..models.task_model import Tasks
from .base_service import BaseService
from ..schemas.tasks_schema import TaskRequest, TaskUpdate
import datetime


class TasksService(BaseService):

    def get_tasks(self):
        """Obtiene todos las tareas"""
        return self.db.query(Tasks).all()
    
    def get_task_by_id(self, task_id: int):
        """Obtiene la tarea por id"""
        return self.db.query(Tasks).filter(Tasks.task_id == task_id).first()        

    def create_task(self, task: TaskRequest):
        """Crea una nueva tarea"""
        task.created_on = datetime.datetime.now().date()
        new_task = Tasks(**task.model_dump())        
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)

    def update_task(self, task_id: int, task_update: TaskUpdate):
        """Actualización de una tarea"""
        # Buscar usuario (Después reemplazar con la función de get ususario)
        task = self.db.query(Tasks).filter(Tasks.task_id == task_id).first()
        if not task:
            return None
        
        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)
        
        self.db.commit()
        self.db.refresh(task)
        return True
    
    def delete_task(self, task_id: int):
        """Eliminar una tarea"""
        task = self.db.query(Tasks).filter(Tasks.task_id == task_id).first()
        if not task:
            None
        self.db.delete(task)
        return True