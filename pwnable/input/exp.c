#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(int argc, const char *argv[])
{
    /* stage 1 */
    int     i   = 0;
    int     pid = 0;
    char    *my_argv[101]; 
    char    *my_env[2]; 
    int     pipe_fd0[2]; 
    int     pipe_fd2[2]; 

    setenv("PATH", "/home/ctf", 1);
    char *path = (char *)getenv("PATH");
    printf("%s", path);

    if (pipe(pipe_fd0) < 0 || pipe(pipe_fd2) < 0){
        printf("pipe0 create error\n");
        return -1;
    }

    for (;i < 100; i++){
        my_argv[i] = "AAAA";
    }
    my_argv['A'] = "\x00"; 
    my_argv['B'] = "\x20\x0a\x0d"; 
    my_argv['C'] = argv[1]; 
    my_argv[100] = NULL;

    if ((pid == fork()) > 0){
        /* child */
        close(pipe_fd0[1]);
        close(pipe_fd2[1]);

        dup2(pipe_fd0[0], 0);
        dup2(pipe_fd2[0], 2);


        /* stage 3 */
        my_env[0] = "\xde\xad\xbe\xef=\xca\xfe\xba\xbe";
        my_env[1] = NULL;
        execve("/home/ctf/pwn/input", my_argv, my_env);
    }
    else if (pid == 0){
        /* parent */
        /* stage 2 */
        close(pipe_fd0[0]);
        close(pipe_fd2[0]);

        write(pipe_fd0[1], "\x00\x0a\x00\xff", 4);
        write(pipe_fd2[1], "\x00\x0a\x02\xff", 4);

        /* stage 4 */
        FILE *fp = fopen("\x0a", "w");
        fwrite("\x00\x00\x00\x00", 4, 1, fp);
        fclose(fp);

        /* stage 5 */
        struct sockaddr_in  serv;
        int                 sd;

        sleep(1);
        bzero(&serv, sizeof(struct sockaddr_in));
        serv.sin_family         = AF_INET;
        serv.sin_port           = htons(atoi(argv[1]));
        serv.sin_addr.s_addr    = inet_addr("127.0.0.1");
        sd = socket(AF_INET, SOCK_STREAM, 0);
        connect(sd, (const struct sockaddr *)&serv, sizeof(struct sockaddr));
        send(sd, "\xde\xad\xbe\xef", 4, 0);
    }
    
    return 0;
}
