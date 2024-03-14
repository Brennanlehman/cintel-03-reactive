import plotly.express as px
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from shiny.express import input, ui, render
from shinywidgets import render_plotly, render_widget
from palmerpenguins import load_penguins
from shiny import reactive, render, req

# Use the built-in function to load the Palmer Penguins dataset
penguins_df = load_penguins()

ui.page_opts(title="Penguin Data Blehman", fillable=True)

@render_plotly
def plot1():
    return px.histogram(
        penguins_df, 
        y="bill_length_mm"
    )

@render_plotly
def plot2():
    return px.histogram(
        penguins_df, 
        y="flipper_length_mm"
    )

with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    ui.input_selectize(
        "selected_attribute",
        "select attribute",
        ["bill_length_mm", "flipper_length_mm", "body_mass_g"],
    )

    # Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Bin Counts", 1, min=1, max=10)  

    # Use ui.input_slider() to create a slider input for the number of Seaborn bins
    ui.input_slider("seaborn_bin_count", "Seaborn Bin Count", 1, 80, 40)

    # Use ui.input_checkbox_group() to create a checkbox group input to filter the species
    ui.input_checkbox_group(  
        "selected_species_list",
        "select species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Chinstrap"],
        inline=True,
    )

# Use ui.hr() to add a horizontal rule to the sidebar
ui.hr()

# Use ui.a() to add a hyperlink to the sidebar
ui.a(
        "Brennan Lehman GitHub Repo",
        href="https://github.com/Brennanlehman/cintel-02-data/tree/main",
        target="_blank",
    )

# Main content

# Define UI
# Displaying Data Table
with ui.card(full_screen=True):
        ui.card_header("Penguins Data Table")
        @render.data_frame
        def render_penguins_table():
            return penguins_df

# Displaying Data Grid
with ui.card(full_screen=True):  # Full screen option
        ui.card_header("Penguins Data Grid")
        @render.data_frame
        def render_penguins_grid():
            return penguins_df

# Use ui.hr() to add a horizontal rule to the sidebar
ui.hr()

# Displaying Plotly Histogram
with ui.card(full_screen=True):  # Full screen option
        ui.card_header("Plotly Histogram")
        @render_plotly
        def render_plotly_histogram():
            # Create a Plotly histogram
            fig = px.histogram(
                penguins_df, 
                x="flipper_length_mm", 
                color="species", 
                title="Palmer Penguins"
            )
            return fig

# Displaying Seaborn Histogram
with ui.card(full_screen=True):  # Full screen option
        @render.plot(alt="A Seaborn histogram on penguin species by island.")
        def plot(): 
            ax = sns.histplot(data=penguins_df, x="island", y="species") 
            ax.set_title("Seaborn Palmer Penguins")
            ax.set_xlabel("Island")
            ax.set_ylabel("Species")
            return ax 

# Display Plotly Scatter plot
with ui.card(full_screen=True):  # Full screen option
        ui.card_header("Plotly Scatterplot: Species")
        @render_plotly
        def plotly_scatterplot():
        # Create a Plotly scatterplot using Plotly Express
            return px.scatter(penguins_df, x="body_mass_g", y="year", color="species", 
                          facet_row="species", facet_col="sex", title="Penguin Scatterplot", labels={"body_mass_g": "Body Mass g", "year": "Year"})

# Use ui.hr() to add a horizontal rule to the sidebar
ui.hr()

# Map Widget
from ipyleaflet import Map
from shiny.express import ui
from shinywidgets import render_widget 

ui.h2("Map")


@render_widget
def map():
    return Map(center=(50.6252978589571, 0.34580993652344), zoom=3)
