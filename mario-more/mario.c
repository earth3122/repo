#include <cs50.h>
#include <stdio.h>

int main(void)
{

    // check if negative or more than eight
    int n;
    do
    {
        n = get_int("Size: ");
    }
    while (n < 1 || n > 8);

    //print pyramid
    for (int i = 0; i < n; i++)
    {

        //first space
        for (int j = n - i - 1; j < n && j > 0; j--)
        {
            printf(" ");
        }

        //first block
        for (int k = n - i - 1; k < n; k++)
        {
            printf("#");
        }

        //middle space
        printf("  ");

        //end block
        for (int k = n - i - 1; k < n; k++)
        {
            printf("#");
        }

        printf("\n");
    }
}