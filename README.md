# GridCleaner
Re-implementing elementary image processing techniques without advanced libraries. These implementations aren't supposed to be faster than library code. I'm implementing these techniques from scractch for my own educational edification.

# Grayscale
It turns out that converting to grayscale is more complicated than you might first think. The naive approach is simply averaging the red, green, and blue channels, but this doesn't account for two things. First, it assumes that human eyes are equally sensitive to red, green, and blue. It turns out we are more sensitive to green. Second, it assumes humans perceive luminance linearly. This is also untrue. Imagine you're in a dark room. The difference between 0 and 1 lightbulb being on is more obvious than 100 lightbulbs versus 101 lightbulbs. Although we don't perceive luminance linearly, most digital cameras do. This leads to a problem called banding which you can learn more about in references.txt. Applying corrections for these problems gives us a more sophisticated grayscale conversion.

Hagia Sophia Grayscale (left = naive, right = sophisticated)
![Alt text](/outputs/hagia_sophia_grayscale_comparison.png)

# Thresholding
## Global Thresholding
Compares global thresholding from Otsu's method versus the naive threshold 255//2.  
![Alt text](/outputs/gates_of_hell_otsu_vs_naive.png)

## Adaptive Thresholding
Local Median Thresholding with radius=1, 10, 20, 40 in descending order.
![Alt text](/outputs/gates_of_hell_local_median_r1.png)
![Alt text](/outputs/gates_of_hell_local_median_r10.png)
![Alt text](/outputs/gates_of_hell_local_median_r20.png)
![Alt text](/outputs/gates_of_hell_local_median_r40.png)
