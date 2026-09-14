import pandas as pd

df = pd.read_csv('data/raw/store-data-6aa6d7a3f171f140353680.csv')

def main():

    print(df.fillna(0))


if __name__ == '__main__':
    main()