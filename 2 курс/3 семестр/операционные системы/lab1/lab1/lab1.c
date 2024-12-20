#include <windows.h>
#include <stdio.h>

#define BUFFER_SIZE 1024

int main() {
	//Для корректного ввода и вывода русских букв
	SetConsoleOutputCP(1251);
	SetConsoleCP(1251);
	
	HANDLE hStdIn = GetStdHandle(STD_INPUT_HANDLE);
	HANDLE hStdOut = GetStdHandle(STD_OUTPUT_HANDLE);

	// Чтобы в output.txt не записывалась лишняя информация
	if (GetFileType(hStdOut) == FILE_TYPE_CHAR) {
		printf("Хэндл стандартного ввода: %p\n", hStdIn);
		printf("Хэндл стандартного вывода: %p\n", hStdOut);
		printf("Ввод: ");
	}

	char buffer[BUFFER_SIZE];
	DWORD bytesRead;
	ReadFile(hStdIn, buffer, BUFFER_SIZE - 1, &bytesRead, NULL);
	buffer[bytesRead] = '\0';
	printf("Вы ввели: %s", buffer);

	return 0;
}