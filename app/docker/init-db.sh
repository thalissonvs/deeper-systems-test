#!/bin/bash

echo "Checking if database needs initialization..."

# Connect to MongoDB and count documents in the users collection
COUNT=$(python -c "from app.database import get_collection; print(get_collection('users').count_documents({}))")

# If there are no users, run the parser to populate the database
if [ "$COUNT" -eq "0" ]; then
    echo "No users found in database. Initializing with data from udata.json..."
    python -m app.parser
    echo "Database initialization completed."
else
    echo "Database already contains $COUNT users. Skipping initialization."
fi

# Start the Flask application
echo "Starting the API server..."
exec python -m flask --app app.server.api run --host=0.0.0.0 --port=5000 