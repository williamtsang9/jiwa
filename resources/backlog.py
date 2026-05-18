import falcon

from services.tasks import TaskService


class BacklogPageResource:
    def __init__(self, renderer):
        self.renderer = renderer

    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        backlog_tasks = TaskService.list_backlog()
        resp.content_type = falcon.MEDIA_HTML
        resp.text = self.renderer.render(
            "backlog.html",
            {
                "title": "Backlog",
                "backlog_tasks": backlog_tasks,
            },
        )


class BacklogCreateResource:
    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        data = req.get_media()
        title = data.get("title")
        if not title:
            raise falcon.HTTPBadRequest("Title is required.")
        description = data.get("description") or ""
        priority = data.get("priority") or "medium"
        TaskService.create_task(title=title, description=description, priority=priority)
        raise falcon.HTTPSeeOther("/backlog")


class BacklogPromoteResource:
    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        data = req.get_media()
        task_id = data.get("task_id")
        if not task_id:
            raise falcon.HTTPBadRequest("Task ID is required.")
        try:
            task_id = int(task_id)
        except ValueError:
            raise falcon.HTTPBadRequest("Task ID must be an integer.")
        TaskService.promote_backlog_task(task_id)
        raise falcon.HTTPSeeOther("/board")
