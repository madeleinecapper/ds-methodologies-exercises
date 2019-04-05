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
# # binning and value_counts: 
# def value_counts(dataframe):
#     for col in dataframe.drop(columns=('customer_id')):
#         if np.issubdtype(dataframe[col].dtype, np.number) and dataframe[col].nunique() > 10:
#             print(dataframe[col].value_counts(bins=10, sort=False))
#         else: 
#             print(dataframe[col].value_counts(sort=False))


# def handle_missing_values(dataframe):
#     return dataframe.assign(
#         total_charges = dataframe.total_charges.fillna(0)
#     )

# def churn_num(dataframe):
#     return dataframe.assign(
#         churn = dataframe['churn'].map({'No': 0, 'Yes': 1})

#     )

# def tenure_year(dataframe):
#     dataframe['tenure_year'] = (dataframe.tenure / 12).astype(int) + 1
#     return dataframe

# choices_lns = [2, 1, 0]
# choices = [3, 2, 1, 0]

# conditions_secback = [
#     (df['online_security'] == 'Yes') & (df['online_backup'] == 'Yes'),
#     (df['online_security'] == 'No') & (df['online_backup'] == 'Yes'), 
#     (df['online_security'] == 'Yes') & (df['online_backup'] == 'No'),
#     (df['online_security'] == 'No') & (df['online_backup'] == 'No')
#     ]

# conditions_strm = [
#     (df['streaming_tv'] == 'Yes') & (df['streaming_movies'] == 'Yes'),
#     (df['streaming_tv'] == 'No') & (df['streaming_movies'] == 'Yes'), 
#     (df['streaming_tv'] == 'Yes') & (df['streaming_movies'] == 'No'),
#     (df['streaming_tv'] == 'No') & (df['streaming_movies'] == 'No')
# ]

# conditions_pdep = [
#     (df['partner'] == 'Yes') & (df['dependents'] == 'Yes'),
#     (df['partner'] == 'No') & (df['dependents'] == 'Yes'), 
#     (df['partner'] == 'Yes') & (df['dependents'] == 'No'),
#     (df['partner'] == 'No') & (df['dependents'] == 'No')
# ]

# conditions_lns = [
#     (df['phone_service'] == 'Yes') & (df['multiple_lines'] == 'Yes'),
#     (df['phone_service'] == 'Yes') & (df['multiple_lines'] == 'No'),
#     (df['phone_service'] == 'No') & (df['multiple_lines'] == 'No')
# ]

# def conditional_encodes(df):
#     df['phone_id'] = np.select(conditions_lns, choices_lns)
#     df['household_type_id'] = np.select(conditions_pdep, choices)
#     df['streaming_services'] = np.select(conditions_strm, choices)
#     df['secback'] = np.select(conditions_secback, choices)
#     return df


# def prep_telco_data(df):
