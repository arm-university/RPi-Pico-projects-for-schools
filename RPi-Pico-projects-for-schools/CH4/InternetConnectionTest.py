import time
try:
    from ppwhttp import * #Try and get the ppwhttp library
except ImportError: #If something goes wrong, output an error
    raise RuntimeError("Cannot find ppwhttp. Have you copied ppwhttp.py to your Pico?")


HTTP_REQUEST_PORT = const(80) #The (default) port used by a website
HTTP_REQUEST_HOST = "google.com" #The site we want to connect to
#HTTP_REQUEST_HOST = "api.thingspeak.com" #The site we want to connect to
HTTP_REQUEST_PATH = "/" #The path of the resource we want to access


#Handle the data that comes back when we make a request
def handler(head, body):
    #A website which responds 'properly' should include a status
    #in the head. Status 200 OK means it's found the resource. However
    #some (Google!) don't include a full status so we have to throw
    #an error if it's not 200 OK, or if it doesn't exist at all.
    if "Status" in head.keys() and head["Status"] == "200 OK":
        set_led(0, 255, 0) #Make the WiFi LED green
        print("Resource accessed ok")
    else:
        #Output the contents of the head and body for checking
        print("Error: {}".format(head))
        print("Body: {}".format(body))
        set_led(255, 0, 0) #Make the WiFi LED red

set_led(0, 0, 255) #Make the WiFi LED blue to start
time.sleep(1)
start_wifi() #Start the WiFi connection
set_dns(GOOGLE_DNS) #When ready, set the DNS for lookups

#Activate the HTTP request. Note same HOST used twice!
http_request(HTTP_REQUEST_HOST,HTTP_REQUEST_PORT,HTTP_REQUEST_HOST,HTTP_REQUEST_PATH,handler)
