import argparse
import glob
import os
import shutil
import random

import numpy as np

from utils import get_module_logger

SPLIT_PARAM = 0.8       # Percentage split of dataset between training and validation
TRAINING_PATH = '/home/workspace/data/training'
VALIDATION_PATH = '/home/workspace/data/validation'

def split(data_dir):
    """
    Create three splits from the processed records. The files should be moved to new folders in the same directory. This folder should be named train, val and test.

    args:
        - data_dir [str]: data directory, /home/workspace/data/waymo
    """
    
    records = glob.glob(data_dir + '/*.tfrecord')
    random.shuffle(records)
    training = records[:int(len(records) * SPLIT_PARAM)]
    validation = records[int(len(records) * SPLIT_PARAM):]

    os.mkdir(TRAINING_PATH)
    for record in training:
        shutil.move(record, os.path.join(TRAINING_PATH, record.split('/')[-1]))

    os.mkdir(VALIDATION_PATH)
    for record in validation:
        shutil.move(record, os.path.join(VALIDATION_PATH, record.split('/')[-1]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split data into training / validation / testing')
    parser.add_argument('--data_dir', required=True, help='data directory')
    args = parser.parse_args()

    logger = get_module_logger(__name__)
    logger.info('Creating splits...')
    split(args.data_dir)