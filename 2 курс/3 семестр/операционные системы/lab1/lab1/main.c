#include <windows.h>
#include <stdio.h>

int main() {
    // Получение хэндлов стандартного ввода и вывода
    HANDLE hStdIn = GetStdHandle(STD_INPUT_HANDLE);
    HANDLE hStdOut = GetStdHandle(STD_OUTPUT_HANDLE);

    // Вывод значений хэндлов
    printf("Standard Input Handle: %p\n", hStdIn);
    printf("Standard Output Handle: %p\n", hStdOut);

    // Приглашение для ввода
    WriteFile(hStdOut, "Enter some text: ", 17, NULL, NULL);

    // Чтение ввода
    char buffer[256];
    DWORD bytesRead;
    ReadFile(hStdIn, buffer, sizeof(buffer) - 1, &bytesRead, NULL);
    buffer[bytesRead] = '\0'; // Добавление завершающего нуля

    // Вывод введенного текста
    WriteFile(hStdOut, "You entered: ", 13, NULL, NULL);
    WriteFile(hStdOut, buffer, bytesRead, NULL, NULL);
    WriteFile(hStdOut, "\n", 1, NULL, NULL);

    return 0;
}