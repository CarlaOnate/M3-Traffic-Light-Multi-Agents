import mesa
import random

class IntersectionTrafficLightsAgent(mesa.Agent):
    def __init__(self, unique_id, model, smt1, smt2, driverSample, layerLevel = 0):
        super().__init__(unique_id, model)
        self.smt1 = smt1
        self.smt2 = smt2
        self.layerLevel = layerLevel
        self.driverSample = driverSample
        
    def changeTrafficLight(self, smt1Color, smt2Color) -> None:
        self.smt1.changeStatus(smt1Color)
        self.smt2.changeStatus(smt2Color)
        
    def calculatePriority(self) -> None:
        # Falta la parte de ambulancias
        agentsInCell = self.model.grid.get_cell_list_contents([self.pos])
        if not type(self.driverSample) in agentsInCell:
            if (self.smt1.congestion > self.smt2.congestion) or (self.smt1.firstETA < self.smt2.firstETA): 
                self.changeTrafficLight("green","red")
            elif (self.smt1.congestion < self.smt2.congestion) or (self.smt1.firstETA > self.smt2.firstETA): 
                self.changeTrafficLight("red","green")
            # Equal congestion
            elif (self.smt1.congestion == self.smt2.congestion) and (len(self.smt1.queue) > 0 and len(self.smt2.queue) > 0):
                # Gets the pass the fastest driver, agent with lower ETA
                if self.smt1.firstETA < self.smt2.firstETA: 
                    self.changeTrafficLight("green","red") 
                elif self.smt1.firstETA > self.smt2.firstETA:
                    self.changeTrafficLight("red","green")
                else: # they have the same ETA
                    randomLight = random.choice([True, False])
                    if randomLight: self.changeTrafficLight("green","red")
                    else: self.changeTrafficLight("red","green")
        
    def step(self) -> None:
        self.calculatePriority()
