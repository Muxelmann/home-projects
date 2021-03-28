# Flocker

Flocker ist ein Wortspiel aus "[Flask](http://flask.palletsprojects.com)" und "[Docker](https://www.docker.com)", obwohl nur das Konzept und nicht die eigentliche Funktionalität der zwei Tools zusammengeführt wird.

## Motivation

Flask stellt eine starre Ordnerstruktur bereit, auf die mit Helferfunktionen (z.B. mittels `url_for()` oder `render_template()`) zugegriffen werden kann. Prinzipiell sieht ein minimales Flask-Projekt wie folgt aus:

```
flask/
├── flask/
│   ├── __init__.py
│   ├── static
│   │   └── style.css
│   ├── templates
│   │   └── base.html.j2
│   └── blueprints
├── instance
├── launch.py
└── launch.wsgi -> launch.py
```

Die vorstehenden Dateien / Ordner haben dabei die folgende Funktion:

| Ordner | Funktion |
| --- | --- |
| `/flask/flask/__init__.py` | Erstellt eine Instanz von Flask (z.B. über `create_app()`) |
| `/flask/flask/static` | Enthält alle statischen abrufbaren Dateien für den Server (z.B. die Datei `style.css`, die als solche abrufbar sein soll) |
| `/flask/flask/templates` | Enthält Jinja2-Dateien, mit denen der HTML-Code der Webseite erzeugt werden soll (z.B. `base.html.j2`, wo die `style.css` Datei über `{% url_for('static', filename='style.css') %}` eingebunden wird) |
| `/flask/flask/blueprints` | Enthält Erweiterungen für die Instanz von Flask (z.B. wenn nicht nur die Index Seite `/` sondern auch `/api/` mit vielen Funktionen bereitgestellt werden soll) |
| `/flask/instance` | Ein Ordner, in dem dynamische Daten beim Betrieb des Servers abgelegt werden können (der Pfad wird über `app.instance_path` bzw. `current_app.instance_path` erhalten) |
| `/flask/launch.py` | Startet den Server (`args` können hier zum Debuggen steuern, wie der Server gestartet werden soll) |
| `/flask/flask/launch.wsgi` | Ist ein symbolischer Verweis auf `launch.py`, sodass das WSGI ([Web Server Gateway Interface](https://de.wikipedia.org/wiki/Web_Server_Gateway_Interface)) gestartet werden kann (ist aber optional) |

Möchte man nun einen Blueprint hinzufügen, und dadurch mehr Funktionen bereitstellen, müssen auch Dateien außerhalb des Blueprints abgelegt werden. Denn ein "alleinstehendes" Blueprint würde nicht funktionieren:

```
flask/
├── flask/
│   ├── ...
│   └── blueprints
│       └── api
│           ├── static
│           │   └── style.css
│           └── templates
│               └── base.html.j2
└── ...
```

Im Ordner `/flask/flask/blueprints/api` wurde nun ein beispielhaftes Blueprint erzeugt. Möchte man dieses Blueprint wie ein eigenständiges Projekt nutzen, und auch die Ordner `static` und `templates` der Ordnung halber im Blueprint belassen, kann Flask nicht auf den Inhalt dieser Ordner zugreifen. Sie müssen vielmehr als Unterordner in den Ordnern `/flask/flask/static` und `/flask/flask/templates` abgelegt werden, wodurch auf sie über `url_for('static', filename='...')` verwiesen und zugegriffen werden kann.

Wie kann also jedes Blueprint als separates Projekt behandelt und in Flask problemlos eingebunden werden?

## Lösung

Flocker erkennt, ob Blueprints vorliegen und erzeugt symbolische Verweise in den Ordnern `/flask/flask/static` und `/flask/flask/templates`. Diese Verweise erzeugen eine Ordnerstruktur, die mit Flask kompatibel ist, aber nicht voraussetzt, dass die Ordner `static` und `templates` des Blueprints außerhalb des Blueprints angelegt werden müssen.

Beim vorstehenden Beispiel sieht dann die Ordnerstruktur wie folgt aus:

```
flask/
├── flask/
│   ├── __init__.py
│   ├── static
│   │   ├── style.css
│   │   └── api -> /flask/flask/blueprints/api/static
│   ├── templates
│   │   ├── base.html.j2
│   │   └── templates -> /flask/flask/blueprints/api/templates
│   └── blueprints
│       └── api
│           ├── static
│           │   └── style.css
│           └── templates
│               └── base.html.j2
├── instance
├── launch.py
└── launch.wsgi -> launch.py
```

Somit kann die Hauptseite über `url_for('static', filename='style.css')` auf ihren Stil zugreifen und der Blueprint über `url_for('static', filename='api/style.css')` seinen Stil zugreifen.

Flocker ist so konzipiert, dass beim Neustart des Flask-Servers geprüft wird, ob Blueprints hinzugefügt, entfernt oder umbenannt wurden. Dementsprechend werden die symbolischen Verweise erzeugt und gelöscht, sodass nach Start des Flask-Servers die Helferfunktionen wie `url_for()` und `render_template()` reibungslos funktionieren, obwohl alle für das Blueprint relevanten Dateien im Ordner des Blueprint verbleiben.