# Объяснение лабораторной работы №3
## Эволюционная программа «Искусственный муравей»

---

## Общая идея работы

Представьте муравья, который ходит по клетчатому полю 32×32 и собирает еду. Мы не пишем для него жёсткие правила — вместо этого мы запускаем **эволюцию**: создаём сотню случайных «мозгов» для муравья, проверяем, у кого получается собрать больше еды, скрещиваем лучших, вносим случайные изменения — и повторяем это 150 раз. Так, через естественный отбор, мозг муравья постепенно становится умнее.

«Мозг» муравья — это **конечный автомат**: таблица правил вида «если я нахожусь в состоянии №2 и вижу еду впереди — повернуть направо и перейти в состояние №0».

---

## Раздел 1. Импорт библиотек

```python
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
from copy import deepcopy

random.seed(42)
np.random.seed(42)
```

Здесь мы подключаем готовые инструменты:

- `numpy` — библиотека для работы с массивами чисел (наше поле — это как раз двумерный массив).
- `random` — встроенный генератор случайных чисел Python.
- `matplotlib` и всё что из него — инструменты для рисования графиков и анимаций.
- `deepcopy` — функция для создания **полной независимой копии** объекта. Это важно: обычное копирование в Python создаёт «ссылку» на тот же объект, а не новый объект. `deepcopy` создаёт именно новый, чтобы изменения в копии не затронули оригинал.

Последние две строки — `random.seed(42)` и `np.random.seed(42)` — устанавливают **начальное значение** генератора случайных чисел. Это нужно для **воспроизводимости**: если запустить программу ещё раз с тем же seed, то все «случайные» числа будут теми же самыми, и результат будет одинаковым. Число 42 — просто традиция, можно использовать любое.

---

## Раздел 2. Модель поля и движение муравья

### 2.1 Константы — описание мира

```python
EMPTY = 0
FOOD  = 1
WALL  = 2

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

ACT_FORWARD   = 0
ACT_TURN_LEFT = 1
ACT_TURN_RIGHT= 2

ACTION_NAMES = {ACT_FORWARD: 'Forward', ACT_TURN_LEFT: 'Left', ACT_TURN_RIGHT: 'Right'}
```

Здесь задаются константы — числа с понятными именами, чтобы в коде не писать загадочные `0`, `1`, `2`, а писать `FOOD`, `WALL`, `EMPTY`.

**Типы клеток:**
- `EMPTY = 0` — пустая клетка.
- `FOOD = 1` — клетка с едой.
- `WALL = 2` — стена, непроходимое препятствие.

**Направления** — список пар `(dr, dc)`, где `dr` — изменение строки, `dc` — изменение столбца при шаге:
- Индекс 0: `(-1, 0)` — вверх (строка уменьшается на 1).
- Индекс 1: `(0, 1)` — вправо (столбец увеличивается на 1).
- Индекс 2: `(1, 0)` — вниз (строка увеличивается на 1).
- Индекс 3: `(0, -1)` — влево (столбец уменьшается на 1).

Порядок именно такой (по часовой стрелке), что позволит легко делать повороты: поворот направо = `(direction + 1) % 4`, налево = `(direction - 1) % 4`.

**Действия** муравья — три возможных поступка на каждом шаге:
- `ACT_FORWARD = 0` — шаг вперёд.
- `ACT_TURN_LEFT = 1` — повернуться налево (без шага).
- `ACT_TURN_RIGHT = 2` — повернуться направо (без шага).

`ACTION_NAMES` — просто словарь для читаемого вывода в таблице в конце.

---

### 2.2 Генерация поля — `generate_field`

```python
def generate_field(grid_size=32, food_density=0.2, wall_density=0.05, seed=0):
    rng = np.random.RandomState(seed)
    field = np.zeros((grid_size, grid_size), dtype=np.int8)

    for r in range(grid_size):
        for c in range(grid_size):
            if r == 0 and c == 0:
                continue
            roll = rng.random()
            if roll < wall_density:
                field[r, c] = WALL
            elif roll < wall_density + food_density:
                field[r, c] = FOOD

    field[0, 1] = EMPTY
    field[1, 0] = EMPTY

    return field
```

Эта функция создаёт случайное игровое поле. Разберём построчно.

`def generate_field(grid_size=32, food_density=0.2, wall_density=0.05, seed=0):`
— объявление функции с параметрами по умолчанию. Если при вызове не передать аргументы, будет использоваться поле 32×32, 20% еды, 5% стен.

`rng = np.random.RandomState(seed)`
— создаём **отдельный** генератор случайных чисел, привязанный к конкретному `seed`. Это позволяет поле генерировать независимо от других случайных чисел в программе: одинаковый `seed` → одинаковое поле каждый раз.

`field = np.zeros((grid_size, grid_size), dtype=np.int8)`
— создаём двумерный массив 32×32, заполненный нулями. `dtype=np.int8` означает, что каждый элемент — целое число от -128 до 127 (нам нужны только 0, 1, 2 — этого достаточно, экономим память).

`for r in range(grid_size):` и `for c in range(grid_size):`
— двойной цикл: перебираем каждую строку `r` и каждый столбец `c`, то есть проходим по каждой клетке поля.

`if r == 0 and c == 0: continue`
— пропускаем клетку (0, 0) — это стартовая позиция муравья, она должна быть пустой. `continue` означает «перейти к следующей итерации цикла».

`roll = rng.random()`
— бросаем «кубик»: получаем случайное число от 0.0 до 1.0 для этой клетки.

```python
if roll < wall_density:
    field[r, c] = WALL
elif roll < wall_density + food_density:
    field[r, c] = FOOD
```
— логика заполнения:
- Если число попало в диапазон от 0 до 0.05 (5% вероятность) — клетка становится стеной.
- Если попало в диапазон от 0.05 до 0.25 (20% вероятность) — клетка становится едой.
- Иначе — клетка остаётся пустой (это уже установлено, ведь мы начали с нулей).

`field[0, 1] = EMPTY` и `field[1, 0] = EMPTY`
— принудительно делаем пустыми две клетки рядом со стартом. Это гарантирует, что муравей с первого же шага не упрётся в стену.

`return field`
— возвращаем готовое поле.

---

### 2.3 Сенсор муравья — `sense_ahead`

```python
def sense_ahead(field, row, col, direction, grid_size):
    dr, dc = DIRECTIONS[direction]
    nr = (row + dr) % grid_size
    nc = (col + dc) % grid_size
    return int(field[nr, nc])
```

Эта крошечная функция отвечает на вопрос: **что находится прямо перед муравьём?** Это единственная информация, которую муравей получает о мире на каждом шаге.

`dr, dc = DIRECTIONS[direction]`
— берём смещение для текущего направления. Например, если `direction = 1` (вправо), то `dr = 0, dc = 1`.

`nr = (row + dr) % grid_size`
`nc = (col + dc) % grid_size`
— вычисляем координаты клетки впереди. Операция `% grid_size` — это взятие остатка от деления, которое реализует **тороидальное поле**: если муравей стоит у правого края и смотрит вправо, `nc` «перепрыгнет» на левый край (31 + 1 = 32, 32 % 32 = 0).

