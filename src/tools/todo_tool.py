from datetime import datetime
from typing import List, Dict, Optional

class TodoManager:
    def __init__(self) -> None:
        self.tasks: List[Dict[str, Optional[str]]] = []

    def add_task(self, title: str, due: Optional[str] = None) -> Dict[str, Optional[str]]:
        task = {"title": title, "due": due, "status": "pending", "created_at": datetime.utcnow().isoformat()}
        self.tasks.append(task)
        return task

    def list_tasks(self) -> List[Dict[str, Optional[str]]]:
        return self.tasks

    def complete_task(self, index: int) -> Dict[str, Optional[str]]:
        if index < 0 or index >= len(self.tasks):
            raise IndexError("Task index out of range")
        self.tasks[index]["status"] = "completed"
        return self.tasks[index]


todo_manager = TodoManager()
