FROM python:3.12
# Use a Python base image

# Install necessary packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip3 install pipenv

# Copy Pipfile and Pipfile.lock (if it exists)
COPY Pipfile /app/
COPY Pipfile.lock /app/

# Set the working directory
WORKDIR /app

# Install dependencies using pipenv
RUN if [ -f Pipfile.lock ]; then pipenv install --deploy --ignore-pipfile; else pipenv install; fi

# Install additional dependencies for init scripts
RUN pipenv run pip3 install pandas vanna

# Copy the initialization scripts, CSV files, and Flask app
COPY init-db/ /app/init-db/
COPY app/ /app/app/
COPY start.sh /app/start.sh
COPY init-db/LEIdata.csv /app/LEIdata.csv
COPY init-db/relations.csv /app/relations.csv

# Copy the API key file
COPY Key/API_KEY.txt /app/Key/API_KEY.txt

# Ensure the entrypoint script is executable
RUN chmod +x /app/init-db/init-db.sh /app/start.sh

# Set the entrypoint to bash and use CMD to run the startup script
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["./start.sh"]
