---
layout: default
title: Individual Contribution & Conclusion  
nav_order: 5
---
# Data Model & Technical Implementation

## 4.1 Struktur und Beziehungen der Daten: 

Das Datenmodell von Redlist beinhaltet mehrere zentrale Entitäten, die miteinander verknüpft sind. Die bedeutendsten Entitäten sind: 



Nutzer: 
Beinhaltet Daten wie  Nutzername und Passwort (passwort, verschlüsselt mit bcrypt). 

Filme: 
Filme werden anhand von Attributen wie Titel, Laufzeit, Bewertung, release datum, Genre und Filmposter gespeichert. 

Matches: 
Wenn zwei Nutzer denselben Film mit einem „Gefällt mir“-Daumen markieren, entsteht ein Match, das in einer entsprechenden Beziehungstabelle abgelegt wird. 

Gruppen: 
Eine Gruppe entsteht, wenn mehrere Nutzer denselben Film mögen. Innerhalb einer Gruppe können Nutzer zusätzliche Mitglieder einladen, um einen Filmabend zu planen.

## 4.2 Technische Implementierung: 
Die Umsetzung aus technischer Sicht erfolgt unter Verwendung einer Kombination zeitgemäßer Webtechnologien und Frameworks: 

Flask (Version 3.1.0): 
Ein leichtgewichtiges Web-Framework für Python, auf dem die Webanwendung basiert. 

Flask-SQLAlchemy (Version 3.1.1): 
Diese Erweiterung bietet die Möglichkeit, eine SQL-Datenbank (hier SQLite) zu nutzen, um Nutzer- und Filmdaten zu speichern und abzurufen. 

SQLAlchemy (Version 2.0.37): 
Ein SQL-Toolkit für Python, das zusammen mit Flask-SQLAlchemy verwendet wird, um Datenbankoperationen auszuführen. 

Flask-Bcrypt (Version 1.0.1): 
Diese Bibliothek nutzt Bcrypt, ein sicheres Hash-Verfahren, um die Passwörter der Nutzer sicher zu speichern. 

Flask-Login (Version 0.6.3): 
Diese Erweiterung bietet die Möglichkeit, Benutzer-Sessions zu verwalten und gewährleistet eine sichere Anmeldung sowie Authentifizierung der Nutzer.
 WTForms (3.2.1) und Flask-WTF (1.2.2):
 Diese Libraries unterstützen bei der Erstellung von Formularen für die Nutzeranmeldung und -registrierung. 

TMDB-API: 
Für den Abruf aktueller Filmdaten wie Titel, Genre und Bewertung wird die TMDB (The Movie Database)-API verwendet. In Echtzeit liefert sie Informationen über Filme. 

SQLite:
 Die Daten werden in einer lokal gespeicherten SQLite-Datenbank abgelegt, die eine leichtgewichtige Lösung zur Datenspeicherung darstellt. 


Darüber hinaus kommen für die Kommunikation und das Routing im Backend HTTP-Anfragen zum Einsatz, die mit Hilfe von Flask und der Werkzeug-Bibliothek bearbeitet werden. Diese Architektur gewährleistet eine schnelle, effiziente und skalierbare Lösung, die den Nutzern eine einfache und sichere Nutzung der Plattform ermöglicht.

