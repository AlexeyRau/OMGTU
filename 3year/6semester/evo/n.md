# Объяснение лабораторной работы №3
## Эволюционная программа «Искусственный муравей»

---

## Часть 0. Что делает программа — общий жизненный цикл

Прежде чем разбирать каждую строку, важно понять **порядок событий** — как программа живёт от запуска до финального результата.

```
1. ПОДГОТОВКА
   └─ Импорт библиотек
   └─ Задание констант (типы клеток, действия, направления)

2. СОЗДАНИЕ МИРА
   └─ generate_field() → создаёт случайное поле 32×32 с едой и стенами

3. СОЗДАНИЕ ПЕРВОГО ПОКОЛЕНИЯ
   └─ random_automaton() × 100 → 100 случайных «мозгов» (конечных автоматов)

4. ГЛАВНЫЙ ЦИКЛ ЭВОЛЮЦИИ (150 раз):
   └─ evaluate_population()
       └─ для каждого автомата: evaluate() → simulate_ant()
           └─ внутри simulate_ant():
               └─ sense_ahead()   — что впереди?
               └─ automaton.transition() — что делать?
               └─ двигаемся / поворачиваем / собираем еду
   └─ сортировка по результату
   └─ evolve_population()
       └─ элиты копируются напрямую
       └─ tournament_select() — выбираем родителей
       └─ crossover_automata() — скрещиваем
       └─ mutate_automaton() — мутируем
       └─ новое поколение готово

5. ФИНАЛ
   └─ simulate_ant() с лучшим автоматом → итоговый путь
   └─ Вывод таблицы переходов
   └─ Графики и анимация
```

Весь код — это реализация именно этого жизненного цикла. Теперь разберём каждый шаг.

---

## Часть 1. Подготовка

### 1.1 Импорт библиотек

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

**Что подключаем и зачем:**

`import numpy as np` — библиотека для работы с многомерными массивами. Наше поле 32×32 — это двумерный массив numpy. Без него пришлось бы вручную писать вложенные списки и все операции над ними.

`import random` — стандартный генератор случайных чисел Python. Используется для случайных решений в эволюции: какую ячейку мутировать, кого выбрать в турнире, куда вставить новое состояние.

`import matplotlib.pyplot as plt` и остальные `matplotlib` — всё для рисования: графики динамики, карта поля, анимация.

`from IPython.display import HTML` — нужно именно для анимации в Jupyter-ноутбуке. Анимация конвертируется в HTML-код и встраивается прямо в ячейку.

`from copy import deepcopy` — один из самых важных инструментов. В Python, когда вы «копируете» объект обычным присваиванием (`b = a`), вы получаете не копию, а **вторую ссылку на тот же объект**. Изменив `b`, вы меняете и `a`. `deepcopy` создаёт полностью независимый дубликат — нужен везде, где мы сохраняем лучшего автомата или создаём потомков.

`random.seed(42)` и `np.random.seed(42)` — устанавливают **стартовую точку** генератора случайных чисел. Это делает программу воспроизводимой: при каждом запуске «случайные» числа будут одинаковыми. Число 42 условное, подойдёт любое.

---

### 1.2 Константы — описание мира

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

Всё это — **имена для чисел**. Вместо того чтобы везде писать `0`, `1`, `2` и гадать что они означают, мы один раз объявляем понятные имена.

**Типы клеток:** каждая клетка поля хранит одно из трёх чисел: 0 — пусто, 1 — еда, 2 — стена.

**Направления** — список из четырёх пар `(dr, dc)`:
- `(-1, 0)` — шаг вверх: строка уменьшается на 1, столбец не меняется.
- `(0, 1)` — шаг вправо: строка не меняется, столбец увеличивается на 1.
- `(1, 0)` — шаг вниз: строка увеличивается на 1.
- `(0, -1)` — шаг влево: столбец уменьшается на 1.

