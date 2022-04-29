# Object Detection in an Urban Environment

Gabriel Maguire
Date: 3/15/2022

This project...

## Exploratory Data Analysis

When familiarizing myself with the dataset, there were a couple of aspects that stood out to me.

First, I noticed the overwhelming quantity of cars in the dataset. To help understand the distribution of the car object class versus the bicycle and pedestrian object classes I took a sample of 1000 images from the dataset and tallied up the quantity of each specific class. I then scaled the quantity by dividing by the number of sampled images. The resulting chart is titled "Distribution of Object Classes". This chart clearly illustrates the bias in the dataset towards the car object class, with an average of ~19 cars per image.

Second, I noticed there are many bounding boxes containing only part of a classified object due to occlusion or framing issues. The distribution of partial objects in an image is a more difficult metric to obtain because this information is not directly labeled. One possible solution to find this metric would be to calculate an average ratio of the bounding box width:height along with the standard distribution for each object class over a large batch of images. You could then determine a variation threshold (say 2 standard deviation) for which the bounding box width:height ratio strays too far from the average and we can determine this to be caused by occlusion of framing issues.

Third, to estimate the day/night distribution of images in the dataset, I calculated the distribution of average light intensity for each image in the dataset. This histrogram plot is titled "Distribution of Image Light Intensity". From the histrogram plot we can see that the majority of the images fall roughly within the middle range of 80-120 out of 255 average lightness. Images in this range are standard daytime images. A small minority of the images were taken at night and are represented as the datapoints in the 10-20 out of 255 average lightness.

Lastly, when viewing images the from .tfrecord files in the "training_and_validation" directory I made a note of each file containing either blurry (rain or fog) or dark (nightime) images. These notes will prove helpful when splitting the dataset to ensure that I have each type of image quality in both the training and validation splits.

## Create Splits

Now that I have spent some time understanding the dataset, I need to create my training, validation, and testing splits. The testing split appears to be created already in "/home/workspace/data/waymo/test" so it is left to me to split the data in the "/home/workspace/data/waymo/training_and_validation" directory into separate training and validation folders using the insight gained from my exploratory data analysis.

I started by creating an 80-20 split for training and validation of the .tfrecord files. I then referenced by notes taken in the exploratory data analysis section of the blurry and dark .tfrecords and checked by hand to make sure that both my training and validation split contained at least one blurry and dark .tfrecord.

## Training and Validation

![Alt test](https://github.com/GabrielMaguire/sdc-urban-object-detection/blob/main/tensorboard_train_val_images/ref_00/Loss_total_loss.svg "Pipeline 0 Total Loss")