#!/usr/bin/python3

from   tkinter import Tk
import re
import sqlite3

text = Tk().clipboard_get()

lexicon = re.findall("\S+", text)
lexicon = [re.sub("[#.:,;!?&]","", item) for item in lexicon]
lexicon = [(item,) for item in lexicon]

print(lexicon)

con    = sqlite3.connect("bewerbungen.db")
cur    = con.cursor()

create = "CREATE TABLE IF NOT EXISTS stellenangebote(id INTEGER PRIMARY KEY, lemma TEXT, zeit DATE DEFAULT(DATETIME('now', 'localtime')))"
insert = "INSERT INTO stellenangebote (lemma) VALUES(?)"

cur.execute(create)

con.commit()

cur.executemany(insert, lexicon)

try:
    drop = "DROP TABLE angebotslexikon"
    cur.execute(drop)
except sqlite3.Error as err:
    print(err)
    print("Tabelle angebotslexikon nicht vorhanden! Wird erstellt!")
    
create = "CREATE TABLE IF NOT EXISTS angebotslexikon(id INTEGER PRIMARY KEY, lemma TEXT, zaehler INTEGER, zeit DATE DEFAULT(DATETIME('now', 'localtime')))"
cur.execute(create)

insert = "INSERT INTO angebotslexikon (lemma, zaehler) SELECT lemma, COUNT(lemma) AS zaehler FROM stellenangebote GROUP BY lemma ORDER BY zaehler desc"
cur.execute(insert)

con.commit()
