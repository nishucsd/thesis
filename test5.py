import sqlite3

conn = sqlite3.connect('test293.db')
c = conn.cursor()

def createtable():
    c.execute('CREATE TABLE IF NOT EXISTS plotme(keyword TEXT)')
def enter():
    c.execute("INSERT INTO plotme VALUES('rtrtrtt')")
    conn.commit()
    c.close()
    conn.close()

createtable()
enter()