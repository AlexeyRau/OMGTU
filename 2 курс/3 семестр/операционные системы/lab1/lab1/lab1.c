#include <windows.h>
#include <stdio.h>

#define BUFFER_SIZE 1024

int main() {
	SetConsoleOutputCP(1251);
	SetConsoleCP(1251);
	// Получение хэндлов стандартного ввода и вывода
	HANDLE hStdIn = GetStdHandle(STD_INPUT_HANDLE);
	HANDLE hStdOut = GetStdHandle(STD_OUTPUT_HANDLE);

	// Проверка, связан ли стандартный вывод с консолью
	if (GetFileType(hStdOut) == FILE_TYPE_CHAR) {
		// Вывод значений хэндлов только если вывод на консоль
		printf("Хэндл стандартного ввода: %p\n", hStdIn);
		printf("Хэндл стандартного вывода: %p\n", hStdOut);
		printf("Ввод: ");
	}

	// Чтение данных из стандартного ввода
	char buffer[BUFFER_SIZE];
	DWORD bytesRead;
	ReadFile(hStdIn, buffer, BUFFER_SIZE - 1, &bytesRead, NULL);
	buffer[bytesRead] = '\0';

	// Вывод введенных данных
	printf("Вы ввели: %s", buffer);

	return 0;
}