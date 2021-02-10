 #!/usr/bin/env python3
import json
import requests
import sys
from termcolor import colored

#your zip
zip = sys.argv[1]

#radius in miles from your zip, seems this doesn't matter as getStores only returns 10 results
radius = 150

location_url = f"https://www.riteaid.com/services/ext/v2/stores/getStores?address={zip}&radius={radius}&pharmacyOnly=true&globalZipCodeRequired=true"

location_response = requests.get(location_url)
location_data = json.loads(location_response.text)

for i in location_data['Data']['stores']:
    store_url = "https://www.riteaid.com/services/ext/v2/vaccine/checkSlots?storeNumber=" + str(i['storeNumber'])
    store_response = requests.get(store_url)
    store_data = json.loads(store_response.text)
    if store_data['Status'] == "SUCCESS":
      if store_data['Data']['slots']['1'] == True:
        if len(str(i['storeNumber'])) == 5:
          print(colored("YAY!!!!!!!!!!!! Store located at " + str(i['address']) + " " + str(i['city']) + " has the vaccine. https://www.riteaid.com/locations/search.html?id=" + str(i['storeNumber']) + " YAY!!!!!!!!!!!!", "green"))
        if len(str(i['storeNumber'])) == 4:
          print(colored("YAY!!!!!!!!!!!! Store located at " + str(i['address']) + " " + str(i['city']) + " has the vaccine. https://www.riteaid.com/locations/search.html?id=0" + str(i['storeNumber']) + " YAY!!!!!!!!!!!!", "green"))
        if len(str(i['storeNumber'])) == 3:
          print(colored("YAY!!!!!!!!!!!! Store number " + str(i) + " has the vaccine. https://www.riteaid.com/locations/search.html?id=00" + str(i) + " YAY!!!!!!!!!!!!", "green"))
      else:
        print(colored("Store " + str(i['storeNumber']) + " at " + str(i['address']) + " " + str(i['city']) + " does not currently accept appointments.","red"))

print("If any of the stores close to you have appointments, you can sign up at https://www.riteaid.com/pharmacy/covid-qualifier")
