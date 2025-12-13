#include <stdio.h>
#include <string.h>

int main(void)
{

    char input[100];
    char *key = "__stack_check";

    printf("Please enter key: ");
    scanf("%99s", input);

    if(!strcmp(input, key))
        printf("Good job.\n");
    else
        printf("Nope.\n");
}