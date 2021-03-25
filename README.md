# MVG Bildschirm

## Übersicht

2018 hat die Münchner Verkehrsgesellschaft (MVG) eine neue Schnittstelle (API) bereitgestellt, die hauptsächlich über die folhende URL abgerufen werden kann:

```
https://www.mvg.de/api/fahrinfo/
```

Laut verschiedenen Quellen benötigt man einen Schlüsse, um atomatisierte Abrufe zu authentifizieren<sup>1</sup>:

```
'X-MVG-Authorization-Key': 5af1beca494712ed38d313714d4caff6
```

## API

Die API lässt sich wie folgt abfragen:

| URL | Info |
| --- | --- |
| `https://www.mvg.de/api/fahrinfo/location/queryWeb?q={name}` | Gibt JSON-Antwort zurück, wobei `{name}` eine Haltestelle oder Bahnhof sein kann. Wenn ein leerer `str` als `{name}` gesendet wird, werden Infos zu allen Haltestellen / Bahnhöfe zurückgegeben. |
| `https://www.mvg.de/api/fahrinfo/departure/{id}?footway={offset}` | Fragt Abfahrtsinfos zu einer bestimmten Haltestelle / zu einem bestimmten Bahnhof ab. Der Wert für `{id}` für eine Haltestelle / einen Bahnhof kann über `queryWeb` erhalten werden. Der Wert `{offset}` gibt den Fußweg zur Haltestelle / zum Bahnhof in Minuten an. |
| `/location/nearby?latitude={lat}&longitude={lon}` | Findet die nächste Haltestelle / den nächsten Bahnhof zu einer Koordinate (Breitengrad: `{lat}`; Längengrad: `{lon}`). |

Zudem gibt es auch eine Schnittstelle über `https://www.mvg.de/api/fahrinfo/routing/`, wobei die folgenden `GET` Werte gesetzt werden können:

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


## Quellen

1: Github: [`leftshift/python_mvg_api`](https://github.com/leftshift/python_mvg_api/issues/2#issuecomment-334437053), Github: [`pc-coholic
/
PyMVGLive`](https://github.com/pc-coholic/PyMVGLive/issues/12#issue-375033276), Web: [core4os](https://core4os.readthedocs.io/en/latest/example/mvg.html)