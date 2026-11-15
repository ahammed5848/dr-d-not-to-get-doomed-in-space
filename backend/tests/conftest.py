import os
os.environ["TESTING"] = "1"

from app.seed import init_db
init_db()
