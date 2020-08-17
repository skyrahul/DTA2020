'''------------------------------------------------------------------------
-----------------------------LIBRARIES IMPORT------------------------------
---------------------------------------------------------------------------'''

import math    #math library to use math function like power and square root
import time     # time library to update the simulation animation after a fixed interval of time
import itertools    #itertools library to use some of the functions
import tkinter      #tkinter library for building the entire GUI
import random       # not used but can be used to have a random demand input at a node
from tkinter import *   #importing all the classes from tkinter library
import networkx as nx   #For making the graphic visualization of the network
import matplotlib.pyplot as plt     #For drawing the charts and statistics associated with the results
from PIL import Image, ImageTk      #For displaying the car animation during the program run
from itertools import count, cycle  #For iterating through the frames of the GIF
from functools import partial       #Use of a method from this library for computation
from collections import defaultdict     #dictionaries to store key-value pairs
import openpyxl     #openpyxl library to print data into the excel files
import pandas as pd     #not used but can be used in place of openpyxl
wb = openpyxl.load_workbook('G:\\result.xlsx')       #Loading the excel file for writing the calculated data
sheet = wb.active   #Taking a particular sheet from the workbook

