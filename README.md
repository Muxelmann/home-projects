# Heimprojekte

Der Server, der alle Heimprojekte bereitstellt, basiert auf [Flask](https://flask.palletsprojects.com/) und benutzt das Grundprojekt namens [Flocker](https://github.com/Muxelmann/mvg-screen/tree/main/src/flocker), um mehrere kleinere Projekte als alleinstehende Blueprints handzuhaben.

Momentan gibt es die folgenden Projekte - mehr Details kann im entsprechenden Blueptint eingesehen werden:

- [mvg-frame](https://github.com/Muxelmann/mvg-screen/tree/main/src/flocker/blueprints/mvg-frame), womit eine Schnittstelle betrieben wird, die Daten von der MVG abfrägt und Bilddaten für eine ESP8266 betriebene Abfahrtsanzeige bereitstellt;
- [blue](https://github.com/Muxelmann/mvg-screen/tree/main/src/flocker/blueprints/blue) und [red](https://github.com/Muxelmann/mvg-screen/tree/main/src/flocker/blueprints/red) sind quasi leere Beispielprojekte, mit denen die Funktionalität von Flocker erklärt werden soll.
