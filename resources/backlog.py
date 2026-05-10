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
        title = req.get_param("title", required=True)
        description = req.get_param("description") or ""
        priority = req.get_param("priority") or "medium"
        TaskService.create_task(title=title, description=description, priority=priority)
        raise falcon.HTTPSeeOther("/backlog")


class BacklogPromoteResource:
    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        task_id = req.get_param_as_int("task_id", required=True)
        TaskService.promote_backlog_task(task_id)
        raise falcon.HTTPSeeOther("/board")
