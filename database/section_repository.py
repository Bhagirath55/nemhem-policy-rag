import psycopg2


class SectionRepository:

   def __init__(self):
       self.conn = psycopg2.connect(
           host="localhost",
           database="nemhem_db",
           user="postgres",
           password="sana"
       )
       self.cursor = self.conn.cursor()

   def get_section_by_id(self, section_id):
       self.cursor.execute("""
           SELECT full_text
           FROM sections
           WHERE section_id = %s
       """, (section_id,))
       result = self.cursor.fetchone()
       return result[0] if result else None

   def close(self):
       self.cursor.close()
       self.conn.close()