Важно, что направления идут **по часовой стрелке** (вверх → право → вниз → лево, индексы 0, 1, 2, 3). Это позволяет делать повороты простой арифметикой: повернуть направо = `(direction + 1) % 4`, налево = `(direction - 1) % 4`. Оператор `%` — остаток от деления — замыкает числа в кольцо: после 3 снова идёт 0.

**Действия:** у муравья ровно три возможных поступка на каждом шаге — шаг вперёд, поворот налево или поворот направо. Никаких прыжков, телепортаций или стоянки на месте по желанию.

`ACTION_NAMES` — словарь только для красивого вывода таблицы в конце. Число → читаемое слово.

---

## Часть 2. Создание мира — функция `generate_field`

**Когда вызывается:** один раз, в разделе 6, в самом начале запуска:
```python
field = generate_field(grid_size=GRID_SIZE, food_density=FOOD_DENSITY,
                       wall_density=WALL_DENSITY, seed=FIELD_SEED)
```

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

**Строка за строкой:**

`rng = np.random.RandomState(seed)` — создаём **отдельный** генератор случайных чисел, независимый от основного `random`. Привязан к `seed=7` (из параметров). Это значит поле всегда генерируется одинаково, независимо от того, сколько случайных чисел было потрачено до этого на другие нужды.

`field = np.zeros((grid_size, grid_size), dtype=np.int8)` — создаём матрицу 32×32, полностью заполненную нулями (то есть `EMPTY`). `dtype=np.int8` — тип данных: целое число от −128 до 127. Нам нужны только 0, 1, 2 — такой тип экономит память по сравнению с обычным int (который занимает в 4–8 раз больше).

`for r in range(grid_size):` и `for c in range(grid_size):` — двойной цикл. `range(32)` даёт числа 0, 1, 2, ..., 31. Итого 32 × 32 = 1024 итерации — перебираем каждую клетку поля.

`if r == 0 and c == 0: continue` — клетку (0, 0) пропускаем. Это стартовая позиция муравья, она всегда должна быть пустой. `continue` — ключевое слово Python: «прекрати текущую итерацию цикла и перейди к следующей».

`roll = rng.random()` — «бросаем монетку» для текущей клетки: случайное число от 0.0 до 1.0.

```python
if roll < wall_density:           # т.е. < 0.05 → 5% вероятность
    field[r, c] = WALL
elif roll < wall_density + food_density:  # т.е. < 0.25 → ещё 20% вероятность
    field[r, c] = FOOD
```

Если число меньше 0.05 — это стена. Если от 0.05 до 0.25 — еда. Если больше 0.25 — остаётся 0 (пусто). Таким образом примерно 5% клеток станут стенами и 20% — едой.

`field[0, 1] = EMPTY` и `field[1, 0] = EMPTY` — принудительно очищаем две клетки рядом со стартом. Иначе муравей может с первого же шага оказаться заблокирован стеной со всех сторон.

`return field` — возвращаем готовую матрицу 32×32. Это поле будет использоваться **одно и то же** для всех 100 муравьёв в каждом из 150 поколений. Каждый муравей получает копию поля (об этом — в `simulate_ant`).

---

## Часть 3. Сенсор муравья — функция `sense_ahead`

**Когда вызывается:** каждый шаг симуляции, внутри `simulate_ant`, перед каждым решением автомата.

```python
def sense_ahead(field, row, col, direction, grid_size):
    dr, dc = DIRECTIONS[direction]
    nr = (row + dr) % grid_size
    nc = (col + dc) % grid_size
    return int(field[nr, nc])
```

Это единственная информация, которую муравей получает о мире: **что находится на клетке прямо перед ним**.

`dr, dc = DIRECTIONS[direction]` — берём смещение для текущего направления. Например, если `direction = 2` (вниз), то `DIRECTIONS[2] = (1, 0)`, значит `dr = 1, dc = 0`.

