import pandas as pd

def load_government_jobs():
    df = pd.read_csv('../data/government_jobs.csv')
    return df.to_dict('records')