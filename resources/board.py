import falcon

from models.task import BOARD_STATUSES
from services.tasks import TaskService


class BoardPageResource:
    def __init__(self, renderer):
        self.renderer = renderer

    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        grouped = TaskService.list_board_grouped()
        resp.content_type = falcon.MEDIA_HTML
        resp.text = self.renderer.render(
            "board.html",
            {
                "title": "Kanban Board",
                "board_statuses": BOARD_STATUSES,
                "grouped_tasks": grouped,
            },
        )


class BoardMoveResource:
    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        task_id = req.get_param_as_int("task_id", required=True)
        status = req.get_param("status", required=True)
        TaskService.move_task(task_id, status)
        raise falcon.HTTPSeeOther("/board")
