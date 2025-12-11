# Reverse me

## Preliminary

### GDB syntax

## Different syntaxe for the dessambly code !

| Syntaxe                               | Ordre                     | Exemple                                           |
| ------------------------------------- | ------------------------- | ------------------------------------------------- |
| **AT&T (Linux/GDB, objdump)**         | `mov source, destination` | `mov %eax, -0x7a(%ebp)` → écrit EAX dans la stack |
| **Intel / NASM / libasm C tutorials** | `mov destination, source` | `mov [ebp-0x7a], eax` → écrit EAX dans la stack   |

---

| Operand Type            | GDB Syntax          | Example             | Stored Where?                       | Notes                                                                |
| ----------------------- | ------------------- | ------------------- | ----------------------------------- | -------------------------------------------------------------------- |
| **Register**            | `$<reg>`            | `$eax`, `$ebx`      | CPU register                        | Fastest access; no memory read/write                                 |
| **Immediate value**     | `$<number>`         | `$0x0`, `$42`       | Encoded in instruction (not memory) | Literal constant; used for comparison or assignment                  |
| **Memory address**      | `<address>`         | `0x5655623a`        | RAM / process memory                | Reading/writing via dereference; `$` not used                        |
| **Dereferenced memory** | `*(type*)<address>` | `*(int*)0x5655623a` | RAM                                 | Reads/writes content at given address, interpreted as specified type |

### GDB commands

| Action                          | GDB Command        |
| ------------------------------- | ------------------ |
| Read register                   | `print $eax`       |
| Set register                    | `set $eax = $0x10` |
| Read immediate (assign literal) | `set $ecx = $42`   |
| Examine memory                  | `x/16x 0x56556000` |
| Examine memory at register      | `x/16x $esp`       |
| Jump execution                  | `jump *0x5655623a` |

### Differents type of values

| Prefix        | Example        | Type                | Stored Where / Meaning                                                                                  |
| ------------- | -------------- | ------------------- | ------------------------------------------------------------------------------------------------------- |
| **`%`**       | `%eax`, `%ebx` | **Register**        | Inside the **CPU**, not in RAM. Holds values like counters, pointers, flags. Fastest access.            |
| **`$`**       | `$0x0`, `$42`  | **Immediate value** | Encoded **in the instruction**. Never in MEMORY !.                                       |
| *(no prefix)* | `0x5655623a`   | **Memory address**  | Points to a location in **RAM** : (stack, heap, .rodata, etc.). Dereference to access content. |

---

PS : You can see my libasm project if you want to know more about assembly.

# LEVEL resolution TUTO from the beginning

First you have to know the archtecture of your binary.

```bash
file level1
level1: ELF 32-bit LSB pie executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=eb5da614822252396c09636a0c179de2fe79938c, for GNU/Linux 3.2.0, not stripped
```

Because it will impact your analyze with gdb. Here this is 32bits. There are not the same registers names. And size of registers are differents. (32bits registers -> 4 bytes)

## Level1

```bash
$ ./level1
Please enter key: test
Nope.
```
We know that this is a comparison that is done.

Let's reverse this.


`gdb ./level1`

`(gdb) disas main`

```bash
...
call strcmp
cmp $0x0, %eax
...
```

So we know that the real key is in the program because it compares it with the input of the user.

Here is the interesting sequence, seem to be a flag/key construction
```text
   0x000011e0 <+32>:    mov    -0x1ff8(%ebx),%eax
   0x000011e6 <+38>:    mov    %eax,-0x7a(%ebp)
   0x000011e9 <+41>:    mov    -0x1ff4(%ebx),%eax
   0x000011ef <+47>:    mov    %eax,-0x76(%ebp)
   0x000011f2 <+50>:    mov    -0x1ff0(%ebx),%eax
   0x000011f8 <+56>:    mov    %eax,-0x72(%ebp)
   0x000011fb <+59>:    mov    -0x1fec(%ebx),%ax
   0x00001202 <+66>:    mov    %ax,-0x6e(%ebp)
   0x00001206 <+70>:    lea    -0x1fea(%ebx),%eax
   0x0000120c <+76>:    mov    %eax,(%esp)
   0x0000120f <+79>:    call   0x1060 <printf@plt>
```

### Important 

This syntax is like **a function call** in reality : `instruction source, destination`

`-0x7a(%ebp)` it means offset(register)

> `Adresse = EBP - 0x7A`

So like we are in AT&T syntax 
`0x000011e0 <+32>:    mov    -0x1ff8(%ebx),%eax` means put content of addr %ebx - 0x8 and put it in eax.


So we can separate all the line by 4 important operation that do the same logic :

```bash
0x000011e0 <+32>:    mov    -0x1ff8(%ebx),%eax -> Copy -0x1ff8(%ebx) in eax, 
0x000011e6 <+38>:    mov    %eax,-0x7a(%ebp)   -> Copy eax in -0x7a(%ebp). START OF THE STRING

0x000011e9 <+41>:    mov    -0x1ff4(%ebx),%eax
0x000011ef <+47>:    mov    %eax,-0x76(%ebp)

0x000011f2 <+50>:    mov    -0x1ff0(%ebx),%eax
0x000011f8 <+56>:    mov    %eax,-0x72(%ebp)

0x000011fb <+59>:    mov    -0x1fec(%ebx),%ax
0x00001202 <+66>:    mov    %ax,-0x6e(%ebp)

eax is just a temporary register to store the value.
All the flag/key is stored in ebp.
```

If we reconstitute the ebp register we can add the 4 bytes.

START -> -0x7a(%ebp) -> ebp - 0x7a

No need to calculate any adress here or maths, GDB do its for you.

## Response 

```bash
(gdb) x/s $ebp-0x7a
0xffffc8fe:     "__stack_check"
```

Why we do x/s to print the key. We use the offset of the adress ebp.
> `x` is examine the memory
> `/s` is the format string

"__stack_check" is our flag
