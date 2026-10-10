import sqlite3
from typing import Any
from App.api.schemas.shipment import ShipmentCreate,ShipmentRead,ShipmentChange

class Database:
    def conn_to_db(self):
        #Make connetention with database
        self.conn = sqlite3.connect('database.db',check_same_thread=False)
        self.cursor =self.conn.cursor()
        
    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS shipment(
                id INTEGER,
                content TEXT,
                weight REAL,
                status TEXT)
            """)
    
    def insert_shipment(self,shipment : ShipmentCreate) -> int:
        self.cursor.execute("""
                            SELECT MAX(id) FROM shipment
                            """)
        result = self.cursor.fetchone()
        print(f"RESULT!!!!!!!!!!!!!!!!!!!!!! {result}")
        new_id=result[0]+1
        self.cursor.execute("""
                            INSERT INTO shipment VALUES(:new_id,:content,:weight,:status)
                            """,
                            {
                                "new_id":new_id,
                                **shipment.model_dump(),
                                "status" :'placed'
                            }
                            )
        self.conn.commit()

        return new_id

    def get_shipment(self, id: int) -> dict[str, Any] | None:
        self.cursor.execute(
            """
                SELECT id, content, weight, status FROM shipment WHERE id = ?
            """,
            (id,),
        )

        row = self.cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "content": row[1],
            "weight": row[2],
            "status": row[3],
        }

    def update(self,id: int,shipment: ShipmentChange):

        self.cursor.execute("""
        UPDATE shipment SET status =:status
        Where id=:id
        """,
        { "id": id , **shipment.model_dump()}
        )
        self.conn.commit()

        return self.get_shipment(id)

    def Delete(self,id: int):
        self.cursor.execute("""
        DELETE FROM shipment
        Where id=:id
        """,{ "id": id })

        self.conn.commit()

    def close(self):
        self.conn.close()

    def __enter__(self):
        self.conn_to_db()
        self.create_table()
        return self
    
    def __exit__(self, *arg):
        self.close()
        

#context manager
with Database() as db:
    print(db.get_shipment(12701))