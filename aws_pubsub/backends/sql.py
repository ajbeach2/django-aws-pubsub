import sqlite3
import time

from .base import BackendWrapperBase


class BackendWrapper(BackendWrapperBase):
    def __init__(self, limit=10, timeout=60, poll_interval=5):
        self.limit = limit
        self.poll_interval = poll_interval
        self.timeout = timeout
        self.conn = sqlite3.connect("queue.db")
        self.c = self.conn.cursor()
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS queue (
                id INTEGER PRIMARY KEY,
                task TEXT NOT NULL,
                processing BOOLEAN NOT NULL,
                message TEXT NOT NULL,
                lastupdated INTEGER NOT NULL,
                count INTEGER DEFAULT 0
            );
           """
        )
        self.conn.commit()

    def queue_name(self):
        return "queue"

    def expire(self):
        self.c.execute(
            """
                DELETE FROM queue
                where (lastupdated - :lastupdated) > :timeout
                and processing = 'true'
                or count > 10
            """,
            {"lastupdated": int(time.time()), "timeout": self.timeout},
        )
        self.conn.commit()

    def send_task(self, messages, task_name, delay=None):
        for message in self.prepare_messages(messages, task_name, delay=delay):
            self.c.execute(
                """
                    INSERT into queue (task,processing, message, lastupdated)
                    VALUES(?, 'false', ?, ?);""",
                (task_name, message["MessageBody"], int(time.time())),
            )
            self.conn.commit()

    def recieve(self):
        self.expire()
        time.sleep(self.poll_interval)
        self.c.execute(
            """
            SELECT * from queue where processing = 'false' limit ?;
            """,
            (self.limit,),
        )
        rows = self.c.fetchall()
        ids = [x[0] for x in rows]

        self.c.execute(
            "UPDATE queue SET processing = 'true', count = count + 1 where id in (%s);"
            % ",".join("?" * len(ids)),
            ids,
        )
        self.conn.commit()

        return [{"MessageId": m[0], "ReceiptHandle": m[0], "Body": m[3],} for m in rows]

    def ack_messages(self, receipts):
        self.c.execute(
            "DELETE FROM queue where id in (%s);" % ",".join("?" * len(receipts)),
            receipts,
        )
        self.conn.commit()

    def query(self, query):
        self.c.execute(query)
        print(self.c.fetchall())
