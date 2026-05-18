import falcon

from services.tasks import TaskService


class TaskCollectionAPIResource:
    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        status = req.get_param("status")
        tasks = TaskService.list_tasks(status=status)
        resp.media = {"tasks": [task.to_dict() for task in tasks]}

    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        payload = req.media or {}
        task = TaskService.create_task(
            title=payload.get("title", ""),
            description=payload.get("description", ""),
            priority=payload.get("priority", "medium"),
            status=payload.get("status", "backlog"),
        )
        resp.status = falcon.HTTP_201
        resp.media = {"task": task.to_dict()}


class TaskItemAPIResource:
    def on_patch(self, req: falcon.Request, resp: falcon.Response, task_id: int) -> None:
        payload = req.media or {}
        task = TaskService.update_task(
            task_id=task_id,
            title=payload.get("title"),
            description=payload.get("description"),
            priority=payload.get("priority"),
            status=payload.get("status"),
        )
        resp.media = {"task": task.to_dict()}

    def on_delete(self, req: falcon.Request, resp: falcon.Response, task_id: int) -> None:
        TaskService.delete_task(task_id)
        resp.status = falcon.HTTP_204
