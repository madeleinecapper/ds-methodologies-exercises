import env
import pandas as pd

select_prop_2016 = '''SELECT prop16.*, pred16.logerror, pred16.transactiondate, 
actype.airconditioningdesc, archtype.architecturalstyledesc, bctype.buildingclassdesc, 
heattype.heatingorsystemdesc, propland.propertylandusedesc,
storytype.storydesc, constype.typeconstructiondesc
	FROM properties_2016 AS prop16
    JOIN predictions_2016 AS pred16
    ON prop16.parcelid = pred16.parcelid
	LEFT JOIN airconditioningtype AS actype 
    ON prop16.airconditioningtypeid = actype.airconditioningtypeid
	LEFT JOIN architecturalstyletype AS archtype
    ON prop16.architecturalstyletypeid = archtype.architecturalstyletypeid
    LEFT JOIN buildingclasstype AS bctype
    ON prop16.buildingclasstypeid = bctype.buildingclasstypeid
    LEFT JOIN  heatingorsystemtype as heattype
    ON prop16.heatingorsystemtypeid = heattype.heatingorsystemtypeid
    LEFT JOIN propertylandusetype AS propland
    ON prop16.propertylandusetypeid = propland.propertylandusetypeid
    LEFT JOIN storytype
    ON prop16.storytypeid = storytype.storytypeid
    LEFT JOIN typeconstructiontype AS constype
    ON prop16.typeconstructiontypeid = constype.typeconstructiontypeid;'''

select_prop_2017 = '''SELECT prop17.*, pred17.logerror, pred17.transactiondate,
actype.airconditioningdesc, archtype.architecturalstyledesc, bctype.buildingclassdesc, 
heattype.heatingorsystemdesc, propland.propertylandusedesc,
storytype.storydesc, constype.typeconstructiondesc
	FROM properties_2017 AS prop17
    JOIN predictions_2017 AS pred17
    ON prop17.parcelid = pred17.parcelid
	LEFT JOIN airconditioningtype AS actype 
    ON prop17.airconditioningtypeid = actype.airconditioningtypeid
	LEFT JOIN architecturalstyletype AS archtype
    ON prop17.architecturalstyletypeid = archtype.architecturalstyletypeid
    LEFT JOIN buildingclasstype AS bctype
    ON prop17.buildingclasstypeid = bctype.buildingclasstypeid
    LEFT JOIN  heatingorsystemtype as heattype
    ON prop17.heatingorsystemtypeid = heattype.heatingorsystemtypeid
    LEFT JOIN propertylandusetype AS propland
    ON prop17.propertylandusetypeid = propland.propertylandusetypeid
    LEFT JOIN storytype
    ON prop17.storytypeid = storytype.storytypeid
    LEFT JOIN typeconstructiontype AS constype
    ON prop17.typeconstructiontypeid = constype.typeconstructiontypeid;'''


def get_connection(db, user=env.user, host=env.host, pw=env.pw):
    return f'mysql+pymysql://{user}:{pw}@{host}/{db}'

def get_prop16():
    return pd.read_sql(select_prop_2016, get_connection('zillow'))

def get_prop17():
    return pd.read_sql(select_prop_2017, get_connection('zillow'))

def get_zillow():
    df = get_prop16()
    df2 = get_prop17()
    df = df.append(df2, ignore_index=True)
    df.drop(columns=['typeconstructiontypeid', 
    'storytypeid','propertylandusetypeid', 
    'heatingorsystemtypeid','buildingclasstypeid', 
    'architecturalstyletypeid','airconditioningtypeid'
    ], inplace=True)
    df = df[~df.latitude.isnull() | ~df.longitude.isnull()]
    df.to_csv('zillow.csv', index=False)
    return df