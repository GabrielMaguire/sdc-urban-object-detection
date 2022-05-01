# Object Detection in an Urban Environment

Gabriel Maguire
Date: 5/1/2022

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

I performed 7 experiments in total. Each experiment completed ~2000-2600 training steps and varied different parameters such as the learning rate and data augmentations. In this section I will cover the top 3 most insightful experiments in detail.

#### Training Versus Validation Loss

The validation loss point displayed in each tensorboard output graph was consistently ~0.5 loss points above the training loss point when compared at the same time step. On average across all experiments, this is expected due to overfitting of the model to the training data. Overfitting is a result of a model with a large number of parameters learning over specific details of the training data. When this happens the model loses its ability to generalize to new data, such as the validation or test data, and perform well. With a limited number of samples, and initially assuming limited data augmentations, overfitting is expected.

#### Virtual Workspace Memory Limitations

Due to memory limitations in Udacity's virtual workspace environment I was unable to run both the training and validation simultaneously without crashing. This meant that the validation process was executed at the conclusion of the training and only produced a single data point in the tensorboard output graphs. Unfortunately, when downloading the .svg images from the tensorboard output the single validation point is not visible. However, I will comment on the training versus validation loss here without this data shown.

#### Virtual Workspace Explore Augmentations Issue

Due to a currently unknown issue with the Udacity virtual workspace I was unable to run the augmentation visualizations using the "Explore augmentations" notebook. My personal attempts to resolve the issue are detailed in the following knowledge article ([Knowledge article: Explore augmentations code not working](https://knowledge.udacity.com/questions/838269)), and I have reached out to Udacity support to further address the issue. I will update this writeup to include the augmentation visualizations if/when the issue is resolved.

### Experiment 0 Results

Pipeline.config: `pipeline_00.config`

The first experiment I ran using the default pipeline.config (renamed to `pipeline_00.config`) file provided for the object detection model. This experiment was unexpectedly successful given that the default learning rate was not changed and few augmentations were performed on the input dataset.

The default augmentations used in this experiment were `random_horizontal_flip` and `random_crop_image`.

The default learning rate parameters in this experiment were:
`learning_rate_base`: 0.04
`total_steps`: 25000
`warmup_learning_rate`: 0.013333
`warmup_steps`: 2000

After ~2600 training steps the total training loss was ~1.0 while the training classification loss was ~0.3 and the training localization loss was ~0.4. Seeing as a total loss metric between 1 and 2 is indicative of a high quality object detection model, this experiment set a high standard for the following experiments. The time series output of these results can be seen in the images below.

*Experiment 0 Total Loss*
![Alt test](https://github.com/GabrielMaguire/sdc-urban-object-detection/blob/main/tensorboard_train_val_images/ref_00/Loss_total_loss.svg "Experiment 0 Total Loss")

*Experiment 0 Classification Loss*
![Alt test](https://github.com/GabrielMaguire/sdc-urban-object-detection/blob/main/tensorboard_train_val_images/ref_00/Loss_classification_loss.svg "Experiment 0 Classification Loss")

*Experiment 0 Localization Loss*
![Alt test](https://github.com/GabrielMaguire/sdc-urban-object-detection/blob/main/tensorboard_train_val_images/ref_00/Loss_localization_loss.svg "Experiment 0 Localization Loss")

*Experiment 0 Learning Rate*
![Alt test](https://github.com/GabrielMaguire/sdc-urban-object-detection/blob/main/tensorboard_train_val_images/ref_00/learning_rate.svg "Experiment 0 Learning Rate")

### Experiment 2 Results

Pipeline.config: `pipeline_02.config`

For experiment 2 I decided to implement 5 data augmentations options (4 additional augmentations compared to experiment 0) and adjust the learning rate parameters.

I kept the `random_crop_image` augmentation used in experiment 0 and added `random_adjust_brightness`, `random_adjust_saturation`, `random_jitter_boxes`, and `random_black_patches`. These augmentations were chosen to simulate the variation seen in the training data. `random_adjust_brightness` and `random_adjust_saturation` are meant to simulate the changes in daylight, while `random_black_patches` is meant to simulate object occlusion. I felt that `random_jitter_boxes` was a worthwhile augmentation to mimic the small variation in the labeling of the bounding boxes.

I also changed the learning rate parameters as follows...
`learning_rate_base`: 0.04 -> 0.1
`warmup_learning_rate`: 0.0133 -> 0.04
`warmup_steps`: 2000 -> 1000
...in an attempt to expedite the convergence process

Unfortunately, the additional augmentations and adaptations to the learning rate backfired and greatly increased the loss metrics as shown below.

Addressing the impact of the additional augmentations first, I believe there are two potential causes for the increased loss metric. First, augmentations options such as the probability of `random_black_patches` (simulating occlusions) being applied to an image being set at 5% may have been too aggressive and not representative of the underlying dataset. Second, there may not have been enough training steps to fully realize the potential of the augmentations. There is a set probability that each image undergoes a certain augmentation. For example, if the probability of an augmentation is set to 50%, every other image will have this augmentation applied and it will practically double the size of the training dataset. Therefore, it would be optimal to run a number of training steps that would take full advantage of the augmented dataset, however, due to space restrictions in the workspace this was not possible.

After ~2500 training steps, the total training loss metric was ~3. A significant increase over the baseline experiment 0.

*Experiment 0 Total Loss*
![Alt test](https://github.com/GabrielMaguire/sdc-urban-object-detection/blob/main/tensorboard_train_val_images/ref_02/Loss_total_loss.svg "Experiment 0 Total Loss")

*Experiment 0 Classification Loss*
![Alt test](https://github.com/GabrielMaguire/sdc-urban-object-detection/blob/main/tensorboard_train_val_images/ref_02/Loss_classification_loss.svg "Experiment 0 Classification Loss")

*Experiment 0 Localization Loss*
![Alt test](https://github.com/GabrielMaguire/sdc-urban-object-detection/blob/main/tensorboard_train_val_images/ref_02/Loss_localization_loss.svg "Experiment 0 Localization Loss")

*Experiment 0 Learning Rate*
![Alt test](https://github.com/GabrielMaguire/sdc-urban-object-detection/blob/main/tensorboard_train_val_images/ref_02/learning_rate.svg "Experiment 0 Learning Rate")


### Experiment 4 Results

Pipeline.config: `pipeline_04.config`

Seeing as experiment 2 produced far worse results than the baseline experiment 0 when increasing the learning rate parameters and adding data augmentations, for experiment 4 I decided to return to the default learning rate parameters and be more selective about the augmentations I implemented.

I chose to keep only the `random_adjust_brightness`, `random_jitter_boxes`, and `random_black_patches` augmentations, removing the `random_crop_image` and `random_adjust_saturation` which I felt did not reflective the natural variation in the dataset.

After ~2500 training steps, the total training loss was ~1.8. This metric shows improvement upon the results of experiment 2, but is still a worse performance than that of the baseline experiment 0.

*Experiment 0 Total Loss*
![Alt test](https://github.com/GabrielMaguire/sdc-urban-object-detection/blob/main/tensorboard_train_val_images/ref_04/Loss_total_loss.svg "Experiment 0 Total Loss")

*Experiment 0 Classification Loss*
![Alt test](https://github.com/GabrielMaguire/sdc-urban-object-detection/blob/main/tensorboard_train_val_images/ref_04/Loss_classification_loss.svg "Experiment 0 Classification Loss")

*Experiment 0 Localization Loss*
![Alt test](https://github.com/GabrielMaguire/sdc-urban-object-detection/blob/main/tensorboard_train_val_images/ref_04/Loss_localization_loss.svg "Experiment 0 Localization Loss")

*Experiment 0 Learning Rate*
![Alt test](https://github.com/GabrielMaguire/sdc-urban-object-detection/blob/main/tensorboard_train_val_images/ref_04/learning_rate.svg "Experiment 0 Learning Rate")


### Experiment 6 Results

Pipeline.config: `pipeline_06.config`

So far, additional augmentations over the baseline configuration seem to increase the loss metrics. Therefore, for the final experiment I chose to remove all data augmentations and keep the default learning rate.

This proved to be the most successful experiment so far with a total training loss metric of ~0.7 after ~2500 training steps. This is an improvement of ~0.3 upon the baseline total training loss metric.

As discussed earlier in experiment 2, one potential reason for data augmentations having a negative impact on the results of the model could be that there is no need to data augmentations since the model is not training for enough steps to exhaust the initial dataset and the augmentations are simply providing a less realistic version of the original dataset.

*Experiment 0 Total Loss*
![Alt test](https://github.com/GabrielMaguire/sdc-urban-object-detection/blob/main/tensorboard_train_val_images/ref_06/Loss_total_loss.svg "Experiment 0 Total Loss")

*Experiment 0 Classification Loss*
![Alt test](https://github.com/GabrielMaguire/sdc-urban-object-detection/blob/main/tensorboard_train_val_images/ref_06/Loss_classification_loss.svg "Experiment 0 Classification Loss")

*Experiment 0 Localization Loss*
![Alt test](https://github.com/GabrielMaguire/sdc-urban-object-detection/blob/main/tensorboard_train_val_images/ref_06/Loss_localization_loss.svg "Experiment 0 Localization Loss")

*Experiment 0 Learning Rate*
![Alt test](https://github.com/GabrielMaguire/sdc-urban-object-detection/blob/main/tensorboard_train_val_images/ref_06/learning_rate.svg "Experiment 0 Learning Rate")
