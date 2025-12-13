#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int	main(void)
{
	char atoi_str[4];
	int ret;
	int val;
	int nb = 2;
	int index = 0;

	char input[100];
	char key[9];
	bool b;

	printf("Please enter key: ");
	scanf("%24s", input);
	if (input[1] != '0' || input[0] != '0')
		return (printf("Nope."));
	memset(key, 0, 9);
	while (true)
	{
		ret = strlen(key);
		b = false;

		if (ret < 8)
		{
			ret = strlen(input);
			b = (nb + 2) < ret;
		}

		if (!b)
			break ;

		atoi_str[0] = input[nb];
		atoi_str[1] = input[nb + 1];
		atoi_str[2] = input[nb + 2];
		atoi_str[3] = '\0';

		int atoi_ret = atoi(atoi_str);
		key[index] = (char)atoi_ret;

		nb += 3;
		index += 1;
	}
	key[index] = '\0';

	if (!strcmp("delabere", key))
		printf("Good job.\n");
	else
		printf("Nope.\n");
}