import pandas as pd

def combine(file1, file2):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    df = pd.concat([df1,df2], ignore_index=True)
    print(len(df))
    return df

def gen_col(df, name):
    df.rename(columns={"show_name": "show_name_imdb"}, inplace=True)
    netflix = pd.read_csv('netflix_ambiguous.csv')
    df.show_id = df.show_id.astype(str)
    netflix.show_id = netflix.show_id.astype(str)
    # print(netflix.info())
    # print(df.info())

    df = df.merge(netflix, on='show_id', how='left')
    df['TitlePrefix'] = df['TitlePrefix'].fillna(df['show_name_imdb'])
    df.rename(columns={"TitlePrefix": "show_name_netflix"}, inplace=True)
    df.drop(['genre'],axis=1, inplace=True)
    print(df.head())
    print(df.info())

    df.to_csv(f'{name}_full.csv', index=False)


if __name__ == "__main__":
    # df = combine('show.csv', 'show_amb.csv')
    # gen_col(df, 'show')

    # df = combine('episode.csv', 'episode_amb.csv')
    # gen_col(df, 'episode')
    df = combine('keyword.csv', 'keyword_amb.csv')
    df.to_csv(f'keyword_full.csv', index=False)
    