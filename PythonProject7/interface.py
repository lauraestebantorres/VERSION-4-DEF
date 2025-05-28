#importamos todo lo necesario para la clase Airspace
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from airSpace import AirSpace
import os
import subprocess
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from math import sqrt
from collections import deque
from queue import PriorityQueue
from kml_exporter import export_points_to_kml
from tkinter import filedialog
import subprocess  # Agregado para la función open_in_google_earth
from kml_exporter import (
  export_points_to_kml,
  export_path_to_kml,
  export_segments_to_kml,
  export_airports_to_kml,
  export_multiple_flight_animations_to_kml
)

# Clase principal de la interfaz gráfica para visualizar y editar el espacio aéreo
class AirSpaceGUI:
  def __init__(self, master):
      # Configuración inicial de la ventana principal
      self.master = master
      self.master.configure(bg="#fce4ec")  # Rosa pastel claro
      self.master.title("Visualizador de Espacio Aéreo")
      self.airspace = AirSpace()
      self.airport_color = 'red'
      self.current_title = "Espacio Aéreo"

      # Crear figura y ejes para el gráfico
      self.figure, self.ax = plt.subplots(figsize=(8, 6))
      self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
      self.toolbar = NavigationToolbar2Tk(self.canvas, self.master)
      self.toolbar.update()
      self.toolbar.grid(row=6, column=0, columnspan=4)
      self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=4)
      self.canvas.draw()
      self.canvas.mpl_connect('button_press_event', self.on_click)



      # Selector de dataset
      ttk.Label(master, text="Zona de vuelo:").grid(row=0, column=0, padx=5, pady=5)
      self.dataset_selector = ttk.Combobox(master, values=["Catalunya", "España", "Europa"], state="readonly")
      self.dataset_selector.grid(row=0, column=1, padx=5, pady=5)
      self.dataset_selector.current(0)
      ttk.Button(master, text="Cargar espacio aéreo", command=self.load_selected_data).grid(row=0, column=2, padx=5,
                                                                                            pady=5)




      # Entradas de texto para nombres de puntos, origen y destino
      ttk.Label(master, text="Nombre del punto:").grid(row=1, column=0, sticky="e")
      self.point_entry = ttk.Entry(master)
      self.point_entry.grid(row=1, column=1, sticky="w")
      ttk.Button(master, text="Mostrar vecinos", command=self.plot_neighbors).grid(row=4, column=2, padx=5, pady=5)



      # Botones de funcionalidades principales
      ttk.Label(master, text="Origen:").grid(row=3, column=0, sticky="e")
      self.origin_entry = ttk.Entry(master)
      self.origin_entry.grid(row=3, column=1, sticky="w")
      ttk.Label(master, text="Destino:").grid(row=4, column=0, sticky="e")
      self.dest_entry = ttk.Entry(master)
      self.dest_entry.grid(row=4, column=1, sticky="w")
      ttk.Button(master, text="Camino más corto", command=self.plot_shortest_path).grid(row=5, column=2, padx=5,
                                                                                        pady=5)

      ttk.Button(master, text="Puntos Alcanzables", command=self.show_reachable_points).grid(row=1, column=2, padx=5,
                                                                                             pady=5)
      ttk.Button(master, text="Exportar NavPoints a KML", command=self.export_all_navpoints_to_kml).grid(row=1,
                                                                                                         column=3,
                                                                                                         padx=5,
                                                                                                         pady=5)
      ttk.Button(master, text="Exportar Ruta a KML", command=self.export_last_path_to_kml).grid(row=0, column=3,
                                                                                                padx=5, pady=5)
      ttk.Button(master, text="Exportar Segmentos a KML", command=self.export_segments_to_kml).grid(row=2, column=3,
                                                                                                    padx=5, pady=5)
      ttk.Button(master, text="Exportar Aeropuertos a KML", command=self.export_airports_to_kml).grid(row=4, column=3,
                                                                                                      padx=5, pady=5)
      ttk.Button(master, text="Exportar Vuelo Animado a KML", command=self.export_animated_flight).grid(row=3, column=3,
                                                                                                  padx=5, pady=5)
      ttk.Button(master, text="Crear grafo desde cero", command=self.create_empty_graph).grid(row=3, column=5, padx=5,
                                                                                         pady=5)
      # Variable para controlar si estamos en modo añadir nodo
      self.add_node_mode = False


      # Botón para activar o desactivar modo añadir nodo
      ttk.Button(master, text="Modo: Añadir Nodo", command=self.toggle_add_node_mode).grid(row=0, column=6, padx=5,
                                                                                           pady=5)


      ttk.Button(master, text="Cargar grafo ",
                 command=self.load_single_file).grid(row=0, column=5, padx=5, pady=5)

      # Etiqueta de información al usuario
      self.info_label = ttk.Label(master, text="")
      self.info_label.grid(row=5, column=0, columnspan=2)
      self.add_segment_mode = False
      self.temp_segment_start = None  # Almacena el primer nodo clicado
      ttk.Button(master, text="Modo: Añadir Segmento", command=self.toggle_add_segment_mode).grid(row=1, column=6,
                                                                                                  padx=5, pady=5)
      self.delete_segment_mode = False
      self.temp_delete_start = None
      ttk.Button(master, text="Modo: Eliminar Segmento", command=self.toggle_delete_segment_mode).grid(row=2, column=6,
                                                                                                       padx=5, pady=5)
      ttk.Button(master, text="Cargar grafo ", command=self.load_single_file).grid(row=0, column=5, padx=5, pady=5)
      ttk.Button(master, text="Guardar grafo editado", command=self.save_graph_to_file).grid(row=1, column=5, padx=5,
                                                                                             pady=5)
      ttk.Button(master, text="Mostrar grafo oficial", command=self.load_official_graph).grid(row=2, column=5, padx=5,
                                                                                              pady=5)
      self.original_xlim = None
      self.original_ylim = None
      ttk.Button(master, text="🔍 Zoom a punto", command=self.zoom_to_point).grid(row=2, column=2, padx=5, pady=5)
      ttk.Button(master, text="🔄 Restaurar vista", command=self.reset_view).grid(row=3, column=2, padx=5, pady=5)
      ttk.Button(master, text="FlightRadar BCN", command=self.export_multiple_flights).grid(row=5, column=3,
                                                                                                   padx=5, pady=5)
      ttk.Button(master, text="FlightRadar ZAR", command=self.export_multiple_flights_from_zar).grid(row=6,
                                                                                                                  column=3,
                                                                                                                  padx=5,
                                                                                                                  pady=5)
      ttk.Button(master, text="FlightRadar IBZ", command=self.export_multiple_flights_from_ib).grid(row=4,
                                                                                                     column=5,
                                                                                                     padx=5,
                                                                                                     pady=5)
      ttk.Button(master, text="FlightRadar ALT", command=self.export_multiple_flights_from_alc).grid(row=5,
                                                                                                    column=5,
                                                                                                    padx=5,
                                                                                                    pady=5)
      ttk.Button(master, text="FlightRadar MHN", command=self.export_multiple_flights_from_mhn).grid(row=6,
                                                                                                    column=5,
                                                                                                    padx=5,
                                                                                                    pady=5)
  # Carga los datos del espacio aéreo dependiendo de la zona seleccionada en el menú desplegable
  def load_selected_data(self):
      zona = self.dataset_selector.get()
      try:
          if zona == "Catalunya":
              self.airspace.load_all("Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")
              self.current_title = "Espacio Aéreo Catalunya"
          elif zona == "España":
              self.airspace.load_all("Esp_nav.txt", "Esp_seg.txt", "Esp_aer.txt")
              self.current_title = "Espacio Aéreo España"
          elif zona == "Europa":
              self.airspace.load_all("Eur_nav.txt", "Eur_seg.txt", "Eur_aer.txt")
              self.current_title = "Espacio Aéreo Europa"

          self.plot_graph()
          self.info_label.config(text=f"Datos de {zona} cargados: {len(self.airspace.nav_points)} puntos")
      except Exception as e:
          messagebox.showerror("Error", f"No se pudieron cargar los datos:\n{str(e)}")



  # Maneja eventos de clic en el gráfico: selección de nodos para acciones como agregar/eliminar segmentos o establecer origen/destino
  def on_click(self, event):
      """Maneja el clic: muestra un menú de acciones para el punto seleccionado."""
      if not event.inaxes:
          return


      clicked_lon, clicked_lat = event.xdata, event.ydata


      if self.add_node_mode:
          self.add_new_node(clicked_lat, clicked_lon)
          return
      if self.add_segment_mode:
          # Encuentra el nodo más cercano al clic
          clicked_point = min(
              self.airspace.nav_points,
              key=lambda p: self.euclidean_distance_coords(clicked_lat, clicked_lon, p.latitude, p.longitude)
          )


          if self.temp_segment_start is None:
              self.temp_segment_start = clicked_point
              self.info_label.config(text=f"Primer nodo seleccionado: {clicked_point.name}")
          else:
              origin = self.temp_segment_start
              destination = clicked_point
              self.temp_segment_start = None


              if origin.number == destination.number:
                  self.info_label.config(text="No se puede crear segmento con el mismo nodo.")
                  return


              dist = self.euclidean_distance(origin, destination)
              new_segment = self.airspace.create_segment(origin.number, destination.number, dist)
              self.airspace.nav_segments.append(new_segment)
              self.plot_graph()
              self.info_label.config(text=f"Segmento añadido entre {origin.name} y {destination.name}")
              self.update_point_selector()
              self.add_segment_mode = False
              self.info_label.config(
                  text=f"Segmento añadido entre {origin.name} y {destination.name}. Modo añadir segmento DESACTIVADO.")


          return
      if self.delete_segment_mode:
          clicked_point = min(
              self.airspace.nav_points,
              key=lambda p: self.euclidean_distance_coords(clicked_lat, clicked_lon, p.latitude, p.longitude)
          )


          if self.temp_delete_start is None:
              self.temp_delete_start = clicked_point
              self.info_label.config(text=f"Seleccionado {clicked_point.name} como primer nodo para eliminar")
          else:
              origin = self.temp_delete_start
              destination = clicked_point
              self.temp_delete_start = None


              before = len(self.airspace.nav_segments)
              self.airspace.nav_segments = [
                  s for s in self.airspace.nav_segments
                  if not ((s.origin_number == origin.number and s.destination_number == destination.number) or
                          (s.origin_number == destination.number and s.destination_number == origin.number))
              ]
              after = len(self.airspace.nav_segments)
              eliminados = before - after


              if eliminados:
                  self.plot_graph()
                  self.info_label.config(
                      text=f"{eliminados} segmento(s) entre {origin.name} y {destination.name} eliminados.")
              else:
                  self.info_label.config(text=f"No hay segmento entre {origin.name} y {destination.name}.")
                  self.delete_segment_mode = False
                  self.info_label.config(
                      text=f"{eliminados} segmento(s) entre {origin.name} y {destination.name} eliminados. Modo eliminar segmento DESACTIVADO.")


          return


      closest = min(
          self.airspace.nav_points,
          key=lambda p: self.euclidean_distance_coords(clicked_lat, clicked_lon, p.latitude, p.longitude)
      )
      # Marcar el punto en el gráfico (opcional, sin zoom)
      self.ax.plot(clicked_lon, clicked_lat, marker='x', color='purple', markersize=10)
      self.canvas.draw_idle()
      # Crear ventana emergente personalizada
      popup = tk.Toplevel()
      popup.title(f"Acciones para {closest.name}")
      popup.geometry("300x150")




      # Función para manejar la selección
      def handle_action(action):
          if action == "origen":
              self.origin_entry.delete(0, tk.END)
              self.origin_entry.insert(0, closest.name)
              self.info_label.config(text=f"Origen asignado: {closest.name}")
          elif action == "destino":
              self.dest_entry.delete(0, tk.END)
              self.dest_entry.insert(0, closest.name)
              self.info_label.config(text=f"Destino asignado: {closest.name}")
          elif action == "eliminar":
              # Eliminar segmentos conectados
              self.airspace.nav_segments = [
                  s for s in self.airspace.nav_segments
                  if s.origin_number != closest.number and s.destination_number != closest.number
              ]
              # Eliminar el nodo
              self.airspace.nav_points = [
                  p for p in self.airspace.nav_points
                  if p.number != closest.number
              ]
              popup.destroy()
              self.plot_graph()
              self.info_label.config(text=f"Nodo '{closest.name}' eliminado junto con sus segmentos")
              self.update_point_selector()


          elif action == "punto":
              self.point_entry.delete(0, tk.END)
              self.point_entry.insert(0, closest.name)
              self.info_label.config(text=f"Punto actual: {closest.name}")
          # "cancelar" no hace nada
          popup.destroy()


      # Botones de acciones
      tk.Button(
          popup, text="Usar como ORIGEN",
          command=lambda: handle_action("origen"), bg="#FFCCCC"
      ).pack(pady=5, fill=tk.X, padx=10)


      tk.Button(
          popup, text="Usar como DESTINO",
          command=lambda: handle_action("destino"), bg="#CCE5FF"
      ).pack(pady=5, fill=tk.X, padx=10)


      tk.Button(
          popup, text="Usar como NOMBRE DE PUNTO",
          command=lambda: handle_action("punto"), bg="#E5FFCC"
      ).pack(pady=5, fill=tk.X, padx=10)




      tk.Button(
          popup, text="🗑️ Eliminar NODO",
          command=lambda: handle_action("eliminar"), bg="#FF6666"
      ).pack(pady=5, fill=tk.X, padx=10)


      tk.Button(
          popup, text="CANCELAR",
          command=lambda: handle_action("cancelar"), bg="#F0F0F0"
      ).pack(pady=5, fill=tk.X, padx=10)

   # Muestra y destaca todos los puntos que son alcanzables desde un nodo específico usando BFS
  def show_reachable_points(self):
      point_name = self.point_entry.get().strip()
      point = self.airspace.get_point_by_name(point_name)
      if not point:
          self.info_label.config(text="Punto no encontrado.")
          return
      reached = set()
      queue = deque([point])
      while queue:
          current = queue.popleft()
          if current.number not in reached:
              reached.add(current.number)
              for segment in self.airspace.nav_segments:
                  # Verificar que el segmento es dirigido desde el nodo actual
                  if segment.origin_number == current.number:
                      neighbor = self.airspace.get_point_by_number(segment.destination_number)
                      if neighbor and neighbor.number not in reached:
                          queue.append(neighbor)




      self.plot_graph()  # Limpiar y redibujar
      for p in self.airspace.nav_points:
          if p.number in reached:
              self.ax.scatter(p.longitude, p.latitude, s=20, color='green')  # Puntos alcanzables en verde




      self.ax.scatter(point.longitude, point.latitude, s=40, color='blue')  # Origen en azul
      self.canvas.draw()




      # Mostrar ventana emergente con los nombres de los puntos alcanzables
      reachable_names = [p.name for p in self.airspace.nav_points if p.number in reached]
      messagebox.showinfo("Puntos Alcanzables", "\n".join(reachable_names))
      self.info_label.config(text=f"Puntos alcanzables desde {point.name}: {len(reached)}")



     # Dibuja el grafo completo en el canvas: puntos de navegación, segmentos y aeropuertos
  def plot_graph(self):
      self.ax.clear()
      self.ax.set_title("Espacio Aéreo Catalunya - Puntos y Rutas")
      self.ax.set_xlabel("Longitud")
      self.ax.set_ylabel("Latitud")
      self.ax.set_title(f"{self.current_title} - Puntos y Rutas")

      # Puntos de navegación
      for point in self.airspace.nav_points:
          self.ax.scatter(point.longitude, point.latitude, s=20, color='black', alpha=0.7)
          self.ax.text(point.longitude, point.latitude, point.name, fontsize=6, color='black')




      # Segmentos
      for segment in self.airspace.nav_segments:
          origin = self.airspace.get_point_by_number(segment.origin_number)
          destination = self.airspace.get_point_by_number(segment.destination_number)
          if origin and destination:
              self.ax.plot([origin.longitude, destination.longitude],
                           [origin.latitude, destination.latitude],
                           '#40E0D0', linewidth=0.7, alpha=0.5,
                           label='Segmentos' if segment == self.airspace.nav_segments[0] else "")




      # Aeropuertos
      for airport in self.airspace.nav_airports:
          if airport.sids:
              for sid in airport.sids:
                  self.ax.scatter(sid.longitude, sid.latitude, s=100, color=self.airport_color)
                  self.ax.text(sid.longitude, sid.latitude, airport.name, fontsize=8, color=self.airport_color)
          elif hasattr(airport, 'latitude') and hasattr(airport, 'longitude'):
              self.ax.scatter(airport.longitude, airport.latitude, s=100, color=self.airport_color)
              self.ax.text(airport.longitude, airport.latitude, airport.name, fontsize=8, color=self.airport_color)




      # Leyenda solo si hay elementos con label
      handles, labels = self.ax.get_legend_handles_labels()
      if handles:
          self.ax.legend(handles=handles, labels=labels)




      self.canvas.draw()
      # Guardar los límites originales solo una vez
      if self.original_xlim is None or self.original_ylim is None:
          self.original_xlim = self.ax.get_xlim()
          self.original_ylim = self.ax.get_ylim()
    # Muestra los vecinos conectados directamente a un punto específico
  def plot_neighbors(self):
      name = self.point_entry.get().strip()
      point = self.airspace.get_point_by_name(name)
      if not point:
          self.info_label.config(text=f"No se ha encontrado el punto {name}")
          return
      self.plot_graph()
      for s in self.airspace.nav_segments:
          if s.origin_number == point.number:
              neighbor = self.airspace.get_point_by_number(s.destination_number)
              if neighbor:
                  self.ax.plot([point.longitude, neighbor.longitude], [point.latitude, neighbor.latitude], 'r-')
                  self.ax.scatter(neighbor.longitude, neighbor.latitude, color='green', s=20)
      self.ax.scatter(point.longitude, point.latitude, color='blue', s=30)
      self.canvas.draw()



   # Calcula y muestra el camino más corto entre dos nodos usando una variante de A*
  def plot_shortest_path(self):
      origin_name = self.origin_entry.get().strip()
      dest_name = self.dest_entry.get().strip()
      origin = self.airspace.get_point_by_name(origin_name)
      dest = self.airspace.get_point_by_name(dest_name)
      if not origin or not dest:
          self.info_label.config(text="Origen o destino no encontrado")
          return
      open_set = PriorityQueue()
      open_set.put((0, [origin]))
      visited = set()
      while not open_set.empty():
          _, path = open_set.get()
          current = path[-1]
          if current.number == dest.number:
              self.last_path = path  # Guardamos el camino para posible exportación
              self.draw_path(path)
              return
          if current.number in visited:
              continue
          visited.add(current.number)
          for s in self.airspace.nav_segments:
              if s.origin_number == current.number:
                  neighbor = self.airspace.get_point_by_number(s.destination_number)
                  if neighbor and neighbor.number not in visited:
                      new_path = list(path)
                      new_path.append(neighbor)
                      cost = self.path_cost(new_path) + self.euclidean_distance(neighbor, dest)
                      open_set.put((cost, new_path))
      self.info_label.config(text="No se encontró camino")



   # Dibuja gráficamente un camino sobre el grafo ya renderizado
  def draw_path(self, path):
      self.plot_graph()
      for i in range(len(path) - 1):
          p1, p2 = path[i], path[i + 1]
          self.ax.plot([p1.longitude, p2.longitude], [p1.latitude, p2.latitude], 'b-', linewidth=2)
      for p in path:
          self.ax.scatter(p.longitude, p.latitude, color='orange', s=30)
      self.canvas.draw()



    # Calcula el coste (suma de distancias) de un camino
  def path_cost(self, path):
      total = 0
      for i in range(len(path) - 1):
          for seg in self.airspace.nav_segments:
              if seg.origin_number == path[i].number and seg.destination_number == path[i + 1].number:
                  total += seg.distance
                  break
      return total



  # Calcula la distancia euclidiana entre dos puntos dados sus coordenadas
  def euclidean_distance(self, p1, p2):
      return sqrt((p1.latitude - p2.latitude) ** 2 + (p1.longitude - p2.longitude) ** 2)



  # Calcula la distancia euclidiana entre dos pares lat-lon
      ...
  def euclidean_distance_coords(self, lat1, lon1, lat2, lon2):
      return sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)



    # Exporta todos los puntos de navegación actuales a un archivo KML
      ...
  def export_all_navpoints_to_kml(self):
      if not self.airspace or not self.airspace.nav_points:
          messagebox.showerror("Error", "No hay puntos de navegación cargados.")
          return
      file_path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
      if file_path:
          export_points_to_kml(self.airspace.nav_points, file_path)
          self.open_in_google_earth(file_path)



      # Exporta el último camino más corto calculado a un archivo KML
      ...
  def export_last_path_to_kml(self):
      if not hasattr(self, 'last_path') or not self.last_path:
          messagebox.showerror("Error", "No hay camino más corto calculado.")
          return
      file_path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
      if file_path:
          export_path_to_kml(self.last_path, file_path)
          self.open_in_google_earth(file_path)



      # Exporta todos los segmentos del grafo a un archivo KML
  def export_segments_to_kml(self):
      points_dict = {p.number: p for p in self.airspace.nav_points}
      file_path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
      if file_path:
          export_segments_to_kml(self.airspace.nav_segments, points_dict, file_path)
          self.open_in_google_earth(file_path)

  # Exporta los aeropuertos del grafo a un archivo KML

  def export_airports_to_kml(self):
      file_path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
      if file_path:
          export_airports_to_kml(self.airspace.nav_airports, file_path)
          self.open_in_google_earth(file_path)



    # Intenta abrir un archivo KML en Google Earth automáticamente
  def open_in_google_earth(self, file_path):
      try:
          subprocess.run([
              r"C:\\Program Files\\Google\\Google Earth Pro\\client\\googleearth.exe", file_path
          ], check=False)
      except Exception as e:
          messagebox.showinfo("KML guardado",
                              f"Archivo guardado en:\n{file_path}\n\nNo se pudo abrir Google Earth automáticamente.")



  # Exporta un vuelo animado del camino más corto calculado a KML
  def export_animated_flight(self):
      from kml_exporter import export_flight_animation_to_kml




      if not hasattr(self, 'last_path') or not self.last_path:
          messagebox.showerror("Error", "No hay camino más corto calculado.")
          return




      file_path = filedialog.asksaveasfilename(
          defaultextension=".kml",
          filetypes=[("KML files", "*.kml")]
      )

      if file_path:
          export_flight_animation_to_kml(self.last_path, file_path)
          # Abrir automáticamente en Google Earth después de exportar
          self.open_in_google_earth(file_path)
          messagebox.showinfo("Exportado", f"Vuelo animado exportado y abierto en Google Earth: {file_path}")

      # Inicializa un nuevo grafo vacío y limpia la vista
  def create_empty_graph(self):
      self.airspace = AirSpace()  # Crea nuevo grafo vacío
      self.current_title = "Grafo desde cero"
      self.plot_graph()
      self.info_label.config(text="Grafo vacío creado")

    # Carga un grafo desde un archivo único con secciones Nodes y Segments
  def load_single_file(self):

      file_path = filedialog.askopenfilename(
          title="Selecciona el fichero de grafo",
          filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
      )
      if not file_path:
          return
      self.current_title = f"Grafo desde {os.path.basename(file_path)}"
      try:
          self.airspace.load_from_single_file(file_path)
          self.plot_graph()
          self.info_label.config(text=f"Grafo cargado de {os.path.basename(file_path)}")
      except Exception as e:
          messagebox.showerror("Error", f"No se pudo cargar el grafo:\n{e}")

  # Alterna el modo de añadir nodos manualmente al hacer clic en el gráfico
  def toggle_add_node_mode(self):
      self.add_node_mode = not self.add_node_mode
      estado = "activado" if self.add_node_mode else "desactivado"
      self.info_label.config(text=f"Modo añadir nodo {estado}")

   # Añade un nuevo nodo al grafo con coordenadas especificadas y nombre personalizado
  def add_new_node(self, lat, lon):
      import tkinter.simpledialog
      nombre = tkinter.simpledialog.askstring("Nuevo Nodo", "Introduce el nombre del nodo:")
      if not nombre:
          return

      # Obtener el número siguiente
      numeros_existentes = [p.number for p in self.airspace.nav_points]
      nuevo_num = max(numeros_existentes, default=0) + 1


      # Crear y añadir el nodo
      nuevo_punto = self.airspace.create_point(nuevo_num, nombre, lat, lon)
      self.airspace.nav_points.append(nuevo_punto)


      # Redibujar el grafo
      self.plot_graph()
      self.ax.scatter(lon, lat, color='purple', s=50)
      self.ax.text(lon, lat, nombre, fontsize=8, color='purple')
      self.canvas.draw()


      self.info_label.config(text=f"Nuevo nodo '{nombre}' añadido en ({lat:.2f}, {lon:.2f})")

  # Alterna el modo de añadir segmentos entre nodos clicados
  def toggle_add_segment_mode(self):
      self.add_segment_mode = not self.add_segment_mode
      self.add_node_mode = False  # Desactiva el modo de nodo
      self.temp_segment_start = None
      estado = "ACTIVO" if self.add_segment_mode else "desactivado"
      self.info_label.config(text=f"Modo Añadir Segmento {estado}")

      # Placeholder: actualiza widgets relacionados con los puntos si es necesario
      ...
  def update_point_selector(self):
      # Si tienes listas desplegables o entradas que necesitan actualizarse
      pass

  # Alterna el modo de eliminar segmentos entre nodos seleccionados
  def toggle_delete_segment_mode(self):
      self.delete_segment_mode = not self.delete_segment_mode
      self.add_node_mode = False
      self.add_segment_mode = False
      self.temp_segment_start = None
      self.temp_delete_start = None
      estado = "ACTIVO" if self.delete_segment_mode else "desactivado"
      self.info_label.config(text=f"Modo Eliminar Segmento {estado}")

  # Guarda el grafo actual (puntos y segmentos) en un archivo .txt personalizado
  def save_graph_to_file(self):
      if not self.airspace.nav_points:
          messagebox.showerror("Error", "No hay nodos para guardar.")
          return


      file_path = filedialog.asksaveasfilename(
          title="Guardar grafo como...",
          defaultextension=".txt",
          filetypes=[("Text files", "*.txt"), ("Todos los archivos", "*.*")]
      )


      if not file_path:
          return


      try:
          with open(file_path, "w") as f:
              f.write("Nodes:\n")
              for point in self.airspace.nav_points:
                  f.write(f"{point.name},{point.latitude},{point.longitude}\n")


              f.write("\nSegments:\n")
              for segment in self.airspace.nav_segments:
                  origin = self.airspace.get_point_by_number(segment.origin_number)
                  dest = self.airspace.get_point_by_number(segment.destination_number)
                  f.write(f"_,{origin.name},{dest.name}\n")


          self.info_label.config(text=f"Grafo guardado en {os.path.basename(file_path)}")
          messagebox.showinfo("Guardado", f"Grafo guardado exitosamente:\n{file_path}")
      except Exception as e:
          messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

     # Carga un grafo oficial desde un archivo fijo llamado 'grafo_oficial.txt'
  def load_official_graph(self):
      self.current_title = "Grafo Oficial"
      try:
          self.airspace.load_from_single_file("grafo_oficial.txt")
          self.plot_graph()
          self.info_label.config(text="Grafo oficial cargado")
      except Exception as e:
          messagebox.showerror("Error", f"No se pudo cargar el grafo oficial:\n{e}")
      # Aplica zoom en el gráfico centrado en un punto especificado
  def zoom_to_point(self):
      name = self.point_entry.get().strip()
      point = self.airspace.get_point_by_name(name)
      if not point:
          self.info_label.config(text=f"No se encontró el punto '{name}'")
          return

      lat, lon = point.latitude, point.longitude
      zoom_margin = 0.8  # antes estaba en 2 → ahora MUCHO más zoom
      self.ax.set_xlim(lon - zoom_margin, lon + zoom_margin)
      self.ax.set_ylim(lat - zoom_margin, lat + zoom_margin)
      self.ax.set_title(f"Zoom al punto {name}")
      self.canvas.draw()
      self.info_label.config(text=f"Vista centrada en {name}")

