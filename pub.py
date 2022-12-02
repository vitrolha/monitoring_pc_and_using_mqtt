from paho.mqtt import client as mqtt_client
import random
import psutil

broker = "localhost"
port = 1883
topic = 'sensors'
topic2 = "ram"
#topic3 = "disco_total"
#topic4 = "disco_usado"
topic5 = "swap_percent"
topic6 = "hardware_temp"
client_id = f'python-mqtt-{random.randint(0,1000)}'

def connect_mqtt():
    def on_connect(client,userdata,flags,rc):
        if rc==0:
            print("Conectado ao broker")
        else:
            print("Falha ao conectar ao broker %d\n",rc)
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def cpu_uso(client):

    cpu_uso = psutil.cpu_percent(2)
    msg_cpu = cpu_uso
    result_cpu = client.publish(topic, msg_cpu, qos=1, retain=False)
    status_cpu = result_cpu[0]

    if status_cpu == 0:
        print(f"Uso cpu: {msg_cpu} para topico {topic}")
    else:
        print(f"Falha ao enviar mensagem para o topico {topic}")

def ram_uso(client):
    ram_uso = psutil.virtual_memory()[2]
    msg_ram = ram_uso
    result_ram = client.publish(topic2, msg_ram, qos=1, retain=False)
    status_ram = result_ram[0]
    if status_ram == 0:
        print(f"Uso ram: {msg_ram} para topico {topic2}")
    else:
        print(f"Falha ao enviar mensagem para o topico {topic2}")

#def disco_total(client):
#    disco_total = psutil.disk_usage("/")[0]
#    msg_disco = disco_total
#    result_disco = client.publish(topic3, msg_disco, qos=1, retain=False)
#    status_disco = result_disco[0]
#    if status_disco == 0:
#        print(f"Disco total: {msg_disco} para topico {topic3}")
#    else:
#        print(f"Falha ao enviar mensagem para topico{topic3}")

#def disco_usado(client):
#    disco_usado = psutil.disk_usage("/")[1]
#    msg_disco = disco_usado
#    result_disco = client.publish(topic4, msg_disco, qos=1, retain=False)
#    status_disco = result_disco[0]
#    if status_disco == 0:
#        print(f"Disoc usado: {msg_disco} para topico {topic4}")
#    else:
#        print(f"Falha ao enviar mensagem para topico {topic4}")


def swap_percent(client):
    swap = psutil.swap_memory()[3]
    msg_swap = swap
    result_swap = client.publish(topic5, msg_swap, qos=1, retain=False)
    status_swap = result_swap[0]
    if status_swap == 0:
        print(f"Swap uso: {msg_swap} para topico {topic5}")
    else:
        print(f"Falha ao enviar mensagem para o topic {topic5}")

def hard_temp(client):
    temp = psutil.sensors_temperatures()
    #temp.items()

    for name, entries in temp.items():
        for entry in entries:
            m = entry.current

    msg_temp = m
    result_temp = client.publish(topic6,msg_temp,qos=1,retain=False)
    status_temp = result_temp[0]
    if status_temp == 0:
        print(f"Temperatura hardware: {msg_temp} para topico {topic6}")
    else:
        print(f"Falha ao enviar mensagem para topico {topic6}")

def publish(client):
    while True:
       # cpu_uso = psutil.cpu_percent(2)
       # ram_uso = psutil.virtual_memory()[2]
       # msg_cpu = cpu_uso
       # msg_ram = ram_uso
        #fazer da ram dps
       # result_cpu = client.publish(topic, msg_cpu, qos=1, retain=False)

       # status_cpu = result_cpu[0]
        #fazer da ram dps

        cpu_uso(client)
        ram_uso(client)
        #disco_total(client)
        #disco_usado(client)
        swap_percent(client)
        hard_temp(client)

        #if status_cpu == 0:
         #   print(f"Uso cpu: {msg_cpu} para topico {topic}")
       # else:
        #    print(f"Falha ao enviar mensagem para o topico {topic}")

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()