import simpy
import numpy as np
import random
import time
import matplotlib.pyplot as plt
memoriaFija = 100
hilosCPU = 1
semillaAleatoria = 100
reqCPU = 20

global tiemposNasheeee
tiemposNasheeee = []

class Programa:

    def __init__(self, name, env, ram, procesador):
        self.name = name
        self.memoria = np.random.randint(1, 10)
        self.num_instruc = np.random.randint(1, 10)
        self.env = env 
        self.ram = ram 
        self.procesador = procesador

    def out(self, msg):
        print(self.name+" "+msg)
        

    def pedir_memoria(self):
        self.out("está pidiendo "+str(self.memoria)+" de memoria.")
        yield self.ram.get(self.memoria)

    def usar_cpu(self):
        self.out("está solicitando el cpu.")
        with self.procesador.request() as req:
            yield req

            self.i = 0
            while self.num_instruc > 0 and self.i < 3:
                yield self.env.timeout(1)
                self.num_instruc -= 1
                self.i+=1 
         

    def pedir_io(self):
        self.out("está solicitando I/O")
        yield self.env.timeout(2)

    def run(self):
        global tiemposNasheeee
        inicio = env.now
        self.out("está corriendo")
        yield self.env.process(self.pedir_memoria())
        while self.num_instruc > 0:
            yield self.env.timeout(1)
            yield self.env.process(self.usar_cpu())

        if np.random.randint(1, 2) == 1:
            yield self.env.process(self.pedir_io())

        self.out("está liberando "+str(self.memoria)+" de memoria.")
        yield self.ram.put(self.memoria)
        tiemposNasheeee.append(env.now)



        

def simular(reqV, env, param, CPU):
    for i in range(reqV):
        name = "task-"+str(i)
        newProcess = Programa(name, env, RAM, CPU)
        env.process(newProcess.run())
        yield env.timeout(random.expovariate(0.1))
        
random.seed(semillaAleatoria)
env = simpy.Environment()
RAM = simpy.Container(env, capacity=memoriaFija, init=memoriaFija)
CPU = simpy.Resource(env, capacity=hilosCPU)

print("Iniciando simulación")
proc = [25, 50, 100, 150, 200]
tiempos = []

for pro in proc:
    env.process(simular(pro, env, RAM, CPU))
    env.run() 
    tiempos.append(tiemposNasheeee)
    tiemposNasheeee = []

average_times = []
std_devs = []
for process_times in tiempos:
    average_times.append(np.mean(process_times))
    std_devs.append(np.std(process_times))

# Create plot with Matplotlib
plt.figure(figsize=(8, 6))
plt.plot(proc, average_times, marker='o', label='Tiempo Promedio')
plt.fill_between(proc, np.subtract(average_times, std_devs), np.add(average_times, std_devs), alpha=0.2, color='b', label='Desviación Estándar')
plt.xlabel('Número de Procesos')
plt.ylabel('Tiempo Promedio (unidades de simulación)')
plt.title('Tiempo Promedio y Desviación Estándar vs. Número de Procesos')
plt.legend()
plt.grid(True)
plt.show()



