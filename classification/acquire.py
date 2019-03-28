import env
import pandas as pd

def get_connection(db, user=env.user, host=env.host, pw=env.pw):
    return f'mysql+pymysql://{user}:{pw}@{host}/{db}'

def get_titanic_data():
    return pd.read_sql('SELECT * FROM passengers', get_connection('titanic_db'))

def get_iris_data():
    return pd.read_sql('SELECT s.species_name, m.* FROM measurements AS m JOIN species AS s ON m.species_id = s.species_id', get_connection('iris_db'))