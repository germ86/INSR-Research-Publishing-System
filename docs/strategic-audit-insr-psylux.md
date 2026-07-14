# Strategisches Audit und Revisionsleitfaden des INSR-Frameworks zur Vorbereitung auf den wissenschaftlichen Dialog mit Psylux

> **Datumsklarstellung:** Der vom Briefing referenzierte Gesprächstermin ist der **13. Juli 2026**. Das Repository wurde am **14. Juli 2026** aktualisiert; relative Formulierungen wie „heute“ sollten in Präsentationsmaterialien daher durch absolute Daten ersetzt werden.

## 1. Strategische Ausgangslage

Die klinische Erforschung und Behandlung der komplexen Posttraumatischen Belastungsstörung (C-PTSD) nach ICD-11 erfordert adaptive, phasenorientierte und belastungssensible Interventionsmodelle. Das unter der früheren Bezeichnung „F.R.A.U.D.“ entwickelte Konzept wurde aus ethischen und methodischen Gründen in **Integrative Neuro-Somatic Recalibration (INSR)** umbenannt.

INSR wird als zustandsbasierte, biometrisch gestützte Entscheidungsarchitektur positioniert, die psychotherapeutische Sequenzierung mit digitalem Monitoring und perspektivisch — aber nicht in der initialen Feasibility-Phase — transkranieller Gleichstromstimulation (tDCS) verbindet.

Das strategische Ziel des Psylux-Dialogs ist nicht die sofortige Initiierung einer voll gepowerten Phase-III-Studie, sondern die Wiederherstellung epistemischen Vertrauens: Das Team muss zeigen, dass ethische, theoretische, regulatorische und biostatistische Schwächen des Altentwurfs erkannt und systematisch gehärtet wurden.

## 2. Psylux-Kritik und methodische Antwort

| Psylux-Kritikpunkt | Schwäche im Altentwurf | Erforderliche Argumentation |
| --- | --- | --- |
| Nomenklatur und Ethik | Das Akronym „F.R.A.U.D.“ kann bei C-PTSD-Patient:innen stigmatisierend, retraumatisierend und nocebo-fördernd wirken. | Die Umbenennung in **Integrative Neuro-Somatic Recalibration (INSR)** ist als fundamentaler ethischer Korrekturakt im Sinne von Non-Malefizienz und Helsinki-Prinzipien zu präsentieren. |
| KI-Autorenschaft | Generative KI wurde offenbar missverständlich als Co-Autorenschaft dargestellt. | Menschliche Autorenschaft, Verantwortlichkeit und Datenhoheit müssen strikt nach ICMJE- und COPE-Logik verbleiben; KI ist nur redaktionelle und organisatorische Assistenz. |
| Operationalisierung | Gating-Kriterien, physiologische Schwellen und Hard-Stops waren zu vage. | Multimodale Datenfusion aus HRV/RMSSD, EDA, Atmung, subjektiven Ratings und klinischer Beobachtung; Artefaktkontrolle und klinische Hard-Stops explizit benennen. |
| Digitaler Layer | Unklare KI-Rolle erzeugt das Risiko einer Eskalation zum autonomen Hochrisiko-Medizinprodukt. | Das System als **Clinical Decision Support System (CDSS) gemäß EU MDR Rule 11** mit strikt assistiver **Human-in-the-Loop**-Architektur deklarieren. |
| tDCS-Maturität | 2-mA-tDCS ohne robuste Verblindungsarchitektur erzeugt Performance-, Allegiance- und Entblindungsrisiken. | tDCS aus der initialen Feasibility-Studie herausnehmen; für spätere Phasen ein **Dual-Clinician Blinding Model** vorsehen. |

## 3. Folienspezifischer Revisionsleitfaden

### 3.1 Folien 2 und 11: Digitaler Implementierungslayer

Die Folien sollten den digitalen Layer nicht nur als „Decision Support“ beschreiben, sondern regulatorisch präzise als **Clinical Decision Support System (CDSS) gemäß EU MDR Rule 11 (Human-in-the-Loop)** einordnen.

Empfohlene Kernbotschaften:

- Der Algorithmus gibt Empfehlungen, aber keine autonome Therapieentscheidung.
- Die klinische Letztverantwortung verbleibt jederzeit beim behandelnden Menschen.
- Während der prospektiven Untersuchung ist das System nicht selbstlernend.
- Schwellenwertänderungen erfolgen nicht im Live-Betrieb, sondern zwischen Studienphasen über einen vordefinierten Change-Control-Prozess.
- Bei internationaler Weiterentwicklung sollte eine PCCP-ähnliche Logik („Predetermined Change Control Plan“) als regulatorische Leitplanke erwähnt werden.

### 3.2 Folie 7: Theoretische Verortung

