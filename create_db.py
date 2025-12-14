import pymysql

# Datenbank erstellen
try:
    conn = pymysql.connect(host='localhost', user='root', password='root')
    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS benchmark_db')
    print("✅ Datenbank 'benchmark_db' wurde erfolgreich erstellt!")
    conn.close()
except Exception as e:
    print(f"❌ Fehler: {e}")
    print("Ist MySQL Server gestartet? Überprüfe user/password!")