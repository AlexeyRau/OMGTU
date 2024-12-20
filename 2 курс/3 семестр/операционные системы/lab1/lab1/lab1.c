#include <windows.h>
#include <stdio.h>

int main() {
    // Получение хэндлов стандартного ввода и вывода
    HANDLE hStdin = GetStdHandle(STD_INPUT_HANDLE);
    HANDLE hStdout = GetStdHandle(STD_OUTPUT_HANDLE);

    // Вывод хэндлов
    printf("Standard Input Handle: %p\n", hStdin);
    printf("Standard Output Handle: %p\n", hStdout);

    // Приглашение для ввода
    WriteFile(hStdout, "Enter some text: ", 17, NULL, NULL);

    // Чтение данных из стандартного ввода
    char buffer[256];
    DWORD bytesRead;
    ReadFile(hStdin, buffer, sizeof(buffer) - 1, &bytesRead, NULL);
    buffer[bytesRead] = '\0'; // Добавление завершающего нуля

    // Вывод введенного текста
    WriteFile(hStdout, "You entered: ", 13, NULL, NULL);
    WriteFile(hStdout, buffer, bytesRead, NULL, NULL);

    return 0;
}