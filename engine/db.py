#                                   ----- Database Code -----
import sqlite3
import csv

#                                   --- building connection --- 
con = sqlite3.connect("jarvis.db")

#                                          --- cursor --- 
cursor = con.cursor()

#                                  --- create a table sys_command --- 
query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

#                                  --- create a table web_command --- 
query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)

#                                  --- create a contact table --- 
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')

#                                  ---  insert into table --- 

# --- sys_command table entries: --- 
# cursor.execute("INSERT INTO sys_command VALUES (null,'telegram', 'C:\\Users\\bodhi\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe')")
# cursor.execute("INSERT INTO sys_command VALUES (null,'calculator', 'C:\\Windows\\System32\\calc.exe')")
# cursor.execute("INSERT INTO sys_command VALUES (null,'msPaint', 'c:\\Windows\\System32\\mspaint.exe')")
# cursor.execute("INSERT INTO sys_command VALUES (null,'spotify', 'C:\\Users\\bodhi\\AppData\\Roaming\\Spotify\\Spotify.exe')")
# con.commit()  # saving the data on db upto this instance


# --- web_command table entries: --- 
# cursor.execute("INSERT INTO web_command VALUES (null,'facebook', 'https://www.facebook.com/')")
# cursor.execute("INSERT INTO web_command VALUES (null,'instagram', 'https://www.instagram.com/')")
# cursor.execute("INSERT INTO web_command VALUES (null,'flipkart', 'https://www.flipkart.com/')")
# cursor.execute("INSERT INTO web_command VALUES (null,'amazon', 'https://www.amazon.in/')")
# cursor.execute("INSERT INTO web_command VALUES (null,'netflix', 'https://www.netflix.com/')")
# cursor.execute("INSERT INTO web_command VALUES (null,'hotstar', 'https://www.hotstar.com/in')")
# cursor.execute("INSERT INTO web_command VALUES (null,'amazon prime', 'https://www.hotstar.com/in')")
# cursor.execute("INSERT INTO web_command VALUES (null,'mail', 'https://mail.google.com/mail/')")
# cursor.execute("INSERT INTO web_command VALUES (null,'maps', 'https://www.google.co.in/maps/')")
# cursor.execute("INSERT INTO web_command VALUES (null,'google news', 'https://news.google.com/')")
# cursor.execute("INSERT INTO web_command VALUES (null,'google photos', 'https://photos.google.com/')")
# cursor.execute("INSERT INTO web_command VALUES (null,'google calendar', 'https://calendar.google.com/calendar/')")
# cursor.execute("INSERT INTO web_command VALUES (null,'google documents', 'https://docs.google.com/document/')")
# cursor.execute("INSERT INTO web_command VALUES (null,'google spreadsheets', 'https://docs.google.com/spreadsheets/')")

# con.commit()  # saving the data on db upto this instance


# --- importing contacts and inserting into contacts table---
# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 32]

# # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

## Commit changes and close connection
# con.commit()
# con.close()


#                           --- Search contacts from database ---
# query = 'Sriza'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])

#                           ------ Adding email of contacts ---------
# cursor.execute('''UPDATE contacts SET email = 'shu7773sea@gmail.com' WHERE id = 13''')
# con.commit()



# ---------------------- Entering phone number and email in contacts -----------------------------
# desired_columns_indices = [0, 32, 30]
# # # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no','email') VALUES (null, ?, ?, ?);''', tuple(selected_data))

# ##Commit changes and close connection
# con.commit()
# con.close()