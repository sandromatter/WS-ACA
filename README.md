# WS-ACA
Dieses Projekt wurde im Modul *«Web Scraping &amp; Automated Content Analysis»* an der Fachhochschule Graubünden umgesetzt.
<p align="center">
![Cover image scrapy and python](docs/scrapy_python.png?raw=true "Cover image scrapy and python")
</p>
---

## Ausgangslage 
Im Rahmen des Seminars lernen Studierende, wie man mit Web Scraping Inhalte unterschiedlicher Formate automatisiert sammeln und zu einem einheitlichen Korpus zusammenführen kann. Weiter lernen sie die möglichen Anwendungsbereiche, Herausforderungen (technische und rechtliche) sowie Limitationen kennen.

In einem zweiten Teil lernen Studierende die Aufbereitung des Analysematerials sowie verschiedene Methoden der automatisierten Inhaltsanalyse aus den Bereichen Textklassifikation und -extraktion kennen. Anhand von einschlägigen Studien werden die Methoden mit der praktischen Anwendung verzahnt. Ferner üben die Studierenden Forschungsideen zu entwickeln und zu präsentieren und diskutieren. Die Ergebnisse fassen Sie in einem Forschungsbericht sinnvoll zusammen und reflektieren sie kritisch.
Die Anwendung und der Einsatz der dazu geeigneten Tools und Frameworks erlernen die Studierenden im Rahmen dieses Projektes.

## Projektbeschrieb
Im Projekt wurde durch Sammlung von Online-Kommentaren der Moutainbike-News-Webseite «pinkbike.com» und Mountainbike-Rennergebnissen von «rootsandrain.com» evaluiert, ob ein Zusammenhang zwischen Rennergebnissen und verschiedenen Ausprägungen von Online-Kommentaren vorliegt. Das Projekt umfasst die Schritte Datensammlung, -bearbeitung und -auswertung.

### Webcrawling 
Für das Projekt wurde der High-Level Prozess in einem Diagramm abgebildet.

![Crawling process pinkbike.com.](docs/crawling-process_1.jpeg?raw=true "Diagram crawling process pinkbike.")
![Crawling process rootsandrain.com.](docs/crawling-process_2.jpeg?raw=true "Diagram crawling process rootsandrain.")

## Installation und Ausführung
Um das Projekt Pyfeed lokal starten zu können, sind verschiedene Abhängigkeiten vorausgesetzt. Die Requirements werden im Pipfile im Projektordner aufgeführt und können mit Hilfe von diesem File installiert werden. Das Projekt wurde mit dem Python packaging tool «pipenv» aufgesetzt.

```
$ cd /{{your_path_to_directory}}/ws-aca/
$ pip install pipenv
$ pipenv install
$ pipenv jupyter-notebook
```

Nach Installation und dem aufsetzten und installieren der Importpakete in der virtuellen Umgebung, kann das Projekt mit <tt>jupyter-notebook</tt> gestartet werden. Anschliessend ist dieses lokal auf <tt>http://127.0.0.1:8888/</tt> erreichbar.

Die Dependencies um das Projekt lokal zu testen befinden sich im Pipfile.

**[packages]**
<tt>scrapy</tt>
<tt>scrapy-user-agents</tt>
<tt>scrapy-proxy-pool</tt>
<tt>sqlalchemy</tt>
<tt>ipython</tt>
<tt>jupyter</tt>
<tt>notebook</tt>
<tt>pandas</tt>
<tt>nltk</tt>
<tt>fasttext</tt>
<tt>contractions</tt>
<tt>matplotlib</tt>
<tt>seaborn</tt>
