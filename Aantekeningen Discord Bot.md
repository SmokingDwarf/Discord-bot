Stap 1: Initiëren, Wie is de user? (message.author)
Stap 2: Wat wil je doen?
    - Welke stat gaat de user gebruiken?
    - Is de user proficient?
Stap 3: Heb ik die informatie?
Stap 3.1: Informatie uitvragen aan user
Stap 3.2: Informatie opslaan in externe file
Stap 4: Uitvoeren activiteit
Stap 4.1: Ophalen en uitvoeren roll_functie met user_modifier
Stap 4.2: Als de user proficient is: roll_functie proficiency die


- Wat is de huidige datum?
- Wanneer hebben ze de vorige keer iets gedaan?
- Hoe lang was toen de cooldown?

Wanneer de bot informatie moet opvragen gaat hij in een "Informatie_opvragen" staat. Vanaf dat moment accepteert de bot alleen nog maar berichten die antwoord zijn op de vraag. De bot reageert op:
- Een integer die het antwoord is op de vraag. Antwoord uitschrijven en "informatie_opvragen" staat beeindigen. 
- Iets anders, geeft een foutmelding terug.
- 


https://realpython.com/python-sqlite-sqlalchemy/
https://www.programiz.com/python-programming/nested-dictionary
https://www.programiz.com/python-programming/class
https://www.programiz.com/python-programming/object-oriented-programming

Voor elke user --> Dict
    - Proficient [Smithing, potters]
    - Cooldown Boolean (True/false)

Zodra bericht binnenkomt: author vergelijken. 
 - Nieuwe speler? Data uitvragen
 - Oude speler? Data ophalen
For loop om door de list van spelers in de extere file te itereren
Nieuwe user bestaat nog niet: Voeg nieuwe user_object toe aan list in externe file

User_dict = {
    user_object_1{}
}

Userclass: 
    username = ""

Regel: Van boven naar beneden lezen

To-do lijst:
Stap 0
    functie 0: opstarten_discord
Stap 1 
    functie 1: ophalen_data: lezen van info uit een externe file en dat schrijf je weg in een globale user_dict
    functie 2: wegschrijven_data: wegschrijven van info van de globale user_dict naar de externe file.

Stap 2
    User_object binnen user_dict bouwen: Beginnen met object naam, en twee attributen. Bijv. username en user player-class. SIMPEL HOUDEN

Stap 3
    functie 3: geef mij de data van de userclass/object
        globale user_dict met username naar user object 

Stap 4
    functie 4: uitvragen van Wisdom Modifier bij Animal Handling check.
        Functie 2 aanroepen: info wegschrijven

Stap 5
    Functie 5: uitvragen van proficiency bij Animal Handling check.
        Functie 2 aanroepen: info wegschrijven
