#include <windows.h>
#include <stdio.h>

int main() {
    // ��������� ������� ������������ ����� � ������
    HANDLE hStdin = GetStdHandle(STD_INPUT_HANDLE);
    HANDLE hStdout = GetStdHandle(STD_OUTPUT_HANDLE);

    // ����� �������
    printf("Standard Input Handle: %p\n", hStdin);
    printf("Standard Output Handle: %p\n", hStdout);

    // ����������� ��� �����
    WriteFile(hStdout, "Enter some text: ", 17, NULL, NULL);

    // ������ ������ �� ������������ �����
    char buffer[256];
    DWORD bytesRead;
    ReadFile(hStdin, buffer, sizeof(buffer) - 1, &bytesRead, NULL);
    buffer[bytesRead] = '\0'; // ���������� ������������ ����

    // ����� ���������� ������
    WriteFile(hStdout, "You entered: ", 13, NULL, NULL);
    WriteFile(hStdout, buffer, bytesRead, NULL, NULL);

    return 0;
}