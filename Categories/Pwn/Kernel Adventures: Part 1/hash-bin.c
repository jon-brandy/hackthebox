#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

unsigned int hash(char *string) {
  int i;
  unsigned int uvar1;
  unsigned int res;

  res = 0;

  for (i = 0; i < strlen(string); i++) {  
    uvar1 = (res + string[i]) * 0x401;
    res = uvar1 ^ uvar1 >> 6 ^ string[i];
  }

  return res;
}

int main() {
  char password[8];
  scanf("%s", password);
  getchar();

  if (hash(password) == 0x03319f75) {
    puts("Yes");
  } else {
    puts("Nope");
  }

  return 0;
}
