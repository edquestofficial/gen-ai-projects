import pandas as pd
from sqlalchemy import create_engine

def insertDataToPostgres():
    try:
        # Read CSV files
        df = pd.read_csv('/app/init-db/LEIdata.csv')
        df.columns = [c.lower() for c in df.columns]  # PostgreSQL doesn't like capitals or spaces
        df.rename(columns=lambda x: x.replace(".", "_"), inplace=True)

        df1 = pd.read_csv('/app/init-db/relations.csv')
        df1.columns = [c.lower() for c in df1.columns]  # PostgreSQL doesn't like capitals or spaces
        df1.rename(columns=lambda x: x.replace(".", "_"), inplace=True)

        # Update the database connection URL with the correct hostname, port, username, password, and database name
        engine = create_engine('postgresql://postgres:postgres@db:5432/GLIEF')

        # Insert data into PostgreSQL tables
        df.to_sql("entity_legal_info", engine, if_exists='replace', index=False)
        df1.to_sql("relationship_information", engine, if_exists='replace', index=False)
    except Exception as e:
        # Catch any exceptions that occur during the connection process
        print(f"An error occurred while connecting to the database: {e}")
        return None

if __name__ == "__main__":
    insertDataToPostgres()
