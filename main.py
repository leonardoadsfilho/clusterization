import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

import tkinter as tk
import numpy as np
from sklearn.cluster import KMeans 

from src.file import read_csv
from src.clusterization import k_means

def plot():

    axes.clear()

    counties, counties_names = read_csv.ReadCounties(uf[sigla.index(selected_uf.get())])
    
    (x_centroids, y_centroids, _error, region) = k_means.clusterizer(
        list(counties['longitude']), list(counties['latitude']), 
        number_clusters.get(), selected_method.get())

    axes.scatter(counties['longitude'], counties['latitude'], c=region, s=50, alpha=0.5, cmap='Accent')
    axes.scatter(x_centroids, y_centroids, c='red', s=50, alpha=0.5)

    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    figure_canvas.draw()

    label_error.configure(text=str(_error))

(uf, estado, sigla) = read_csv.ReadUFs()

window = tk.Tk()
window.title("Tratamento de Lixo")
window.geometry("550x500")

options = tk.Frame(window)

# create a figure
figure = Figure(figsize=(6, 4), dpi=100)

# create FigureCanvasTkAgg object
figure_canvas = FigureCanvasTkAgg(figure, window)

# create the toolbar
NavigationToolbar2Tk(figure_canvas, window)

# create axes
axes = figure.add_subplot()

number_clusters = tk.IntVar(window)
number_clusters.set(2)
array_clusters = range(2, 11)

clusters = tk.OptionMenu(window, number_clusters, *array_clusters)
clusters.pack(side='top')

selected_uf = tk.StringVar(window)
selected_uf.set(sigla[16])

ufs = tk.OptionMenu(window, selected_uf, *sigla)
ufs.pack(side='top')

selected_method = tk.StringVar(window)
selected_method.set("kmeans")

array_methods = ["kmeans", "kmedoids"]
methods = tk.OptionMenu(window, selected_method, *array_methods)
methods.pack(side='top')

plot_button = tk.Button(master = window, 
                     command = plot,
                     height = 2, 
                     width = 10,
                     text = "Plot")
plot_button.pack(side='top')

error = tk.DoubleVar(window)
error.set(0.0)

label_error = tk.Label(window, text=str(error.get()))
label_error.pack()

window.mainloop()