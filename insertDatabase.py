import sqlite3
import json

# Function to establish DB connection and execute query
def db_connection(query, params=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
   
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
   
    # Commit changes and close connection
    conn.commit()
    conn.close()




# Class to add JSON data dynamically to a specified table
class Add_Json():
    def __init__(self, json_data):
        # Parse the input JSON data
        self.json_data = json_data
        self.table_name = json_data.get('table_name')
        self.data = json_data.get('data')
       
        # Generate dynamic SQL query to insert the data into the table
        if self.table_name and self.data:
            self.generate_insert_query()

    def generate_insert_query(self):
        # Extract columns and values from the 'data' dictionary
        columns = ', '.join(self.data.keys())
        placeholders = ', '.join(['?' for _ in self.data])
        values = tuple(self.data.values())
       
        # Construct the SQL query
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
       
        # Execute the query using the db_connection function
        db_connection(query, values)
        print(f"Data inserted into {self.table_name} table.")


# Example Usage:
# Simulate receiving dynamic JSON data (from API, file, etc.)
json_input = '''{
    "table_name": "users",
    "data": {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "age": 30
    }
}'''

# Convert the JSON string to a Python dictionary
json_data = json.loads(json_input)

# Create an instance of Add_Json and insert data
add_json = Add_Json(json_data)