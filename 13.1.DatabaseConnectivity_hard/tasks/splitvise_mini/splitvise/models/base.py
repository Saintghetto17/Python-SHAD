from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_PATH = Path('database')
DATABASE_PATH.mkdir(parents=True, exist_ok=True)
DATABASE_URL = f'sqlite:///{DATABASE_PATH.as_posix()}/sqlite.db'


engine = create_engine(
    DATABASE_URL, echo=False, future=True, connect_args={'check_same_thread': False}
)
Session = sessionmaker(engine, future=True, expire_on_commit=False)


Base = declarative_base()


def clear_database() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
