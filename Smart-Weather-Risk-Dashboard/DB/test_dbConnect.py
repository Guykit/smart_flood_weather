from connection import connect_database

conn = connect_database()

print("เชื่อมได้ละ")
      
conn.close()
