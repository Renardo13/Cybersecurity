#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/hmac.h>
#include <openssl/sha.h>

uint32_t hotp(uint8_t *key, size_t key_len, uint64_t counter) {
    unsigned char counter_bytes[8];
    for(int i=7; i>=0; i--) {
        counter_bytes[i] = counter & 0xFF;
        counter >>= 8;
    }

    unsigned char hmac_result[SHA_DIGEST_LENGTH];
    unsigned int len = SHA_DIGEST_LENGTH;

    HMAC(EVP_sha1(), key, key_len, counter_bytes, 8, hmac_result, &len);

    int offset = hmac_result[19] & 0x0F;
    uint32_t bin_code = ((hmac_result[offset] & 0x7F) << 24) |
                        ((hmac_result[offset+1] & 0xFF) << 16) |
                        ((hmac_result[offset+2] & 0xFF) << 8) |
                        (hmac_result[offset+3] & 0xFF);
    return bin_code % 1000000;
}

int main() {
    uint8_t key[32] = { /* tes 32 octets ici */ };
    uint64_t counter = 0; // lire depuis fichier

    uint32_t otp = hotp(key, 32, counter);
    printf("%06u\n", otp);

    // incrémenter et sauvegarder le compteur pour la prochaine fois
    return 0;
}