from pathlib import Path
import logging

import falcon
from jinja2 import Environment, FileSystemLoader, select_autoescape
from wsgiref.simple_server import make_server

from config import Config
from db import init_db
from resources.api_tasks import TaskCollectionAPIResource, TaskItemAPIResource
from resources.backlog import BacklogCreateResource, BacklogPageResource, BacklogPromoteResource
from resources.board import BoardMoveResource, BoardPageResource
from resources.task_actions import TaskDeleteResource, TaskUpdateResource


BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
LOG_DIR = BASE_DIR / "logs"


class RequestLoggerMiddleware:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def process_request(self, req: falcon.Request, resp: falcon.Response) -> None:
        self.logger.info("request started method=%s path=%s", req.method, req.path)

    def process_response(
        self, req: falcon.Request, resp: falcon.Response, resource, req_succeeded: bool
    ) -> None:
        self.logger.info(
            "request completed method=%s path=%s status=%s",
            req.method,
            req.path,
            resp.status,
        )


class TemplateRenderer:
    def __init__(self, template_dir: Path):
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(["html", "xml"]),
        )

    def render(self, template_name: str, context: dict) -> str:
        return self.env.get_template(template_name).render(**context)


def handle_value_error(
    ex: ValueError, req: falcon.Request, resp: falcon.Response, params
) -> None:
    raise falcon.HTTPBadRequest(title="Validation error", description=str(ex))


def create_app() -> falcon.App:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file_path = BASE_DIR / Config.LOG_FILE
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file_path, encoding="utf-8"),
        ],
    )
    logger = logging.getLogger("jiwa")

    init_db()

    app = falcon.App(middleware=[RequestLoggerMiddleware(logger)])
    app.add_error_handler(ValueError, handle_value_error)
    app.add_static_route("/static", str(STATIC_DIR))

    renderer = TemplateRenderer(TEMPLATES_DIR)

    app.add_route("/", RedirectResource("/board"))
    app.add_route("/board", BoardPageResource(renderer))
    app.add_route("/board/move", BoardMoveResource())
    app.add_route("/backlog", BacklogPageResource(renderer))
    app.add_route("/backlog/create", BacklogCreateResource())
    app.add_route("/backlog/promote", BacklogPromoteResource())
    app.add_route("/task/update", TaskUpdateResource())
    app.add_route("/task/delete", TaskDeleteResource())
    app.add_route("/api/tasks", TaskCollectionAPIResource())
    app.add_route("/api/tasks/{task_id:int}", TaskItemAPIResource())

    return app


class RedirectResource:
    def __init__(self, location: str):
        self.location = location

    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        raise falcon.HTTPSeeOther(self.location)


app = create_app()


if __name__ == "__main__":
    with make_server(Config.APP_HOST, Config.APP_PORT, app) as httpd:
        print(f"Serving on http://{Config.APP_HOST}:{Config.APP_PORT}")
        httpd.serve_forever()