`return int(field[nr, nc])`
— возвращаем тип клетки впереди: 0 (EMPTY), 1 (FOOD) или 2 (WALL).

---

### 2.4 Симуляция одного прохода муравья — `simulate_ant`

```python
def simulate_ant(field_in, automaton, max_steps, grid_size=32):
    field = field_in.copy()
    row, col = 0, 0
    direction = 1
    state = 0
    food_collected = 0
    path = [(row, col)]
```

Это главная функция движения. Она запускает муравья на поле и возвращает результат.

`field = field_in.copy()`
— создаём **копию** поля. Важно! Муравей будет «съедать» еду (заменять FOOD → EMPTY). Копируя поле, мы защищаем исходник, чтобы следующий муравей получал ту же карту.

`row, col = 0, 0` — начальная позиция: строка 0, столбец 0 (левый верхний угол).

`direction = 1` — муравей изначально смотрит вправо (индекс 1 в списке DIRECTIONS).

`state = 0` — автомат начинает в состоянии №0.

`food_collected = 0` — счётчик собранной еды.

`path = [(row, col)]` — список всех посещённых клеток. Начинаем с начальной позиции.

```python
    for _ in range(max_steps):
        sensor = sense_ahead(field, row, col, direction, grid_size)
        action, new_state = automaton.transition(state, sensor)
        state = new_state
```

`for _ in range(max_steps):` — основной цикл: повторяем `max_steps` раз. Знак `_` вместо переменной — соглашение, означающее «номер итерации нам не нужен».

`sensor = sense_ahead(...)` — спрашиваем: что впереди? Получаем 0, 1 или 2.

`action, new_state = automaton.transition(state, sensor)` — «мозг» муравья (автомат) принимает решение: смотрим в таблицу переходов, получаем пару (что делать, в какое состояние перейти).

`state = new_state` — обновляем текущее состояние автомата.

```python
        if action == ACT_TURN_LEFT:
            direction = (direction - 1) % 4
        elif action == ACT_TURN_RIGHT:
            direction = (direction + 1) % 4
        else:  # ACT_FORWARD
            dr, dc = DIRECTIONS[direction]
            nr = (row + dr) % grid_size
            nc = (col + dc) % grid_size
            if field[nr, nc] != WALL:
                row, col = nr, nc
                if field[row, col] == FOOD:
                    food_collected += 1
                    field[row, col] = EMPTY
```

Выполняем действие:

- **Поворот налево**: `(direction - 1) % 4`. Если были направлены вправо (1), станем направлены вверх (0). `% 4` обеспечивает «кольцо»: из 0 можно уйти в 3 (влево).
- **Поворот направо**: `(direction + 1) % 4`. Аналогично.
- **Шаг вперёд**: вычисляем клетку впереди. Если там **не стена** — переходим туда. Если на новой клетке **еда** — увеличиваем счётчик на 1 и убираем еду (ставим 0).

Заметьте: если впереди стена, муравей **остаётся на месте**. Он не прыгает через стену и не исчезает — просто теряет один шаг.

```python
        path.append((row, col))

    return food_collected, path
```

`path.append((row, col))` — записываем текущую позицию в маршрут (даже если муравей никуда не двинулся из-за стены).

В конце возвращаем два значения: количество еды и весь пройденный путь.

---

## Раздел 3. Конечный автомат — «мозг» муравья

### 3.1 Что такое конечный автомат

Конечный автомат — это таблица правил. Строки таблицы — состояния (например, «ищу еду», «обхожу стену», «двигаюсь вперёд»). Столбцы — что видит муравей (EMPTY, FOOD, WALL). В каждой ячейке — инструкция: что сделать и в какое состояние перейти.

Пример таблицы с 2 состояниями:

| Состояние | Вижу EMPTY       | Вижу FOOD        | Вижу WALL        |
|-----------|-----------------|-----------------|-----------------|
| s0        | Вперёд → s0     | Вперёд → s0     | Повернуть L → s1 |
| s1        | Повернуть R → s0 | Вперёд → s0     | Повернуть L → s1 |

Это и есть «мозг» — минималистичная программа без памяти о прошлом, только текущее состояние + то, что видишь.

### 3.2 Класс `FiniteAutomaton`

```python
N_INPUTS = 3
N_ACTIONS = 3

class FiniteAutomaton:
    def __init__(self, n_states, table):
        self.n_states = n_states
        self.table = table
        self.fitness = None

    def transition(self, state, sensor):
        return self.table[state][sensor]

    def __repr__(self):
        return f"FiniteAutomaton(n_states={self.n_states}, fitness={self.fitness})"
```

`N_INPUTS = 3` — три возможных сенсорных входа (EMPTY, FOOD, WALL).
`N_ACTIONS = 3` — три возможных действия.

`class FiniteAutomaton:` — объявляем класс, то есть шаблон для создания объектов-автоматов.

`def __init__(self, n_states, table):` — конструктор: код, который запускается при создании нового автомата.
- `self.n_states = n_states` — запоминаем количество состояний.
- `self.table = table` — запоминаем таблицу переходов. Это список списков кортежей: `table[состояние][вход] = (действие, следующее_состояние)`.
- `self.fitness = None` — поле для хранения «оценки» этого автомата. Пока неизвестна.

`def transition(self, state, sensor):` — метод «сделать шаг автомата».
`return self.table[state][sensor]` — просто ищем в таблице: строка = текущее состояние, столбец = что видим. Возвращаем пару (действие, следующее состояние).

`def __repr__(self):` — метод для отображения объекта в виде строки (например, при выводе в консоль).

---

### 3.3 Случайный автомат — `random_automaton`

```python
def random_automaton(n_states):
    table = [
        [
            (random.randint(0, N_ACTIONS - 1), random.randint(0, n_states - 1))
            for _ in range(N_INPUTS)
        ]
        for _ in range(n_states)
    ]
    return FiniteAutomaton(n_states, table)
```

Создаёт автомат с абсолютно случайными правилами — с него начинается каждая особь в популяции.

`table = [...]` — строим таблицу через **генераторные выражения** (компактный способ создать список в Python).

Внешний цикл `for _ in range(n_states)` — создаём строку для каждого состояния.

Внутренний цикл `for _ in range(N_INPUTS)` — для каждого из трёх входов создаём ячейку.

`(random.randint(0, N_ACTIONS - 1), random.randint(0, n_states - 1))` — каждая ячейка — случайная пара: случайное действие (0, 1 или 2) и случайное следующее состояние (от 0 до n_states-1).

---

### 3.4 Мутация — `mutate_automaton`

```python
def mutate_automaton(automaton, mutation_rate=0.1,
                      add_state_prob=0.02, del_state_prob=0.02,
                      min_states=2, max_states=12):
    fa = deepcopy(automaton)
    n = fa.n_states
```

`fa = deepcopy(automaton)` — создаём полную независимую копию, чтобы не испортить исходный автомат. Все изменения будем делать в копии.

`n = fa.n_states` — запоминаем текущее число состояний.

```python
    for s in range(n):
        for inp in range(N_INPUTS):
            if random.random() < mutation_rate:
                act = random.randint(0, N_ACTIONS - 1)
                nxt = random.randint(0, n - 1)
                fa.table[s][inp] = (act, nxt)
```

