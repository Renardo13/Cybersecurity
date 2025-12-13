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


## Understanding EBX and .rodata in 32-bit PIE Binaries

In a 32-bit **PIE (Position Independent Executable)** binary, memory layout is dynamic. One of the important segments is **`.rodata`**, which stores **read-only data** like:

- Strings and messages (`"Please enter key"`, `"Good job."`, `"Nope."`)  
- Constants used by the program  

The CPU uses **registers** to keep track of addresses. In this context:

**EBX = Pointer to `.rodata`**

---

## How EBX Works

- When a PIE binary starts, the **exact location of `.rodata` is unknown** because the program can be loaded at different addresses in memory.  
- The program calculates the base address of `.rodata` at runtime.  
- **EBX stores this base address**.

### Accessing Data in `.rodata`

Each string or constant in `.rodata` is accessed with an **offset from EBX**:

