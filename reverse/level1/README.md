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
> `x` is eXamine the memory
> `/s` is the format string

"__stack_check" is our flag

---

## Second method (real one)

### Stack layout explanation

In a 32-bit binary, local variables are stored in the function stack frame and accessed using EBP-relative offsets:

Ghidra pseudo code c :
```text
local_c = 0;
local_7e[0] = '_';
local_7e[1] = '_';
local_7e[2] = 's';
local_7e[3] = 't';
local_7a[0] = 'a';
local_7a[1] = 'c';
local_7a[2] = 'k';
local_7a[3] = '_';
local_76[0] = 'c';
local_76[1] = 'h';
local_76[2] = 'e';
local_76[3] = 'c';
local_72[0] = 'k';
local_72[1] = '\0';
```

```text
EBP - 0x7a  -> local_7e (4 bytes)
EBP - 0x76  -> local_7a (4 bytes)
EBP - 0x72  -> local_76 (4 bytes)
EBP - 0x6e  -> local_72 (2 bytes)
```

The key is separate in for blocs, but you can easily reconstruct it.