**Точечные мутации:** проходим по каждой ячейке таблицы. `random.random()` возвращает число от 0 до 1. Если оно меньше `mutation_rate` (12%), то ячейка мутирует: в ней случайно меняется действие и/или следующее состояние. Это как случайная «опечатка» в генетическом коде.

```python
    if n < max_states and random.random() < add_state_prob:
        new_row = [(random.randint(0, N_ACTIONS - 1), random.randint(0, n))
                   for _ in range(N_INPUTS)]
        fa.table.append(new_row)
        fa.n_states += 1
```

**Добавление состояния:** с вероятностью 2%, если автомат ещё не достиг максимума (12 состояний), добавляем новую строку в таблицу — это расширяет «словарный запас» поведения.

```python
    elif n > min_states and random.random() < del_state_prob:
        idx = random.randint(1, n - 1)
        fa.table.pop(idx)
        fa.n_states -= 1
        new_n = fa.n_states
        for s in range(new_n):
            for inp in range(N_INPUTS):
                act, nxt = fa.table[s][inp]
                if nxt >= new_n:
                    nxt = random.randint(0, new_n - 1)
                fa.table[s][inp] = (act, nxt)
```

**Удаление состояния:** с вероятностью 1.5%, если состояний больше минимума (2), удаляем случайное состояние (не стартовое — поэтому `randint(1, n-1)`).

`fa.table.pop(idx)` — удаляем строку из таблицы.

Затем — важный шаг: некоторые ячейки могли ссылаться на только что удалённое состояние. Проходим по всей таблице и если встречаем ссылку `nxt >= new_n` (то есть на несуществующее теперь состояние) — заменяем её на случайное существующее.

`fa.fitness = None` — сбрасываем оценку: автомат изменился, старая оценка больше не актуальна.

---

### 3.5 Кроссовер — `crossover_automata`

```python
def crossover_automata(fa1, fa2):
    n = min(fa1.n_states, fa2.n_states)

    table1, table2 = [], []
    for s in range(n):
        if random.random() < 0.5:
            table1.append(deepcopy(fa1.table[s]))
            table2.append(deepcopy(fa2.table[s]))
        else:
            table1.append(deepcopy(fa2.table[s]))
            table2.append(deepcopy(fa1.table[s]))
```

Кроссовер — скрещивание двух родительских автоматов для получения двух дочерних.

`n = min(fa1.n_states, fa2.n_states)` — берём минимальное число состояний из двух родителей, чтобы оба потомка имели корректные таблицы.

Цикл по состояниям: для каждой строки таблицы подбрасываем монетку. С вероятностью 50% потомок №1 получает строку от родителя №1 (а потомок №2 — от родителя №2), и наоборот. Это **однородный кроссовер**: каждая строка независимо берётся от одного из родителей.

```python
    def fix(table, max_s):
        for s in range(len(table)):
            for inp in range(N_INPUTS):
                act, nxt = table[s][inp]
                if nxt >= max_s:
                    nxt = random.randint(0, max_s - 1)
                table[s][inp] = (act, nxt)

    fix(table1, n)
    fix(table2, n)

    return FiniteAutomaton(n, table1), FiniteAutomaton(n, table2)
```

`fix` — вспомогательная функция внутри `crossover_automata`. Проверяет и исправляет ссылки на несуществующие состояния (та же проблема, что и при удалении состояния в мутации).

В конце возвращаем **двух** новых потомков.

---

## Раздел 4. Параметры алгоритма

```python
GRID_SIZE     = 32
FOOD_DENSITY  = 0.20
WALL_DENSITY  = 0.05
FIELD_SEED    = 7
MAX_STEPS     = 500

POP_SIZE       = 100
N_GENERATIONS  = 150
INIT_STATES    = 4
ELITISM_K      = 5
TOURNAMENT_K   = 4
MUTATION_RATE  = 0.12
CROSSOVER_PROB = 0.70
ADD_STATE_PROB = 0.02
DEL_STATE_PROB = 0.015
```

Все настройки собраны в одном месте для удобства.

**Параметры поля:**
- Поле 32×32, 20% клеток содержат еду, 5% — стены.
- `FIELD_SEED = 7` — фиксирует случайность генерации поля: одно и то же поле при каждом запуске.
- `MAX_STEPS = 500` — каждый муравей делает не более 500 шагов.

**Параметры эволюции:**
- `POP_SIZE = 100` — в каждом поколении 100 автоматов.
- `N_GENERATIONS = 150` — всего 150 поколений.
- `INIT_STATES = 4` — начинаем с автоматов, у каждого по 4 состояния.
- `ELITISM_K = 5` — 5 лучших автоматов переходят в следующее поколение без изменений.
- `TOURNAMENT_K = 4` — при отборе родителей сравниваем 4 случайных кандидата.
- `MUTATION_RATE = 0.12` — каждая ячейка таблицы мутирует с вероятностью 12%.
- `CROSSOVER_PROB = 0.70` — 70% шанс применить кроссовер; иначе потомок — просто мутированная копия одного родителя.

---

## Раздел 5. Эволюционный алгоритм

### 5.1 Оценка особи — `evaluate` и `evaluate_population`

```python
def evaluate(automaton, field, max_steps=MAX_STEPS, grid_size=GRID_SIZE):
    food, _ = simulate_ant(field, automaton, max_steps, grid_size)
    automaton.fitness = food
    return food
```

`food, _ = simulate_ant(...)` — запускаем симуляцию. `simulate_ant` возвращает два значения: количество еды и путь. Знак `_` означает «второе значение нам здесь не нужно, игнорируем».

`automaton.fitness = food` — записываем результат прямо в объект автомата.

```python
def evaluate_population(population, field):
    for ind in population:
        if ind.fitness is None:
            evaluate(ind, field)
```

Проходим по всем особям. Строчка `if ind.fitness is None` — важная оптимизация: если особь уже оценена (например, это элита из прошлого поколения), не гоняем симуляцию заново.

---

### 5.2 Турнирный отбор — `tournament_select`

```python
def tournament_select(population, k=TOURNAMENT_K):
    contestants = random.sample(population, min(k, len(population)))
    return max(contestants, key=lambda ind: ind.fitness)
```

Это механизм выбора родителей для следующего поколения.

`random.sample(population, min(k, len(population)))` — случайно выбираем `k` (по умолчанию 4) особей из популяции без повторений.

`return max(contestants, key=lambda ind: ind.fitness)` — возвращаем того, у кого **максимальный** фитнес среди выбранных. `lambda ind: ind.fitness` — это короткая анонимная функция: «взять у `ind` поле `fitness`».

Смысл турнирного отбора: лучшие имеют больше шансов стать родителями, но даже слабые имеют шанс попасть в «турнир» и победить там. Это сохраняет разнообразие популяции лучше, чем просто «всегда берём лучших».

---

### 5.3 Одно поколение — `evolve_population`

```python
def evolve_population(population, field):
    evaluate_population(population, field)

    population.sort(key=lambda ind: ind.fitness, reverse=True)

    new_population = [deepcopy(ind) for ind in population[:ELITISM_K]]
```

`population.sort(key=lambda ind: ind.fitness, reverse=True)` — сортируем популяцию по убыванию фитнеса (лучшие — первые).

