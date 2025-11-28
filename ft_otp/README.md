## ft_otp


## Introduction

OTP -> "One-Time Password"

Based on the HMAC-Based One-Time Password (HOTP) algorithm.

This is used for 2 factors authentification (2fa).


## Algorithm 

The HOTP value must be at least a 6-digit value.

Based on a shared value between user and server.

The algorithm MUST use a strong shared secret.  
The length of the shared secret MUST be at least 128 bits.

