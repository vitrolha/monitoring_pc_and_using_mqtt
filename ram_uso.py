#Influx imports
from unittest import result
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

#MQTT imports
import random
from paho.mqtt import client as mqtt_client

#influxdb
token = "mwV68Svp2xRZ4DRGnM3VtJwOwdp2OS2-AEBJYJenZh--2quQEqwjej9MrD1poW2wP-yw4SpDXGInagO6pLsf7g=="
org = "fivetec01@gmail.com"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"

client_influx = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="Sensores"

write_api = client_influx.write_api(write_options=SYNCHRONOUS)

#SUB MQTT

broker = "localhost"
port = 1883
topic2 = "ram"


client_id = f"python-mqtt-{random.randint(0, 100)}"
client_id_ram = "client_ram"

def connect_mqtt() -> mqtt_client:
    def on_connect(client,userdata,flags,rc):
        if rc == 0:
            print("Conectado ao broker mqtt")
        else:
            print("Falha ao conctar ao broker %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe_ram(client: mqtt_client):
    def on_message(client,userdata,msg):
        print(f"Recebendo {msg.payload.decode()} do topico {msg.topic}")

        #influxdb mandando dados
        resultado = float(msg.payload)
        p = influxdb_client.Point("USO").tag("location", "PC").field("RAM",resultado)
        print(resultado)
        write_api.write(bucket=bucket, org=org,record=p)        
    client.subscribe(topic2)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe_ram(client)
    #subscribe_ram(client)
    client.loop_forever()
    

if __name__ == "__main__":
    run()

