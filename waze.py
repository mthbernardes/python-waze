import datetime
import requests

class Waze(object):
    def __init__(self,):
        self.BASEURL = "https://www.waze.com/"
        self.HEADERS = {
            "Referer":"https://www.waze.com/pt-BR/livemap",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0"
        }
        self.KEY = "AIzaSyBIfV0EMXrTDjrvD92QX5bBiyFmBbT-W8E"
        self.SESSION= requests.Session()
        self.__getCookie()

    def __getCookie(self,):
        url = "{}/login/get".format(self.BASEURL)
        self.SESSION.get(url,headers=self.HEADERS)

    def __getRouteInfo(self,time_delta=0):
        params = {
            "at":time_delta,
            "clientVersion":"4.0.0",
            "from":self.cordFrom,
            "nPaths":1,
            "options":"AVOID_TRAILS:t,ALLOW_UTURNS:t",
            "returnGeometries":False,
            "returnInstructions":True,
            "returnJSON":True,
            "timeout":60000,
            "to":self.cordTo
        }
        url = "{}/row-RoutingManager/routingRequest".format(self.BASEURL)
        r = self.SESSION.get(url,headers=self.HEADERS,params=params)
        return r.json()

    def __getPlaceId(self,name): 
        params = {
            "input": name,
            "key": self.KEY,
        }
        url = "{}/maps/api/place/autocomplete/json".format(self.BASEURL)
        place = self.SESSION.get(url,headers=self.HEADERS,params=params).json()
        place = place["predictions"][0]
        print("Place found: {}".format(place["description"]))
        return place["place_id"]

    def __getPlaceCoordenates(self,name):    
        params = {
            "placeid": self.__getPlaceId(name),
            "key": self.KEY,
        }
        url = "{}/maps/api/place/details/json".format(self.BASEURL)
        place = self.SESSION.get(url,headers=self.HEADERS,params=params).json()
        place = place["result"]["geometry"]["location"]
        return "x:{} y:{}".format(place["lng"],place["lat"])

    def getTravelTimeAndDistance(self,placeFrom,placeTo):
        self.cordFrom = self.__getPlaceCoordenates(placeFrom)
        self.cordTo = self.__getPlaceCoordenates(placeTo)
        traffic = self.__getRouteInfo()
        traveltime,distance = (0,0)
        for street in traffic["response"]["results"]:
            traveltime = traveltime+ street["crossTime"]
            distance = distance + street["length"]
        traveltime = (str(datetime.timedelta(seconds=traveltime)))
        distance = distance/ 1000
        return traveltime,distance

if __name__ == "__main__":
    w = Waze()
    traveltime, distance = w.getTravelTimeAndDistance("Rodoviaria Tiete","Aeroporto de Guarulho")
    print("You'll travel {} km and will probably spent {} hours on it.".format(distance,traveltime))
