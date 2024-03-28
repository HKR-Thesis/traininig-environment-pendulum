import csv, time, sys, os
from datetime import datetime
from jtop import jtop

def get_metrics(jetson) -> dict:
    return {
        'Time': datetime.now().strftime('%H:%M:%S'),
        'CPU Util': jetson.cpu['total']['user'],
        'GPU Util': jetson.gpu['gpu']['status']['load'],
        'MEM Util': jetson.memory['RAM']['used'] / jetson.memory['RAM']['tot'],
        'CPU Temp': jetson.temperature['CPU']['temp'],
        'GPU Temp': jetson.temperature['GPU']['temp'],
        'CPU Voltage': jetson.power['rail']['POM_5V_CPU']['volt'],
        'CPU Current': jetson.power['rail']['POM_5V_CPU']['curr'],
        'GPU Voltage': jetson.power['rail']['POM_5V_GPU']['volt'],
        'GPU Current': jetson.power['rail']['POM_5V_GPU']['curr'],
        'Total Voltage': jetson.power['tot']['volt'],
        'Total Current': jetson.power['tot']['curr'],
        'Average Power Consumption': jetson.power['tot']['avg']
    }

def measure(target_pid, training_type):
    filename = f"/media/nano/Nano Micro SD/measurements/benchmarks/metrics-{training_type}_{datetime.now().strftime('%Y-%m-%d@%H-%M-%S')}.csv"
    with jtop() as jetson:
        with open(filename, mode='w', newline='') as file:
            fieldnames = [
                'Time', 'CPU Util', 'GPU Util', 
                'MEM Util', 'CPU Temp', 'GPU Temp', 
                'CPU Voltage', 'CPU Current', 'GPU Voltage', 
                'GPU Current', 'Total Voltage', 'Total Current', 
                'Average Power Consumption'
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            while jetson.ok():
                metrics = get_metrics(jetson)
                writer.writerow(metrics)
                time.sleep(2.5)
                
    print(f'Finished collecting metrics - (calling process, {target_pid}, killed)')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3.x src/benchmarking/jetson_metrics.py <target_pid> <training_type>")
        sys.exit(1)
    target_pid = int(sys.argv[1])
    training_type = sys.argv[2]
    measure(target_pid, training_type)