#define SYSCALL_WRITE 1
#define SYSCALL_READ  0
#define SYSCALL_EXIT 60

#define STDOUT_FD 1

typedef long long int64;

void exit(int64 arg1) {
  asm(
      "mov $60, %%rax\n"
      "mov %0, %%rdi\n"
      "syscall"
      :
      : "r"(arg1)
      : "%rdi"
  );
}

int64 write_t(int64 arg1, int64 arg2, int64 arg3) {
  asm(
      "mov $1, %%rax\n"
      "mov %0, %%rdi\n"
      "mov %1, %%rsi\n"
      "mov %2, %%rdx\n"
      "syscall"
      :
      : "r"(arg1), "r"(arg2), "r"(arg3)
      : "%rdi", "%rsi", "%rdx"
  );
}

int64 read_t(int64 arg1, int64 arg2, int64 arg3) {
  asm(
      "mov $0, %%rax\n"
      "mov %0, %%rdi\n"
      "mov %1, %%rsi\n"
      "mov %2, %%rdx\n"
      "syscall"
      :
      : "r"(arg1), "r"(arg2), "r"(arg3)
      : "%rdi", "%rsi", "%rdx"
  );
}

void read(int64 arg1, int64 arg2, int64 arg3) {
    int64 num = arg3;
    int64 loc = 0;
    int64 temp = 0;
    while (loc < num) {
        temp = read_t(arg1, arg2 + loc, arg3);
        if (temp < 0)
            exit(1);
        loc += temp;
    }
}

void write(int64 arg1, int64 arg2, int64 arg3) {
    int64 num = arg3;
    int64 loc = 0;
    int64 temp = 0;
    while (loc < num) {
        temp = write_t(arg1, arg2 + loc, arg3);
        if (temp < 0)
            exit(1);
        loc += temp;
    }
}