`new_population = [deepcopy(ind) for ind in population[:ELITISM_K]]` — **элитизм**: копируем 5 лучших особей напрямую в новое поколение, не трогая их. Это гарантирует, что лучшее решение, найденное к данному моменту, не потеряется.

```python
    while len(new_population) < POP_SIZE:
        parent1 = tournament_select(population)

        if random.random() < CROSSOVER_PROB:
            parent2 = tournament_select(population)
            child, _ = crossover_automata(parent1, parent2)
        else:
            child = deepcopy(parent1)

        child = mutate_automaton(
            child,
            mutation_rate=MUTATION_RATE,
            add_state_prob=ADD_STATE_PROB,
            del_state_prob=DEL_STATE_PROB
        )
        new_population.append(child)

    return new_population
```

Заполняем популяцию до 100 особей:

1. Выбираем первого родителя турниром.
2. С вероятностью 70% — выбираем второго родителя и скрещиваем. С вероятностью 30% — просто копируем первого родителя.
3. К потомку применяем мутацию.
4. Добавляем в новое поколение.

Процесс повторяется, пока не наберём 100 особей.

---

### 5.4 Главный цикл эволюции — `run_evolution`

```python
def run_evolution(field):
    total_food = int(field.sum() == FOOD * (field == FOOD).sum()
                     or True) and int((field == FOOD).sum())

    population = [random_automaton(INIT_STATES) for _ in range(POP_SIZE)]

    history_best   = []
    history_avg    = []
    history_states = []

    best_ever = None
```

`total_food = int((field == FOOD).sum())` — подсчитываем общее количество еды на поле. `(field == FOOD)` создаёт массив из True/False, `.sum()` суммирует True как 1. Это нужно для процентного отображения прогресса.

`population = [random_automaton(INIT_STATES) for _ in range(POP_SIZE)]` — создаём начальную популяцию из 100 случайных автоматов, каждый с 4 состояниями.

Списки `history_best`, `history_avg`, `history_states` — для записи статистики по поколениям (для графиков).

`best_ever = None` — здесь будем хранить лучший автомат за всё время.

```python
    for gen in range(N_GENERATIONS):
        evaluate_population(population, field)

        fitnesses   = [ind.fitness for ind in population]
        best_ind    = max(population, key=lambda ind: ind.fitness)
        avg_fitness = float(np.mean(fitnesses))
        avg_states  = float(np.mean([ind.n_states for ind in population]))

        if best_ever is None or best_ind.fitness > best_ever.fitness:
            best_ever = deepcopy(best_ind)

        history_best.append(best_ever.fitness)
        history_avg.append(avg_fitness)
        history_states.append(avg_states)

        print(f"Gen {gen+1:4d}/{N_GENERATIONS} | ...")

        population = evolve_population(population, field)

    return best_ever, history_best, history_avg, history_states
```

Основной цикл — 150 итераций, каждая итерация = одно поколение.

`evaluate_population(population, field)` — оцениваем всех ещё не оценённых особей.

`fitnesses = [ind.fitness for ind in population]` — собираем все оценки в список.

`best_ind = max(population, key=lambda ind: ind.fitness)` — находим лучшую особь этого поколения.

`avg_fitness = float(np.mean(fitnesses))` — среднее значение фитнеса по популяции.

`avg_states = float(np.mean([ind.n_states for ind in population]))` — среднее число состояний (интересно наблюдать, как оно меняется в ходе эволюции).

```python
        if best_ever is None or best_ind.fitness > best_ever.fitness:
            best_ever = deepcopy(best_ind)
```

Если текущий лучший лучше абсолютного рекорда — обновляем рекорд. `deepcopy` снова важен: мы сохраняем снимок, а не ссылку, которая может измениться в следующем поколении.

`population = evolve_population(population, field)` — порождаем следующее поколение.

В конце возвращаем лучшего за всё время и всю статистику.

---

## Раздел 6. Запуск

```python
field = generate_field(
    grid_size=GRID_SIZE,
    food_density=FOOD_DENSITY,
    wall_density=WALL_DENSITY,
    seed=FIELD_SEED
)
total_food = int((field == FOOD).sum())
print(f"Поле {GRID_SIZE}×{GRID_SIZE}: {total_food} клеток с едой, "
      f"{int((field == WALL).sum())} препятствий\n")

best_fa, hist_best, hist_avg, hist_states = run_evolution(field)
```

Просто вызываем всё, что написали выше:
1. Генерируем поле с фиксированным seed=7.
2. Считаем и печатаем количество еды и стен.
3. Запускаем эволюцию.

Результат: `best_fa` — лучший автомат, три списка — история метрик.

---

## Раздел 7. Вывод результатов

```python
food_collected, best_path = simulate_ant(field, best_fa, MAX_STEPS, GRID_SIZE)
```

Запускаем лучший автомат ещё раз на исходном поле (до эволюции), чтобы получить точный маршрут для визуализации. Именно поэтому мы передаём `field` (исходное), а не изменённое в ходе эволюции.

```python
print("=" * 55)
print(f"  Собрано еды : {food_collected} / {total_food}  "
      f"({100*food_collected/total_food:.1f}%)")
print(f"  Шагов       : {len(best_path) - 1}")
print(f"  Состояний   : {best_fa.n_states}")
print("=" * 55)
```

Выводим итоги. `len(best_path) - 1` — длина пути без стартовой точки (в `path` первый элемент добавляется до начала движения).

```python
print("Таблица переходов лучшего автомата:")
print(f"{'Состояние':<12}{'Вход (EMPTY)':<20}{'Вход (FOOD)':<20}{'Вход (WALL)':<20}")
print("-" * 72)# Объяснение лабораторной работы №3
## Эволюционная программа «Искусственный муравей»

---

## Общая идея работы

Представьте муравья, который ходит по клетчатому полю 32×32 и собирает еду. Мы не пишем для него жёсткие правила — вместо этого мы запускаем **эволюцию**: создаём сотню случайных «мозгов» для муравья, проверяем, у кого получается собрать больше еды, скрещиваем лучших, вносим случайные изменения — и повторяем это 150 раз. Так, через естественный отбор, мозг муравья постепенно становится умнее.

«Мозг» муравья — это **конечный автомат**: таблица правил вида «если я нахожусь в состоянии №2 и вижу еду впереди — повернуть направо и перейти в состояние №0».

---

## Раздел 1. Импорт библиотек

```python
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
from copy import deepcopy

random.seed(42)
np.random.seed(42)
```

Здесь мы подключаем готовые инструменты:

- `numpy` — библиотека для работы с массивами чисел (наше поле — это как раз двумерный массив).
- `random` — встроенный генератор случайных чисел Python.
- `matplotlib` и всё что из него — инструменты для рисования графиков и анимаций.
- `deepcopy` — функция для создания **полной независимой копии** объекта. Это важно: обычное копирование в Python создаёт «ссылку» на тот же объект, а не новый объект. `deepcopy` создаёт именно новый, чтобы изменения в копии не затронули оригинал.

Последние две строки — `random.seed(42)` и `np.random.seed(42)` — устанавливают **начальное значение** генератора случайных чисел. Это нужно для **воспроизводимости**: если запустить программу ещё раз с тем же seed, то все «случайные» числа будут теми же самыми, и результат будет одинаковым. Число 42 — просто традиция, можно использовать любое.

---

## Раздел 2. Модель поля и движение муравья

### 2.1 Константы — описание мира

```python
EMPTY = 0
FOOD  = 1
WALL  = 2

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

