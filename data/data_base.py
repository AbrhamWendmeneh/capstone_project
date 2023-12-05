import psycopg2

connect = psycopg2.connect(host="localhost", dbname="rideHealing", user="postgres", password="RH@ab1317", port= 5432)

curs= connect.cursor()


# create users table
curs.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL,
                    fullname TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    role TEXT NOT NULL,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    rating INTEGER
                )
             
             
             """)

# create rides table
curs.execute("""
                CREATE TABLE IF NOT EXISTS rides (
                    ride_id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(user_id) NOT NULL,
                    start_location TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    estimated_arrival_time TIMESTAMP,
                    fare_estimate NUMERIC,
                    status TEXT DEFAULT 'pending'
        
                )
             
             
             """)

# create driver alerts table
curs.execute("""
                CREATE TABLE IF NOT EXISTS driver_alerts (
                    alert_id SERIAL PRIMARY KEY,
                    ride_id INTEGER REFERENCES rides(ride_id) NOT NULL,
                    driver_id INTEGER REFERENCES users(user_id) NOT NULL,
                    alert_type VARCHAR(20) NOT NULL
                    
                )
                
            """)


# create rating_reviews table
curs.execute("""
                CREATE TABLE IF NOT EXISTS rating_reviews (
                    alert_id SERIAL PRIMARY KEY,
                    ride_id INTEGER REFERENCES rides(ride_id) NOT NULL,
                    driver_id INTEGER REFERENCES users(user_id) NOT NULL,
                    alert_type TEXT NOT NULL
                )
             
             
             """)


# create ride_history table
curs.execute("""
                CREATE TABLE IF NOT EXISTS ride_history (
                    history_id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(user_id) NOT NULL,
                    ride_id INTEGER REFERENCES rides(ride_id) NOT NULL,
                    completion_time TIMESTAMP
                )
             
             
             """)



connect.commit()

curs.close()
connect.close()