`nr = (row + dr) % grid_size` и `nc = (col + dc) % grid_size` — вычисляем координаты клетки впереди. Операция `% grid_size` реализует **тороидальное (кольцевое) поле**: муравей, дошедший до правого края, появляется с левого. Например, если `col = 31` и `dc = 1`, то `(31 + 1) % 32 = 0` — снова столбец 0.

`return int(field[nr, nc])` — возвращаем тип клетки: 0 (EMPTY), 1 (FOOD) или 2 (WALL). Именно это число автомат получает как «сенсорный вход» и ищет в своей таблице.

---

## Часть 4. Конечный автомат — «мозг» муравья

Прежде чем разбирать код автомата, нужно понять **что он из себя представляет**.

### Что такое конечный автомат

Конечный автомат — это таблица правил. Представьте её так:

|
 Состояние 
|
 Вижу ПУСТО       
|
 Вижу ЕДУ         
|
 Вижу СТЕНУ       
|
|
-----------
|
-----------------
|
-----------------
|
-----------------
|
|
 s0        
|
 Вперёд → s0     
|
 Вперёд → s1     
|
 Повернуть L → s0 
|
|
 s1        
|
 Повернуть R → s0 
|
 Вперёд → s1     
|
 Повернуть L → s2 
|
|
 s2        
|
 Вперёд → s0     
|
 Повернуть R → s1 
|
 Повернуть R → s2 
|

На каждом шаге муравей смотрит: «я в состоянии **s1**, впереди **ЕДА** — что делать?» Находит ячейку таблицы `[s1][FOOD]`, читает: «Вперёд → s1». Делает шаг вперёд (собирает еду) и остаётся в состоянии s1.

Состояния — это грубая «память» автомата. Он не помнит всю историю движений, но может находиться в разных режимах поведения (например «иду вдоль стены» или «ищу еду по прямой»).

### 4.1 Константы автомата

```python
N_INPUTS = 3   # EMPTY, FOOD, WALL
N_ACTIONS = 3  # Forward, TurnLeft, TurnRight
```

Три возможных входа (то, что видит муравей) и три возможных действия. Это размерность таблицы: каждая строка (состояние) имеет ровно 3 ячейки.

---

### 4.2 Класс `FiniteAutomaton`

```python
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

`class FiniteAutomaton:` — объявляем **шаблон** для создания объектов-автоматов. Класс — это как чертёж: он описывает, какие данные хранит объект и что умеет делать.

`def __init__(self, n_states, table):` — конструктор: код, который выполняется **при создании** нового автомата. `self` — ссылка на сам создаваемый объект. Все поля начинаются с `self.`.

`self.n_states = n_states` — запоминаем, сколько состояний у этого автомата.

`self.table = table` — сохраняем таблицу переходов. Структура: `table[состояние][вход]` → `(действие, следующее_состояние)`. Например, `table[1][2]` — «что делать, если я в состоянии 1 и вижу стену».

`self.fitness = None` — поле для оценки приспособленности. Пока автомат не запущен на симуляции, оценки нет.

`def transition(self, state, sensor):` — главный метод: «сделай один шаг автомата».
`return self.table[state][sensor]` — просто находим нужную ячейку таблицы и возвращаем пару `(действие, следующее_состояние)`. Вся «магия» автомата — это обращение к таблице по двум индексам.

`def __repr__(self):` — метод для отображения объекта в виде строки. Python вызывает его когда вы пишете `print(automaton)`. Двойное подчёркивание означает «специальный метод Python».

---

### 4.3 Функция `random_automaton` — создание случайного автомата

**Когда вызывается:** при инициализации популяции в `run_evolution`. Вызывается 100 раз, создавая стартовое поколение.

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

`table = [...]` — строим таблицу через **вложенные генераторы списков**. Это компактный Python-способ написать то, что можно было бы написать через несколько вложенных циклов.

Внешний цикл `for _ in range(n_states)` — создаём одну строку для каждого состояния.

Внутренний цикл `for _ in range(N_INPUTS)` — для каждого из трёх возможных входов создаём ячейку.

`(random.randint(0, N_ACTIONS - 1), random.randint(0, n_states - 1))` — каждая ячейка — **пара случайных чисел**: случайное действие (0, 1 или 2) и случайное следующее состояние (от 0 до n_states−1). Вся таблица заполнена полностью случайно — этот автомат, скорее всего, почти ничего не соберёт, но с него начинается эволюция.

`return FiniteAutomaton(n_states, table)` — создаём объект автомата и возвращаем его.

---

## Часть 5. Симуляция муравья — функция `simulate_ant`

**Когда вызывается:** внутри `evaluate`, которая вызывается для каждого автомата в каждом поколении. Это самая «дорогая» по времени функция — она работает 100 × 150 = 15 000 раз за всю эволюцию. Также вызывается один раз в конце (раздел 7) для получения финального пути.

```python
def simulate_ant(field_in, automaton, max_steps, grid_size=32):
    field = field_in.copy()
    row, col = 0, 0
    direction = 1
    state = 0
    food_collected = 0
    path = [(row, col)]
