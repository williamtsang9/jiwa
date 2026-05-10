from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

from config import Config


class Base(DeclarativeBase):
    pass


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, future=True)
SessionLocal = scoped_session(
    sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
)


def init_db() -> None:
    # Imported here to avoid circular imports during metadata discovery.
    from models.task import Task  # noqa: F401

    Base.metadata.create_all(bind=engine)