ACT_FORWARD   = 0
ACT_TURN_LEFT = 1
ACT_TURN_RIGHT= 2

ACTION_NAMES = {ACT_FORWARD: 'Forward', ACT_TURN_LEFT: 'Left', ACT_TURN_RIGHT: 'Right'}
```

Здесь задаются константы — числа с понятными именами, чтобы в коде не писать загадочные `0`, `1`, `2`, а писать `FOOD`, `WALL`, `EMPTY`.

**Типы клеток:**
- `EMPTY = 0` — пустая клетка.
- `FOOD = 1` — клетка с едой.
- `WALL = 2` — стена, непроходимое препятствие.

**Направления** — список пар `(dr, dc)`, где `dr` — изменение строки, `dc` — изменение столбца при шаге:
- Индекс 0: `(-1, 0)` — вверх (строка уменьшается на 1).
- Индекс 1: `(0, 1)` — вправо (столбец увеличивается на 1).
- Индекс 2: `(1, 0)` — вниз (строка увеличивается на 1).
- Индекс 3: `(0, -1)` — влево (столбец уменьшается на 1).

Порядок именно такой (по часовой стрелке), что позволит легко делать повороты: поворот направо = `(direction + 1) % 4`, налево = `(direction - 1) % 4`.

**Действия** муравья — три возможных поступка на каждом шаге:
- `ACT_FORWARD = 0` — шаг вперёд.
- `ACT_TURN_LEFT = 1` — повернуться налево (без шага).
- `ACT_TURN_RIGHT = 2` — повернуться направо (без шага).

`ACTION_NAMES` — просто словарь для читаемого вывода в таблице в конце.

---

### 2.2 Генерация поля — `generate_field`

```python
def generate_field(grid_size=32, food_density=0.2, wall_density=0.05, seed=0):
    rng = np.random.RandomState(seed)
    field = np.zeros((grid_size, grid_size), dtype=np.int8)

    for r in range(grid_size):
        for c in range(grid_size):
            if r == 0 and c == 0:
                continue
            roll = rng.random()
            if roll < wall_density:
                field[r, c] = WALL
            elif roll < wall_density + food_density:
                field[r, c] = FOOD

    field[0, 1] = EMPTY
    field[1, 0] = EMPTY

    return field
```

Эта функция создаёт случайное игровое поле. Разберём построчно.

`def generate_field(grid_size=32, food_density=0.2, wall_density=0.05, seed=0):`
— объявление функции с параметрами по умолчанию. Если при вызове не передать аргументы, будет использоваться поле 32×32, 20% еды, 5% стен.

`rng = np.random.RandomState(seed)`
— создаём **отдельный** генератор случайных чисел, привязанный к конкретному `seed`. Это позволяет поле генерировать независимо от других случайных чисел в программе: одинаковый `seed` → одинаковое поле каждый раз.

`field = np.zeros((grid_size, grid_size), dtype=np.int8)`
— создаём двумерный массив 32×32, заполненный нулями. `dtype=np.int8` означает, что каждый элемент — целое число от -128 до 127 (нам нужны только 0, 1, 2 — этого достаточно, экономим память).

`for r in range(grid_size):` и `for c in range(grid_size):`
— двойной цикл: перебираем каждую строку `r` и каждый столбец `c`, то есть проходим по каждой клетке поля.

`if r == 0 and c == 0: continue`
— пропускаем клетку (0, 0) — это стартовая позиция муравья, она должна быть пустой. `continue` означает «перейти к следующей итерации цикла».

`roll = rng.random()`
— бросаем «кубик»: получаем случайное число от 0.0 до 1.0 для этой клетки.

```python
if roll < wall_density:
    field[r, c] = WALL
elif roll < wall_density + food_density:
    field[r, c] = FOOD
```
— логика заполнения:
- Если число попало в диапазон от 0 до 0.05 (5% вероятность) — клетка становится стеной.
- Если попало в диапазон от 0.05 до 0.25 (20% вероятность) — клетка становится едой.
- Иначе — клетка остаётся пустой (это уже установлено, ведь мы начали с нулей).

`field[0, 1] = EMPTY` и `field[1, 0] = EMPTY`
— принудительно делаем пустыми две клетки рядом со стартом. Это гарантирует, что муравей с первого же шага не упрётся в стену.

`return field`
— возвращаем готовое поле.

---

### 2.3 Сенсор муравья — `sense_ahead`

```python
def sense_ahead(field, row, col, direction, grid_size):
    dr, dc = DIRECTIONS[direction]
    nr = (row + dr) % grid_size
    nc = (col + dc) % grid_size
    return int(field[nr, nc])
```

Эта крошечная функция отвечает на вопрос: **что находится прямо перед муравьём?** Это единственная информация, которую муравей получает о мире на каждом шаге.

`dr, dc = DIRECTIONS[direction]`
— берём смещение для текущего направления. Например, если `direction = 1` (вправо), то `dr = 0, dc = 1`.

`nr = (row + dr) % grid_size`
`nc = (col + dc) % grid_size`
— вычисляем координаты клетки впереди. Операция `% grid_size` — это взятие остатка от деления, которое реализует **тороидальное поле**: если муравей стоит у правого края и смотрит вправо, `nc` «перепрыгнет» на левый край (31 + 1 = 32, 32 % 32 = 0).

`return int(field[nr, nc])`
— возвращаем тип клетки впереди: 0 (EMPTY), 1 (FOOD) или 2 (WALL).

---

### 2.4 Симуляция одного прохода муравья — `simulate_ant`

```python
def simulate_ant(field_in, automaton, max_steps, grid_size=32):
    field = field_in.copy()
    row, col = 0, 0
    direction = 1
    state = 0
    food_collected = 0
    path = [(row, col)]
```

Это главная функция движения. Она запускает муравья на поле и возвращает результат.

`field = field_in.copy()`
— создаём **копию** поля. Важно! Муравей будет «съедать» еду (заменять FOOD → EMPTY). Копируя поле, мы защищаем исходник, чтобы следующий муравей получал ту же карту.

`row, col = 0, 0` — начальная позиция: строка 0, столбец 0 (левый верхний угол).

`direction = 1` — муравей изначально смотрит вправо (индекс 1 в списке DIRECTIONS).

`state = 0` — автомат начинает в состоянии №0.

`food_collected = 0` — счётчик собранной еды.

`path = [(row, col)]` — список всех посещённых клеток. Начинаем с начальной позиции.

```python
    for _ in range(max_steps):
        sensor = sense_ahead(field, row, col, direction, grid_size)
        action, new_state = automaton.transition(state, sensor)
        state = new_state
