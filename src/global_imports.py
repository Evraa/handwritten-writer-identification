import cv2
import pywt
import numpy as np
from skimage import feature   
from matplotlib import pyplot as plt
from PIL import Image
import time
from sklearn import svm
import sklearn
from statistics import mode, StatisticsError
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils import shuffle