import sqlite3
from datetime import date, datetime

class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect("expenses.db")
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            amount REAL,
            category TEXT,
            cycle TEXT,
            start_date TEXT
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            amount REAL,
            category TEXT,
            date TEXT
        )
        """)
        self.conn.commit()

    def add_subscription(self, data):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO subscriptions (name, amount, category, cycle, start_date)
            VALUES (?, ?, ?, ?, ?)
        """, (data["name"], data["amount"], data["category"], data["cycle"], data["start_date"].isoformat()))
        self.conn.commit()

    def get_all_subscriptions(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM subscriptions")
        rows = cur.fetchall()
        return [{
            "id": row["id"],
            "name": row["name"],
            "amount": row["amount"],
            "category": row["category"],
            "cycle": row["cycle"],
            "start_date": datetime.fromisoformat(row["start_date"]).date()
        } for row in rows]

    def delete_subscription(self, sub_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM subscriptions WHERE id = ?", (sub_id,))
        self.conn.commit()

    def add_expense(self, data):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO expenses (name, amount, category, date)
            VALUES (?, ?, ?, ?)
        """, (data["name"], data["amount"], data["category"], data["date"].isoformat()))
        self.conn.commit()

    def get_all_expenses(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM expenses")
        rows = cur.fetchall()
        return [{
            "id": row["id"],
            "name": row["name"],
            "amount": row["amount"],
            "category": row["category"],
            "date": datetime.fromisoformat(row["date"]).date()
        } for row in rows]

    def delete_expense(self, expense_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.conn.commit()
