from city_model import CityModel
import mesa
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
    "agents": 10,
    "time": 25
}

results = mesa.batch_run(
    CityModel,
    parameters=params,
    iterations=100,
    max_steps=200,  # time
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)

results_df = pd.DataFrame(results)
middleIntersectionTime_1 = pd.DataFrame(results_df, columns=['MiddleIntersectionTime_EAST'])
middleIntersectionTime_2 = pd.DataFrame(results_df, columns=['RightIntersectionTime_EAST'])
middleIntersectionTime_3 = pd.DataFrame(results_df, columns=['UpperIntersectionTime_EAST'])
congestion = pd.DataFrame(results_df, columns=['Congestion'])

crashes = pd.DataFrame(results_df, columns=['Crashes'])
results_filtered_1 = middleIntersectionTime_1[(results_df.Step == 50)]
results_filtered_2 = middleIntersectionTime_2[(results_df.Step == 50)]
results_filtered_3 = middleIntersectionTime_3[(results_df.Step == 50)]
crashes_filtered = crashes[(results_df.Step == 50)]
congestion_filtered = congestion[(results_df.Step == 50)]

results_filtered_1.plot()
results_filtered_2.plot()
results_filtered_3.plot()
crashes_filtered.plot()
congestion_filtered.plot()

chartCrashes = ChartModule([{"Label": "Crashes", "Color": "Red"}], data_collector_name='datacollector')
chartTimeOfTrafficLightOn_1 = ChartModule([{"Label": "MiddleIntersectionTime_EAST", "Color": "Blue"}], data_collector_name='datacollector')
chartTimeOfTrafficLightOn_2 = ChartModule([{"Label": "RightIntersectionTime_EAST", "Color": "Blue"}], data_collector_name='datacollector')
chartTimeOfTrafficLightOn_3 = ChartModule([{"Label": "UpperIntersectionTime_EAST", "Color": "Blue"}], data_collector_name='datacollector')
chartCongestion = ChartModule([{"Label": "Congestion", "Color": "Red"}], data_collector_name='datacollector')


grid = CanvasGrid(agent_portrayal, 21, 21, PIXELS_GRID, PIXELS_GRID)

server = mesa.visualization.ModularServer(
    CityModel, [grid,
                chartCrashes,
                chartTimeOfTrafficLightOn_1,
                chartTimeOfTrafficLightOn_2,
                chartTimeOfTrafficLightOn_3,
                chartCongestion], 
    "Smart Traffic Light", simulation_params
)

server.port = 8524
server.launch()


