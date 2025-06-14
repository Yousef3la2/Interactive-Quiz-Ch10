import fitz
import re
import streamlit as st
import random
from collections import defaultdict

questions = [
    {
        "question": "1. What is the primary goal of image segmentation?",
        "options": {
            "A": "Enhance the contrast of an image",
            "B": "Reduce noise in the image",
            "C": "Partition an image into meaningful regions",
            "D": "Convert RGB images to grayscale"
        },
        "correct": "C"
    },
    {
        "question": "2. What type of segmentation is based on abrupt changes in intensity?",
        "options": {
            "A": "Thresholding",
            "B": "Region growing",
            "C": "Edge-based segmentation",
            "D": "Clustering"
        },
        "correct": "C"
    },
    {
        "question": "3. Which segmentation method is most affected by uneven lighting?",
        "options": {
            "A": "Morphological segmentation",
            "B": "Global thresholding",
            "C": "K-means clustering",
            "D": "Graph-based segmentation"
        },
        "correct": "B"
    },
    {
        "question": "4. In global thresholding, what determines whether a pixel is foreground or background?",
        "options": {
            "A": "Color gradient",
            "B": "Pixel shape",
            "C": "Threshold value T",
            "D": "Noise pattern"
        },
        "correct": "C"
    },
    {
        "question": "5. What is the result of applying edge detection to a uniform region?",
        "options": {
            "A": "Random colors",
            "B": "Uniform threshold",
            "C": "No edges",
            "D": "High contrast"
        },
        "correct": "C"
    },
    {
        "question": "6. Which of the following methods segments based on pixel similarity?",
        "options": {
            "A": "Laplacian",
            "B": "Thresholding",
            "C": "Region growing",
            "D": "Canny edge detection"
        },
        "correct": "C"
    },
    {
        "question": "7. What does the standard deviation of pixel intensity indicate in texture segmentation?",
        "options": {
            "A": "Color tone",
            "B": "Noise strength",
            "C": "Edge sharpness",
            "D": "Texture variation"
        },
        "correct": "D"
    },
    {
        "question": "8. What does a histogram valley typically suggest for thresholding?",
        "options": {
            "A": "A blur",
            "B": "A good threshold value",
            "C": "A noisy area",
            "D": "High reflectance"
        },
        "correct": "B"
    },
    {
        "question": "9. What is the first step in the iterative thresholding algorithm?",
        "options": {
            "A": "Smoothing the image",
            "B": "Selecting an initial threshold",
            "C": "Calculating region mean",
            "D": "Histogram equalization"
        },
        "correct": "B"
    },
    {
        "question": "10. Which method improves thresholding by considering local neighborhoods?",
        "options": {
            "A": "Global thresholding",
            "B": "Adaptive thresholding",
            "C": "Canny edge detection",
            "D": "Watershed segmentation"
        },
        "correct": "B"
    },
    {
        "question": "11. What does the Marr-Hildreth edge detector use for finding edges?",
        "options": {
            "A": "Histogram binning",
            "B": "Gradient direction",
            "C": "Zero-crossings in Laplacian of Gaussian",
            "D": "Smoothing filters"
        },
        "correct": "C"
    },
    {
        "question": "12. Which edge detector is most sensitive to diagonal edges?",
        "options": {
            "A": "Sobel",
            "B": "Kirsch",
            "C": "Prewitt",
            "D": "Roberts"
        },
        "correct": "B"
    },
    {
        "question": "13. Region splitting is based on what type of image partitioning?",
        "options": {
            "A": "Predefined labels",
            "B": "Texture edges",
            "C": "Quadtree decomposition",
            "D": "Morphological erosion"
        },
        "correct": "C"
    },
    {
        "question": "14. Which of the following is a point-based edge feature?",
        "options": {
            "A": "Laplacian",
            "B": "Gaussian",
            "C": "Isolated pixel",
            "D": "Texture gradient"
        },
        "correct": "C"
    },
    {
        "question": "15. What causes over-segmentation in watershed algorithms?",
        "options": {
            "A": "Edge linking",
            "B": "High contrast",
            "C": "Excessive local minima",
            "D": "Large kernels"
        },
        "correct": "C"
    },
    {
        "question": "16. Which filter reduces the number of spurious edges before segmentation?",
        "options": {
            "A": "Laplacian",
            "B": "High-pass filter",
            "C": "Smoothing (low-pass) filter",
            "D": "Gabor filter"
        },
        "correct": "C"
    },
    {
        "question": "17. What does k in k-means clustering signify?",
        "options": {
            "A": "Image width",
            "B": "Kernel size",
            "C": "Number of clusters",
            "D": "Threshold index"
        },
        "correct": "C"
    },
    {
        "question": "18. What is the role of a prototype in k-means clustering?",
        "options": {
            "A": "Controls contrast",
            "B": "Represents the image histogram",
            "C": "Defines cluster mean",
            "D": "Measures texture"
        },
        "correct": "C"
    },
    {
        "question": "19. What type of feature is commonly used for clustering in grayscale images?",
        "options": {
            "A": "RGB values",
            "B": "Intensity",
            "C": "Texture vectors",
            "D": "Frequency domain coefficients"
        },
        "correct": "B"
    },
    {
        "question": "20. What is the purpose of superpixels in segmentation?",
        "options": {
            "A": "Increase detail",
            "B": "Accelerate computation",
            "C": "Blur boundaries",
            "D": "Add contrast"
        },
        "correct": "B"
    },
    {
        "question": "21. What property is often used to grow regions in region growing methods?",
        "options": {
            "A": "Color saturation",
            "B": "Pixel proximity",
            "C": "Intensity similarity",
            "D": "Histogram shape"
        },
        "correct": "C"
    },
    {
        "question": "22. The Sobel operator uses what kind of masks for edge detection?",
        "options": {
            "A": "Gaussian",
            "B": "Laplacian",
            "C": "Gradient-based",
            "D": "Threshold"
        },
        "correct": "C"
    },
    {
        "question": "23. What does a binary segmentation output typically consist of?",
        "options": {
            "A": "RGB values",
            "B": "Probability maps",
            "C": "Intensity histograms",
            "D": "Foreground and background regions"
        },
        "correct": "D"
    },
    {
        "question": "24. What does the term �seed� refer to in region growing?",
        "options": {
            "A": "Local minimum",
            "B": "Threshold value",
            "C": "Initial pixel(s) for growing",
            "D": "Edge magnitude"
        },
        "correct": "C"
    },
    {
        "question": "25. Which is a disadvantage of region-based segmentation?",
        "options": {
            "A": "Low processing speed",
            "B": "Ignores texture",
            "C": "Sensitive to noise",
            "D": "Requires RGB images"
        },
        "correct": "C"
    },
    {
        "question": "26. Which technique involves comparing pixel intensity with neighbors?",
        "options": {
            "A": "Thresholding",
            "B": "Region splitting",
            "C": "Region growing",
            "D": "Watershed"
        },
        "correct": "C"
    },
    {
        "question": "27. The Laplacian operator is most sensitive to what type of edge?",
        "options": {
            "A": "Sloped",
            "B": "Uniform",
            "C": "Sharp and thin",
            "D": "High-frequency textured"
        },
        "correct": "C"
    },
    {
        "question": "28. Which of the following is a drawback of the Laplacian operator?",
        "options": {
            "A": "Requires RGB input",
            "B": "Ignores vertical edges",
            "C": "Sensitive to noise",
            "D": "Blurs the image"
        },
        "correct": "C"
    },
    {
        "question": "29. What is the purpose of applying a Gaussian filter before edge detection?",
        "options": {
            "A": "Sharpen edges",
            "B": "Increase brightness",
            "C": "Reduce noise",
            "D": "Quantize colors"
        },
        "correct": "C"
    },
    {
        "question": "30. What is a common step after initial edge detection?",
        "options": {
            "A": "Color transformation",
            "B": "Edge linking",
            "C": "Histogram equalization",
            "D": "Fourier transform"
        },
        "correct": "B"
    },
    {
        "question": "31. What type of segmentation results from applying a high global threshold?",
        "options": {
            "A": "Background is maximized",
            "B": "Edge detection",
            "C": "Too many small objects",
            "D": "Blurry output"
        },
        "correct": "A"
    },
    {
        "question": "32. What does the Canny edge detector use to reduce spurious edges?",
        "options": {
            "A": "Histogram stretching",
            "B": "Fourier domain filtering",
            "C": "Non-maximum suppression",
            "D": "Thresholding"
        },
        "correct": "C"
    },
    {
        "question": "33. Which statement is true about threshold-based segmentation?",
        "options": {
            "A": "It always uses multiple features",
            "B": "It uses local gradient vectors",
            "C": "It segments based on intensity differences",
            "D": "It works only in the frequency domain"
        },
        "correct": "C"
    },
    {
        "question": "34. What effect does poor contrast have on segmentation?",
        "options": {
            "A": "Enhances threshold selection",
            "B": "Makes edge detection easier",
            "C": "Reduces segmentation accuracy",
            "D": "Improves region labeling"
        },
        "correct": "C"
    },
    {
        "question": "35. The Canny edge detector includes which of the following steps?",
        "options": {
            "A": "Region splitting",
            "B": "Morphological reconstruction",
            "C": "Hysteresis thresholding",
            "D": "Histogram matching"
        },
        "correct": "C"
    },
    {
        "question": "36. Which edge detection method is based on first derivatives?",
        "options": {
            "A": "Laplacian",
            "B": "Canny",
            "C": "Marr-Hildreth",
            "D": "Sobel"
        },
        "correct": "D"
    },
    {
        "question": "37. What is typically true of object boundaries in images?",
        "options": {
            "A": "They are always circular",
            "B": "They correspond to sharp intensity changes",
            "C": "They match noise patterns",
            "D": "They are invariant to all transformations"
        },
        "correct": "B"
    },
    {
        "question": "38. How does adaptive thresholding differ from global thresholding?",
        "options": {
            "A": "It uses RGB components",
            "B": "It selects one threshold per image",
            "C": "It applies a different threshold per region",
            "D": "It requires edge detection"
        },
        "correct": "C"
    },
    {
        "question": "39. Which feature is least used in basic segmentation?",
        "options": {
            "A": "Intensity",
            "B": "Texture",
            "C": "Phase spectrum",
            "D": "Color"
        },
        "correct": "C"
    },
    {
        "question": "40. In image segmentation, connected components are used to:",
        "options": {
            "A": "Apply filters",
            "B": "Count and label regions",
            "C": "Create histograms",
            "D": "Detect motion"
        },
        "correct": "B"
    },
    {
        "question": "41. In segmentation by thresholding, what does bimodal histogram imply?",
        "options": {
            "A": "One object in the image",
            "B": "Noise-dominant image",
            "C": "Two distinct intensity groups",
            "D": "Uniform region intensity"
        },
        "correct": "C"
    },
    {
        "question": "42. The Canny edge detector uses which two main steps for edge detection?",
        "options": {
            "A": "Thresholding and filtering",
            "B": "Laplacian and morphological filtering",
            "C": "Gradient calculation and non-maximum suppression",
            "D": "Watershed and thresholding"
        },
        "correct": "C"
    },
    {
        "question": "43. What role does non-maximum suppression play in edge detection?",
        "options": {
            "A": "Smooths the edges",
            "B": "Detects boundaries",
            "C": "Sharpens edges by thinning",
            "D": "Segments objects"
        },
        "correct": "C"
    },
    {
        "question": "44. What does the gradient magnitude represent in edge detection?",
        "options": {
            "A": "Average intensity",
            "B": "Color intensity",
            "C": "Strength of intensity change",
            "D": "Noise level"
        },
        "correct": "C"
    },
    {
        "question": "45. What is the purpose of a Laplacian operator in edge detection?",
        "options": {
            "A": "Computes average intensity",
            "B": "Measures second-order intensity changes",
            "C": "Smooths the image",
            "D": "Enhances colors"
        },
        "correct": "B"
    },
    {
        "question": "46. What segmentation method grows a region by comparing neighboring pixels?",
        "options": {
            "A": "Thresholding",
            "B": "Region growing",
            "C": "Clustering",
            "D": "Watershed"
        },
        "correct": "B"
    },
    {
        "question": "47. The main condition for adding a pixel in region growing is:",
        "options": {
            "A": "High-frequency response",
            "B": "Color depth",
            "C": "Similarity to seed pixel",
            "D": "Edge sharpness"
        },
        "correct": "C"
    },
    {
        "question": "48. Which method segments the image by merging regions based on similarity?",
        "options": {
            "A": "Region splitting",
            "B": "Canny edge detection",
            "C": "Region merging",
            "D": "Thresholding"
        },
        "correct": "C"
    },
    {
        "question": "49. What segmentation approach is based on spatial and intensity proximity?",
        "options": {
            "A": "Morphological watershed",
            "B": "Clustering",
            "C": "Region growing",
            "D": "Graph cuts"
        },
        "correct": "C"
    },
    {
        "question": "50. Which edge detector is known for simplicity and uses diagonal differences?",
        "options": {
            "A": "Prewitt",
            "B": "Sobel",
            "C": "Roberts",
            "D": "Laplacian"
        },
        "correct": "C"
    },
    {
        "question": "51. What does over-segmentation mean in image segmentation?",
        "options": {
            "A": "Ignoring edges",
            "B": "Missing regions",
            "C": "Producing too many small regions",
            "D": "Detecting only background"
        },
        "correct": "C"
    },
    {
        "question": "52. The primary drawback of using only edge information for segmentation is:",
        "options": {
            "A": "It captures all textures",
            "B": "It merges similar objects",
            "C": "It may result in fragmented boundaries",
            "D": "It enhances brightness"
        },
        "correct": "C"
    },
    {
        "question": "53. What property of an image is most exploited in threshold-based segmentation?",
        "options": {
            "A": "Geometric shape",
            "B": "Texture orientation",
            "C": "Pixel intensity",
            "D": "Frequency domain"
        },
        "correct": "C"
    },
    {
        "question": "54. Which segmentation technique is based on the flooding analogy?",
        "options": {
            "A": "Region growing",
            "B": "Clustering",
            "C": "Watershed",
            "D": "Edge linking"
        },
        "correct": "C"
    },
    {
        "question": "55. What does the term �catchment basin� refer to in watershed segmentation?",
        "options": {
            "A": "A gradient filter",
            "B": "A smoothing kernel",
            "C": "A region growing from a local minimum",
            "D": "A histogram-based cluster"
        },
        "correct": "C"
    },
    {
        "question": "56. Which operation helps suppress minor local minima in watershed?",
        "options": {
            "A": "Gaussian filtering",
            "B": "Histogram equalization",
            "C": "Marker-based segmentation",
            "D": "Thresholding"
        },
        "correct": "C"
    },
    {
        "question": "57. What does SLIC stand for in superpixel generation?",
        "options": {
            "A": "Simple Line Intensity Clustering",
            "B": "Selective Light Intensity Coloring",
            "C": "Simple Linear Iterative Clustering",
            "D": "Soft Linear Image Clustering"
        },
        "correct": "C"
    },
    {
        "question": "58. What is the typical benefit of using superpixels before clustering?",
        "options": {
            "A": "Sharper boundaries",
            "B": "Faster computation and smoother regions",
            "C": "Enhanced noise",
            "D": "Multiscale detail"
        },
        "correct": "B"
    },
    {
        "question": "59. What is the main advantage of graph-based segmentation methods?",
        "options": {
            "A": "Simplified mathematics",
            "B": "Handles only binary images",
            "C": "Captures global image context",
            "D": "Avoids computation entirely"
        },
        "correct": "C"
    },
    {
        "question": "60. In clustering-based segmentation, what does intra-cluster similarity refer to?",
        "options": {
            "A": "Variation between classes",
            "B": "Colorfulness of pixels",
            "C": "Similarity among members of a group",
            "D": "Size of the image"
        },
        "correct": "C"
    },
    {
        "question": "61. What is the main goal of edge linking in edge-based segmentation?",
        "options": {
            "A": "Estimate threshold values",
            "B": "Reconstruct color histograms",
            "C": "Connect fragmented edges into meaningful contours",
            "D": "Create texture descriptors"
        },
        "correct": "C"
    },
    {
        "question": "62. In region splitting and merging, which data structure is typically used?",
        "options": {
            "A": "Decision trees",
            "B": "Quadtree",
            "C": "Stack",
            "D": "Hash map"
        },
        "correct": "B"
    },
    {
        "question": "63. Which method can suffer from �edge fragmentation�?",
        "options": {
            "A": "Thresholding",
            "B": "Region growing",
            "C": "Canny edge detection",
            "D": "Laplacian edge detection"
        },
        "correct": "D"
    },
    {
        "question": "64. How does Canny reduce false edge detection?",
        "options": {
            "A": "Uses morphological reconstruction",
            "B": "Uses double thresholding and edge tracking",
            "C": "Applies region merging",
            "D": "Uses Gabor filtering"
        },
        "correct": "B"
    },
    {
        "question": "65. What is a limitation of global thresholding methods?",
        "options": {
            "A": "Cannot detect textures",
            "B": "Requires large convolution masks",
            "C": "Doesn�t work on grayscale images",
            "D": "Needs user input for clustering"
        },
        "correct": "A"
    },
    {
        "question": "66. What segmentation technique is well-suited to extract regions with uniform texture?",
        "options": {
            "A": "Sobel",
            "B": "Laplacian",
            "C": "Region growing",
            "D": "Watershed"
        },
        "correct": "C"
    },
    {
        "question": "67. What defines the merging condition in region merging?",
        "options": {
            "A": "Proximity of edge pixels",
            "B": "Histogram valleys",
            "C": "Similarity of adjacent regions",
            "D": "Threshold iteration"
        },
        "correct": "C"
    },
    {
        "question": "68. What is an advantage of K-means clustering in image segmentation?",
        "options": {
            "A": "Captures fine edges",
            "B": "Simple and fast for intensity-based grouping",
            "C": "Uses region adjacency graphs",
            "D": "Requires labeled data"
        },
        "correct": "B"
    },
    {
        "question": "69. Which is a drawback of K-means for image segmentation?",
        "options": {
            "A": "Cannot process color images",
            "B": "Requires predefined number of clusters",
            "C": "Needs frequency domain input",
            "D": "Only works with binary images"
        },
        "correct": "B"
    },
    {
        "question": "70. What is a key difference between edge-based and region-based segmentation?",
        "options": {
            "A": "Region-based works in frequency domain",
            "B": "Edge-based ignores local intensity",
            "C": "Region-based uses pixel connectivity",
            "D": "Edge-based uses histogram similarity"
        },
        "correct": "C"
    },
    {
        "question": "71. What is a common post-processing step after applying thresholding?",
        "options": {
            "A": "Histogram equalization",
            "B": "Component labeling",
            "C": "Fourier transform",
            "D": "Logarithmic transform"
        },
        "correct": "B"
    },
    {
        "question": "72. What causes under-segmentation in watershed methods?",
        "options": {
            "A": "Sparse edges",
            "B": "Excessive smoothing",
            "C": "Merged regions due to insufficient minima",
            "D": "Strong Gaussian filtering"
        },
        "correct": "C"
    },
    {
        "question": "73. What does the gradient magnitude image represent in watershed segmentation?",
        "options": {
            "A": "Texture variation",
            "B": "Region intensity",
            "C": "Edge strength",
            "D": "Noise distribution"
        },
        "correct": "C"
    },
    {
        "question": "74. What does the \"catchment basin\" in watershed segmentation represent?",
        "options": {
            "A": "Region of similar histogram",
            "B": "Area around a minimum",
            "C": "Edge linking path",
            "D": "Zone of maximum intensity"
        },
        "correct": "B"
    },
    {
        "question": "75. What preprocessing step reduces over-segmentation in watershed methods?",
        "options": {
            "A": "High-boost filtering",
            "B": "Histogram equalization",
            "C": "Marker-controlled segmentation",
            "D": "Dilation"
        },
        "correct": "C"
    },
    {
        "question": "76. What type of segmentation uses an optimization criterion like minimal cut?",
        "options": {
            "A": "Region growing",
            "B": "Histogram splitting",
            "C": "Graph-based segmentation",
            "D": "Canny edge detection"
        },
        "correct": "C"
    },
    {
        "question": "77. Superpixels help segmentation by:",
        "options": {
            "A": "Increasing noise tolerance",
            "B": "Enhancing texture features",
            "C": "Grouping similar pixels to reduce complexity",
            "D": "Detecting edges automatically"
        },
        "correct": "C"
    },
    {
        "question": "78. Which technique is based on second-order derivatives?",
        "options": {
            "A": "Sobel operator",
            "B": "Canny detector",
            "C": "Laplacian operator",
            "D": "Thresholding"
        },
        "correct": "C"
    },
    {
        "question": "79. In region splitting, when does the subdivision stop?",
        "options": {
            "A": "When the edge map is complete",
            "B": "When region homogeneity criteria are met",
            "C": "After histogram equalization",
            "D": "At maximum frequency"
        },
        "correct": "B"
    },
    {
        "question": "80. What defines the threshold in Otsu's method?",
        "options": {
            "A": "Pixel gradients",
            "B": "Laplacian zero-crossings",
            "C": "Maximal inter-class variance",
            "D": "Seed point values"
        },
        "correct": "C"
    },
    {
        "question": "81. What feature does the Canny edge detector optimize?",
        "options": {
            "A": "Spatial frequency",
            "B": "Edge gradient",
            "C": "Signal-to-noise ratio and localization",
            "D": "Texture directionality"
        },
        "correct": "C"
    },
    {
        "question": "82. What is a key benefit of marker-controlled watershed segmentation?",
        "options": {
            "A": "It enhances Laplacian responses",
            "B": "Reduces over-segmentation",
            "C": "Requires no preprocessing",
            "D": "Avoids region merging"
        },
        "correct": "B"
    },
    {
        "question": "83. In graph-based segmentation, what do the graph nodes typically represent?",
        "options": {
            "A": "Histograms",
            "B": "Intensity ranges",
            "C": "Pixels or superpixels",
            "D": "Threshold intervals"
        },
        "correct": "C"
    },
    {
        "question": "84. What criterion does the normalized cut method optimize in segmentation?",
        "options": {
            "A": "Minimum gradient",
            "B": "High pixel entropy",
            "C": "Balanced partitioning with minimum cut weight",
            "D": "Maximum Laplacian energy"
        },
        "correct": "C"
    },
    {
        "question": "85. What is a disadvantage of using only intensity for segmentation?",
        "options": {
            "A": "Increased computational complexity",
            "B": "Fails in high-contrast images",
            "C": "Ignores spatial context and texture",
            "D": "Overuses region merging"
        },
        "correct": "C"
    },
    {
        "question": "86. Which method benefits most from good initial seed selection?",
        "options": {
            "A": "K-means",
            "B": "Region growing",
            "C": "Graph cut",
            "D": "Thresholding"
        },
        "correct": "B"
    },
    {
        "question": "87. How does superpixel segmentation affect graph-based methods?",
        "options": {
            "A": "Adds pixel noise",
            "B": "Prevents convergence",
            "C": "Reduces the number of nodes",
            "D": "Increases label complexity"
        },
        "correct": "C"
    },
    {
        "question": "88. Which clustering method adapts to complex, non-convex region shapes?",
        "options": {
            "A": "K-means",
            "B": "Fuzzy c-means",
            "C": "DBSCAN",
            "D": "Watershed"
        },
        "correct": "C"
    },
    {
        "question": "89. What is the primary reason K-means may converge to a local minimum?",
        "options": {
            "A": "Random histogram values",
            "B": "Poor marker selection",
            "C": "Random initial cluster centers",
            "D": "Mislabeling connected components"
        },
        "correct": "C"
    },
    {
        "question": "90. Which algorithm assumes clusters are spherical in the feature space?",
        "options": {
            "A": "Region merging",
            "B": "K-means",
            "C": "Watershed",
            "D": "Graph cut"
        },
        "correct": "B"
    },
    {
        "question": "91. What happens during the merging phase of split-and-merge segmentation?",
        "options": {
            "A": "Adjacent regions are combined if similar",
            "B": "Large clusters are divided",
            "C": "Threshold values are computed",
            "D": "Gradient maps are refined"
        },
        "correct": "A"
    },
    {
        "question": "92. Which algorithm evaluates intra- and inter-cluster variance for optimal thresholding?",
        "options": {
            "A": "Canny",
            "B": "K-means",
            "C": "Otsu�s method",
            "D": "Graph cut"
        },
        "correct": "C"
    },
    {
        "question": "93. In marker-based watershed, what are markers typically used for?",
        "options": {
            "A": "Detecting zero-crossings",
            "B": "Seeding regions of interest",
            "C": "Measuring texture",
            "D": "Reducing global threshold"
        },
        "correct": "B"
    },
    {
        "question": "94. What causes noise sensitivity in gradient-based edge detection?",
        "options": {
            "A": "Histogram binning",
            "B": "Convolution smoothing",
            "C": "Derivative amplification",
            "D": "Low-pass filtering"
        },
        "correct": "C"
    },
    {
        "question": "95. Which of the following is true of the Prewitt edge detector?",
        "options": {
            "A": "Uses second-order derivatives",
            "B": "Is directional and uses first-order derivatives",
            "C": "Requires adaptive thresholding",
            "D": "Works only with binary images"
        },
        "correct": "B"
    },
    {
        "question": "96. The term \"oversegmentation\" often applies to which method?",
        "options": {
            "A": "Otsu�s thresholding",
            "B": "Sobel edge detection",
            "C": "Watershed segmentation",
            "D": "Region merging"
        },
        "correct": "C"
    },
    {
        "question": "97. What does �region homogeneity� refer to?",
        "options": {
            "A": "Uniformity in color and shape",
            "B": "High gradient magnitude",
            "C": "Textural variation",
            "D": "Low edge density"
        },
        "correct": "A"
    },
    {
        "question": "98. What defines the termination of a region-growing algorithm?",
        "options": {
            "A": "Number of histogram bins",
            "B": "No more similar neighbors",
            "C": "Threshold value exceeded",
            "D": "Number of connected components"
        },
        "correct": "B"
    },
    {
        "question": "99. What is the most typical cause of �false edges� in edge detection?",
        "options": {
            "A": "Region-based merging",
            "B": "Noise and texture variations",
            "C": "Histogram smoothing",
            "D": "Low-frequency background"
        },
        "correct": "B"
    },
    {
        "question": "100. What is a limitation of fuzzy c-means clustering for segmentation?",
        "options": {
            "A": "Does not support color input",
            "B": "Requires binary images",
            "C": "Sensitive to noise and initial conditions",
            "D": "Only works in frequency domain"
        },
        "correct": "C"
    },
    {
        "question": "101. What distinguishes deep learning-based segmentation from traditional methods?",
        "options": {
            "A": "It requires Fourier transforms",
            "B": "It ignores local features",
            "C": "It learns hierarchical features from data",
            "D": "It works only on grayscale images"
        },
        "correct": "C"
    },
    {
        "question": "102. What is a key component of U-Net architecture for biomedical segmentation?",
        "options": {
            "A": "High-pass filtering",
            "B": "Multi-resolution quadtree",
            "C": "Encoder-decoder structure with skip connections",
            "D": "Laplacian pyramid"
        },
        "correct": "C"
    },
    {
        "question": "103. Which loss function is especially useful in deep segmentation for unbalanced classes?",
        "options": {
            "A": "Cross-entropy",
            "B": "L2 loss",
            "C": "Dice coefficient loss",
            "D": "Gradient magnitude loss"
        },
        "correct": "C"
    },
    {
        "question": "104. What is the main role of skip connections in CNN-based segmentation?",
        "options": {
            "A": "Speed up training",
            "B": "Increase batch size",
            "C": "Fuse low-level spatial and high-level semantic features",
            "D": "Avoid histogram equalization"
        },
        "correct": "C"
    },
    {
        "question": "105. Which model type is most commonly used for pixel-level segmentation tasks?",
        "options": {
            "A": "Fully connected networks (FCNs)",
            "B": "Support vector machines",
            "C": "Bayesian classifiers",
            "D": "PCA models"
        },
        "correct": "A"
    },
    {
        "question": "106. Why is semantic segmentation considered harder than classification?",
        "options": {
            "A": "Requires grayscale input",
            "B": "Involves temporal data",
            "C": "Predicts one label per pixel rather than one per image",
            "D": "Only works on binary images"
        },
        "correct": "C"
    },
    {
        "question": "107. What preprocessing step improves learning in deep segmentation models?",
        "options": {
            "A": "Fourier transform",
            "B": "Intensity inversion",
            "C": "Data normalization and augmentation",
            "D": "Threshold sharpening"
        },
        "correct": "C"
    },
    {
        "question": "108. What type of segmentation does Mask R-CNN perform?",
        "options": {
            "A": "Binary thresholding",
            "B": "Region merging",
            "C": "Instance segmentation",
            "D": "Texture-based segmentation"
        },
        "correct": "C"
    },
    {
        "question": "109. What challenge does class imbalance present in segmentation tasks?",
        "options": {
            "A": "Prevents threshold calculation",
            "B": "Causes boundary over-smoothing",
            "C": "Makes model biased toward dominant classes",
            "D": "Requires inverse Fourier analysis"
        },
        "correct": "C"
    },
    {
        "question": "110. How do Conditional Random Fields (CRFs) enhance CNN-based segmentation?",
        "options": {
            "A": "Replace convolution layers",
            "B": "Predict object centroids",
            "C": "Refine pixel labeling with context-based smoothing",
            "D": "Perform dimensionality reduction"
        },
        "correct": "C"
    },
    {
        "question": "111. Which feature of superpixels improves deep model efficiency?",
        "options": {
            "A": "Randomization",
            "B": "Large convolution kernels",
            "C": "Reduced number of elements for processing",
            "D": "Spatial derivatives"
        },
        "correct": "C"
    },
    {
        "question": "112. What advantage do dilated convolutions offer in segmentation models?",
        "options": {
            "A": "Reduces image resolution",
            "B": "Allows larger receptive field without increasing parameters",
            "C": "Applies histogram-based thresholding",
            "D": "Sharpens image boundaries"
        },
        "correct": "B"
    },
    {
        "question": "113. What is the main difference between semantic and instance segmentation?",
        "options": {
            "A": "Semantic uses texture; instance uses color",
            "B": "Instance labels each object separately; semantic labels object class only",
            "C": "Semantic works on binary images",
            "D": "Instance uses Laplacian operators"
        },
        "correct": "B"
    },
    {
        "question": "114. What is a key advantage of using ensemble models in deep segmentation?",
        "options": {
            "A": "Faster convergence",
            "B": "Lower GPU usage",
            "C": "Improved robustness and accuracy",
            "D": "Fewer annotations needed"
        },
        "correct": "C"
    },
    {
        "question": "115. What does the Intersection over Union (IoU) metric measure in segmentation?",
        "options": {
            "A": "Gradient intensity",
            "B": "Similarity between prediction and ground truth regions",
            "C": "Histogram separation",
            "D": "Texture strength"
        },
        "correct": "B"
    },
    {
        "question": "116. Which segmentation method benefits most from transfer learning?",
        "options": {
            "A": "Thresholding",
            "B": "K-means",
            "C": "CNN-based semantic segmentation",
            "D": "Watershed"
        },
        "correct": "C"
    },
    {
        "question": "117. Which is a downside of training segmentation models from scratch?",
        "options": {
            "A": "Requires histogram equalization",
            "B": "Over-segmentation",
            "C": "Needs large annotated datasets",
            "D": "Doesn�t support binary masks"
        },
        "correct": "C"
    },
    {
        "question": "118. How does attention mechanism improve segmentation models?",
        "options": {
            "A": "Applies Otsu�s method",
            "B": "Selects pixels with high color variance",
            "C": "Focuses computation on relevant features or spatial areas",
            "D": "Avoids convolution operations"
        },
        "correct": "C"
    },
    {
        "question": "119. What technique is used to convert fully connected layers to convolutional ones in",
        "options": {
            "A": "Fourier transformation",
            "B": "Weight sharing",
            "C": "Reshaping and sliding window application",
            "D": "Spectral clustering"
        },
        "correct": "C"
    },
    {
        "question": "120. In segmentation, the term �boundary recall� refers to:",
        "options": {
            "A": "Number of edges in Fourier space",
            "B": "Fraction of true object boundaries correctly predicted",
            "C": "Histogram peak accuracy",
            "D": "Distance between region centroids"
        },
        "correct": "B"
    }
]

