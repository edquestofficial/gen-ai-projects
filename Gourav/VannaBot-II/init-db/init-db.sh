#!/bin/bash

DB_FLAG_FILE="/var/lib/postgresql/data/.db_initialized"
VANNA_FLAG_FILE="/var/lib/postgresql/data/.vanna_initialized"

# Check if the flag file exists
if [ ! -f "$DB_FLAG_FILE" ]; then
  echo "Initializing database..."
  
  # Call the Python script to initialize the database
  python3 /app/init-db/init_db.py
  
  # Create the flag file to indicate that initialization has been done
  mkdir -p /var/lib/postgresql/data
  touch "$DB_FLAG_FILE"
  echo "Database initialized."
fi

# Check if the Vanna model has been initialized
if [ ! -f "$VANNA_FLAG_FILE" ]; then
  echo "Initializing Vanna model..."
  
  # Run the Vanna initialization script
  python3 /app/app/vanna_init.py
  
  # Create the flag file to indicate that Vanna initialization has been done
  touch "$VANNA_FLAG_FILE"
  echo "Vanna model initialized."
fi

# Continue with the normal entrypoint script
exec "$@"
