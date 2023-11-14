import psycopg2

# Print connection details
print("Connecting to the PostgreSQL database...")
dbname = "itinero_db"
user = "postgres"
password = ""
host = "localhost"
port = "5432"
print(f"DB Name: {dbname}, User: {user}, Host: {host}, Port: {port}")

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)
print("Connection established successfully.")

# ... (rest of the script remains the same)
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS trips_state (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS trips_city (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        state_id INTEGER,
        FOREIGN KEY (state_id) REFERENCES trips_state(id) ON DELETE CASCADE
    )
''')

# Read the data from the file and insert it into the table
with open('loc.txt', 'r') as file:
    for line in file:
        try:
            state_data = line.strip().split(':')
            state_name = state_data[0].strip()
            cities = [city.strip().strip(",'") for city in state_data[1].strip().strip("[]'").split(",")]

            # Insert state
            cursor.execute('INSERT INTO trips_state (name) VALUES (%s) RETURNING id', (state_name,))
            state_id = cursor.fetchone()[0]

            print(f"State: {state_name} (ID: {state_id})")

            # Insert cities
            for city in cities:
                print(f"City: {city}")
                cursor.execute('INSERT INTO trips_city (name, state_id) VALUES (%s, %s)', (city[:50], state_id))
        except Exception as e:
            print(f"An error occurred: {e}")

# Commit the changes and close the connection
conn.commit()
conn.close()