Folie 7 ist der neurobiologische Anker der Präsentation. Die theoretische Verortung sollte konsequent vom umstrittenen polyvagalen Narrativ auf das **Neurovisceral Integration Model (NIM)** und das **Central Autonomic Network (CAN)** verschoben werden.

Empfohlene Sprecherlinie:

> INSR stützt biometrisches Gating nicht auf metaphorische oder evolutionär umstrittene Konstrukte, sondern auf das Neurovisceral Integration Model: Präfrontale Regulationskapazität, Amygdala-Inhibition und vagaler Ausfluss werden als funktionelles Netzwerk verstanden, dessen Dynamik über HRV/RMSSD näherungsweise operationalisiert werden kann.

Diese Umstellung schützt das Framework vor akademischer Kritik an polyvagalen Überdehnungen und stärkt die Anschlussfähigkeit an affektive Neurowissenschaften und Präzisionspsychiatrie.

### 3.3 Folien 8 und 9: State Detection und Operationalisierung

Die Folien sollten die größte biostatistische Schwäche ambulatorischer HRV-Messung offen adressieren: **RMSSD ist respiratorisch konfundierbar**. Sprechen, Weinen, Atemanhalten oder Hyperventilation können die respiratorische Sinusarrhythmie verändern und damit false positives im State-Gating erzeugen.

Pflicht-Ergänzung für Folie 8:

- **Multivariable Artefaktunterdrückung und RSA-Kontrolle**.

Empfohlene Operationalisierung für Folie 9:

- Keine starren universellen Normwerte.
- Individuelle Baselines pro Patient:in und Sitzung.
- Relative Schwellenlogik, etwa abrupter RMSSD-Abfall gegenüber Tages-Baseline plus synchroner EDA-Anstieg.
- Signalqualitätsprüfung vor jeder algorithmischen Empfehlung.
- Klinische Hard-Stops bei Dissoziation, Suizidalität, Panikeskalation oder therapeutischer Inkohärenz.

Als klinische Rationale kann der **Twice-Exceptional-(2e)-Phänotyp** genutzt werden: Hochintelligente und neurodivergente Patient:innen können affektive Dysregulation verbal und kognitiv überdecken. Bottom-up-Gating verhindert, dass verbale Kohärenz fälschlich als autonome Stabilität interpretiert wird.

### 3.4 Folie 10: Therapeutische Sequenzierung und Avoidance-Policy-Risiko

Die Modulzuordnung — Stabilisierung, EMDR/AIP, MBT und parts-informierte Schamreduktion ohne Reifizierung von „Anteilen“ — ist plausibel, muss aber algorithmisch abgesichert werden.

Zentrale Warnung:

> Ein naiver Algorithmus, der akuten Distress sofort bestraft, kann Exposition dauerhaft blockieren und eine algorithmische Vermeidungsstrategie erzeugen.

Deshalb sollte die Entscheidungslogik nicht-monotone und verzögerte Outcome-Funktionen nutzen: Kurzfristiger Distress darf toleriert werden, wenn Signalqualität, therapeutischer Kontext, Rückkehrfähigkeit und mittelfristige Extinktionsindikatoren stimmen.

### 3.5 Folien 12 und 14: Endpunkt-Architektur

Eine reine CAPS-5-Logik ist für ICD-11-C-PTSD unzureichend, weil sie DSO-Dimensionen nur begrenzt erfasst. Für spätere Wirksamkeitsstudien sollte daher eine duale Endpunktstrategie skizziert werden.

| Endpunktstrategie | Messinstrument | Rationale | Fokus |
| --- | --- | --- | --- |
| Co-Primär 1 | CAPS-5 Total Score | PTSD-Kernsymptome und historische Vergleichbarkeit | DSM-5 / internationale Vergleichbarkeit |
| Co-Primär 2 | ITQ DSO Score | Affektdysregulation, negatives Selbstbild und interpersonelle Störungen | ICD-11-C-PTSD-Komplexität |
| Sekundär explorativ | Allostatic Load Index | Somatische Rekalibrierung und physiologische Belastungsreduktion | Whole-Person-Recovery |
| Ökonomisch / HTA | WHODAS 2.0, EQ-5D-5L | Funktionsniveau, QALYs und patientenrelevanter Zusatznutzen | G-BA / IQWiG / AMNOG-Anschlussfähigkeit |

### 3.6 Folie 15: tDCS-Deferral und Blinding-Dilemma

Die tDCS-Komponente sollte ausdrücklich als spätere, methodisch kontrollierte Erweiterung behandelt werden. Für die initiale Psylux-Phase ist der Verzicht ein Zeichen biostatistischer Disziplin, nicht Schwäche.

Für spätere Phasen sollte die Folie das **Dual-Clinician Blinding Model** nennen:

