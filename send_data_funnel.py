import sys, time, requests, json, math, collect_data

interval=15

print("Starting soil moisture measurement! Press Ctrl+C to stop this script.")
time.sleep(1)

while True:
    # Track the current time so we can loop at regular intervals
    loop_start_time = time.time()

    # Read the distance using the read_distance function from hcsr04.py
    moisture = collect_data.get_measurement()

    if moisture:
        print("Current Mositure Level: {}".format(moisture))

        # Set the HTTP request header and payload content
        headers = {"Content-Type": "application/json"}
        payload = {"moisture": moisture }

        # Send the HTTP request to Funnel
        print("Sending data %s to Funnel..." % (json.dumps(payload)))
        try:
            response = requests.post("http://unified.soracom.io", data=json.dumps(payload), headers=headers, timeout=5)
        except requests.exceptions.ConnectTimeout:
            print("Error: Connection timeout. Is the modem connected?")

        # Display HTTP request response
        if response.status_code == 201:
            print("Response 201: Success!")
        elif response.status_code == 400:
            print("Error 400: Funnel did not accept the data. Is Funnel enabled?")
            sys.exit(1)


    # sleep until next loop
    time_to_wait = loop_start_time + interval - time.time()
    if time_to_wait > 0:
        time.sleep(time_to_wait)

