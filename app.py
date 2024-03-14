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
        filtered_data(), 
        y="bill_length_mm"
    )

@render_plotly
def plot2():
    return px.histogram(
        filtered_data(), 
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
            return filtered_data()

# Displaying Data Grid
with ui.card(full_screen=True):  # Full screen option
        ui.card_header("Penguins Data Grid")
        @render.data_frame
        def render_penguins_grid():
            return filtered_data()

# Use ui.hr() to add a horizontal rule to the sidebar
ui.hr()

ui.page_opts(fillable=False)

with ui.navset_card_tab():  
    with ui.nav_panel("Plotly Histogram"):
        @render_plotly
        def render_plotly_histogram():
            # Create a Plotly histogram
            fig = px.histogram(
                filtered_data(), 
                x="species", 
                color="island", 
                title="Palmer Penguins"
            )
            return fig

    with ui.nav_panel("Seaborn Histogram"):
        @render.plot(alt="A Seaborn histogram on penguin species by island.")
        def plot(): 
            ax = sns.histplot(filtered_data(), x="island", y="species") 
            ax.set_title("Seaborn Palmer Penguins")
            ax.set_xlabel("Island")
            ax.set_ylabel("Species")
            return ax 


    with ui.nav_panel("Plotly Scatterplot: Species"):
        @render_plotly
        def plotly_scatterplot():
        # Create a Plotly scatterplot using Plotly Express
            return px.scatter(filtered_data(), x="body_mass_g", y="year", color="species", 
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

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    return penguins_df[penguins_df["species"].isin(input.selected_species_list())]
