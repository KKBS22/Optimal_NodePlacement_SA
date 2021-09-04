# Optimal_NodePlacement_SA
Using Simulated Annealing optimization technique for finding the optimal number of sensors required to observe a given environment.

## Problem

You are asked to come up with a minimum cost sensor placement plan that covers a 500mx500m surveillance
area.
* You have access to three types of omnidirectional sensors:
* Type S1 with a detection range of 100 meters,
* Type S2 with a detection rage of 70 meters.
* Type S3 with a detection range of 30 meters.
* The cost of type S1 is 300 units, S2 is 170 units, S3 is 65 units.
* You have access to unlimited supply of these sensors. The network is tasked with monitoring 17 targets.

These targets are randomly and uniformly positioned within the boundaries of the surveillance area.
1. Device a function to distribute the 17 targets around the surveillance area.
2. Device either a genetic algorithm or a simulated annealing algorithm to compute an optimal node
placement, using the model proposed above.

## Results

### Initial Random Placement 

<img src="https://github.com/KKBS22/Optimal_NodePlacement_SA/blob/master/Layout_First_1.png" width="500">

### Sensor Placement after Simulated Annealing

<img src="https://github.com/KKBS22/Optimal_NodePlacement_SA/blob/master/After_SA_1.png" width="500">

### Cost Trend after each iteration

<img src="https://github.com/KKBS22/Optimal_NodePlacement_SA/blob/master/SA_Swap_Trend_1.png" width="500">
