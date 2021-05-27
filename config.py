class Config:
    host = "localhost"
    port = '27017'
    database = 'local'
    collection = 'my_collection'

    file_list = ['Odata2019File.csv', 'Odata2020File.csv']
    delimiter = ";"

    int_columns_list = ['Birth', 'UkrBall12', 'UkrBall', 'UkrAdaptScale', 'histBall12',
                        'histBall', 'mathBall12', 'mathBall', 'physBall12', 'physBall', 'chemBall12',
                        'chemBall', 'bioBall12', 'bioBall', 'geoBall12', 'geoBall', 'engBall12', 'engBall',
                        'fraBall12', 'fraBall', 'deuBall12', 'deuBall', 'spaBall12', 'spaBall']
    float_columns_list = ['UkrBall100', 'histBall100', 'mathBall100', 'physBall100', 'chemBall100',
                          'bioBall100', 'geoBall100', 'engBall100', 'fraBall100', 'deuBall100', 'spaBall100']