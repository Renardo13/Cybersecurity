# Reverse me

## GDB syntax

| Operand Type            | GDB Syntax          | Example             | Stored Where?                       | Notes                                                                |
| ----------------------- | ------------------- | ------------------- | ----------------------------------- | -------------------------------------------------------------------- |
| **Register**            | `$<reg>`            | `$eax`, `$ebx`      | CPU register                        | Fastest access; no memory read/write                                 |
| **Immediate value**     | `$<number>`         | `$0x0`, `$42`       | Encoded in instruction (not memory) | Literal constant; used for comparison or assignment                  |
| **Memory address**      | `<address>`         | `0x5655623a`        | RAM / process memory                | Reading/writing via dereference; `$` not used                        |
| **Dereferenced memory** | `*(type*)<address>` | `*(int*)0x5655623a` | RAM                                 | Reads/writes content at given address, interpreted as specified type |

## GDB commands

| Action                          | GDB Command        |
| ------------------------------- | ------------------ |
| Read register                   | `print $eax`       |
| Set register                    | `set $eax = $0x10` |
| Read immediate (assign literal) | `set $ecx = $42`   |
| Examine memory                  | `x/16x 0x56556000` |
| Examine memory at register      | `x/16x $esp`       |
| Jump execution                  | `jump *0x5655623a` |

## Differents type of values

| Prefix        | Example        | Type                | Stored Where / Meaning                                                                                  |
| ------------- | -------------- | ------------------- | ------------------------------------------------------------------------------------------------------- |
| **`%`**       | `%eax`, `%ebx` | **Register**        | Inside the **CPU**, not in RAM. Holds values like counters, pointers, flags. Fastest access.            |
| **`$`**       | `$0x0`, `$42`  | **Immediate value** | Encoded **in the instruction**. Never in MEMORY !.                                       |
| *(no prefix)* | `0x5655623a`   | **Memory address**  | Points to a location in **process memory** RAM : (stack, heap, .rodata, etc.). Dereference to access content. |
