**Hochschule für Wirtschaft und Recht Berlin**

**Kurs: Wi-Inf-M09-F02 Full-Stack Web Development 2024/2025**

**Dozent: Herr Prof. Dr. Alexander Eck**


# **webapp.Redlist**
Die Website Redlist ermöglicht es den Nutzern, innerhalb von Sekunden Filme auszuwählen, die ihnen gefallen. Diese Filme kann man entweder gemeinsam mit neuen Freunden oder mit Menschen, die man bereits kennt, anschauen.

# RedList

Mitglieder: 

Wladimir Evdokimov: 77211970281

Samed Sevinc: 77211971390



## Präsentation
[Präsentation](https://github.com/Rotweinpirat257/webapp.Redlist/blob/main/docs/RedList.pdf)


## **Eidesstattliche Erklärung**

Die genannten Teammitglieder erklären an Eides statt:

Diese Arbeit wurde selbständig und eigenhändig erstellt. Die den benutzten Quellen wörtlich oder inhaltlich entnommenen Stellen sind als solche kenntlich gemacht. Diese Erklärung gilt für jeglichen Inhalt und umfasst sowohl diese Dokumentation als auch den als Projektergebnis eingereichten Quellcode.


## Getting started 
Hier finden Sie die einzelnen Schritte, wie Sie Redlist zum laufen bringen.

## 1. GitHub Repository klonen
###  Clone Repo
1. Besuchen Sie das GitHub-Repository von Redlist [https://github.com/Rotweinpirat257/webapp.Redlist].
2. Kopieren Sie die HTTPS-URL über den „Code“-Button.
3. Öffnen Sie das Terminal und navigieren zum gewünschten Speicherort.
4. Klonen Sie das Repository: 

### Clone repo

```bash

git clone {https://github.com/Rotweinpirat257/webapp.Redlist]
```
5.  Gehen Sie in das geklonte Repository:
   
cd Redlist
## 2. Virtuelle Umgebung einrichten


###  Create venv:

```bash

python -m venv venv 
source venv/bin/activate


```
##  3. Abhängigkeiten installieren
1. Stelle Sie sicher, dass die neueste Version von pip installiert ist:
```bash
pip install --upgrade pip
```
### Install requierements:


```bash

pip install -r requirements.txt


```
## 4. Datenbank Initialisieren
### Initialized Database 


In Terminal
```bash
Flask init-db

```

## 5. Projekt starten
1. Stelle Sie sicher, dass die virtuelle Umgebung aktiv ist.
2. Starte Sie die Anwendung: 
### Run Redlist

```bash

flask run

```
3. Öffnen Sie http://127.0.0.1:5000/ im Webbrowser, um Redlist zu testen.
