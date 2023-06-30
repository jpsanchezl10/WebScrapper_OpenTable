import sqlite3

# Connect to the SQLite database 1
conn1 = sqlite3.connect("concierge.db")
cursor1 = conn1.cursor()

#connect to db 2
conn2 = sqlite3.connect("concierge-uppercase.db")
cursor2 = conn2.cursor()


def Create_Table():
    # SQLite command to create the restaurants table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_name TEXT,
            restaurant_rating TEXT,
            restaurant_price TEXT,
            restaurant_phone TEXT,
            restaurant_location TEXT,
            restaurant_style TEXT,
            restaurant_rank TEXT,
            restaurant_email TEXT,
            restaurant_url TEXT,
            restaurant_map TEXT,
            restaurant_hours TEXT,
            restaurant_image TEXT
        )
    '''

    # Execute the create table command
    cursor2.execute(create_table_query)

    # Commit the changes and close the connection
    conn2.commit()

#get restaurn info into array
def get_rest(id):
    array = []
    # Execute the SQLite query
    cursor1.execute(f"SELECT * FROM restaurants WHERE id = {id}")

    # Fetch the result
    result = cursor1.fetchone()

    # Extract the first parameter from the result

    for item in result:
        array.append(str(item))
    return array


#restaurant id
rest_id = 1
def insert_rest(rest_id):
    #init array
    restaurant_item = []

    #isert into new array
    restaurant_item = get_rest(rest_id)

    #insert values from old db to new db in upper case exept from urls
    cursor2.execute("INSERT INTO restaurants (restaurant_name, restaurant_rating, restaurant_price, restaurant_phone, restaurant_location, restaurant_style, restaurant_rank, restaurant_email, restaurant_url, restaurant_map, restaurant_hours, restaurant_image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (restaurant_item[1].upper(),restaurant_item[2].upper(),restaurant_item[3].upper(), restaurant_item[4].upper(), restaurant_item[5].upper(), restaurant_item[6].upper(), restaurant_item[7].upper(), restaurant_item[8],restaurant_item[9],restaurant_item[10], restaurant_item[11].upper(),restaurant_item[12] ))
  
            # Commit the changes to the database
        

    conn2.commit()

Create_Table()

#GETS THE HIGHEST ID FROM THE DB    
def get_highest_id():
    # Execute the SELECT statement to retrieve the highest ID
    cursor1.execute("SELECT MAX(id) FROM restaurants")
    # Fetch the result
    result = cursor1.fetchone()
    # Extract the highest ID from the result
    highest_id = result[0]
    return highest_id


roof = get_highest_id()
print(roof, "this is roof")

for i in range(1,roof+1):
    insert_rest(i)