```

`field = field_in.copy()` — **создаём копию поля**. Критически важно. Во время симуляции муравей «съедает» еду (заменяет FOOD на EMPTY). Если бы мы не копировали, то второй запущенный муравей получал бы поле, уже объеденное первым. Копия защищает исходное поле.

`row, col = 0, 0` — стартовая позиция: левый верхний угол поля.

`direction = 1` — муравей изначально смотрит вправо (индекс 1 в списке DIRECTIONS).

`state = 0` — автомат стартует всегда в состоянии №0. Это фиксированное начальное состояние.

`food_collected = 0` — счётчик собранной еды. Это и есть будущий фитнес.

`path = [(row, col)]` — список всех посещённых клеток, начинаем со стартовой позиции.

```python
    for _ in range(max_steps):
        sensor = sense_ahead(field, row, col, direction, grid_size)
        action, new_state = automaton.transition(state, sensor)
        state = new_state
```

`for _ in range(max_steps):` — главный цикл симуляции, `max_steps = 500` итераций. Знак `_` — общепринятое обозначение «нам не нужен счётчик итерации».

`sensor = sense_ahead(...)` — вызываем функцию-сенсор: узнаём тип клетки впереди (0, 1 или 2).

`action, new_state = automaton.transition(state, sensor)` — вызываем метод автомата: находим в таблице строку `state` и столбец `sensor`. Получаем пару: что делать и куда переходить.

`state = new_state` — обновляем текущее состояние автомата на следующий шаг.

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

Выполняем выбранное действие:

**Поворот налево:** `(direction - 1) % 4`. Если смотрели вправо (1) — теперь смотрим вверх (0). Если смотрели вверх (0) — теперь смотрим влево (3). Оператор `% 4` обеспечивает кольцо: из 0 вычесть 1 в Python даст −1, но (−1) % 4 = 3 — правильно.

**Поворот направо:** `(direction + 1) % 4`. Аналогично в обратную сторону.

**Шаг вперёд:** вычисляем координаты клетки впереди (те же формулы, что в `sense_ahead`). Проверяем: если там не стена — переходим. Если на новой клетке еда — увеличиваем счётчик и «съедаем» еду (заменяем FOOD → EMPTY, чтобы не собирать её дважды). Если впереди стена — муравей **остаётся на месте**, теряя один шаг.

```python
        path.append((row, col))

    return food_collected, path
