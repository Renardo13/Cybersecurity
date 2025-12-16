# ft_otp (RFC 4226)


## Introduction

OTP -> "One-Time Password"

Based on the HMAC-Based One-Time Password (HOTP) algorithm. The H is for HMAC.
Difference with TOTP that use "time" to generate new passeword.

This is used for 2 factors authentification (2fa).

We use Big endian for the calcul -> The bits are read from the left to the right, the left is the most significant bit

---
## Prerequisites / Usage

You must use python3

### 1. Generate an encrypted key
Before using the OTP generator, you need a secret key to share between you and the server. You can provide a hexadecimal key (at least 64 characters) to generate an **encrypted key file**:

```bash
python3 ft_otp.py -g YOUR_HEX_KEY
```
The output is a ft_otp.key that just appeared in the folder.
You can now use it.
PS : The secret key enter by the user should be shared between the server and the person, its has to be __128__ bits size minimum but 160 is better.
```bash
python3 ft_otp.py -k ft_otp.key
```
The output is a new password OTP.

## Algorithm : ***Key points to code it***

***Step 1*** HMAC-SHA1: Generate a 20-byte (160-bit) HMAC __using the secret key__ and the __counter__.
PS : The counter increment at each time a new passeword is generated.
```
We take decimal value for more clarity
Bytes # :  0   1   2    3   4   5    6    7   8   9   10   11   12   13   14   15   16   17   18   19
Value :   31   134 152  105 14  2    202  22  97  133 80   239  127  25   218  142  148  91   85   90
```

***Step 2*** Dynamic Truncation: Instead of always taking the same 4 bytes, choose a dynamic offset based on the __low 4 bits__ of the __last byte__ of the HMAC to make it less predictable
```
Dynamic truncation because we never take the same bits.
---
Last byte is 90 -> in Binary 90 is 01011010.
Bits Less significant -> 1010.
1010 is 10 in decimal.
10 is our offset
```

***Step 3*** Extract 4 bytes: Take 4 consecutive bytes starting from this offset → this gives 31 significant bits (the most significant bit is masked to avoid signed integer issues).
```
So, we take the 4 bytes since the offset (10 in our exemple) -> since the 10th bytes
Bytes 10, 11, 12, 13 = 80, 239, 127, 25.
This is a total of 32 bits (4 Bytes* 8bits)
We take only the 31 bits to prevent to be interpreted as a negative value. The first bit should be 0.
Ex :
01010000 (0x50) -> 80 in decimal
AND
01111111  (0x7F) -> 127 in decimal
----------
00000000  = 0
So we do val & 0x7F
---
val = (80 << 24) + (239 << 16) + (127 << 8) + 25
     = 1342177280 + 15663104 + 32512 + 25
     = 1357880921
```

***Step 4*** Modulo: Compute code % 10^digits to reduce the number to a 6-digit OTP (or more if desired).
The HOTP value must be at least a 6-digit value

```
OTP = val & 10^6  |   (1 000 000)
OTP = 880921      |   (6 digit value)
```
---

## Conclusion

We can resume with the formula : 

### ***HOTP=Truncate(HMAC-SHA-1(K,C))mod10^6***

### Good to know

# ft_otp Key Handling

- The key is **not stored as raw hexadecimal** in the program when you enter it, because the shell considerate it as character and not number -> When you pass a key to the Python script, it is always received as a **string** (`str`).  

Example:

```bash
python3 ft_otp.py -g 35483176234978369723dhgfsdhfsagdhdsfhdfdfdgfshdgjhsgdfsf438756438765873465387465

So you have to convert it before using it
# If key is hexadecimal
key_bytes = bytes.fromhex(hex_key)

# If key is plain text
key_bytes = key_str.encode()

To make good conversion here is a tab with corresponding values ->
| Base                  | Bits par caractère |
| --------------------- | ------------------ |
| Binaire (base 2)      | 1 bit              |
| Octal (base 8)        | 3 bits             |
| Décimal (base 10)     | ~3.32 bits         |
| Hexadécimal (base 16) | 4 bits             | 
