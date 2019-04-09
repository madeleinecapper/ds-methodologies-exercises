def groom_singles(dfz):
    single_cats = ['Single Family Residential', 'Mobile Home', 'Manufactured, Modular, Prefabricated Homes', 'Residential General', 'Townhouse']
    dfz[['propertylandusedesc', 'unitcnt']][dfz.propertylandusedesc.isin(single_cats)]
    dfz = dfz.assign(unitcnt = dfz.unitcnt.fillna(0))
    dfz = dfz[(dfz.propertylandusedesc.isin(single_cats)) & dfz.unitcnt.isin([0,1])]
    dfz = dfz[~(dfz.bathroomcnt == 0) & ~(dfz.bedroomcnt == 0)]
    return dfz()

