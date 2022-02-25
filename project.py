#/bin/python3
#
#  project.py
#
#  Copyright 2022 Oğuz Toraman <oguz.toraman@protonmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.
#

import cv2
import numpy as np
import time as t
from scipy import ndimage

class leaf_segmentation:
    filter_size = (11, 11)
    filter_sigma = 5

    otsu_threshold_min = 0
    otsu_threshold_max = 255
    
    structuring_element = cv2.MORPH_RECT
    structuring_element_size = (15, 15)
    
    def __init__(self, rgb_folder, segmented_folder, image_count):
        self.m_rgb_folder = str(rgb_folder)
        self.m_segmented_folder = str(segmented_folder)
        if image_count < 1:
            image_count = 1
        elif image_count > 20:
            image_count = 20
        self.m_image_count = image_count

    def segment(self):
        self.average_succes_rate = 0
        self.average_elapsed_time = 0
        for i in range(1, self.m_image_count + 1, 1):
            rgb = self.m_rgb_folder + '/' + str(i) + '.jpg'
            rgb_img = cv2.imread(rgb)
            segmented = self.m_segmented_folder + '/' + str(i) + '.jpg'
            segmented_img = cv2.imread(segmented)
            start_time = t.time()
            resulted_img = self.perform_segmentation(rgb_img)
            end_time = t.time()
            self.print_line()
            cv2.imshow('RGB image ' + str(i), rgb_img)
            cv2.imshow( 'Resulted image ' + str(i), resulted_img)
            cv2.imshow( 'Segmented image ' + str(i), segmented_img)
            succes_rate = self.success_rate(resulted_img, segmented_img)
            elapsed_time = end_time - start_time
            print('Success rate of image ', i, ': %', self.success_rate(resulted_img, segmented_img))
            print('Elapsed time for image ', i, ': ', elapsed_time, 's')
            self.average_succes_rate = self.average_succes_rate + succes_rate
            self.average_elapsed_time = self.average_elapsed_time + elapsed_time
            cv2.waitKey(10000)
            cv2.destroyAllWindows()
        self.average_succes_rate = self.average_succes_rate/self.m_image_count
        self.average_elapsed_time = self.average_elapsed_time/self.m_image_count
        self.print_line()
        print('Average success rate: %', self.average_succes_rate)
        print('Average elapsed time:', self.average_elapsed_time, 's')

    def histogram_equalization(self, img):
        return cv2.equalizeHist(img)

    def gaussian_filter(self, img):
        filtered = np.copy(img)
        filtered = cv2.GaussianBlur(img, self.filter_size, self.filter_sigma)
        return filtered

    def create_mask_using_otsu(self, img):
        threshold, mask = cv2.threshold(img, 
                                        self.otsu_threshold_min, 
                                        self.otsu_threshold_max,
                                        cv2.THRESH_OTSU)
        x, y = mask.shape
        for i in range(0, x, 1):
            for j in range(0, y, 1):
                if mask[i, j] == self.otsu_threshold_max:
                    mask[i, j] = self.otsu_threshold_min
                else:
                    mask[i, j] = self.otsu_threshold_max 
        return mask
        
    def improve_mask(self, mask):
        SE = cv2.getStructuringElement(self.structuring_element,
                                       self.structuring_element_size)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, SE)
        return ndimage.binary_fill_holes(mask) 
    
    def perform_segmentation(self, img):
        img_copy = np.copy(img)
        blue, green, red = cv2.split(img)
        img_blue = self.histogram_equalization(blue)
        img_blue = self.gaussian_filter(img_blue)
        mask_blue = self.create_mask_using_otsu(img_blue)
        mask_blue = self.improve_mask(mask_blue)
        x, y = mask_blue.shape
        for i in range(0, x, 1):
            for j in range(0, y, 1):
                if mask_blue[i, j] == 0:
                    img_copy[i, j, :] = 0
        return img_copy     
        
    def success_rate(self, resulted, segmented):
        success = 0
        resulted_gray = cv2.cvtColor(resulted, cv2.COLOR_BGR2GRAY)
        segmented_gray = cv2.cvtColor(segmented, cv2.COLOR_BGR2GRAY)
        x, y = segmented_gray.shape
        pixel_count = x*y
        for i in range(0, x, 1):
            for j in range(0, y, 1):
                if (segmented_gray[i, j] != 0 and resulted_gray[i, j] != 0) or \
                (segmented_gray[i, j] == 0 and resulted_gray[i, j] == 0):
                    success = success + 1                    
        success = (success/pixel_count)*100
        return success
    
    def print_line(self):
        print('===================================')
