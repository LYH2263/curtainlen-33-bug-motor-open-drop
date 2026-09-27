from app.db import connect

def get_all():
    c = connect()
    try:
        return {r["key"]: r["value"] for r in c.execute("SELECT key,value FROM settings").fetchall()}
    finally:
        c.close()

def set_values(values: dict):
    c = connect()
    try:
        for k, v in values.items():
            c.execute(
                "INSERT INTO settings(key,value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (k, str(v)),
            )
        c.commit()
    finally:
        c.close()
