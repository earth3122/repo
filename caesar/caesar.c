#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

int main(int argc, string argv[])
{
    // handle lack of argv[1]
    if (argc == 1)
    {
        printf("Usage: ./caesar key\n");
        return 1; // 1 = error, 0 = ok
    }
    else

        // handle too many argument
        if (argc > 2)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
        else

            // handle normal
            if (argc == 2 && atoi(argv[1]) > 0)
            {
                string s = get_string("plaintext:  ");
                printf("ciphertext: ");
                int n = strlen(s);
                for (int i = 0; i < n; i++)
                {
                    if (isalpha(s[i])) // A=65, a=97, plus minus 32
                    {
                        if (isupper(s[i]))
                        {
                            printf("%c", ((s[i] + 13 + atoi(argv[1])) % 26) + 65);
                        }
                        else if (islower(s[i]))
                        {
                            printf("%c", ((s[i] + 7 + atoi(argv[1])) % 26) + 97);
                        }
                    }
                    else
                    {
                        printf("%c", s[i]);
                    }
                }
                printf("\n");
            }
            else

                // handle non-numeric
                if (!isdigit(argv[1][0]))
                {
                    printf("Usage: ./caesar key\n");
                    return 1;
                }
                else return 1;
}