from waze import Waze

w = Waze()
traveltime, distance = w.getTravelTimeAndDistance("Rodoviaria Tiete","Aeroporto de Guarulhos")
print("You'll travel {} km and will probably spent {} hours on it.".format(distance,traveltime))

