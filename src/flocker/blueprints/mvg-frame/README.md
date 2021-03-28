# MVG Bildschirm

## Übersicht

2018 hat die Münchner Verkehrsgesellschaft (MVG) eine neue Schnittstelle (API) bereitgestellt, die hauptsächlich über die folgende URL abgerufen werden kann:

```
https://www.mvg.de/api/fahrinfo/
```

Laut verschiedenen Quellen benötigt man einen Schlüsse, um automatisierte Abrufe zu authentifizieren<sup>1</sup>:

```
'X-MVG-Authorization-Key': 5af1beca494712ed38d313714d4caff6
```

Über diese Schnittstelle lassen sich auch die Abfahrtszeiten der Busse, U-Bahnen, S-Bahnen und Trams für eine Haltestelle / einen Bahnhof abrufen. Dieses Projekt stellt einen Server für den eInk Bildschirm bereit und bildet dadurch ein Relais, das:

1. die Abfahrtsdaten über die MVG-Schnittstelle abruft,
2. ein Bild mit den nächsten 7 Abfahrten anzeigt,
3. die Pixeldaten des Bildes in ein für den eInk Bildschirm kompatibles Format konvertiert, und
4. die konvertierten Pixeldaten häppchenweise an den eInk Bildschirm überträgt - der Buffer im ESP8266 ist sehr beschränkt.

## MVG Schnittstelle (API)

Die Schnittstelle lässt sich wie folgt abfragen:

| URL | Info |
| --- | --- |
| `https://www.mvg.de/api/fahrinfo/location/queryWeb?q={name}` | Gibt JSON-Antwort zurück, wobei `{name}` eine Haltestelle oder Bahnhof sein kann. Wenn ein leerer `str` als `{name}` gesendet wird, werden Infos zu allen Haltestellen / Bahnhöfe zurückgegeben. |
| `https://www.mvg.de/api/fahrinfo/departure/{id}?footway={offset}` | Fragt Abfahrtsinfos zu einer bestimmten Haltestelle / zu einem bestimmten Bahnhof ab. Der Wert für `{id}` für eine Haltestelle / einen Bahnhof kann über `queryWeb` erhalten werden. Der Wert `{offset}` gibt den Fußweg zur Haltestelle / zum Bahnhof in Minuten an. |
| `/location/nearby?latitude={lat}&longitude={lon}` | Findet die nächste Haltestelle / den nächsten Bahnhof zu einer Koordinate (Breitengrad: `{lat}`; Längengrad: `{lon}`). |

Diese Funktionen werden auch vom Server genutzt. Zudem gibt es auch eine Schnittstelle über `https://www.mvg.de/api/fahrinfo/routing/`, wobei die folgenden `GET` Werte gesetzt werden können - die wird aber nur der Vollständigkeit hier aufgelistet und nicht vom Server genutzt:

| Argument | Wert | Info |
| --- | --- | --- |
| `fromLatitude` | `float` | Breitengrad von dem aus die Verbindung berechnet werden soll. |
| `fromLongitude ` | `float` | Längengrad von dem aus die Verbindung berechnet werden soll. |
| `fromStation ` | `str` | ID der Haltestelle / des Bahnhofs von der / von dem aus die Verbindung berechnet werden soll. |
| `toLatitude ` | `float` | Breitengrad zu dem die Verbindung berechnet werden soll. |
| `toLongitude ` | `float` | Längengrad zu dem die Verbindung berechnet werden soll. |
| `toStation ` | `str` | ID der Haltestelle / des Bahnhofs zu der / zu dem die Verbindung berechnet werden soll. |
| `time ` | `str` | Abfahrts- / Ankunftszeit. |
| `arrival` | `bool` | Bestimmt ob es sich bei `time` um die Abfahrts- oder Ankunftszeit handelt (z.B. `arrival=true`). || `arrival` | `bool` | Bestimmt ob es sich bei `time` um die Abfahrts- oder Ankunftszeit handelt (z.B. `arrival=true`). |
| `maxTravelTimeFootwayToStation ` | `int` | Maximale Minutenanzahl zur Haltestelle / zum Bahnhof vom Abfahrtspunkt. |
| `maxTravelTimeFootwayToDestination ` | `int` | Maximale Minutenanzahl zum Abfahrtspunkt von der Haltestelle / vom Bahnhof. |
| `changeLimit ` | `int` | Maximale Anzahl der Umstiege. |
| `transportTypeUnderground ` | `bool` | Lässt U-Bahnen bei der Suche außer Acht. |
| `transportTypeBus ` | `bool ` | Lässt Busse bei der Suche außer Acht. |
| `transportTypeTram ` | `bool ` | Lässt Trambahnen bei der Suche außer Acht. |
| `transportTypeSBahn ` | `bool ` | Lässt S-Bahnen bei der Suche außer Acht. |

## Konvertierung für eInk Bildschirm

Das ESP8266 kann nur eine begrenze HTTP-Antwort mit Bilddaten erhalten. Da nur 3 Farben (Schwarz, Weiß und Rot/Gelb) übertragen werden können, habe ich beschlossen, jedes Pixel mit 2 Bit zu kodieren (also "2bpp"):

| Farbe | ursprünglicher Wert (24bpp) | konvertierter Wert (2bpp) |
| --- | --- | --- |
| Schwarz | `0x000000` | `0b00` |
| Rot / Gelb | `0x010101` bis `0xfefefe` | `0b01` |
| Rot / Gelb | `0x010101` bis `0xfefefe` | `0b10` |
| Weiß | `0xffffff` | `0b00` |

Die Reihe von 2 Bit (z.B. `"00110000110000111100..."`) wird dann nicht als solche übertragen (jedes Bit würde ja als ASCII bzw. UTF-8 Symbol übertragen und ein Byte benötigen) sondern in HEX umgewandelt (z.B. `0x30c3c...`). Die Umwandlung eines `str` mit Bits in ein `str` mit HEX-Werten geschieht in Python sehr einfach:

```
'{:02x}'.format(int(data, base=2))
```

Das Ergebnis kann dann an den Bildschirm übertragen werden.

### Warum keine Rohdaten?

Ich hatte überlegt, ein 1bpp Bitmap zu übertragen. Jedoch scheint der ESP8266 bei `NULL` also `0x00` bzw. `0b00000000` das Ende der Nachricht zu erkennen anstatt (richtig) 8 aufeinanderfolgende schwarze Pixel zu erkennen. Da auch die Längenangabe des Inhalts der Nachricht (`Content-Length` im HTTP Header) ignoriert zu werden scheint, habe ich die Alternative mit HEX-Werten implementiert.

## Quellen

1: Github: [`leftshift/python_mvg_api`](https://github.com/leftshift/python_mvg_api/issues/2#issuecomment-334437053), Github: [`pc-coholic
/
PyMVGLive`](https://github.com/pc-coholic/PyMVGLive/issues/12#issue-375033276), Web: [core4os](https://core4os.readthedocs.io/en/latest/example/mvg.html)