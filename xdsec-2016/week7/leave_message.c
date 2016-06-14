#include <stdio.h>
#include <stdlib.h>


char name[32];
char *ptr[12];
int ptr_count = 0;

void menu()
{
  printf("\n\nWelcome to Message System\n\n");
  printf("1.leave message\n");
  printf("2.show message\n");
  printf("3.edit message\n");
  printf("4.delete message\n");
  printf("5. Exit\n");
}

void input_name()
{
  memset(name,0,32);
  printf("What's your name\n");
  read(0,name,31);
}


void leave_message()
{
    int index;
    if(ptr_count>=0 &&  ptr_count<=11)
    {
        char *buf = (char *)malloc(32);
        if(buf > 0)
        {
              memset(buf,0,32);
              read(0,buf,31);
              index = ptr_count;
              ptr_count++;
              ptr[index] = buf;
        }
        else
        {
          printf("malloc error\n");
          exit(0);
        }
    }
    else
    {
      printf("full\n");
    }
}

int get_choice()
{
  int choice;
  scanf("%d",&choice);
  return choice;
}
void show_message()
{
  int index;
  printf("Input show index:\n");
  index = get_choice();
  if(index>=0 && index <=11)
  {
      printf("%s",ptr[index]);
  }
  else
  {
    printf("error\n");
  }
}


void edit_message()
{
    printf("Input edit index:\n");
    int index;
    index = get_choice();
    if(index >=0 && index <=11)
    {
        read(0,ptr[index],31);
    }
    else
    {
      printf("error index\n");
    }
}

void delete_message()
{
  printf("Input delete index:\n");
  int index;
  index = get_choice();
  if (index >=0 && index <= 11)
  {
    free(ptr[index]);
  }
  else
  {
      printf("error index\n");    
  }
}

void main()
{
  setbuf(stdin,0);
  setbuf(stdout,0);
  input_name();
  while ( 1 )
  {
    menu();
    switch ( get_choice() )
    {
      case 1:
        leave_message();
        break;
      case 2:
        show_message();
        break;
      case 3:
        edit_message();
        break;
      case 4:
        delete_message();
        break;
      case 5:
        exit(0);
        return;
      default:
        printf("opt error!\n");
        break;
    }
  }
}