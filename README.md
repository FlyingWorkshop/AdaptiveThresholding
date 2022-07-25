# GridCleaner
Re-implementing elementary image processing techniques without advanced libraries. These implementations aren't supposed to be faster than library code. I'm implementing these techniques from scractch for my own educational edification.

# Grayscale
It turns out that converting to grayscale is more complicated than you might first think. The naive approach is simply averaging the red, green, and blue channels, but this doesn't account for two things. First, it assumes that human eyes are equally sensitive to red, green, and blue. It turns out we are more sensitive to green. Second, it assumes humans perceive luminance linearly. This is also untrue. Imagine you're in a dark room. The difference between 0 and 1 lightbulb being on is more obvious than 100 lightbulbs versus 101 lightbulbs. Although we don't perceive luminance linearly, most digital cameras do. This leads to a problem called banding which you can learn more about in references.txt. Applying corrections for these problems gives us a more sophisticated grayscale conversion.

Hagia Sophia Grayscale (left = naive, right = sophisticated)  
*It can be hard to spot the difference. Look at the clarity of the detail in the dome and in the shadows on the right compared to the left.
![Alt text](/outputs/hagia_sophia_grayscale_comparison.png)

# Thresholding
Thresholding is the process of turning a grayscale image into a purely black and white image. Grayscale images aren't black and white because they have gray pixels. A black and white image has only fully-black pixels and fully-white pixels (i.e., pixel values at 0 or 255). The naive approach is to simply pick a threshold between 0 and 255, but this approach is often too crude for very dark/bright images. Another approach is to use Otsu's method which you learn more about from references.txt, but even this method is insufficient if we only search for a global threshold. We can refine this approach by applying Otsu's method (or searching for other measures of central tendency) locally across a scrolling window over the image.

## Global Thresholding
Black and White Gates of Hell (left = naive threshold, right = Otsu's method)
![Alt text](/outputs/gates_of_hell_otsu_vs_naive.png)
Black and White Hagia Sophia (left = naive threshold, right = Otsu's method)
![Alt text](/outputs/hagia_sophia_bw_comparison.png)



## Adaptive Thresholding
Local Median Thresholding with radius=1, 10, 20, 40 in descending order.
![Alt text](/outputs/gates_of_hell_local_median_r1.png)
![Alt text](/outputs/gates_of_hell_local_median_r10.png)
![Alt text](/outputs/gates_of_hell_local_median_r20.png)
![Alt text](/outputs/gates_of_hell_local_median_r40.png)
Local Median Thresholding with radius=20, 40 in descending order.
![Alt text](/outputs/hagia_sophia_local_median_r20.png)
![Alt text](/outputs/hagia_sophia_local_median_r40.png)

