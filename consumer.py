from kafka import KafkaConsumer
import matplotlib.pyplot as plt

consumer = KafkaConsumer('myfirsttopic', bootstrap_servers='localhost:9092')

temperatures, humidities = [], []

plt.ion()  # Turn on interactive mode

while True:
    for message in consumer:
        data = message.value.decode()
        temp = int(data.split("Temperature: ")[1].split("°C")[0])
        humidity = int(data.split("Humidity: ")[1].split("%")[0])

        temperatures.append(temp)
        humidities.append(humidity)

        if len(temperatures) > 50:
            temperatures.pop(0)
            humidities.pop(0)

        plt.clf()  # clear the plot
        plt.subplot(2, 1, 1)
        plt.plot(temperatures, label="Temperature (°C)")
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(humidities, label="Humidity (%)")
        plt.legend()

        plt.pause(5)  # refresh every 5 seconds