# Restaura la vista del gráfico a los límites originales
      ...
  def reset_view(self):
      if self.original_xlim and self.original_ylim:
          self.ax.set_xlim(self.original_xlim)
          self.ax.set_ylim(self.original_ylim)
          self.ax.set_title("Espacio Aéreo Catalunya - Puntos y Rutas")
          self.canvas.draw()
          self.info_label.config(text="Vista restaurada")
      else:
          self.info_label.config(text="No hay vista original guardada")

  import random
  # Genera y exporta múltiples rutas de vuelo animadas desde BCN a destinos válidos
  ...
  def export_multiple_flights(self):
      from kml_exporter import export_multiple_flight_animations_to_kml

      nombres_aerolineas = ["Ryanair", "Vueling", "Iberia", "Air Europa", "EasyJet", "Volotea"]
      rutas = []

      # Forzar origen desde BCN.D
      origen = self.airspace.get_point_by_name("BCN.D")
      if not origen:
          messagebox.showerror("Error", "No se encontró el punto 'BCN.D'")
          return

      # Lista de destinos válidos permitidos
      destinos_validos = [
          "PAL.A", "PAL.D", "JOA", "VLC.A", "VLC.D", "VLC", "RES", "RES.D", "RES.A",
          "SLL.A", "SLL.D", "GIR.D", "GIR.A", "ZAR.D", "ZAR.A", "IBZ", "IZA.A", "IZA.D", "IBI", "IBA"
      ]

      # Filtrar los destinos que existen en el grafo
      posibles_destinos = [p for p in self.airspace.nav_points if p.name in destinos_validos]

      if not posibles_destinos:
          messagebox.showerror("Error", "No se encontraron destinos válidos en el grafo.")
          return

      intentos = 0
      max_intentos = 30
      usados = set()

      while len(rutas) < 6 and intentos < max_intentos:
          destino = random.choice(posibles_destinos)

          # Evitar repetir destino
          if destino.name in usados:
              intentos += 1
              continue

          airline_name = nombres_aerolineas[len(rutas) % len(nombres_aerolineas)]
          ruta = self.find_path(origen, destino)
          if ruta and len(ruta) > 1:
              rutas.append((airline_name, ruta))
              usados.add(destino.name)

          intentos += 1

      if not rutas:
          messagebox.showerror("Error", "No se pudieron generar rutas válidas desde BCN.D.")
          return

      file_path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
      if file_path:
          export_multiple_flight_animations_to_kml(rutas, file_path)
          self.open_in_google_earth(file_path)
          messagebox.showinfo("Exportado", f"{len(rutas)} vuelos exportados desde BCN.D a destinos válidos.")

   # Genera y exporta múltiples rutas de vuelo animadas desde ZAR a destinos válidos
  def export_multiple_flights_from_zar(self):
      nombres_aerolineas = ["Ryanair", "Vueling", "Iberia", "Air Europa", "EasyJet", "Volotea"]
      rutas = []

      origen = self.airspace.get_point_by_name("ZAR.D")
      if not origen:
          messagebox.showerror("Error", "No se encontró el punto 'ZAR.D'")
          return

      destinos_validos = [
          "PAL.A", "PAL.D", "JOA", "VLC.A", "VLC.D", "VLC", "RES", "RES.D", "RES.A",
          "SLL.A", "SLL.D", "GIR.D", "GIR.A", "BCN.A", "BCN.D", "IBZ", "IZA.A", "IZA.D", "IBI", "IBA"
      ]

      posibles_destinos = [p for p in self.airspace.nav_points if p.name in destinos_validos]

      if not posibles_destinos:
          messagebox.showerror("Error", "No se encontraron destinos válidos en el grafo.")
          return

      intentos = 0
      max_intentos = 30
      usados = set()

      while len(rutas) < 6 and intentos < max_intentos:
          destino = random.choice(posibles_destinos)

          if destino.name in usados:
              intentos += 1
              continue

          airline_name = nombres_aerolineas[len(rutas) % len(nombres_aerolineas)]
          ruta = self.find_path(origen, destino)
          if ruta and len(ruta) > 1:
              rutas.append((airline_name, ruta))
              usados.add(destino.name)

          intentos += 1

      if not rutas:
          messagebox.showerror("Error", "No se pudieron generar rutas válidas desde ZAR.A.")
          return

      file_path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
      if file_path:
          export_multiple_flight_animations_to_kml(rutas, file_path)
          self.open_in_google_earth(file_path)
          messagebox.showinfo("Exportado", f"{len(rutas)} vuelos exportados desde ZAR.A a destinos válidos.")

  # Genera y exporta múltiples rutas de vuelo animadas desde ALT a destinos válidos
  def export_multiple_flights_from_alc(self):
      nombres_aerolineas = ["Ryanair", "Vueling", "Iberia", "Air Europa", "EasyJet", "Volotea"]
      rutas = []

      origen = self.airspace.get_point_by_name("ALT")
      if not origen:
          messagebox.showerror("Error", "No se encontró el punto 'ALT'")
          return

      destinos_validos = [
          "PAL.A", "PAL.D", "JOA", "VLC.A", "VLC.D", "VLC", "RES", "RES.D", "RES.A",
          "SLL.A", "SLL.D", "GIR.D", "GIR.A", "BCN.A", "BCN.D", "IBZ", "IZA.A", "IZA.D", "IBI", "IBA"
      ]

      posibles_destinos = [p for p in self.airspace.nav_points if p.name in destinos_validos]

      if not posibles_destinos:
          messagebox.showerror("Error", "No se encontraron destinos válidos en el grafo.")
          return

      intentos = 0
      max_intentos = 30
      usados = set()

      while len(rutas) < 6 and intentos < max_intentos:
          destino = random.choice(posibles_destinos)

          if destino.name in usados:
              intentos += 1
              continue

          airline_name = nombres_aerolineas[len(rutas) % len(nombres_aerolineas)]
          ruta = self.find_path(origen, destino)
          if ruta and len(ruta) > 1:
              rutas.append((airline_name, ruta))
              usados.add(destino.name)

          intentos += 1

      if not rutas:
          messagebox.showerror("Error", "No se pudieron generar rutas válidas desde ALT.")
          return

      file_path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
      if file_path:
          export_multiple_flight_animations_to_kml(rutas, file_path)
          self.open_in_google_earth(file_path)
          messagebox.showinfo("Exportado", f"{len(rutas)} vuelos exportados desde ALT a destinos válidos.")

  # Genera y exporta múltiples rutas de vuelo animadas desde MHN a destinos válidos
  def export_multiple_flights_from_mhn(self):
      nombres_aerolineas = ["Ryanair", "Vueling", "Iberia", "Air Europa", "EasyJet", "Volotea"]
      rutas = []

      origen = self.airspace.get_point_by_name("MHN")
      if not origen:
          messagebox.showerror("Error", "No se encontró el punto 'MHN'")
          return

      destinos_validos = [
          "PAL.A", "PAL.D", "JOA", "VLC.A", "VLC.D", "VLC", "RES", "RES.D", "RES.A",
          "SLL.A", "SLL.D", "GIR.D", "GIR.A", "BCN.A", "BCN.D", "IBZ", "IZA.A", "IZA.D", "IBI", "IBA"
      ]

      posibles_destinos = [p for p in self.airspace.nav_points if p.name in destinos_validos]

      if not posibles_destinos:
          messagebox.showerror("Error", "No se encontraron destinos válidos en el grafo.")
          return

      intentos = 0
      max_intentos = 30
      usados = set()

      while len(rutas) < 6 and intentos < max_intentos:
          destino = random.choice(posibles_destinos)

          if destino.name in usados:
              intentos += 1
              continue

          airline_name = nombres_aerolineas[len(rutas) % len(nombres_aerolineas)]
          ruta = self.find_path(origen, destino)
          if ruta and len(ruta) > 1:
              rutas.append((airline_name, ruta))
              usados.add(destino.name)

          intentos += 1

      if not rutas:
          messagebox.showerror("Error", "No se pudieron generar rutas válidas desde MHN.")
          return

      file_path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
      if file_path:
          export_multiple_flight_animations_to_kml(rutas, file_path)
          self.open_in_google_earth(file_path)
          messagebox.showinfo("Exportado", f"{len(rutas)} vuelos exportados desde MHN a destinos válidos.")

     # Genera y exporta múltiples rutas de vuelo animadas desde IZA.D a destinos válidos
  def export_multiple_flights_from_ib(self):
      nombres_aerolineas = ["Ryanair", "Vueling", "Iberia", "Air Europa", "EasyJet", "Volotea"]
      rutas = []

      origen = self.airspace.get_point_by_name("IZA.D")
      if not origen:
          messagebox.showerror("Error", "No se encontró el punto 'IZA.D'")
          return

      destinos_validos = [
          "PAL.A", "PAL.D", "JOA", "VLC.A", "VLC.D", "VLC", "RES", "RES.D", "RES.A",
          "SLL.A", "SLL.D", "GIR.D", "GIR.A", "BCN.A", "BCN.D","IBI", "IBA"
      ]

      posibles_destinos = [p for p in self.airspace.nav_points if p.name in destinos_validos]

      if not posibles_destinos:
          messagebox.showerror("Error", "No se encontraron destinos válidos en el grafo.")
          return

      intentos = 0
      max_intentos = 30
      usados = set()

      while len(rutas) < 6 and intentos < max_intentos:
          destino = random.choice(posibles_destinos)

          if destino.name in usados:
              intentos += 1
              continue

          airline_name = nombres_aerolineas[len(rutas) % len(nombres_aerolineas)]
          ruta = self.find_path(origen, destino)
          if ruta and len(ruta) > 1:
              rutas.append((airline_name, ruta))
              usados.add(destino.name)

          intentos += 1

      if not rutas:
          messagebox.showerror("Error", "No se pudieron generar rutas válidas desde IZA.D.")
          return

      file_path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
      if file_path:
          export_multiple_flight_animations_to_kml(rutas, file_path)
          self.open_in_google_earth(file_path)
          messagebox.showinfo("Exportado", f"{len(rutas)} vuelos exportados desde IZA.D a destinos válidos.")

      # Encuentra el camino más corto entre dos nodos usando una cola de prioridad (A*)
  def find_path(self, origin, dest):
      open_set = PriorityQueue()
      open_set.put((0, [origin]))
      visited = set()

      while not open_set.empty():
          _, path = open_set.get()
          current = path[-1]
          if current.number == dest.number:
              return path
          if current.number in visited:
              continue
          visited.add(current.number)
          for s in self.airspace.nav_segments:
              if s.origin_number == current.number:
                  neighbor = self.airspace.get_point_by_number(s.destination_number)
                  if neighbor and neighbor.number not in visited:
                      new_path = list(path)
                      new_path.append(neighbor)
                      cost = self.path_cost(new_path) + self.euclidean_distance(neighbor, dest)
                      open_set.put((cost, new_path))
      return None


if __name__ == "__main__":
  root = tk.Tk()
  app = AirSpaceGUI(root)
  root.mainloop()
