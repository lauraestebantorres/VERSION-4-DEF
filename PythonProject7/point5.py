import numpy as np
import matplotlib.pyplot as plt




g = 9.81                     # gravity (m/s²)
m = 5100                    # mass (kg)
W = m * g                   # weight (N)
S = 27                      # wing area (m²)
CD0 = 0.019                 # zero-lift drag coefficient
k = 0.11                    # induced drag factor
rho = 1.225                 # air density at sea level (kg/m³)




V = np.linspace(40, 200, 500)  # airspeed in m/s


CL = 2 * W / (rho * V**2 * S)               # lift coefficient
CD = CD0 + k * CL**2                        # drag coefficient
LD_ratio = CL / CD                         # lift-to-drag ratio
glide_angle_rad = np.arctan(1 / LD_ratio)  # glide angle in radians
glide_angle_deg = np.degrees(glide_angle_rad)  # in degrees




idx_min_glide_angle = np.argmin(glide_angle_deg)
best_angle = glide_angle_deg[idx_min_glide_angle]
best_speed = V[idx_min_glide_angle]
best_ld = LD_ratio[idx_min_glide_angle]




plt.figure(figsize=(10, 6))
plt.plot(V, glide_angle_deg, label="Glide Angle (°)", color='blue')
plt.scatter(best_speed, best_angle, color='green', label=f'Min Glide Angle\n{best_angle:.2f}° at {best_speed:.1f} m/s', zorder=5)
plt.title("Airspeed vs Glide Angle")
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Glide Angle (degrees)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

