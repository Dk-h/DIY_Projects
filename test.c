#include <stdio.h>

union test {
    char a;
    char b;
    int c;
} t;

struct dev {
    char a;
    char b;
    int c;
} tl;

int main() {
    printf("%lu\n", sizeof(t));   // size of union
    printf("%lu\n", sizeof(tl));  // size of struct
    return 0;
}
