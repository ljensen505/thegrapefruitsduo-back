from app.db.base_queries import BaseQueries
from app.models.event import EVENT_TABLE, InsertionEvent, NewEvent


class EventQueries(BaseQueries):
    def __init__(self) -> None:
        super().__init__()
        self.table = EVENT_TABLE

    async def insert_one(self, event: InsertionEvent) -> int:
        query = f"INSERT INTO {self.table} (name, location, description, time, poster) VALUES (%s, %s, %s, %s, %s)"
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute(
            query,
            (event.name, event.location, event.description, event.time, event.poster),
        )
        inserted_id = cursor.lastrowid
        db.commit()
        cursor.close()
        db.close()
        return inserted_id

    async def delete_one(self, id: int) -> None:
        query = f"DELETE FROM {self.table} WHERE id = %s"
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute(query, (id,))
        db.commit()
        cursor.close()
        db.close()
