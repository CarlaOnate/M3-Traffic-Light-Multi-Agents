from city_model import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule, CanvasGrid

PIXELS_GRID = 600

def agent_portrayal(agent): # A color is assigned to each type of agent
    portrayal = {"Shape": "circle", "Filled": "true"}
    if agent.layerLevel == 2: # Traffic Lights
        portrayal["Shape"] = "arrowHead"
        portrayal["Layer"] = 2
        portrayal["scale"] = 0.8
        portrayal["Color"] = agent.color
        if agent.direction == "east":
            portrayal["heading_x"] = 1
            portrayal["heading_y"] = 0
        elif agent.direction == "north":
            portrayal["heading_x"] = 0
            portrayal["heading_y"] = 1
        elif agent.direction == "south":
            portrayal["heading_x"] = 0
            portrayal["heading_y"] = -1
        elif agent.direction == "west":
            portrayal["heading_x"] = -1
            portrayal["heading_y"] = 0
    elif agent.layerLevel == 1: # Cars
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.8
    else: # Road
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0
        portrayal["h"] = 1
        portrayal["w"] = 1
    return portrayal

simulation_params = {
    "agents": UserSettableParameter(
        "slider",
        "Number of Agents",
        value=4,
        min_value=1,
        max_value=30,
        step=1,
        description="Number of Agents",
    ),
    "time": UserSettableParameter(
        "number",
        "Time",
        25,
        description="Time to end",
    )
}

params = {
    "agents": 5,
    "time": 25
}
results = mesa.batch_run(
    CityModel,
    parameters=params,
    iterations=1,
    max_steps=50,  # time
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)

chartCrashes = ChartModule([{"Label": "Crashes", "Color": "Red"}], data_collector_name='datacollector_general')
chartTimeOfTrafficLightOn_1 = ChartModule([{"Label": "MiddleIntersectionTime_EAST", "Color": "Blue"}], data_collector_name='datacollector_lights')
chartTimeOfTrafficLightOn_2 = ChartModule([{"Label": "RightIntersectionTime_EAST", "Color": "Blue"}], data_collector_name='datacollector_lights')
chartTimeOfTrafficLightOn_3 = ChartModule([{"Label": "UpperIntersectionTime_EAST", "Color": "Blue"}], data_collector_name='datacollector_lights')
chartCongestion = ChartModule([{"Label": "Congestion", "Color": "Red"}], data_collector_name='datacollector_general')

""" chartSuccessRateWithoutCrash = ChartModule([{"Label": "SuccessRateWithoutCrash", "Color": "Blue"}], data_collector_name='datacollector')
chartMovesByDriver = ChartModule([{"Label": "MovesByDriver", "Color": "Blue"}], data_collector_name='datacollector') """

grid = CanvasGrid(agent_portrayal, 21, 21, PIXELS_GRID, PIXELS_GRID)

server = mesa.visualization.ModularServer(
    CityModel, [grid,
                chartCongestion,
                chartCrashes,
                chartTimeOfTrafficLightOn_1,
                chartTimeOfTrafficLightOn_2,
                chartTimeOfTrafficLightOn_3], 
    "Smart Traffic Light", simulation_params
)

#print(results)

server.port = 8524
server.launch()
