import numpy as np
import matplotlib.pyplot as plt




g = 9.81                      # gravedad (m/s²)
m = 5100                     # masa del avión (kg)
W = m * g                    # peso (N)
S = 27                       # superficie alar (m²)
CD0 = 0.019                  # coeficiente de arrastre parásito
k = 0.11                     # constante del arrastre inducido
rho = 1.225                  # densidad del aire al nivel del mar (kg/m³)




V = np.linspace(40, 200, 500)  # velocidad horizontal (m/s)




CL = 2 * W / (rho * V**2 * S)            # coeficiente de sustentación
CD = CD0 + k * CL**2                     # coeficiente de arrastre
LD_ratio = CL / CD                      # relación sustentación/arrastre
sink_rate = V / LD_ratio                # tasa de descenso: V / (L/D)




idx_best_glide = np.argmax(LD_ratio)          # mejor distancia de planeo
idx_best_endurance = np.argmin(sink_rate)     # mejor tiempo de planeo




plt.figure(figsize=(10, 6))
plt.plot(V, sink_rate, label="Sink Rate", color='blue')
plt.scatter(V[idx_best_glide], sink_rate[idx_best_glide], color='green', label='Max Glide Distance')
plt.scatter(V[idx_best_endurance], sink_rate[idx_best_endurance], color='red', label='Max Glide Time')
plt.title("Airspeed vs Sink Rate (Glide Performance)")
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Sink Rate (m/s)")
plt.legend()
plt.grid(True)
plt.gca().invert_yaxis()  # El descenso va hacia abajo
plt.tight_layout()
plt.show()

