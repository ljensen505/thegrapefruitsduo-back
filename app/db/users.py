from app.db.base_queries import BaseQueries
from app.models.user import USER_TABLE


class UserQueries(BaseQueries):
    def __init__(self) -> None:
        super().__init__()
        self.table = USER_TABLE

    async def get_one_by_auth0_id(self, auth0_id: str) -> dict:
        query = f"SELECT * FROM {self.table} WHERE auth0_id = %s"
        db = self.connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (auth0_id,))
        data = cursor.fetchone()
        cursor.close()
        db.close()

        if not data:
            raise Exception("error retrieving user")

        return data
