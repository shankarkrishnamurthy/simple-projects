#include<string.h>
#include<stdio.h>
char * changestr(char *ptr, int len)
{
    strncpy(ptr,"Hello World", len);
    return ptr;
}


int square(int i) 
{
    return i*i;
}

typedef struct t_s  {
    double v;
    int t;
    char *p;
} t_t;

static t_t t={12.1, 99, "whatever"};
t_t *getstruct(t_t *s)
{
    printf("C : %f %d %s\n", s->v, s->t, s->p);
    return &t;
}

struct CA {
   char *Keys;
   float *Values;
   char *Title;
   int Index;
};

void myfunc (struct CA *in, int n)
{
    int i;
    printf("Array of Struct Length: %d\n", n);
    for(i = 0; i < n; ++i)
    {
        printf("%d: Keys = %s\n",i,in[i].Keys);
        printf("%d: Values = %f %f\n",i,in[i].Values[0],in[i].Values[1]);
        printf("%d: Title = %s\n",i,in[i].Title);
        printf("%d: Index = %d\n",i,in[i].Index);
    }
}
