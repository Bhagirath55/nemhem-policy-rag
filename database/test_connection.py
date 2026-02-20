import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="nemhem_db",
    user="postgres",
    password="sana"
)

cur = conn.cursor()

# Insert Act
cur.execute("""
    INSERT INTO acts (act_id, act_name, year)
    VALUES (%s, %s, %s)
    ON CONFLICT (act_id) DO NOTHING;
""", ("ITA_1961", "Income Tax Act", 1961))

# Insert Section
cur.execute("""
    INSERT INTO sections (
        section_id,
        act_id,
        section_number,
        title,
        full_text,
        effective_from
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (section_id) DO NOTHING;
""", (
    "ITA_80C_2023_v1",
    "ITA_1961",
    "80C",
    "Deduction",
    "Sample legal text",
    "2023-04-01"
))

conn.commit()
cur.close()
conn.close()

print("Check In DB.")