HOUGH TRANSFORM TO DETECT CIRCLES
=================================

INTRODUCTION
------------
This Project detects the boundary points of the object in a given image. By appliying Hough Transform techniques on an image, here we find the coordinates of location of the center and radius of the circular coins (objects) in the given image by finding the local maxima from an accumulator which helps in storing the values of the radii and coordinates of the coin circles. We have used techniques like threshold so as to obstruct the unwanted intensity values in the image like noise, convolution, Sobel edge detecting the edges of the coins and further using the gradient obtained to obtain smoother edges and morphological operations of opening and closing for removal of spurious edges. We have mainly used the algorithm given in textbook as a guideline, a few reference papers and other informative pages over the net for detecting the coins in the image. The algorithm was used along with the material provided by the TAs.

![alt tag](https://raw.githubusercontent.com/manasiye/Coin-Collection/master/HoughCircles.jpg)

APPROACH
--------
Our approach was basically following the simple guidelines given and try to find the best fitting technique to implement the same. Initially we tried a few different ways to perform a particular task and figure out which gave the best result.
The technique we used is a cumulative of the one outlined in the book and a few papers available online. This is very much aligned with the flowchart below.

» Preprocessing
» Blurring
» Morphological Closing
» Sobel Convolution
» Thinning Edges
» Detecting Circles
» Display Detected Circles
» Thresholding

We have used Canopy editor by Enthought for programming in python language. Other methodologies include the techniques we implemented for detection of the circles over the coins like blurring using Gaussian filter, convolution, morphological operation called opening, Sobel edge detection, applying Hough transform and finally performing radii range fixing done by edge thinning and angle calculations plus the usage of an accumulator for the same.

OUTCOME AND DEVIATION
---------------------
✑ Blurring: It removes small background noise by averaging with neighboring pixels.
✑ Morphological Closing: noise inside the coin circles were removed by performing closing operation. In which sequentially dilation was applied 5 times followed by erosion for 5 times to reverse the dilation effect. It gave near to complete noise removal of spurious edges inside the object boundary.
✑ Convolution: Absolute of the horizontal and vertical edge detected output of the image boundary.
✑ Thresholding and Thinning: It further smoothens the object boundary by thinning and filling the gaps between the edges.
✑ Detection of circles: Circles around the coin boundary in the original image. Little deviation of circles formed around circle boundary for some of the coins. This occurred due to approximation between 3 radii taken together to contribute for center of the circle detection while the circle boundary was little deformed causing deviation of found radii from the original radii.
✑ Lessons Learnt: To get a deep understanding of all the basic steps required for the project development and think about as much small boundary cases as possible before the starting writing software. This may cause less invest for less debugging time after completion of the project.

EXPLANATION OF SOFTWARE AND PROGRAM DEVELOPMENT
-----------------------------------------------
We have used the Enthought Canopy software programming in python for this project. It has a very simple and user friendly editor and built in package manager that allows you to download any additional library that may be required. We are also using openCV as an additional feature that allows us to work on the images easily. The following are the steps followed in order to obtain the detection of circles locating the coins in the image-

✑ Preprocessing: The first step we performed was to take the coin image as the input using Opencv2 library which will be used for the further processing. We get the image height and width using the numpy library function shape. As a part of preprocessing, we have created horizontal and vertical Sobel kernels with values as follows which will be used to perform edge detection on the image by convolution.

-1 -2 -1

 0  0  0

 1  2  1

Vertical Kernel(Dx) Horizontal Kernel (Dy)
------------------------------------------

✑ Blurring and Gaussian Filter Application: In this step we perform the opening operations on the image for five times to remove of noise like small objects and spurious edges. For blurring we have used the Gaussian Filter which again helps in reducing the noise from the image.

✑ Morphological Closing: Dilation is performed 5 times to fill the holes, smoothing the object outline and filling the narrow gulfs between the near the object edge boundaries. Dilation is followed by erosion to retain the original size of the object. Erosion also helps remove small object edges which contribute to noise and are smaller than the structure size of the erosion.

✑ Sobel Convolution: Then we applied the Sobel kernels on the image and obtained the following image giving us the edges of the coin. This was performed by applying convolution of the individual kernels and then finding the gradient magnitude. The edges were detected as follows-

✑ Thinning Edges: Here using the gradient Dx and Dy obtained from the previous step we find the angles between the horizontal and vertical edges detected using the arctan function from SciPy library. This function gives the tangent value of the angle formed in radians. Angles near the error range of 22.5 degrees at 0, 45, 90 degrees is approximated to these angles in the first, second, third and fourth quadrant. This in turn is used in thinning of the object boundary. The intensities are checked of every neighboring pixels of the edge detected and the stronger ones are retained to obtain a better thin version of edges of the circle.

✑ Thresholding: In this step we applied a threshold value on the image obtained from the gradient of the Sobel convolution for removal of unwanted edges with the intensity values that were not strong enough. Post thresholding, we removed the horizontal edges existing in the vertical edges detected.

-1 0 1

-2 0 2

-1 0 1

![alt tag](https://raw.githubusercontent.com/manasiye/Coin-Collection/master/convolutionDetectedCirclesGradHori.jpg)

 Then we filled recursively the edges in the horizontal edge detected image that were having pixel values present in the vertical image at neighboring locations.
Image after Application of convolution, thinning, thresholding on the image

✑ Detection of Circle: This step is performed to figure out the radius values for the Hough circles to be generated. After hit and trial we found the radii with minimum and maximum value required which successfully captures coins of minimum and maximum size. We then captured circles with 3 pixel radii approximation. By seeking for circles made in the approximation range of 3 and thereby storing the centers in the new array, taken as “cntrPts”. We then iteratively check for the circles with next 3 radii pixel approximations and store them in the “cntrPts” array. The center points of the circle are found by making the circle of the 3 radii values at each edge pixel storing them in the array named “countIntrsct”. “countIntrsct” array stores the frequency of intersection of these circles. The “countIntrsct” array is searched for the local maxima with the adaptive frequency threshold starting at 46 and incremented at each iteration to find a bigger circle. The accumulator is used to store the radii values along with the centers of the detected circles. The accumulator is also referred while searching for a circle with larger radii

✑ if there is already a smaller circle found in the range of 20 pixels, then the circle finding step is avoided to location. The “storeCenter” function adds the local maxima values which contributes to the center of the circle to the “cntrPts” based thresholding and iterations of the circle formations.

✑ Result: Display the circle on intensity 255 a little outside the edges of the coins so as to include the entire coin inside the circle generated. The final image generated is as below.
![alt tag](https://raw.githubusercontent.com/manasiye/Coin-Collection/master/DetectCirclesHoughTransform.jpg)
