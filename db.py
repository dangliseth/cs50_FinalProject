from sqlalchemy import create_engine, Table, MetaData

engine = create_engine("mysql+mysqlconnector://root:root@localhost/cs50")

def get_table(table_name: str):
    return Table(table_name, MetaData(), autoload_with=engine)