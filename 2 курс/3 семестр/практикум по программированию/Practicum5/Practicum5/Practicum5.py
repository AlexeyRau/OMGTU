import pandas as pd

data = {
    'Name': ['Strom, Mrs. Wilhelm (Elna Matilda Persson)', 'Navratil, Mr. Michel ("Louis M Hoffman")', 'Minahan, Miss. Daisy E'],
    'Age': [29, 36.5, 33],
    'Sex': ['female', 'male', 'female']
}
df1 = pd.DataFrame(data)
print('Задание 1')
print(df1)
print('')

df2 = pd.read_csv('titanic_csv.csv', delimiter=';')
print('Задание 2')
print(df2)
print('')

url = 'https://gist.githubusercontent.com/zaryanezrya/8b4ef51c707cb16d5e88a44dc00a1bb2/raw/41230f49c6268e072dbf102672f670be256922ab/gistfile1.txt'
df3 = pd.read_csv(url, delimiter=',')
print('Задание 3')
print(df3)
print('')

df2.columns = df2.columns.str.lower()
df4 = pd.concat([df2, df3], ignore_index=True)
df4 = df4.drop_duplicates()
print('Задание 4')
print(df4)
print('')

df5 = df4
df5.set_index('passengerid', inplace=True)
df5.sort_index(inplace=True)
print('Задание 5')
print(df5)
print('')

print('Задание 6')
print('Информация о датафрейме:')
print(df5.info())
print('')
print('Базовая статистика:')
print(df5.describe())
print('')

df5.iloc[0], df5.iloc[2] = df5.iloc[2].copy(), df5.iloc[0].copy()
print('Задание 7')
print(df5)
print('')

df5['sex'] = df5['sex'].map({'female': 'f', 'male': 'm'})
print('Задание 8')
print(df5)
print('')

ticket_counts = df5.groupby('ticket').size()
popular_tickets = ticket_counts[ticket_counts >= 6].index
df9 = df5[df5['ticket'].isin(popular_tickets)]
df9 = df9.sort_values(by='ticket')
print('Задание 9')
print(df9)
print('')

names_from_df1 = df1['Name'].tolist()
cabin_mates = df5[df5['name'].isin(names_from_df1)]
print('Задание 10')
print(cabin_mates)
print('')

df5['birthyear'] = 2023 - df5['age']
print('Задание 11')
print(df5)
print('')

cabin_counts = df5.groupby('Cabin').size()
df5['Companion'] = df5['Cabin'].map(cabin_counts)
print('Задание 12')
print(df5)
print('')