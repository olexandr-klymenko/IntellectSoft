from core.config import settings
from sqlalchemy import event
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker


def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
    dbapi_con.execute("pragma foreign_keys=ON")


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_engine(
            url=url,
            echo=echo,
        )
        # Enforce foreign keys checking
        # which in sqlite is turned off by default
        if "sqlite" in url:
            event.listen(self.engine, "connect", _fk_pragma_on_connect)

        self.session_factory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )


db_helper = DatabaseHelper(
    url=settings.db.url,
    echo=settings.db.echo,
)
