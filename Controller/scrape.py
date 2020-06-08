import pandas as pd

def print_texts():
    df = pd.read_json(r'scraped_results.json')
    print(df)
    df.to_csv('test.csv')

    csv_file = pd.read_csv(r'test.csv')
    print(csv_file['texts'][3])

print_texts()
