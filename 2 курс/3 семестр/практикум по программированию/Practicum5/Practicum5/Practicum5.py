import pandas as pd

# Создаем датафрейм
data = {
    'Name': ['Strom, Mrs. Wilhelm (Elna Matilda Persson)', 'Navratil, Mr. Michel ("Louis M Hoffman")', 'Minahan, Miss. Daisy E'],
    'Age': [29, 36.5, 33],
    'Sex': ['female', 'male', 'female']
}
df1 = pd.DataFrame(data)
print(df1)