```

`for _ in range(max_steps):` — основной цикл: повторяем `max_steps` раз. Знак `_` вместо переменной — соглашение, означающее «номер итерации нам не нужен».

`sensor = sense_ahead(...)` — спрашиваем: что впереди? Получаем 0, 1 или 2.

`action, new_state = automaton.transition(state, sensor)` — «мозг» муравья (автомат) принимает решение: смотрим в таблицу переходов, получаем пару (что делать, в какое состояние перейти).

`state = new_state` — обновляем текущее состояние автомата.

```python
        if action == ACT_TURN_LEFT:
            direction = (direction - 1) % 4
        elif action == ACT_TURN_RIGHT:
            direction = (direction + 1) % 4
        else:  # ACT_FORWARD
            dr, dc = DIRECTIONS[direction]
            nr = (row + dr) % grid_size
            nc = (col + dc) % grid_size
            if field[nr, nc] != WALL:
                row, col = nr, nc
                if field[row, col] == FOOD:
                    food_collected += 1
                    field[row, col] = EMPTY
```

Выполняем действие:

- **Поворот налево**: `(direction - 1) % 4`. Если были направлены вправо (1), станем направлены вверх (0). `% 4` обеспечивает «кольцо»: из 0 можно уйти в 3 (влево).
- **Поворот направо**: `(direction + 1) % 4`. Аналогично.
- **Шаг вперёд**: вычисляем клетку впереди. Если там **не стена** — переходим туда. Если на новой клетке **еда** — увеличиваем счётчик на 1 и убираем еду (ставим 0).

Заметьте: если впереди стена, муравей **остаётся на месте**. Он не прыгает через стену и не исчезает — просто теряет один шаг.

```python
        path.append((row, col))

    return food_collected, path
```

`path.append((row, col))` — записываем текущую позицию в маршрут (даже если муравей никуда не двинулся из-за стены).

В конце возвращаем два значения: количество еды и весь пройденный путь.

---

## Раздел 3. Конечный автомат — «мозг» муравья

### 3.1 Что такое конечный автомат

Конечный автомат — это таблица правил. Строки таблицы — состояния (например, «ищу еду», «обхожу стену», «двигаюсь вперёд»). Столбцы — что видит муравей (EMPTY, FOOD, WALL). В каждой ячейке — инструкция: что сделать и в какое состояние перейти.

Пример таблицы с 2 состояниями:

| Состояние | Вижу EMPTY       | Вижу FOOD        | Вижу WALL        |
|-----------|-----------------|-----------------|-----------------|
| s0        | Вперёд → s0     | Вперёд → s0     | Повернуть L → s1 |
| s1        | Повернуть R → s0 | Вперёд → s0     | Повернуть L → s1 |

Это и есть «мозг» — минималистичная программа без памяти о прошлом, только текущее состояние + то, что видишь.

### 3.2 Класс `FiniteAutomaton`

```python
N_INPUTS = 3
N_ACTIONS = 3

class FiniteAutomaton:
    def __init__(self, n_states, table):
        self.n_states = n_states
        self.table = table
        self.fitness = None

    def transition(self, state, sensor):
        return self.table[state][sensor]

    def __repr__(self):
        return f"FiniteAutomaton(n_states={self.n_states}, fitness={self.fitness})"
```

`N_INPUTS = 3` — три возможных сенсорных входа (EMPTY, FOOD, WALL).
`N_ACTIONS = 3` — три возможных действия.

`class FiniteAutomaton:` — объявляем класс, то есть шаблон для создания объектов-автоматов.

`def __init__(self, n_states, table):` — конструктор: код, который запускается при создании нового автомата.
- `self.n_states = n_states` — запоминаем количество состояний.
- `self.table = table` — запоминаем таблицу переходов. Это список списков кортежей: `table[состояние][вход] = (действие, следующее_состояние)`.
- `self.fitness = None` — поле для хранения «оценки» этого автомата. Пока неизвестна.

`def transition(self, state, sensor):` — метод «сделать шаг автомата».
`return self.table[state][sensor]` — просто ищем в таблице: строка = текущее состояние, столбец = что видим. Возвращаем пару (действие, следующее состояние).

`def __repr__(self):` — метод для отображения объекта в виде строки (например, при выводе в консоль).

---

### 3.3 Случайный автомат — `random_automaton`

```python
def random_automaton(n_states):
    table = [
        [
            (random.randint(0, N_ACTIONS - 1), random.randint(0, n_states - 1))
            for _ in range(N_INPUTS)
        ]
        for _ in range(n_states)
    ]
    return FiniteAutomaton(n_states, table)
```

Создаёт автомат с абсолютно случайными правилами — с него начинается каждая особь в популяции.

`table = [...]` — строим таблицу через **генераторные выражения** (компактный способ создать список в Python).

Внешний цикл `for _ in range(n_states)` — создаём строку для каждого состояния.

Внутренний цикл `for _ in range(N_INPUTS)` — для каждого из трёх входов создаём ячейку.

`(random.randint(0, N_ACTIONS - 1), random.randint(0, n_states - 1))` — каждая ячейка — случайная пара: случайное действие (0, 1 или 2) и случайное следующее состояние (от 0 до n_states-1).

---

### 3.4 Мутация — `mutate_automaton`

```python
def mutate_automaton(automaton, mutation_rate=0.1,
                      add_state_prob=0.02, del_state_prob=0.02,
                      min_states=2, max_states=12):
    fa = deepcopy(automaton)
    n = fa.n_states
```

`fa = deepcopy(automaton)` — создаём полную независимую копию, чтобы не испортить исходный автомат. Все изменения будем делать в копии.

`n = fa.n_states` — запоминаем текущее число состояний.

```python
    for s in range(n):
        for inp in range(N_INPUTS):
            if random.random() < mutation_rate:
                act = random.randint(0, N_ACTIONS - 1)
                nxt = random.randint(0, n - 1)
                fa.table[s][inp] = (act, nxt)
```

**Точечные мутации:** проходим по каждой ячейке таблицы. `random.random()` возвращает число от 0 до 1. Если оно меньше `mutation_rate` (12%), то ячейка мутирует: в ней случайно меняется действие и/или следующее состояние. Это как случайная «опечатка» в генетическом коде.

```python
    if n < max_states and random.random() < add_state_prob:
        new_row = [(random.randint(0, N_ACTIONS - 1), random.randint(0, n))
                   for _ in range(N_INPUTS)]
        fa.table.append(new_row)
        fa.n_states += 1
```

**Добавление состояния:** с вероятностью 2%, если автомат ещё не достиг максимума (12 состояний), добавляем новую строку в таблицу — это расширяет «словарный запас» поведения.

```python
    elif n > min_states and random.random() < del_state_prob:
        idx = random.randint(1, n - 1)
        fa.table.pop(idx)
        fa.n_states -= 1
        new_n = fa.n_states
        for s in range(new_n):
            for inp in range(N_INPUTS):
                act, nxt = fa.table[s][inp]
                if nxt >= new_n:
                    nxt = random.randint(0, new_n - 1)
                fa.table[s][inp] = (act, nxt)
