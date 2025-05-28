
from navPoint import NavPoint
from navSegment import NavSegment
from navAirport import NavAirport


class AirSpace:
 def __init__(self):
     # Inicializa las listas vacías para almacenar los elementos del espacio aéreo
     self.nav_points = [] # Lista de todos los puntos de navegación (NavPoint)
     self.nav_segments = [] # Lista de todos los segmentos (NavSegment)
     self.nav_airports = [] # Lista de aeropuertos (NavAirport)


 def get_point_by_number(self, number):
     # Devuelve el punto con el número especificado, si existe
     return next((p for p in self.nav_points if p.number == int(number)), None)
 def get_point_by_name(self, name):
     # Devuelve el punto con el nombre especificado, si existe
     return next((p for p in self.nav_points if p.name == name), None)
 def load_nav_points(self, filename):
     # Carga puntos de navegación desde un archivo con el formato:
     # número nombre latitud longitud
     with open(filename, 'r') as f:
         for line in f:
             if line.strip():
                 parts = line.split()
                 number = parts[0]
                 name = parts[1]
                 lat = parts[2]
                 lon = parts[3]
                 self.nav_points.append(NavPoint(number, name, lat, lon))


 def load_nav_segments(self, filename):
     # Carga segmentos entre puntos desde un archivo con el formato:
     # origen destino distancia
     with open(filename, 'r') as f:
         for line in f:
             if line.strip():
                 origin, dest, dist = line.split()
                 self.nav_segments.append(NavSegment(origin, dest, dist))


 def load_nav_airports(self, filename):
     # Carga aeropuertos, SIDs y STARs desde un archivo estructurado por bloques
     with open(filename, 'r') as f:
         current_airport = None
         for line in f:
             line = line.strip()
             if not line:
                 continue # Ignora líneas vacías
             if line.startswith('LE'):  # airport code
                 if current_airport:
                     self.nav_airports.append(current_airport)# Línea que representa un SID
                 current_airport = NavAirport(line)
             elif line.endswith('.D') and current_airport:# Línea que representa un STAR
                 point = self.get_point_by_name(line)
                 if point:
                     current_airport.sids.append(point)
             elif line.endswith('.A') and current_airport:
                 point = self.get_point_by_name(line)
                 if point:
                     current_airport.stars.append(point)
         if current_airport:
             self.nav_airports.append(current_airport)


 def load_all(self, nav_file, seg_file, aer_file):
     # Carga todos los elementos del espacio aéreo desde tres archivos separados
     self.load_nav_points(nav_file)
     self.load_nav_segments(seg_file)
     self.load_nav_airports(aer_file)


 def load_from_single_file(self, filepath):
     """
     Carga un grafo descrito en un solo fichero con dos secciones:
     'Nodes:' y 'Segments:'
     """
     self.nav_points = []
     self.nav_segments = []
     self.nav_airports = []


     with open(filepath, "r") as f:
         lines = [ln.strip() for ln in f if ln.strip()]
     try:
         nodes_idx = lines.index("Nodes:")
         segs_idx = lines.index("Segments:")
     except ValueError:
         raise ValueError("El fichero debe contener las líneas 'Nodes:' y 'Segments:'")
     # Se extraen las líneas que definen los nodos
     node_lines = lines[nodes_idx + 1:segs_idx]
     seg_lines = lines[segs_idx + 1:]
     name_to_number = {}
     # Procesa cada nodo
     for i, ln in enumerate(node_lines, start=1):
         parts = [p for p in ln.split(",") if p]
         if len(parts) != 3:
             raise ValueError(f"Línea de nodo mal formateada: {ln}")
         name, x, y = parts
         name_to_number[name] = i
         self.nav_points.append(
             self.create_point(i, name, float(x), float(y))
         )
     for ln in seg_lines:
         parts = [p for p in ln.split(",") if p]
         if len(parts) < 3:
             raise ValueError(f"Línea de segmento mal formateada: {ln}")
         _, orig_name, dest_name = parts[:3]
         if orig_name not in name_to_number or dest_name not in name_to_number:
             raise ValueError(f"Nombre de nodo no definido en segmentos: {ln}")
         o_num = name_to_number[orig_name]
         d_num = name_to_number[dest_name]
         p1 = self.get_point_by_number(o_num)
         p2 = self.get_point_by_number(d_num)
         # Calcula la distancia euclídea entre los dos puntos
         dist = ((p1.latitude - p2.latitude) ** 2 + (p1.longitude - p2.longitude) ** 2) ** 0.5
         self.nav_segments.append(self.create_segment(o_num, d_num, dist))
 def create_point(self, number, name, lat, lon):
     # Crea y devuelve un objeto NavPoint
     from navPoint import NavPoint
     return NavPoint(number, name, lat, lon)




 def create_segment(self, origin, destination, distance):
     # Crea y devuelve un objeto NavSegment
     from navSegment import NavSegment
     return NavSegment(origin, destination, distance)




 def get_point_by_number(self, number):
     # Busca un punto por su número
     return next((p for p in self.nav_points if p.number == number), None)
 def __repr__(self):
     # Devuelve una representación del objeto AirSpace para depuración


     return f"AirSpace(NavPoints: {len(self.nav_points)}, NavSegments: {len(self.nav_segments)}, NavAirports: {len(self.nav_airports)})"







