#include "helpers.h"
#include <math.h>

// EXE gray sepia reflect blur
// ./filter -g infile.bmp outfile.bmp
// ./filter -s infile.bmp outfile.bmp
// ./filter -r infile.bmp outfile.bmp
// ./filter -b infile.bmp outfile.bmp

// Convert image to grayscale / make r g b value to the same avg amt
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)    // row
    {
        for (int j = 0; j < width; j++) // column
        {
            int avg = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            image[i][j].rgbtRed   = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue  = avg;
        }
    }
    return;
}
// ./filter -g images/yard.bmp out.bmp

// Convert image to sepia / convert to sepia equiv
// formular below / round to the nearest integer
// have to be in valid range (min 1, max 255)
// sepia Red   = (0.393 * Red) + (0.769 * Green) + (0.189 * Blue)
// sepia Green = (0.349 * Red) + (0.686 * Green) + (0.168 * Blue)
// sepia Blue  = (0.272 * Red) + (0.534 * Green) + (0.131 * Blue)
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float newR = (0.393 * image[i][j].rgbtRed) + (0.769 * image[i][j].rgbtGreen) + (0.189 * image[i][j].rgbtBlue);
            float newG = (0.349 * image[i][j].rgbtRed) + (0.686 * image[i][j].rgbtGreen) + (0.168 * image[i][j].rgbtBlue);
            float newB = (0.272 * image[i][j].rgbtRed) + (0.534 * image[i][j].rgbtGreen) + (0.131 * image[i][j].rgbtBlue);

            int newred   = (int) round(fmin(fmax(newR, 0), 255));
            int newgreen = (int) round(fmin(fmax(newG, 0), 255));
            int newblue  = (int) round(fmin(fmax(newB, 0), 255));

            image[i][j].rgbtRed   = newred;
            image[i][j].rgbtGreen = newgreen;
            image[i][j].rgbtBlue  = newblue;
        }
    }
    return;
}
// ./filter -s images/yard.bmp out.bmp

// Reflect image horizontally
// rows stay in order / columns reflect
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width /2; j++)
        {
            RGBTRIPLE triple = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width -j -1] = triple;
        }
    }
    return;
}
// ./filter -r images/yard.bmp out.bmp

// Blur image / average 9 pixels around (1+8 around)
// for edges, average available pixels only (1+3 at corner, 1+5 at side)
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE newpic[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float red = 0, green = 0, blue = 0;
            int count = 0;

    // pixels at corners
        if ((((i == 0) && (j == 0))) || (((i == 0) && (j == width - 1))) || (((i == height - 1) && (j == 0))) || (((i == height - 1) && (j == width - 1))))
        {
            for (int di = 0; di <= 1; di++)
            {
                for (int dj = 0; dj <= 1; dj++)
                {
                    if (i + di < height && j + dj < width)
                    {
                        red   += image[i + di][j + dj].rgbtRed;
                        green += image[i + di][j + dj].rgbtGreen;
                        blue  += image[i + di][j + dj].rgbtBlue;
                        count++;
                    }
                }
            }
        } else

    // pixels at sides
        if (i == 0 || i == height - 1 || j == 0 || j == width -1)
        {
            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    if (i + di >= 0 && i + di < height && j + dj >= 0 && j + dj < width)
                    {
                        red   += image[i + di][j + dj].rgbtRed;
                        green += image[i + di][j + dj].rgbtGreen;
                        blue  += image[i + di][j + dj].rgbtBlue;
                        count++;
                    }
                }
            }
        } else

    // pixels else
        {
            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    if (i + di >= 0 && i + di < height && j + dj >= 0 && j + dj < width)
                    {
                        red   += image[i + di][j + dj].rgbtRed;
                        green += image[i + di][j + dj].rgbtGreen;
                        blue  += image[i + di][j + dj].rgbtBlue;
                        count++;
                    }
                }
            }
        }

        newpic[i][j].rgbtRed   = round(red   / count);
        newpic[i][j].rgbtGreen = round(green / count);
        newpic[i][j].rgbtBlue  = round(blue  / count);
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = newpic[i][j];
        }
    }
    return;
}
// ./filter -b images/yard.bmp out.bmp