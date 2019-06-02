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
            r = requests.post('http://funnel.soracom.io', data=json.dumps(payload), headers=headers, timeout=5)
            print(r)
        except requests.exceptions.ConnectTimeout:
            print('ERROR: connection timeout. Is 3G connection online?')
            sys.exit(1)
        if r.status_code == 400:
            print('ERROR: failed to submit data. Did you configure Funnel for your SIM?')
            sys.exit(1)

    # sleep until next loop
    time_to_wait = loop_start_time + interval - time.time()
    if time_to_wait > 0:
        time.sleep(time_to_wait)

