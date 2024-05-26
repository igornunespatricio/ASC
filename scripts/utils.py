import pandas as pd
import sqlite3


def store_in_database(df: pd.DataFrame, database_path:str, table_name:str) -> None:
    
    # open connection to database
    conn = sqlite3.connect(database_path)

    # save dataframe to sql lite database
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # close connection to database
    conn.close()
    
def read_table_from_database(database_path:str, table_name:str):
    conn = sqlite3.connect(database_path)

    # load table from database
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

    # close database connection
    conn.close()
    
    return df

def main():
    print(
        read_table_from_database(
            database_path='../data/asc.db',
            table_name='results'
        )
    )

if __name__ == '__main__':
    main()