```

После каждого шага записываем текущую позицию в список пути — даже если муравей никуда не двинулся (уткнулся в стену).

Возвращаем два значения: сколько еды собрано (это станет фитнесом) и весь пройденный путь (нужен для визуализации, но не для эволюции).

---

## Часть 6. Параметры алгоритма

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

Все числа, которые управляют поведением программы, собраны здесь. Смысл каждого:

**Параметры мира:**
- `GRID_SIZE = 32` — поле 32×32 = 1024 клетки.
- `FOOD_DENSITY = 0.20` — примерно 205 клеток с едой.
- `WALL_DENSITY = 0.05` — примерно 51 клетка-стена.
- `FIELD_SEED = 7` — фиксирует карту поля. Измените это число — получите другое поле.
- `MAX_STEPS = 500` — каждый муравей ходит ровно 500 шагов. Ни больше, ни меньше.

**Параметры эволюции:**
- `POP_SIZE = 100` — в каждом поколении живёт 100 автоматов.
- `N_GENERATIONS = 150` — столько раз проходит «смена поколений». Итого 100 × 150 = 15 000 запусков симуляции.
- `INIT_STATES = 4` — у каждого автомата первого поколения ровно 4 состояния.
- `ELITISM_K = 5` — 5 лучших автоматов каждого поколения переходят в следующее **без изменений**. Это защищает лучшие найденные решения.
- `TOURNAMENT_K = 4` — при выборе родителя случайно берём 4 кандидата и выбираем лучшего из них.
- `MUTATION_RATE = 0.12` — каждая ячейка таблицы мутирует с вероятностью 12%.
- `CROSSOVER_PROB = 0.70` — 70% потомков создаётся скрещиванием двух родителей; остальные 30% — просто мутированная копия одного.
- `ADD_STATE_PROB = 0.02` и `DEL_STATE_PROB = 0.015` — 2% и 1.5% шанс изменить число состояний при мутации.

---

## Часть 7. Оценка автоматов — функции `evaluate` и `evaluate_population`

**Когда вызываются:** в начале каждого поколения, внутри `evolve_population` → `evaluate_population`.

```python
def evaluate(automaton, field, max_steps=MAX_STEPS, grid_size=GRID_SIZE):
    food, _ = simulate_ant(field, automaton, max_steps, grid_size)
    automaton.fitness = food
    return food
```

`food, _ = simulate_ant(...)` — запускаем симуляцию. `simulate_ant` возвращает два значения: количество еды и путь. Символ `_` означает «второе значение нас здесь не интересует, игнорируем».

`automaton.fitness = food` — записываем результат прямо в объект автомата. Теперь `automaton.fitness` — это его «оценка»: чем больше еды, тем лучше.

```python
def evaluate_population(population, field):
    for ind in population:
        if ind.fitness is None:
            evaluate(ind, field)
```

`for ind in population:` — перебираем всех особей в списке.

`if ind.fitness is None:` — **оптимизация**: элиты из прошлого поколения уже имеют оценку (мы их не меняли). Пересчитывать смысла нет. Оцениваем только новых особей. `is None` — проверка на то, что значение ещё не было установлено.

---

## Часть 8. Мутации — функция `mutate_automaton`

**Когда вызывается:** при создании каждого потомка внутри `evolve_population`. Это главный источник новизны в эволюции.

```python
def mutate_automaton(automaton, mutation_rate=0.1,
                      add_state_prob=0.02, del_state_prob=0.02,
                      min_states=2, max_states=12):
    fa = deepcopy(automaton)
    n = fa.n_states
```

`fa = deepcopy(automaton)` — **полная независимая копия**. Все изменения вносим в копию, а не в оригинал. Иначе мутация испортила бы родителя, который ещё нужен для эволюции.

`n = fa.n_states` — запоминаем текущее число состояний для удобства.

```python
    for s in range(n):
        for inp in range(N_INPUTS):
            if random.random() < mutation_rate:
                act = random.randint(0, N_ACTIONS - 1)
                nxt = random.randint(0, n - 1)
                fa.table[s][inp] = (act, nxt)
```

**Точечные мутации:** двойным циклом проходим по каждой ячейке таблицы. Для каждой ячейки `random.random()` даёт число от 0 до 1 — если оно меньше `mutation_rate` (0.12), ячейка мутирует: в ней случайно меняется и действие, и следующее состояние. Для таблицы 4×3 = 12 ячеек в среднем будет изменено около 12 × 0.12 ≈ 1–2 ячейки за одну мутацию.

```python
    if n < max_states and random.random() < add_state_prob:
        new_row = [(random.randint(0, N_ACTIONS - 1), random.randint(0, n))
                   for _ in range(N_INPUTS)]
        fa.table.append(new_row)
        fa.n_states += 1