1. Eine technisch geschulte Person appliziert active oder sham tDCS.
2. Diese Person ist nicht identisch mit der psychotherapeutisch behandelnden Person.
3. Sichtbare Entblindungshinweise wie Erytheme werden kontrolliert oder maskiert.
4. Die behandelnde Person beginnt die Sitzung erst nach Abschluss der Applikationslogistik und bleibt gegenüber active/sham strikt verblindet.

### 3.7 Folie 17: Redaktionelle Verantwortung und KI-Nutzung

Die Folie sollte klarstellen:

- Keine KI-Autorenschaft.
- Keine Delegation wissenschaftlicher Verantwortung an generative KI.
- Vollständige menschliche Verantwortung für Hypothesen, Studiendesign, Dateninterpretation, klinische Sicherheit und finale Manuskriptfassung.
- KI-Nutzung nur als deklarierte Assistenz für Strukturierung, Sprachglättung, Literaturorganisation oder redaktionelle Vorbereitung.

## 4. Biostatistische Diskussionspunkte für Expert:innen

Für ein wissenschaftlich anspruchsvolles Gespräch können folgende Punkte als hypothesengenerierende, vorsichtig formulierte Diskussionsachsen genutzt werden:

- **Therapist-Clustering-Reduktion:** Standardisiertes Gating kann Behandler-Varianz reduzieren und damit statistische Power erhöhen.
- **Biologische Frühindikatoren:** HRV, EDA, Haarkortisol oder allostatische Marker könnten psychometrischen Verbesserungen zeitlich vorauslaufen.
- **Nicht-lineare Phasenübergänge:** Adaptive, zustandsbasierte Sequenzierung könnte abrupte State-Switches statt linearer Symptomverläufe erzeugen.
- **Follow-up-Dynamik:** Stabil erworbene Regulationsfähigkeit könnte nach Therapieende eine weitere funktionelle Verbesserung unterstützen.

Diese Punkte sollten nicht als gesicherte Effekte behauptet werden, sondern als präregistrierbare Analysehypothesen für spätere RCTs.

## 5. Datenschutz und internationale Kooperation

Für ein binationales Deutschland-USA-Design ist eine einfache Übertragung pseudonymisierter Gesundheitsdaten rechtlich riskant. Empfohlen wird eine **Trusted Research Environment (TRE)**- beziehungsweise **Secure Compute Enclave**-Architektur.

Kernprinzipien:

- Europäische Patientendaten verbleiben physisch auf europäischen Servern.
- Externe Forschungspartner erhalten nur kontrollierten Remote-Zugriff.
- Rohdaten werden nicht exportiert.
- Analysen, Audit-Trails, Rollenrechte und Re-Identifikationsschutz werden zentral kontrolliert.
- Standardvertragsklauseln werden durch technische und organisatorische Zusatzmaßnahmen flankiert.

## 6. Taktische Gesprächsempfehlungen

1. **Ethische Bereinigung proaktiv voranstellen:** Umbenennung in INSR und menschliche Autorenschaft in den ersten Minuten klären.
2. **Verzicht auf tDCS als Stärke verkaufen:** Die initiale Studie soll den State-Detection-Layer kalibrieren, nicht mehrere experimentelle Variablen gleichzeitig vermischen.
3. **2e-Rationale nutzen:** Bottom-up-Gating als Antwort auf Intellektualisierung und affektive Maskierung darstellen.
4. **Kooperationsmodell B priorisieren:** Passive Kalibration im Shadow Mode während regulärer Psylux-Sitzungen minimiert Risiko und generiert Schwellenwertdaten.
5. **Claims disziplinieren:** Starke Zukunftshypothesen nur als Hypothesen, nicht als belegte Wirksamkeitsversprechen formulieren.

## 7. Minimaler Foliensatz-Patch

Falls nur kurze Textänderungen möglich sind, sollten mindestens folgende Begriffe ergänzt werden:

- Folie 2: „CDSS gemäß EU MDR Rule 11; Human-in-the-Loop; keine autonome Therapieentscheidung“.
- Folie 7: „Neurovisceral Integration Model / Central Autonomic Network statt Polyvagal-Theorie“.
- Folie 8: „Multivariable Artefaktunterdrückung und RSA-Kontrolle“.
- Folie 9: „Individuelle Baselines, relative Schwellen, Signalqualitätsprüfung, klinische Hard-Stops“.
- Folie 14: „ITQ DSO Score als Co-Primary Endpoint für ICD-11-C-PTSD“.
- Folie 15: „tDCS deferred; Dual-Clinician Blinding Model für spätere Phasen“.
- Folie 17: „Keine KI-Autorenschaft; ICMJE-/COPE-konforme menschliche Verantwortung“.
