from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, session: Session):
        self.session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session.rollback()
        return False

    def commit(self) -> None:
        self.session.commit()

    def flush(self) -> None:
        self.session.flush()

    def rollback(self) -> None:
        self.session.rollback()
