#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from PIL import Image
from collections import Counter
from sklearn.cluster import KMeans

WIDTH = 500
HEIGHT = 500

class CPG(object):
    def __init__(self, image=None, cluster=6):
        self.image = image
        self.cluster = cluster
        try:
            self.width = self.image.size[0]
            self.height = self.image.size[1]
            self.format = self.image.format
            self.mode = self.image.mode
        except FileNotFoundError:
            print('No such file or directory exists: {}'.format(path))
    
    def get_data(self):
        print("Width - {}".format(self.width))
        print("Height - {}".format(self.height))
        print("Format - {}".format(self.format))
        print("Mode - {}".format(self.mode))
        
    def show(self):
        plt.figure(figsize=(8, 8))
        plt.imshow(self.image)
        plt.axis('off')
        
    def calculate_new_size(self):
        if self.width >= self.height:
            wpercent = (WIDTH / float(self.width))
            hsize = int((float(self.height) * float(wpercent)))
            new_width, new_height = WIDTH, hsize
        else:
            hpercent = (HEIGHT / float(self.height))
            wsize = int((float(self.width) * float(hpercent)))
            new_width, new_height = wsize, HEIGHT
        return new_width, new_height
    
    def resize(self):
        if self.width > WIDTH or self.height > HEIGHT:
            new_width, new_height = self.calculate_new_size()
            new_image = self.image.resize((new_width, new_height), Image.ANTIALIAS)
            return new_image
        else:
            return self.image
        
    def rgb2hex(self,rgb):
        hex = "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
        return hex
    
    def has_transparency(self):
        img = self.image
        if img.mode == "P":
            transparent = img.info.get("transparency", -1)
            for _, index in img.getcolors():
                if index == transparent:
                    return True
        elif img.mode == "RGBA":
            extrema = img.getextrema()
            if extrema[3][0] < 255:
                return True

        return False
    
    def remove_transparency(self, img):
        img_array = np.array(img)
        img_vector = img_array.reshape((img_array.shape[0] * img_array.shape[1], 4))
        new_img_vector = [i[:3] for i in img_vector if i[3] == 255]
        return new_img_vector
    
    def get_matrix(self, img):
        transparent = self.has_transparency()
        if transparent:
            if self.mode == 'P':
                img = img.convert('RGBA')
                img_vector = self.remove_transparency(img)
            else:
                img_vector = self.remove_transparency(img)
        else:
            img = img.convert("RGB")
            img_array = np.array(img)
            img_vector = img_array.reshape((img_array.shape[0] * img_array.shape[1], 3))
            
        return img_vector  
    
    def get_color(self):
        cluster = self.cluster
        image = self.resize()
        img_vector = self.get_matrix(image)
        
        model = KMeans(n_clusters=cluster, random_state=101)
        labels = model.fit_predict(img_vector)
        label_counts = Counter(labels)
        
        values = [value for key, value in label_counts.most_common()]
        orders = [key for key, value in label_counts.most_common()]
        centers = [model.cluster_centers_[order] for order in orders]
        
        len_lc = len(label_counts)
        len_cc = len(model.cluster_centers_)
        
        if len_lc == len_cc:
            hex_colors = [self.rgb2hex(center) for center in centers]

            plt.figure(figsize=(14, 8))
            plt.subplot(221)
            plt.imshow(image)
            plt.axis('off')

            plt.subplot(222)
            plt.pie(values, labels=hex_colors, colors=hex_colors, startangle=90)
            plt.axis('equal')
            plt.show()
        else:
            hex_colors = [self.rgb2hex(center) for center in centers]

            plt.figure(figsize=(14, 8))
            plt.subplot(221)
            plt.imshow(image)
            plt.axis('off')

            plt.subplot(222)
            plt.pie(values, labels=hex_colors[:len_lc], colors=hex_colors[:len_lc], startangle=90)
            plt.axis('equal')
            plt.show()