```

**Удаление состояния:** с вероятностью 1.5%, если состояний больше минимума (2), удаляем случайное состояние (не стартовое — поэтому `randint(1, n-1)`).

`fa.table.pop(idx)` — удаляем строку из таблицы.

Затем — важный шаг: некоторые ячейки могли ссылаться на только что удалённое состояние. Проходим по всей таблице и если встречаем ссылку `nxt >= new_n` (то есть на несуществующее теперь состояние) — заменяем её на случайное существующее.

`fa.fitness = None` — сбрасываем оценку: автомат изменился, старая оценка больше не актуальна.

---

### 3.5 Кроссовер — `crossover_automata`

```python
def crossover_automata(fa1, fa2):
    n = min(fa1.n_states, fa2.n_states)

    table1, table2 = [], []
    for s in range(n):
        if random.random() < 0.5:
            table1.append(deepcopy(fa1.table[s]))
            table2.append(deepcopy(fa2.table[s]))
        else:
            table1.append(deepcopy(fa2.table[s]))
            table2.append(deepcopy(fa1.table[s]))
```

Кроссовер — скрещивание двух родительских автоматов для получения двух дочерних.

`n = min(fa1.n_states, fa2.n_states)` — берём минимальное число состояний из двух родителей, чтобы оба потомка имели корректные таблицы.

Цикл по состояниям: для каждой строки таблицы подбрасываем монетку. С вероятностью 50% потомок №1 получает строку от родителя №1 (а потомок №2 — от родителя №2), и наоборот. Это **однородный кроссовер**: каждая строка независимо берётся от одного из родителей.

```python
    def fix(table, max_s):
        for s in range(len(table)):
            for inp in range(N_INPUTS):
                act, nxt = table[s][inp]
                if nxt >= max_s:
                    nxt = random.randint(0, max_s - 1)
                table[s][inp] = (act, nxt)

    fix(table1, n)
    fix(table2, n)

    return FiniteAutomaton(n, table1), FiniteAutomaton(n, table2)
```

`fix` — вспомогательная функция внутри `crossover_automata`. Проверяет и исправляет ссылки на несуществующие состояния (та же проблема, что и при удалении состояния в мутации).

В конце возвращаем **двух** новых потомков.

---

## Раздел 4. Параметры алгоритма

```python
GRID_SIZE     = 32
FOOD_DENSITY  = 0.20
WALL_DENSITY  = 0.05
FIELD_SEED    = 7
MAX_STEPS     = 500

POP_SIZE       = 100
N_GENERATIONS  = 150
INIT_STATES    = 4
ELITISM_K      = 5
TOURNAMENT_K   = 4
MUTATION_RATE  = 0.12
CROSSOVER_PROB = 0.70
ADD_STATE_PROB = 0.02
DEL_STATE_PROB = 0.015
```

Все настройки собраны в одном месте для удобства.

**Параметры поля:**
- Поле 32×32, 20% клеток содержат еду, 5% — стены.
- `FIELD_SEED = 7` — фиксирует случайность генерации поля: одно и то же поле при каждом запуске.
- `MAX_STEPS = 500` — каждый муравей делает не более 500 шагов.

**Параметры эволюции:**
- `POP_SIZE = 100` — в каждом поколении 100 автоматов.
- `N_GENERATIONS = 150` — всего 150 поколений.
- `INIT_STATES = 4` — начинаем с автоматов, у каждого по 4 состояния.
- `ELITISM_K = 5` — 5 лучших автоматов переходят в следующее поколение без изменений.
- `TOURNAMENT_K = 4` — при отборе родителей сравниваем 4 случайных кандидата.
- `MUTATION_RATE = 0.12` — каждая ячейка таблицы мутирует с вероятностью 12%.
- `CROSSOVER_PROB = 0.70` — 70% шанс применить кроссовер; иначе потомок — просто мутированная копия одного родителя.

---

## Раздел 5. Эволюционный алгоритм

### 5.1 Оценка особи — `evaluate` и `evaluate_population`

```python
def evaluate(automaton, field, max_steps=MAX_STEPS, grid_size=GRID_SIZE):
    food, _ = simulate_ant(field, automaton, max_steps, grid_size)
    automaton.fitness = food
    return food
```

`food, _ = simulate_ant(...)` — запускаем симуляцию. `simulate_ant` возвращает два значения: количество еды и путь. Знак `_` означает «второе значение нам здесь не нужно, игнорируем».

`automaton.fitness = food` — записываем результат прямо в объект автомата.

```python
def evaluate_population(population, field):
    for ind in population:
        if ind.fitness is None:
            evaluate(ind, field)
```

Проходим по всем особям. Строчка `if ind.fitness is None` — важная оптимизация: если особь уже оценена (например, это элита из прошлого поколения), не гоняем симуляцию заново.

---

### 5.2 Турнирный отбор — `tournament_select`

```python
def tournament_select(population, k=TOURNAMENT_K):
    contestants = random.sample(population, min(k, len(population)))
    return max(contestants, key=lambda ind: ind.fitness)
```

Это механизм выбора родителей для следующего поколения.

`random.sample(population, min(k, len(population)))` — случайно выбираем `k` (по умолчанию 4) особей из популяции без повторений.

`return max(contestants, key=lambda ind: ind.fitness)` — возвращаем того, у кого **максимальный** фитнес среди выбранных. `lambda ind: ind.fitness` — это короткая анонимная функция: «взять у `ind` поле `fitness`».

Смысл турнирного отбора: лучшие имеют больше шансов стать родителями, но даже слабые имеют шанс попасть в «турнир» и победить там. Это сохраняет разнообразие популяции лучше, чем просто «всегда берём лучших».

---

### 5.3 Одно поколение — `evolve_population`

```python
def evolve_population(population, field):
    evaluate_population(population, field)

    population.sort(key=lambda ind: ind.fitness, reverse=True)

    new_population = [deepcopy(ind) for ind in population[:ELITISM_K]]
```

`population.sort(key=lambda ind: ind.fitness, reverse=True)` — сортируем популяцию по убыванию фитнеса (лучшие — первые).

`new_population = [deepcopy(ind) for ind in population[:ELITISM_K]]` — **элитизм**: копируем 5 лучших особей напрямую в новое поколение, не трогая их. Это гарантирует, что лучшее решение, найденное к данному моменту, не потеряется.

```python
    while len(new_population) < POP_SIZE:
        parent1 = tournament_select(population)

        if random.random() < CROSSOVER_PROB:
            parent2 = tournament_select(population)
            child, _ = crossover_automata(parent1, parent2)
        else:
            child = deepcopy(parent1)

        child = mutate_automaton(
            child,
            mutation_rate=MUTATION_RATE,
            add_state_prob=ADD_STATE_PROB,
            del_state_prob=DEL_STATE_PROB
        )
        new_population.append(child)

    return new_population
```

Заполняем популяцию до 100 особей:

1. Выбираем первого родителя турниром.
2. С вероятностью 70% — выбираем второго родителя и скрещиваем. С вероятностью 30% — просто копируем первого родителя.
3. К потомку применяем мутацию.
4. Добавляем в новое поколение.

Процесс повторяется, пока не наберём 100 особей.

---

### 5.4 Главный цикл эволюции — `run_evolution`

```python
def run_evolution(field):
    total_food = int(field.sum() == FOOD * (field == FOOD).sum()
                     or True) and int((field == FOOD).sum())

    population = [random_automaton(INIT_STATES) for _ in range(POP_SIZE)]

    history_best   = []
    history_avg    = []
    history_states = []

    best_ever = None
