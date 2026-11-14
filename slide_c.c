#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

/* 精确黄金对: UGCSystem 密文(去 12B 头) + 明文 */
static uint32_t cdata[4096];
static int n;
static uint8_t ref[64];

static uint32_t rotl(uint32_t x, int s) { return (x << s) | (x >> (32 - s)); }

/* XXTEA 解密并检查前 64B 匹配明文 */
static int check(const uint8_t *key16) {
    uint32_t k[4];
    memcpy(k, key16, 16);
    uint32_t v[4096];
    memcpy(v, cdata, n * 4);
    uint32_t delta = 0x9e3779b9;
    int rounds = 6 + 52 / n;
    uint32_t sumv = rounds * delta;
    while (sumv != 0) {
        uint32_t e = sumv >> 2;
        uint32_t y = v[0];
        for (int p = n - 1; p > 0; p--) {
            uint32_t z = v[p - 1];
            uint32_t ki = (p ^ e) & 3;
            uint32_t mx = ((((z ^ k[ki]) + (y ^ sumv)) & 0xffffffffu) ^
                           ((((y >> 3) ^ ((z << 4) & 0xffffffffu)) +
                             (((y << 2) & 0xffffffffu) ^ (z >> 5))) & 0xffffffffu)) & 0xffffffffu;
            v[p] = (v[p] - mx) & 0xffffffffu;
            y = v[p];
        }
        {
            uint32_t z = v[n - 1];
            uint32_t ki = e & 3;
            uint32_t mx0 = (((((z >> 5) ^ ((y << 2) & 0xffffffffu)) +
                              (((z << 4) & 0xffffffffu) ^ (y >> 3))) & 0xffffffffu) ^
                            (((y ^ sumv) + (z ^ k[ki])) & 0xffffffffu)) & 0xffffffffu;
            v[0] = (v[0] - mx0) & 0xffffffffu;
        }
        sumv -= delta;
    }
    /* 比较前 64B */
    uint8_t *out = (uint8_t *)v;
    int m = 0;
    for (int i = 0; i < 64; i++) if (out[i] == ref[i]) m++;
    return m > 48;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s cipher.bin plain.luac\n", argv[0]); return 1; }
    FILE *fc = fopen(argv[1], "rb");
    if (!fc) { perror("cipher"); return 1; }
    fseek(fc, 12, SEEK_SET); /* 跳过 X1V5fzTo + nonce */
    n = (int)fread(cdata, 4, 4096, fc);
    fclose(fc);
    FILE *fp = fopen(argv[2], "rb");
    if (!fp) { perror("plain"); return 1; }
    fread(ref, 1, 64, fp);
    fclose(fp);
    /* 从 stdin 读候选 16B 块, 每行一个 hex */
    char line[64];
    uint8_t key[16];
    long tested = 0, hits = 0;
    while (fgets(line, sizeof(line), stdin)) {
        if (strlen(line) >= 32) {
            for (int i = 0; i < 16; i++) {
                unsigned v;
                sscanf(line + i * 2, "%2x", &v);
                key[i] = (uint8_t)v;
            }
            tested++;
            if (check(key)) {
                hits++;
                fprintf(stderr, "HIT: %s\n", line);
            }
        }
    }
    fprintf(stderr, "tested=%ld hits=%ld\n", tested, hits);
    return 0;
}
