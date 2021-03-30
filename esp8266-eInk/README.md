# eInk Anzeige mit ESP8266

## Komponenten

Die Anzeige besteht aus den folgenden Komponenten:

- 7,5" eInk Anzeige ([Shop](https://www.waveshare.com/7.5inch-e-paper-hat.htm) - [Wiki](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT))
- ESP8266 Board ([Shop](https://www.waveshare.com/product/displays/e-paper-esp8266-driver-board.htm), [Wiki](https://www.waveshare.com/product/displays/e-paper-esp8266-driver-board.htm))
- RIBBA Bilderrahmen von IKEA ([Shop](https://www.ikea.com/de/de/p/ribba-rahmen-weiss-50378410/))
- Pappe zum Ausrichten und Fixieren der Anzeige im Bilderrahmen

## Funktion

Das ESP8266 verbindet sich mit dem WLAN und kommuniziert mit dem Zwischenserver (siehe [mvg-frame](https://github.com/Muxelmann/mvg-screen/tree/main/src/flocker/blueprints/mvg-frame)) um ein Bild der aktuellsten Abfahrtszeiten zu laden und anzuzeigen.

Hierbei wird eine Schleife mit den folgenden Schritten wiederholt ausgeführt:

1. sende eine Aktualisierungsanfrage an den Zwischenserver;
2. lade kodierte Bilddaten für ein Segment des Bildes (da der Empfangs-Buffer des ESP8266 zu klein für das ganze Bild ist);
3. dekodiere und übertrage die Bilddaten an die Anzeige;
4. wiederhole Schritte 2 und 3 bis das vollständige Bild (also alle Segmente) geladen wurden;
5. weise die Anzeige an, das übertragene Bild anzuzeigen; und
6. frage die Wartezeit ab, nach der die Schleife wiederholt werden soll und warte dementsprechend lange.

Die Schnittstelle des Zwischenservers reagiert für diese Schritte gemäß den folgenden Anfragen:

### `mvg-frame/update/<mac_address>`

Sendet eine an die MAC-Adresse des ESP8266 geknüpfte Aktualisierungsanfrage an den Zwischenserver - es muss also `<mac_address>` durch die MAC-Adresse des ESP8266 ersetzt werden. Der Zwischenservert kann dann:

- auf neue (also noch nicht registrierte) Anzeigen reagieren,
- die neusten Abfahrtszeiten über die Schnittstelle der MVG abfragen, und
- das anzuzeigende Bild erzeugen und speichern.

Als Antwort wird dann eine `0` (nicht i.O.) oder eine `1` (alles i.O.) zurückgegeben.

### `mvg-frame/imageData/<mac_address>?segCount=<X>&seg=<Y>`

Sendet eine an die MAC-Adresse des ESP8266 geknüpfte Bilddatenabfrage an den Zwischenserver. Die Bilddaten werden in Segmente (bzw. horizontale Abschnitte) des Bildes unterteilt. Die Anzahl der Segmenten wird durch `<X>` angezeigt, und für welches Segment Daten übertragen werden sollen, wird durch `<Y>` angezeigt.

Die empfangenen Bilddaten sind Zeichenketten, wobei jedes Zeichen als HEX-Wert interpretiert wird und Daten für jeweils zwei Pixel angibt. Daraus ergibt sich:

| Zeichen | Binärwert | Pixel[0] | Pixel[1] |
| --- | --- | --- | --- |
| `0` | `0b0000` | `0b00` (schwarz) | `0b00` (schwarz) |
| `1` | `0b0001` | `0b00` (schwarz) | `0b01` (farbig) |
| `2` | `0b0010` | `0b00` (schwarz) | `0b10` (farbig) |
| `3` | `0b0011` | `0b00` (schwarz) | `0b11` (weiß) |
| `4` | `0b0100` | `0b01` (farbig) | `0b00` (schwarz) |
| `5` | `0b0101` | `0b01` (farbig) | `0b01` (farbig) |
| `6` | `0b0110` | `0b01` (farbig) | `0b10` (farbig) |
| `7` | `0b0111` | `0b01` (farbig) | `0b11` (weiß) |
| `8` | `0b1000` | `0b10` (farbig) | `0b00` (schwarz) |
| `9` | `0b1001` | `0b10` (farbig) | `0b01` (farbig) |
| `a` | `0b1010` | `0b10` (farbig) | `0b10` (farbig) |
| `b` | `0b1011` | `0b10` (farbig) | `0b11` (weiß) |
| `c` | `0b1100` | `0b11` (weiß) | `0b00` (schwarz) |
| `d` | `0b1101` | `0b11` (weiß) | `0b01` (farbig) |
| `e` | `0b1110` | `0b11` (weiß) | `0b10` (farbig) |
| `f` | `0b1111` | `0b11` (weiß) | `0b11` (weiß) |

### `mvg-frame/delayTime/<mac_address>`

Sendet eine an die MAC-Adresse des ESP8266 geknüpfte Wartezeitabfrage an den Zwischenserver. Die Wartezeit ist in `ms` und gibt an, wie lange der ESP8266  bzw. wie lange die Anzeige in den Ruhezustand versetzt werden soll, bevor die vorstehende Schleife von Anfang an ausgeführt wird.

Dadurch wird vermieden, dass unnötig viele Anfragen an den Zwischenserver und MVG gesendet werden, und dass die Anzeigen sich unnötig oft aktualisieren. Die eInk Anzeigen blinken nämlich bei jeder Aktualisierung des Bildinhalts auf, wodurch die Abfahrtszeiten nicht so leicht zu erkennen sind.

Eine Wartezeit von mindestens 30 Sekunden scheint zweckdienlich zu sein, da die Anzeigen mehrere Sekunden zum Herunterladen der Bilddaten und (insbesondere die farbfähigen Anzeigen) zum Aktualisieren des Bildinhalts brauchen. Somit werden ungefähr einmal pro Minute die Abfahrtszeiten aktualisiert.