```

`total_food = int((field == FOOD).sum())` — подсчитываем общее количество еды на поле. `(field == FOOD)` создаёт массив из True/False, `.sum()` суммирует True как 1. Это нужно для процентного отображения прогресса.

`population = [random_automaton(INIT_STATES) for _ in range(POP_SIZE)]` — создаём начальную популяцию из 100 случайных автоматов, каждый с 4 состояниями.

Списки `history_best`, `history_avg`, `history_states` — для записи статистики по поколениям (для графиков).

`best_ever = None` — здесь будем хранить лучший автомат за всё время.

```python
    for gen in range(N_GENERATIONS):
        evaluate_population(population, field)

        fitnesses   = [ind.fitness for ind in population]
        best_ind    = max(population, key=lambda ind: ind.fitness)
        avg_fitness = float(np.mean(fitnesses))
        avg_states  = float(np.mean([ind.n_states for ind in population]))

        if best_ever is None or best_ind.fitness > best_ever.fitness:
            best_ever = deepcopy(best_ind)

        history_best.append(best_ever.fitness)
        history_avg.append(avg_fitness)
        history_states.append(avg_states)

        print(f"Gen {gen+1:4d}/{N_GENERATIONS} | ...")

        population = evolve_population(population, field)

    return best_ever, history_best, history_avg, history_states
```

Основной цикл — 150 итераций, каждая итерация = одно поколение.

`evaluate_population(population, field)` — оцениваем всех ещё не оценённых особей.

`fitnesses = [ind.fitness for ind in population]` — собираем все оценки в список.

`best_ind = max(population, key=lambda ind: ind.fitness)` — находим лучшую особь этого поколения.

`avg_fitness = float(np.mean(fitnesses))` — среднее значение фитнеса по популяции.

`avg_states = float(np.mean([ind.n_states for ind in population]))` — среднее число состояний (интересно наблюдать, как оно меняется в ходе эволюции).

```python
        if best_ever is None or best_ind.fitness > best_ever.fitness:
            best_ever = deepcopy(best_ind)
```

Если текущий лучший лучше абсолютного рекорда — обновляем рекорд. `deepcopy` снова важен: мы сохраняем снимок, а не ссылку, которая может измениться в следующем поколении.

`population = evolve_population(population, field)` — порождаем следующее поколение.

В конце возвращаем лучшего за всё время и всю статистику.

---

## Раздел 6. Запуск

```python
field = generate_field(
    grid_size=GRID_SIZE,
    food_density=FOOD_DENSITY,
    wall_density=WALL_DENSITY,
    seed=FIELD_SEED
)
total_food = int((field == FOOD).sum())
print(f"Поле {GRID_SIZE}×{GRID_SIZE}: {total_food} клеток с едой, "
      f"{int((field == WALL).sum())} препятствий\n")

best_fa, hist_best, hist_avg, hist_states = run_evolution(field)
```

Просто вызываем всё, что написали выше:
1. Генерируем поле с фиксированным seed=7.
2. Считаем и печатаем количество еды и стен.
3. Запускаем эволюцию.

Результат: `best_fa` — лучший автомат, три списка — история метрик.

---

## Раздел 7. Вывод результатов

```python
food_collected, best_path = simulate_ant(field, best_fa, MAX_STEPS, GRID_SIZE)
```

Запускаем лучший автомат ещё раз на исходном поле (до эволюции), чтобы получить точный маршрут для визуализации. Именно поэтому мы передаём `field` (исходное), а не изменённое в ходе эволюции.

```python
print("=" * 55)
print(f"  Собрано еды : {food_collected} / {total_food}  "
      f"({100*food_collected/total_food:.1f}%)")
print(f"  Шагов       : {len(best_path) - 1}")
print(f"  Состояний   : {best_fa.n_states}")
print("=" * 55)
```

Выводим итоги. `len(best_path) - 1` — длина пути без стартовой точки (в `path` первый элемент добавляется до начала движения).

```python
print("Таблица переходов лучшего автомата:")
print(f"{'Состояние':<12}{'Вход (EMPTY)':<20}{'Вход (FOOD)':<20}{'Вход (WALL)':<20}")
print("-" * 72)
for s, row in enumerate(best_fa.table):
    cols = []
    for inp in range(N_INPUTS):
        act, nxt = row[inp]
        cols.append(f"{ACTION_NAMES[act]}→s{nxt}")
    print(f"  s{s:<10}{cols[0]:<20}{cols[1]:<20}{cols[2]:<20}")
```

`enumerate(best_fa.table)` — перебираем строки таблицы, получая одновременно индекс `s` и саму строку `row`.

Для каждой строки и каждого входа форматируем ячейку в читаемый вид: например `Forward→s2` означает «сделать шаг вперёд и перейти в состояние 2».

`:<12` и `:<20` — форматирование с выравниванием по левому краю с заданной шириной поля. Это делает вывод аккуратным столбцами.

---

## Итог: как всё работает вместе

1. **Генерируется поле** — случайная карта с едой и стенами.
2. **Создаётся 100 случайных автоматов** — у каждого своя случайная таблица правил.
3. **Каждый автомат «играет»** — муравей с таким мозгом ходит по полю 500 шагов, считаем сколько еды собрал.
4. **Отбираем лучших** — 5 лучших переходят в следующее поколение как есть.
5. **Скрещиваем и мутируем** — из лучших создаём 95 потомков: смешиваем таблицы переходов двух родителей, вносим случайные изменения.
6. **Повторяем 150 раз** — с каждым поколением автоматы становятся лучше, потому что случайные улучшения сохраняются, а ухудшения отсеиваются.
7. **Выводим результат** — лучший найденный автомат, его таблицу переходов, путь и графики.
for s, row in enumerate(best_fa.table):
    cols = []
    for inp in range(N_INPUTS):
        act, nxt = row[inp]
        cols.append(f"{ACTION_NAMES[act]}→s{nxt}")
    print(f"  s{s:<10}{cols[0]:<20}{cols[1]:<20}{cols[2]:<20}")
```

`enumerate(best_fa.table)` — перебираем строки таблицы, получая одновременно индекс `s` и саму строку `row`.

Для каждой строки и каждого входа форматируем ячейку в читаемый вид: например `Forward→s2` означает «сделать шаг вперёд и перейти в состояние 2».

`:<12` и `:<20` — форматирование с выравниванием по левому краю с заданной шириной поля. Это делает вывод аккуратным столбцами.

---

## Итог: как всё работает вместе

1. **Генерируется поле** — случайная карта с едой и стенами.
2. **Создаётся 100 случайных автоматов** — у каждого своя случайная таблица правил.
3. **Каждый автомат «играет»** — муравей с таким мозгом ходит по полю 500 шагов, считаем сколько еды собрал.
4. **Отбираем лучших** — 5 лучших переходят в следующее поколение как есть.
5. **Скрещиваем и мутируем** — из лучших создаём 95 потомков: смешиваем таблицы переходов двух родителей, вносим случайные изменения.
6. **Повторяем 150 раз** — с каждым поколением автоматы становятся лучше, потому что случайные улучшения сохраняются, а ухудшения отсеиваются.
7. **Выводим результат** — лучший найденный автомат, его таблицу переходов, путь и графики.