```

**Добавление состояния:** с вероятностью 2%, если не достигли лимита (12 состояний), добавляем новую строку в таблицу. `.append(new_row)` добавляет строку в конец списка. `fa.n_states += 1` — увеличиваем счётчик.

Обратите внимание: в новой строке ссылки идут до `n` включительно — это корректно, т.к. новое состояние будет иметь индекс `n` (старый размер).

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

**Удаление состояния:** с вероятностью 1.5%, если состояний больше минимума (2), удаляем случайное. Важно: `random.randint(1, n - 1)` — **не удаляем состояние 0**, потому что каждая симуляция начинается именно с него.

`fa.table.pop(idx)` — удаляем строку из таблицы. `.pop(idx)` убирает элемент с указанным индексом.

После удаления — **обязательная починка ссылок**: некоторые ячейки могли указывать на удалённое состояние или на индекс, ставший невалидным. Проходим по всей таблице: если `nxt >= new_n` — такое состояние больше не существует — заменяем на случайное из оставшихся.

`fa.fitness = None` — сбрасываем оценку: мы изменили автомат, старая оценка недействительна.

---

## Часть 9. Скрещивание — функция `crossover_automata`

**Когда вызывается:** внутри `evolve_population` с вероятностью 70%, когда создаётся очередной потомок.

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

`n = min(fa1.n_states, fa2.n_states)` — берём **меньшее** из двух чисел состояний. Если у родителей разное количество состояний (например, 4 и 6), потомки получат 4 состояния. Лишние строки большего родителя просто игнорируются.

Цикл `for s in range(n)` — для каждой строки таблицы «бросаем монетку»:
- Орёл (< 0.5): потомок 1 берёт строку от родителя 1, потомок 2 — от родителя 2.
- Решка (≥ 0.5): наоборот.

Это **однородный кроссовер**: каждая строка независимо, случайно достаётся от одного из родителей. В результате получаем двух разных потомков — смеси обоих родителей.

`deepcopy(fa1.table[s])` — копируем строку, а не берём ссылку. Если потомок изменит свою таблицу — это не должно затронуть таблицу родителя.

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

`def fix(table, max_s):` — вложенная вспомогательная функция, видимая только внутри `crossover_automata`. Проверяет и исправляет ссылки на несуществующие состояния — та же задача, что и при удалении состояния в мутации. Если родитель-6 имел ссылку на состояние 5, а потомок имеет только 4 состояния (0–3) — такую ссылку нужно исправить.

`return FiniteAutomaton(n, table1), FiniteAutomaton(n, table2)` — возвращаем **двух** потомков сразу. В `evolve_population` используется только первый (`child, _ = crossover_automata(...)`).

---

## Часть 10. Отбор родителей — функция `tournament_select`

**Когда вызывается:** внутри `evolve_population` при создании каждого потомка.

```python
def tournament_select(population, k=TOURNAMENT_K):
    contestants = random.sample(population, min(k, len(population)))
    return max(contestants, key=lambda ind: ind.fitness)
```

`random.sample(population, min(k, len(population)))` — случайно выбираем `k = 4` особей **без повторений**. `min(k, len(population))` — защита: нельзя взять больше особей, чем есть в популяции.

`return max(contestants, key=lambda ind: ind.fitness)` — из четырёх случайных кандидатов возвращаем того, у кого **максимальный** фитнес. `lambda ind: ind.fitness` — анонимная функция: «взять у особи поле fitness».

**Почему турнир, а не просто «лучшие»?** Если всегда брать только топ-5 особей как родителей, популяция быстро станет однородной — все потомки будут похожи, эволюция застрянет. Турнирный отбор даёт шанс и средним особям стать родителями — это сохраняет **разнообразие генофонда**.

---

## Часть 11. Одно поколение — функция `evolve_population`

**Когда вызывается:** в конце каждой итерации главного цикла в `run_evolution`.

```python
def evolve_population(population, field):
    evaluate_population(population, field)

    population.sort(key=lambda ind: ind.fitness, reverse=True)

    new_population = [deepcopy(ind) for ind in population[:ELITISM_K]]
