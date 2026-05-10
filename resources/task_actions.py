import falcon

from services.tasks import TaskService


class TaskUpdateResource:
    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        task_id = req.get_param_as_int("task_id", required=True)
        title = req.get_param("title")
        description = req.get_param("description")
        priority = req.get_param("priority")
        status = req.get_param("status")
        next_url = req.get_param("next") or "/board"

        TaskService.update_task(
            task_id=task_id,
            title=title,
            description=description,
            priority=priority,
            status=status,
        )
        raise falcon.HTTPSeeOther(next_url)


class TaskDeleteResource:
    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        task_id = req.get_param_as_int("task_id", required=True)
        next_url = req.get_param("next") or "/board"
        TaskService.delete_task(task_id)
        raise falcon.HTTPSeeOther(next_url)
