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