```

`evaluate_population(population, field)` — оцениваем всех ещё не оценённых особей (новичков прошлого поколения).

`population.sort(key=lambda ind: ind.fitness, reverse=True)` — сортируем список особей по убыванию фитнеса. `reverse=True` — от большего к меньшему. После этого `population[0]` — лучший, `population[-1]` — худший.

`new_population = [deepcopy(ind) for ind in population[:ELITISM_K]]` — **элитизм**: берём первые `ELITISM_K = 5` особей (лучших) и копируем их напрямую в новое поколение. `population[:5]` — срез списка: первые 5 элементов. `deepcopy` — полная копия, иначе элита и потомки были бы одними и теми же объектами.

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

`while len(new_population) < POP_SIZE:` — продолжаем, пока не наберём 100 особей (5 уже есть — элиты).

`parent1 = tournament_select(population)` — выбираем первого родителя турниром.

`if random.random() < CROSSOVER_PROB:` — с вероятностью 70% делаем скрещивание:
- Выбираем второго родителя.
- `child, _ = crossover_automata(parent1, parent2)` — скрещиваем. Функция возвращает двух потомков, берём только первого.

Иначе (30%) — `child = deepcopy(parent1)` — потомок является точной копией одного родителя (клонирование), к которой затем применяется только мутация.

`child = mutate_automaton(child, ...)` — **мутация применяется всегда**, и к детям от кроссовера, и к клонам.

`new_population.append(child)` — добавляем потомка в новое поколение.

`return new_population` — возвращаем готовое следующее поколение из 100 особей.

---

## Часть 12. Главный цикл — функция `run_evolution`

**Когда вызывается:** один раз, в разделе 6. Это «сердце» всей программы.

```python
def run_evolution(field):
    total_food = int(field.sum() == FOOD * (field == FOOD).sum()
                     or True) and int((field == FOOD).sum())
```

Эта строка выглядит сложно, но суть проста: `int((field == FOOD).sum())` — считаем количество клеток с едой на поле. `(field == FOOD)` создаёт матрицу True/False (True там, где значение равно FOOD=1). `.sum()` суммирует: True считается как 1, False как 0. Результат — общее число клеток с едой.

```python
    population = [random_automaton(INIT_STATES) for _ in range(POP_SIZE)]

    history_best   = []
    history_avg    = []
    history_states = []

    best_ever = None
```

`[random_automaton(INIT_STATES) for _ in range(POP_SIZE)]` — создаём список из 100 случайных автоматов, каждый с `INIT_STATES = 4` состояниями. Это **первое поколение**.

Три пустых списка `history_*` — для записи статистики по поколениям. Будут использованы для графиков.

`best_ever = None` — переменная для хранения лучшего автомата за **всё время** (не только за текущее поколение). Начинается как `None` — «ничего ещё не видели».

```python
    for gen in range(N_GENERATIONS):
        evaluate_population(population, field)

        fitnesses   = [ind.fitness for ind in population]
        best_ind    = max(population, key=lambda ind: ind.fitness)
        avg_fitness = float(np.mean(fitnesses))
        avg_states  = float(np.mean([ind.n_states for ind in population]))
