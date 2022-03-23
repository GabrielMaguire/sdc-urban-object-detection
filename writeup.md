# Object Detection in an Urban Environment

Gabriel Maguire
Date: 3/15/2022

This project...

## Exploratory Data Analysis

When familiarizing myself with the dataset, there were a couple of aspects that stood out to me.

First, I noticed the overwhelming quantity of cars in the dataset. To help understand the distribution of the car object class versus the bicycle and pedestrian object classes I took a sample of 1000 images from the dataset and tallied up the quantity of each specific class. I then scaled the quantity by dividing by the number of sampled images. The resulting chart is titled "Distribution of Object Classes". This chart clearly illustrates the bias in the dataset towards the car object class, with an average of ~19 cars per image.

Second, I noticed there are many bounding boxes containing only part of a classified object due to occlusion or framing issues. The distribution of partial objects in an image is a more difficult metric to obtain because this information is not directly labeled. One possible solution to find this metric would be to calculate an average ratio of the bounding box width:height along with the standard distribution for each object class over a large batch of images. You could then determine a variation threshold (say 2 standard deviation) for which the bounding box width:height ratio strays too far from the average and we can determine this to be caused by occlusion of framing issues.

Lastly, to estimate the day/night distribution of images in the dataset, I calculated the distribution of average light intensity for each image in the dataset. This histrogram plot is titled "Distribution of Image Light Intensity". From the histrogram plot we can see that the majority of the images fall roughly within the middle range of 80-120 out of 255 average lightness. Images in this range are standard daytime images. A small minority of the images were taken at night and are represented as the datapoints in the 10-20 out of 255 average lightness.