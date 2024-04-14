import threading
import time
import json
import socket
import message_helper

# create a global variable to control the thread
thread_running = False
# create a global variable to store the humidity threshold
humidity_threshold = None

# this is the IP address of the Raspberry Pi2
IP2 = "10.20.0.58"
# this is the IP address of the Raspberry Pi1
IP1 = "10.20.0.22"

# This function monitors the humidity and controls the LEDs based on the humidity value
# It sends service calls to the Raspberry Pi1 to turn on/off the LEDs based on the humidity value
# It sends service calls to the Raspberry Pi2 to get the humidity value
def monitor_humidity():
    global thread_running, IP1, IP2, humidity_threshold
    while thread_running:
        # send service call to get humidity
        result = message_helper.send_service_call('Humidity', 'DHT11', IP2, ())
        if result[0]:
            humidity = result[1]["Service Result"]
            try:
                # try to convert the humidity to float
                humidity_value = float(humidity)
                print(f"Current humidity: {humidity_value}%")
                if humidity_value > humidity_threshold:
                    # if humidity is higher than the threshold, turn on the red LED, and turn off the green LED
                    result_red = message_helper.send_service_call('TurnOnRedLED', 'LED', IP1, ())
                    result_green = message_helper.send_service_call('TurnOffGreenLED', 'LED', IP1, ())
                    if result_red and result_green:
                        print("\n----------------------------------------")
                        print("red led is on")
                        print("green led is off")
                        print("----------------------------------------\n")
                        return
                else:
                    # if humidity is lower than the threshold, turn off the red LED, and turn on the green LED
                    result_red = message_helper.send_service_call('TurnOffRedLED', 'LED', IP1, ())
                    result_green = message_helper.send_service_call('TurnOnGreenLED', 'LED', IP1, ())
                    if result_red and result_green:
                        print("\n----------------------------------------")
                        print("red led is off")
                        print("green led is on")
                        print("----------------------------------------\n")
                        return
            except ValueError:
                # if the humidity cannot be converted to float, print an error message
                print("Error: Unable to convert humidity to float.")
            else:
                print('\nWaiting\n')
                return
            time.sleep(10)


# 主程序
def main():
    global thread_running, humidity_threshold

    while True:
        print("*** Welcome to the ATLAS IoT Services ***")
        print("\tg6 ATLAS SERVICES")
        print("*** Choose from the following options: ***")
        print("(1) Turn On RED LED")
        print("(2) Turn Off RED LED")
        print("(3) Start Monitoring Humidity")
        print("(4) Get Temperature")
        print("(5) Get Humidity")
        print("(6) Exit")
        print("(7) Turn On GREEN LED")
        print("(8) Turn Off GREEN LED")
        print("\nEnter your choice:")
        choice = int(input())
        result = None

        if choice == 1:
            result = message_helper.send_service_call('TurnOnRedLED', 'LED', IP1, ())
        elif choice == 2:
            result = message_helper.send_service_call('TurnOffRedLED', 'LED', IP1, ())
        elif choice == 3:
            if not thread_running:
                print("Enter humidity threshold:")
                humidity_threshold = float(input())
                thread_running = True
                threading.Thread(target=monitor_humidity, daemon=True).start()
                print("Started monitoring humidity...")
            else:
                print("Humidity monitoring is already running.")
        elif choice == 4:
            # send service call to get temperature
            result = message_helper.send_service_call('HumThanGreen', 'DHT11', IP2, ())
        elif choice == 5:
            # send service call to get humidity
            result = message_helper.send_service_call('Humidity', 'DHT11', IP2, ())
        elif choice == 6:
            print("Bye!")
            thread_running = False
            break
        elif choice == 7:
            result = message_helper.send_service_call('BlinkGreen', 'LED', IP2, ())
        elif choice == 8:
            result = message_helper.send_service_call('TurnOffGreenLED', 'LED', IP1, ())
        else:
            print("\nUnsupported choice!\n")
        if result is not None:
            print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            if result[0]:
                print('EXECUTED Choice {}. Result was: {}.'.format(
                    choice, result[1]["Service Result"]))
            else:
                print('\nService {} execution failed due to a TCP error.'.format(choice))
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")


if __name__ == "__main__":
    main()
