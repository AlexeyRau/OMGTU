import pandas as pd

pd.set_option('display.max_columns', None)  # Показывать все столбцы
pd.set_option('display.width', None)  # Позволяет отображать данные без обрезания

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

cabins_from_df1 = df5[df5['name'].isin(df1['Name']) & df5['cabin'].notna()]['cabin'].unique()
people_in_same_cabins = df5[df5['cabin'].isin(cabins_from_df1)]
print('Задание 10')
print(people_in_same_cabins)
print('')

df5['birthyear'] = 1912 - df5['age']
print('Задание 11')
print(df5)
print('')

cabin_counts = df5.groupby('cabin').transform('size')
df5['Companion'] = cabin_counts - 1
print('Задание 12')
print(df5)
print('')

df5.iloc[0], df5.iloc[1] = df5.iloc[1].copy(), df5.iloc[0].copy()
print('Задание 13')
print(df5)
print('')

df5.to_csv('titanic_final.csv', sep=';')
print('Задание 14')
print('Датафрейм сохранен в файл titanic_final.csv')
print('')

top_10_paid = df5.sort_values(by='fare', ascending=False).head(10)
print('Задание 15')
print(top_10_paid)
print('')

survival_by_sex = df5.groupby(['sex', 'survived']).size().unstack()
print('Задание 16')
print(survival_by_sex)
print('')