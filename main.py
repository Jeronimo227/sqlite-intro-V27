#шаг1 создание БД
import sqlite3
from pathlib import Path

folder = Path(__file__).resolve().parent
con = sqlite3.connect(folder / "app.db")

con.execute("""
CREATE TABLE IF NOT EXISTS marathons (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    value INTEGER
)
""")
# name — название марафона;
# category — жанр;
# value — плановое количество страниц.

#шаг2 Заполнение БД
data = [
    ("Классика за неделю: от Пушкина до Толстого", "Классика", 500),
    ("Вокруг света за 52 книги: приключения в литературе", "Фантастика", 100),
    ("Детективы осени", "Детектив", 200),
    ("Магический реализм: погружение в фантазию", "Фэнтези", 450),
    ("Наука через литературу: великие открытия", "Научно-популярное", 150),
    ("Тёмные начала, страшных эпох", "Фантастика", 300),
    ("Мировая поэзия: от античности до наших дней", "Историческая", 750),
    ("Современная проза: новое будущее или устоявшееся прошлое?", "Современная проза", 250),
]

count = con.execute(
    "SELECT COUNT(*) FROM marathons"
).fetchone()[0]

# защита от лишнего заполнения данных
if count == 0:
    con.executemany(
        "INSERT INTO marathons (name, category, value) "
        "VALUES (?, ?, ?)",
        data
    )
    con.commit()

#шаг3
print("Все записи:")
rows = con.execute(
    "SELECT * FROM marathons ORDER BY id"
).fetchall()

for row in rows:
    print(row)

# шаг4 Записи категории «Фантастика»
chosen_category = "Фантастика"
print("\nВыбранная категория — Фантастика:")
rows = con.execute(
    "SELECT * FROM marathons WHERE category = ?",(chosen_category,)
).fetchall()

for row in rows:
    print(row)

# шаг5 Марафоны, где плановое количество страниц больше 200
limit = 200
print(f"\nФильтр: value > {limit}:")
rows = con.execute(
    "SELECT * FROM marathons WHERE value > ?",(limit,)
).fetchall()

for row in rows:
    print(row)

# шаг6 Сортировка по количеству страниц по возрастанию
print("\nСортировка по количеству страниц по возрастанию:")
rows = con.execute(
    "SELECT * FROM marathons ORDER BY value ASC, id ASC"
).fetchall()

for row in rows:
    print(row)

#шаг7 Изменяем количество страниц у марафона id = 2.
record_id = 2
new_value = 220

con.execute(
    "UPDATE marathons SET value = ? WHERE id = ?",(new_value, record_id)
)
con.commit()
print(f"\nБыло новое значение cтраниц = {new_value} и на него мы заменим книгу с id = {record_id}:")
print(f"После изменения записи с id = {record_id}:")
print(con.execute(
    "SELECT * FROM marathons WHERE id = ?",
    (record_id,)
).fetchone())

#шаг8 Удаляем марафон с id = 5.
record_id = 5

con.execute(
    "DELETE FROM marathons WHERE id = ?",
    (record_id,)
)
con.commit()

print("\nПосле удаления записи с id =", record_id, ":")

for row in con.execute("SELECT * FROM marathons ORDER BY id"):
    print(row)

# Закрываем соединение с базой данных.
con.close()