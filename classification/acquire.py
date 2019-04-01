import env
import pandas as pd

def get_connection(db, user=env.user, host=env.host, pw=env.pw):
    return f'mysql+pymysql://{user}:{pw}@{host}/{db}'

def get_titanic_data():
    return pd.read_sql('SELECT * FROM passengers', get_connection('titanic_db'))

def get_iris_data():
    return pd.read_sql('SELECT s.species_name, m.* FROM measurements AS m JOIN species AS s ON m.species_id = s.species_id', get_connection('iris_db'))

selection = '''SELECT c.*, p.payment_type, i.internet_service_type, ctr.contract_type
FROM customers AS c
JOIN payment_types as p
ON p.payment_type_id = c.payment_type_id
JOIN internet_service_types AS i
ON i.internet_service_type_id = c.internet_service_type_id
JOIN contract_types as ctr
ON c.contract_type_id = ctr.contract_type_id;'''

def get_telco_data():
    return pd.read_sql(selection, get_connection('telco_churn'))