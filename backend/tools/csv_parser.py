import pandas as pd


def parse_csv(filename):
    df = pd.read_csv(filename)
    data = df.to_dict('records')
    return data