# ترتيب الأسئلة عشوائي
if "shuffled_questions" not in st.session_state:
    st.session_state.shuffled_questions = random.sample(questions, len(questions))
    st.session_state.current_q = 0
    st.session_state.correct_count = 0
    st.session_state.user_answers = {}
    st.session_state.submitted = False

q_index = st.session_state.current_q
q = st.session_state.shuffled_questions[q_index]

# إعداد واجهة Streamlit
st.set_page_config(page_title="Chapter 10 Quiz", layout="centered")
st.title("🧠 Chapter 10 Interactive Quiz")

# عرض الحالة في الأعلى
st.info(f"Question {q_index + 1} of {len(st.session_state.shuffled_questions)}")
st.success(f"Correct Answers: {st.session_state.correct_count}")

# عرض السؤال الحالي
st.markdown(f"**{q_index + 1}. {q['question']}**")

# عرض الاختيارات
selected_letter = st.radio("Select your answer:", list(q['options'].keys()), format_func=lambda x: f"{x}) {q['options'][x]}", key=f"choice_{q_index}")

# زرار السبمت
if st.button("Submit Answer") and not st.session_state.submitted:
    st.session_state.user_answers[q_index] = selected_letter
    if selected_letter == q['correct']:
        st.success("✅ Correct!")
        st.session_state.correct_count += 1
    else:
        st.error("❌ Incorrect.")
        st.info(f"Correct answer: {q['correct']}) {q['options'][q['correct']]}")
    st.session_state.submitted = True

# زر التالي بعد السبمت فقط
if st.session_state.submitted:
    if st.button("Next Question"):
        st.session_state.current_q += 1
        st.session_state.submitted = False
        if st.session_state.current_q >= len(st.session_state.shuffled_questions):
            st.success("🎉 You've completed all questions! Restarting from beginning.")
            st.session_state.shuffled_questions = random.sample(questions, len(questions))
            st.session_state.current_q = 0
            st.session_state.correct_count = 0
            st.session_state.user_answers = {}