from pandas import DataFrame
from sklearn.preprocessing import LabelEncoder

def prep_iris(df):
    df.drop(columns=['measurement_id', 'species_id'], inplace=True)
    df = df.rename(columns={'species_name': 'species'})
    encoder = LabelEncoder()
    encoder.fit(df.species)
    df['species_encode'] = encoder.transform(df.species)
    return df

def encode_embarked(dft):
    encoder = LabelEncoder()
    encoder.fit(dft.embarked)
    dft['embarked_encode'] = encoder.transform(dft.embarked)
    return dft


def prep_titanic_data(dft):
    dft = dft.assign(embark_town = dft.embark_town.fillna('Other'),
                    embarked = dft.embarked.fillna('O'))
    dft.drop(columns='deck', inplace=True)
    encode_embarked(dft)
    return dft