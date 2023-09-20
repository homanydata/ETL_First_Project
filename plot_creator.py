import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import io
from lookups import Colors
import random

def create_plot_image(source:pd.DataFrame, is_bar:bool, variable_type:str, variable:str):
    if is_bar:
        result_plt = create_bar_chart(source=source, variable_type=variable_type)
    else:
        result_plt = create_line_graph(source=source, variable=variable, variable_type=variable_type)
    result_image = return_plot_as_image(result_plt)
    
    return result_image

def return_plot_as_image(plt_object):
    img_bytes = io.BytesIO()
    plt_object.savefig(img_bytes, format='png', bbox_inches='tight')
    plt_object.close()
    img_bytes.seek(0)

    image = Image.open(img_bytes)
    return image

def create_bar_chart(source:pd.DataFrame, variable_type:str):
    sns.set(style="whitegrid")
    plt.figure(figsize=(12,6))
    x = source.iloc[:, 0]
    y = source.iloc[:,1]

    ax = sns.barplot(x=x, y=y, palette="bright")
    ax.set(xlabel=variable_type.split('_')[0].capitalize(), ylabel="Total Duration (in minutes)")
    plt.title(f"Total Duration by {variable_type.capitalize()}")
    plt.xticks(rotation=45)
    return plt

def create_line_graph(source:pd.DataFrame, variable:str, variable_type:str):
    sns.set(style="whitegrid")
    plt.figure(figsize=(12,6))
    
    x = source.iloc[:, 0]
    y = source.iloc[:,1]
    
    colors = Colors.All_Colors
    color = random.choice(colors)
    ax = sns.lineplot(x=x, y=y, marker='o', markersize=8, color=color, linewidth=2)
    ax.set(xlabel=variable_type.split('_')[0].capitalize(), ylabel="Total Duration (in minutes)")
    plt.title(f"Total Duration by {variable_type.split('_')[0].capitalize()}")
    plt.xticks(rotation=45)
    plt.ylim(0)
    plt.title(f"{variable.capitalize()} {variable_type.split('_')[0].capitalize()} Total Duration Over Time")
    plt.xticks(rotation=45)
    return plt