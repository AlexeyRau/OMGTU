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