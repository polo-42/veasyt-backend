

def TransportCost(consumption, distance, gasPrice, startCountry, endCountry, transitCosts):

    if startCountry == "Suisse" and endCountry == "Suisse":
        total = 0.0
        for truckConsumption in consumption:
            total = total + (truckConsumption * distance * gasPrice)
        return total
    
    else :
        #TODO: CHECK WHICH COUNTRY IS CH
        costs = transitCosts[f"{endCountry}"]
        for truckConsumption in consumption:
            total = total + (truckConsumption * distance * gasPrice)
        return total + costs

#It is assumed that 0.3 m3 is moved on each trip
#It is assumed that the return distance is shorter because the mover walks faster : x1.6
def DistanceByFoot(volume, carryDistance):
    return (volume/0.3) * (carryDistance * 1.5)

#It is assumed that the distance between each floor is 10m
def DistanceByFloor(floor):
    return floor * 10

#It is assumed that with no lift 0.2 m3 is moved on each trip
#It is assumed that the return distance is shorter because the mover takes the lift faster : x1.5
#It is assumed that while carrying furniture, a mover walks at 1000m/h
def MovingTime(floor, lift, carryDistance, volume):
    if lift == False :
        foot = DistanceByFoot(volume, carryDistance)
        floor = DistanceByFloor(floor)
        noLift = (volume/0.2) * floor * 1.5
        distance = foot + noLift
        return distance/1000
    elif lift == True:
        foot = DistanceByFoot(volume, carryDistance)
        floor = DistanceByFloor(floor)
        #if freighter:
        #    waiting_time = 0
        withLift = (volume/0.4) * floor * 1.3 #+ waiting_time
        distance = foot + withLift
        return distance/1300
    #elif freighter == True:

#It is assumed that productivity diminishes (time increases by 1.2 when there's 3 movers)
def Movers(time):
    totalTime = time
    movers = 0
    while(totalTime > 6.5):
        movers += 1
        totalTime = totalTime / movers

    if movers == 3:
        totalTime = totalTime * 1.8
    elif movers >= 4 :
        totalTime = totalTime * 2

    if totalTime > 7 :
        movers += 1
    return movers

time = MovingTime(6, False, 10, 20)
movers = Movers(time)
#print(movers)

for i in range(20):
    increment = 20 + i*10
    y = MovingTime(7, False, 10, increment)

    print(increment)
    print(y)

    movers =  Movers(y)
    print(movers)

    print("\n")





    
    
    
    #carryPerHour = 
    #carryPerHourLift = 
#
    #if lift == True :
    #diff = (volume/0.3 * carryDistance)    
    #TODO:DIFFICULTY SHOULD RETURN A NUMBER OF RECOMMENDED MOVERS AND TIME



