def export_points_to_kml(points, filename):
 with open(filename, 'w') as f:
     # Cabecera XML y apertura del documento KML
     f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
     f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
     f.write('  <Document>\n')


     # Para cada punto, se crea un marcador con nombre y coordenadas
     for p in points:
         f.write('    <Placemark>\n')
         f.write(f'      <name>{p.name}</name>\n')
         f.write('      <Point>\n')
         f.write(f'        <coordinates>{p.longitude},{p.latitude},0</coordinates>\n')
         f.write('      </Point>\n')
         f.write('    </Placemark>\n')
     # Cierre del documento
     f.write('  </Document>\n')
     f.write('</kml>\n')


def export_path_to_kml(points, filename):
   with open(filename, 'w') as f:
       f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
       f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
       f.write('  <Document>\n')
       # Definimos el estilo verde para la línea del camino
       f.write('    <Style id="greenLineStyle">\n')
       f.write('      <LineStyle>\n')
       f.write('        <color>ff00ff00</color>\n')  # Verde, opacidad total
       f.write('        <width>4</width>\n')
       f.write('      </LineStyle>\n')
       f.write('    </Style>\n')
       # Placemark con estilo aplicado
       f.write('    <Placemark>\n')
       f.write('      <name>Camino más corto</name>\n')
       f.write('      <styleUrl>#greenLineStyle</styleUrl>\n')
       f.write('      <LineString>\n')
       f.write('        <coordinates>\n')
       for p in points:
           f.write(f'          {p.longitude},{p.latitude},0\n')
       f.write('        </coordinates>\n')
       f.write('      </LineString>\n')
       f.write('    </Placemark>\n')
       f.write('  </Document>\n')
       f.write('</kml>\n')


def export_segments_to_kml(segments, points_dict, filename):
 with open(filename, 'w', encoding="utf-8") as f:
     f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
     f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
     f.write('  <Document>\n')
     total_skipped = 0  # Contador de segmentos no válidos
     for seg in segments:
         p1 = points_dict.get(seg.origin_number)
         p2 = points_dict.get(seg.destination_number)
         # Validar que ambos extremos existan y tengan coordenadas válidas
         if not p1 or not p2:
             total_skipped += 1
             continue
         if None in (p1.longitude, p1.latitude, p2.longitude, p2.latitude):
             total_skipped += 1
             continue


         # Exporta el segmento como línea
         f.write('    <Placemark>\n')
         f.write(f'      <name>Segmento {seg.origin_number} → {seg.destination_number}</name>\n')
         f.write('      <LineString>\n')
         f.write('        <coordinates>\n')
         f.write(f'          {p1.longitude},{p1.latitude},0\n')
         f.write(f'          {p2.longitude},{p2.latitude},0\n')
         f.write('        </coordinates>\n')
         f.write('      </LineString>\n')
         f.write('    </Placemark>\n')
     f.write('  </Document>\n')
     f.write('</kml>\n')
     # Mensaje informativo
     print(f"[INFO] Exportación terminada. Segmentos omitidos por falta de nodos: {total_skipped}")
def export_airports_to_kml(airports, filename):
 with open(filename, 'w') as f:
     f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
     f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
     f.write('  <Document>\n')
     for airport in airports:
         if airport.sids:  # Solo si tiene SID(s)
             sid = airport.sids[0]
             f.write('    <Placemark>\n')
             f.write(f'      <name>{airport.name}</name>\n')
             f.write('      <Point>\n')
             f.write(f'        <coordinates>{sid.longitude},{sid.latitude},0</coordinates>\n')
             # Estilo rojo para aeropuertos
             f.write('      </Point>\n')
             f.write('      <Style>\n')
             f.write('        <IconStyle>\n')
             f.write('          <color>ff0000ff</color>\n')  # rojo
             f.write('        </IconStyle>\n')
             f.write('      </Style>\n')
             f.write('    </Placemark>\n')
     f.write('  </Document>\n')
     f.write('</kml>\n')
