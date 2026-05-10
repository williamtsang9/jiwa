from sqlalchemy import select

from db import SessionLocal
from models.task import (
    ALLOWED_STATUSES,
    BOARD_STATUSES,
    STATUS_BACKLOG,
    STATUS_TO_BE_STARTED,
    Task,
)


class TaskService:
    @staticmethod
    def list_backlog() -> list[Task]:
        with SessionLocal() as session:
            stmt = select(Task).where(Task.status == STATUS_BACKLOG).order_by(Task.created_at.desc())
            return list(session.scalars(stmt).all())

    @staticmethod
    def list_board_grouped() -> dict[str, list[Task]]:
        grouped: dict[str, list[Task]] = {status: [] for status in BOARD_STATUSES}
        with SessionLocal() as session:
            stmt = select(Task).where(Task.status.in_(BOARD_STATUSES)).order_by(Task.created_at.desc())
            for task in session.scalars(stmt).all():
                grouped[task.status].append(task)
        return grouped

    @staticmethod
    def list_tasks(status: str | None = None) -> list[Task]:
        with SessionLocal() as session:
            stmt = select(Task).order_by(Task.created_at.desc())
            if status:
                stmt = stmt.where(Task.status == status)
            return list(session.scalars(stmt).all())

    @staticmethod
    def get_task(task_id: int) -> Task | None:
        with SessionLocal() as session:
            return session.get(Task, task_id)

    @staticmethod
    def create_task(title: str, description: str = "", priority: str = "medium") -> Task:
        clean_title = title.strip()
        if not clean_title:
            raise ValueError("Title is required.")

        with SessionLocal() as session:
            task = Task(
                title=clean_title,
                description=(description or "").strip(),
                priority=(priority or "medium").strip() or "medium",
                status=STATUS_BACKLOG,
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            return task

    @staticmethod
    def move_task(task_id: int, status: str) -> Task:
        if status not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status: {status}")

        with SessionLocal() as session:
            task = session.get(Task, task_id)
            if not task:
                raise ValueError("Task not found.")
            task.status = status
            session.commit()
            session.refresh(task)
            return task

    @staticmethod
    def promote_backlog_task(task_id: int) -> Task:
        return TaskService.move_task(task_id, STATUS_TO_BE_STARTED)

    @staticmethod
    def update_task(
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        priority: str | None = None,
        status: str | None = None,
    ) -> Task:
        with SessionLocal() as session:
            task = session.get(Task, task_id)
            if not task:
                raise ValueError("Task not found.")

            if title is not None:
                clean_title = title.strip()
                if not clean_title:
                    raise ValueError("Title cannot be empty.")
                task.title = clean_title
            if description is not None:
                task.description = description.strip()
            if priority is not None:
                task.priority = priority.strip() or "medium"
            if status is not None:
                if status not in ALLOWED_STATUSES:
                    raise ValueError(f"Invalid status: {status}")
                task.status = status

            session.commit()
            session.refresh(task)
            return task

    @staticmethod
    def delete_task(task_id: int) -> None:
        with SessionLocal() as session:
            task = session.get(Task, task_id)
            if not task:
                return
            session.delete(task)
            session.commit()
