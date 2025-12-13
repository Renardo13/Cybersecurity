#include "out.h"

int	_init(EVP_PKEY_CTX *ctx)

{
	int iVar1;

	iVar1 = __gmon_start__();
	return (iVar1);
}

void	FUN_00101020(void)

{
	(*(code *)(undefined *)0x0)();
	return ;
}

// WARNING: Unknown calling convention -- yet parameter storage is locked

int	puts(char *__s)

{
	int iVar1;

	iVar1 = puts(__s);
	return (iVar1);
}

// WARNING: Unknown calling convention -- yet parameter storage is locked

size_t	strlen(char *__s)

{
	size_t sVar1;

	sVar1 = strlen(__s);
	return (sVar1);
}

// WARNING: Unknown calling convention -- yet parameter storage is locked

int	printf(char *__format, ...)

{
	int iVar1;

	iVar1 = printf(__format);
	return (iVar1);
}

// WARNING: Unknown calling convention -- yet parameter storage is locked

void	*memset(void *__s, int __c, size_t __n)

{
	void *pvVar1;

	pvVar1 = memset(__s, __c, __n);
	return (pvVar1);
}

// WARNING: Unknown calling convention -- yet parameter storage is locked

int	strcmp(char *__s1, char *__s2)

{
	int iVar1;

	iVar1 = strcmp(__s1, __s2);
	return (iVar1);
}

// WARNING: Unknown calling convention -- yet parameter storage is locked

int	fflush(FILE *__stream)

{
	int iVar1;

	iVar1 = fflush(__stream);
	return (iVar1);
}

// WARNING: Unknown calling convention -- yet parameter storage is locked

int	atoi(char *__nptr)

{
	int iVar1;

	iVar1 = atoi(__nptr);
	return (iVar1);
}

void	__isoc99_scanf(void)

{
	__isoc99_scanf();
	return ;
}

// WARNING: Unknown calling convention -- yet parameter storage is locked

void	exit(int __status)

{
	// WARNING: Subroutine does not return (exit(__status));
}

void	__cxa_finalize(void)

{
	__cxa_finalize();
	return ;
}

void processEntry	_start(undefined8 param_1, undefined8 param_2)

{
	undefined1 auStack_8[8];

	__libc_start_main(main, param_2, &stack0x00000008, 0, 0, param_1,
		auStack_8);
	do
	{
		// WARNING: Do nothing block with infinite loop
	} while (true);
}

// WARNING: Removing unreachable block (ram,0x00101113)
// WARNING: Removing unreachable block (ram,0x0010111f)

void	deregister_tm_clones(void)

{
	return ;
}

// WARNING: Removing unreachable block (ram,0x00101154)
// WARNING: Removing unreachable block (ram,0x00101160)

void	register_tm_clones(void)

{
	return ;
}

void	__do_global_dtors_aux(void)

{
	if (completed_0 != '\0')
	{
		return ;
	}
	__cxa_finalize(__dso_handle);
	deregister_tm_clones();
	completed_0 = 1;
	return ;
}

void	frame_dummy(void)

{
	register_tm_clones();
	return ;
}

void	wt(void)

{
	puts("********");
	return ;
}

int	nice(int __inc)

{
	int iVar1;

	iVar1 = puts("nice");
	return (iVar1);
}

void	try(void)

{
	puts("try");
	return ;
}

void	but(void)

{
	puts("but");
	return ;
}

void	this(void)

{
	puts("this");
	return ;
}

void	it(void)

{
	puts("it");
	return ;
}

void	not(void)

{
	puts("not.");
	return ;
}

void	that(void)

{
	puts("that.");
	return ;
}

void	easy(void)

{
	puts("easy.");
	return ;
}

void	___syscall_malloc(void)

{
	puts("Nope.");
	// WARNING: Subroutine does not return (exit(1));
}

void	____syscall_malloc(void)

{
	puts("Good job.");
	return ;
}

// WARNING: Globals starting with '_' overlap smaller symbols at the same address

undefined8	main(void)

{
	ulong uVar1;
	int nb;
	size_t nbr;
	bool bool;
	char a;
	char b;
	char c;
	undefined1 local_49;
	char comparison_value[31];
	char str[9];
	ulong i;
	int local_18;
	int str_index;
	int scanf_ret;
	undefined4 local_c;

	local_c = 0;
	printf("Please enter key: ");
	scanf_ret = __isoc99_scanf(&DAT_00102056);
	if (scanf_ret != 1)
	{
		___syscall_malloc();
	}
	if (comparison_value[1] != '2')
	{
		___syscall_malloc();
	}
	if (comparison_value[0] != '4')
	{
		___syscall_malloc();
	}
	fflush(_stdin);
	memset(str, 0, 9);
	str[0] = '*';
	local_49 = 0;
	i = 2;
	str_index = 1;
	while (true)
	{
		nbr = strlen(str);
		uVar1 = i;
		bool = false;
		if (nbr < 8)
		{
			nbr = strlen(comparison_value);
			bool = uVar1 < nbr;
		}
		if (!bool)
			break ;
        // we know that this is contigus in memory 
		a = comparison_value[i];
		b = comparison_value[i + 1];
		c = comparison_value[i + 2];
		nb = atoi(&a);
		str[str_index] = (char)nb;
        // It goes 3 by 3 again 
		i += 3;
		str_index += 1;
	}
    // str_index should be 9 
	str[str_index] = '\0';
    // Result should be "********\n"
	local_18 = strcmp(str, "********");
	if (local_18 == -2)
	{
		___syscall_malloc();
	}
	else if (local_18 == -1)
	{
		___syscall_malloc();
	}
	else if (local_18 == 0)
	{
		____syscall_malloc();
	}
	else if (local_18 == 1)
	{
		___syscall_malloc();
	}
	else if (local_18 == 2)
	{
		___syscall_malloc();
	}
	else if (local_18 == 3)
	{
		___syscall_malloc();
	}
	else if (local_18 == 4)
	{
		___syscall_malloc();
	}
	else if (local_18 == 5)
	{
		___syscall_malloc();
	}
	else if (local_18 == 0x73)
	{
		___syscall_malloc();
	}
	else
	{
		___syscall_malloc();
	}
	return (0);
}

void	_fini(void)

{
	return ;
}