def export_flight_animation_to_kml(points, filename):
 from datetime import datetime, timedelta
 start_time = datetime(2025, 1, 1, 12, 0, 0)  # hora inicial ficticia
 time_step = timedelta(seconds=3)  # tiempo entre puntos
 with open(filename, 'w', encoding='utf-8') as f:
     f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
     f.write('<kml xmlns="http://www.opengis.net/kml/2.2"\n')
     f.write('     xmlns:gx="http://www.google.com/kml/ext/2.2">\n')
     f.write('  <Document>\n')
     f.write('    <name>Animación de vuelo</name>\n')
     # Estilo con icono de avión grande
     f.write('    <Style id="planeStyle">\n')
     f.write('      <IconStyle>\n')
     f.write('        <scale>2.0</scale>\n')  # tamaño grande
     f.write('        <Icon>\n')
     f.write('          <href>http://maps.google.com/mapfiles/kml/shapes/airports.png</href>\n')
     f.write('        </Icon>\n')
     f.write('      </IconStyle>\n')
     f.write('    </Style>\n')
     # Animación de cámara que sigue al avión
     f.write('    <gx:Tour>\n')
     f.write('      <name>Seguimiento de cámara</name>\n')
     f.write('      <gx:Playlist>\n')
     # Mensajes automáticos en momentos clave
     f.write('        <gx:AnimatedUpdate>\n')
     f.write('          <gx:duration>3.0</gx:duration>\n')
     f.write('          <Update>\n')
     f.write('            <targetHref/>\n')
     f.write('            <Change>\n')
     f.write('              <Placemark>\n')
     f.write('                <description><![CDATA[🚀 Despegando de Barcelona...]]></description>\n')
     f.write('              </Placemark>\n')
     f.write('            </Change>\n')
     f.write('          </Update>\n')
     f.write('        </gx:AnimatedUpdate>\n')




     f.write('        <gx:Wait>\n')
     f.write('          <gx:duration>5.0</gx:duration>\n')
     f.write('        </gx:Wait>\n')




     for i, point in enumerate(points):
         when = start_time + i * time_step
         f.write('        <gx:FlyTo>\n')
         f.write('          <gx:duration>1.5</gx:duration>\n')
         f.write('          <gx:flyToMode>smooth</gx:flyToMode>\n')
         f.write('          <LookAt>\n')
         f.write(f'            <longitude>{point.longitude}</longitude>\n')
         f.write(f'            <latitude>{point.latitude}</latitude>\n')
         f.write('            <altitude>0</altitude>\n')
         f.write('            <heading>0</heading>\n')
         f.write('            <tilt>70</tilt>\n')
         f.write('            <range>50000</range>\n')
         f.write('            <altitudeMode>relativeToGround</altitudeMode>\n')
         f.write('          </LookAt>\n')
         f.write('        </gx:FlyTo>\n')
     f.write('      </gx:Playlist>\n')
     f.write('    </gx:Tour>\n')
     f.write('    <Placemark>\n')
     f.write('      <name>Vuelo animado</name>\n')
     f.write('      <styleUrl>#planeStyle</styleUrl>\n')  # aplica el estilo del avión
     f.write('      <gx:Track>\n')
     f.write('        <altitudeMode>clampToGround</altitudeMode>\n')
     for i, point in enumerate(points):
         when = start_time + i * time_step
         f.write(f'        <when>{when.isoformat()}Z</when>\n')
     for point in points:
         f.write(f'        <gx:coord>{point.longitude} {point.latitude} 0</gx:coord>\n')
     f.write('      </gx:Track>\n')
     f.write('    </Placemark>\n')
     f.write('  </Document>\n')
     f.write('</kml>\n')
def export_multiple_flight_animations_to_kml(paths_with_names, filename):
  from datetime import datetime, timedelta
  start_time = datetime(2025, 1, 1, 12, 0, 0)
  time_step = timedelta(seconds=2)
  color_map = {
      "Ryanair": "ff0000ff",   # rojo
      "Vueling": "ff00ff00",   # verde
      "Iberia": "ffff0000",    # azul
      "Air Europa": "ff00ffff", # amarillo
      "EasyJet": "ff7f00ff",   # naranja
      "Volotea": "ffff00ff",   # rosa
  }
  with open(filename, 'w', encoding='utf-8') as f:
      f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
      f.write('<kml xmlns="http://www.opengis.net/kml/2.2"\n')
      f.write('     xmlns:gx="http://www.google.com/kml/ext/2.2">\n')
      f.write('  <Document>\n')
      f.write('    <name>Tráfico Aéreo Simulado</name>\n')
      # Estilos por aerolínea
      for airline, color in color_map.items():
          f.write(f'    <Style id="{airline}Style">\n')
          f.write('      <IconStyle>\n')
          f.write('        <scale>1.8</scale>\n')
          f.write('        <Icon>\n')
          f.write('          <href>http://maps.google.com/mapfiles/kml/shapes/airports.png</href>\n')
          f.write('        </Icon>\n')
          f.write(f'        <color>{color}</color>\n')
          f.write('      </IconStyle>\n')
          f.write('    </Style>\n')
      # Crear cada vuelo
      for index, (airline_name, path) in enumerate(paths_with_names):
          f.write(f'    <Placemark>\n')
          f.write(f'      <name>{airline_name}</name>\n')
          f.write(f'      <styleUrl>#{airline_name}Style</styleUrl>\n')
          f.write('      <gx:Track>\n')
          f.write('        <altitudeMode>clampToGround</altitudeMode>\n')
          for i in range(len(path)):
              when = start_time + (index * timedelta(seconds=5)) + (i * time_step)
              f.write(f'        <when>{when.isoformat()}Z</when>\n')
          for point in path:
              f.write(f'        <gx:coord>{point.longitude} {point.latitude} 0</gx:coord>\n')
          f.write('      </gx:Track>\n')
          f.write('    </Placemark>\n')




      f.write('  </Document>\n')
      f.write('</kml>\n')