```

`for gen in range(N_GENERATIONS):` — главный цикл: 150 итераций = 150 поколений.

`evaluate_population(population, field)` — оцениваем всех, кто ещё не оценён.

`fitnesses = [ind.fitness for ind in population]` — собираем все оценки в отдельный список для удобного вычисления статистики.

`best_ind = max(population, key=lambda ind: ind.fitness)` — находим лучшую особь **текущего** поколения.

`avg_fitness = float(np.mean(fitnesses))` — среднее значение фитнеса по всей популяции. `np.mean` считает среднее арифметическое. `float(...)` конвертирует результат numpy в обычное число Python.

`avg_states = float(np.mean([ind.n_states for ind in population]))` — среднее число состояний автоматов. Это интересная метрика: эволюция сама выбирает, сколько состояний нужно — меньше или больше начальных четырёх.

```python
        if best_ever is None or best_ind.fitness > best_ever.fitness:
            best_ever = deepcopy(best_ind)
```

Если `best_ever` ещё не задан (первое поколение) или текущий лучший лучше абсолютного рекорда — обновляем рекорд. `deepcopy` — сохраняем снимок, не ссылку: в следующем поколении этот объект может быть изменён мутацией.

```python
        history_best.append(best_ever.fitness)
        history_avg.append(avg_fitness)
        history_states.append(avg_states)

        print(f"Gen {gen+1:4d}/{N_GENERATIONS} | ...")

        population = evolve_population(population, field)

    return best_ever, history_best, history_avg, history_states
```

Добавляем текущую статистику в историю. Печатаем прогресс. Вызываем `evolve_population` — получаем следующее поколение. И снова — на следующую итерацию.

В конце 150 поколений возвращаем: лучший автомат за всё время + три списка статистики для графиков.

---

## Часть 13. Запуск и финальный результат — разделы 6 и 7

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

Генерируем поле, считаем еду, запускаем эволюцию. Всё предыдущее — подготовка, вот здесь начинается реальная работа.

```python
food_collected, best_path = simulate_ant(field, best_fa, MAX_STEPS, GRID_SIZE)
```

После эволюции запускаем лучшего автомата ещё раз — но теперь **на исходном поле** (без изменений). Это нужно, чтобы получить полный путь для визуализации. В ходе эволюции путь не сохранялся (он был бы выброшен через `_`).

```python
for s, row in enumerate(best_fa.table):
    cols = []
    for inp in range(N_INPUTS):
        act, nxt = row[inp]
        cols.append(f"{ACTION_NAMES[act]}→s{nxt}")
    print(f"  s{s:<10}{cols[0]:<20}{cols[1]:<20}{cols[2]:<20}")
```

`enumerate(best_fa.table)` — перебирает строки таблицы, одновременно давая индекс `s` и саму строку `row`.

Для каждой строки формируем читаемый текст ячейки: `ACTION_NAMES[act]` превращает число действия в слово, `→s{nxt}` добавляет номер следующего состояния. Например: `Forward→s2`.

`:<10` и `:<20` — форматирование с выравниванием: текст дополняется пробелами до указанной ширины, что создаёт аккуратные столбцы.

---

## Итог: полный жизненный цикл ещё раз

Теперь, зная все функции, можно прочитать весь процесс как одну историю:

1. `generate_field` → поле создано, на нём ~205 клеток с едой.
2. `random_automaton × 100` → 100 случайных «мозгов», каждый — таблица из 4×3 случайных правил.
3. **Поколение 1:** `evaluate_population` → для каждого автомата запускается `simulate_ant` (500 шагов, `sense_ahead` и `automaton.transition` на каждом шаге). Лучший собрал, допустим, 15 единиц еды из 205.
4. `evolve_population` → 5 лучших сохранены, 95 новых создаются через `tournament_select` + `crossover_automata` + `mutate_automaton`.
5. **Поколение 2–150:** процесс повторяется. Каждые несколько поколений появляются автоматы, нашедшие более удачные паттерны движения — идти вдоль стен, разворачиваться при тупиках, целенаправленно двигаться к еде.
6. После 150 поколений `best_ever` — автомат, который за 500 шагов собрал максимум еды за всю историю эволюции. Его таблица переходов, маршрут и статистика выводятся в финале.
Done
