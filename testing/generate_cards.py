from card_functions import create_bingo_card

personen = [
    "Lokalhis-toriker*innen", 
    "Historische Gesellschaft", 
    "Pfarrer*innen", 
    "notgeile alte Menschen", 
    "weirde Aristokraten", 
    "lokale Eigenbröd-ler*innen", 
    "Dorfbewohner gegen.../ Villagers against ...", 
    "religiöse Fanatiker*innen", 
    "Antiquitäten-händler*innen", 
    "Dorfarzt/-ärztin", 
    "neugierige Nachbarn", 
    "hormonelle Teenager", 
    "Heiden", 
    "Pferde",
]
orte = [
    "Badgers Drift",
    "B&B",
    "Farm",
    "Herrenhaus",
    "Reiterhof",
    "Zirkus",
    "Midsomer Worthy",
    "Causton",
    "Fletchers Cross",
    "Aspen Tallow",

]

dinge = [
    "Oldtimer",
    "Kanalboote",
    "Nischenhobby (Fliegenfischen, Orchideen, ...)",
    "Geister",
    "Militär",
    "Schrotflinte",
    "Testament",
    "weirde Dorftradition",
    "Dorffeier/-event",
    "Lokalpolitik",
    "Beerdigung",
    "Jagd",
    "Familienfehde",
    "Affäre",
    "Wasser",
    "Cricket",
    "Lokalzeitung"
]

handlung_fall = [
    'Inzest',
    'Streit über Landansprüche',
    'Dorfevent bedroht durch Mord',
    'irgendetwas steht kurz vor der Insolvenz',
    'Pfarrer*in hat definitiv Dreck am Stecken',
    'Publeute haben definitiv Dreck am Stecken',
    'jemand wird erpresst',
    'Motiv: Erbe',
    'Motiv: Vertuschung vorheriger Morde',
    'Erbüberraschung',
    'jemand bekommt bedrohliche Briefe',
    'jemand hat kein Alibi',
    'reiche Menschen gar nicht so reich',
    'kaputtes Dach',
    'reiche Menschen respektieren Polizei nicht',
    'überraschende Enthüllung sexueller Orientierung',
    'Mann war nie zeugungsfähig',
    'uneheliche Kinder',
    'Totgeglaubte gar nicht tot',
    'jemand kehrt zurück ins Dorf',
    'letzte Worte à la "Was machst du denn hier?"',
    'nächstes Opfer wollte Täter*in erpressen',
    'Schuld eigen',
    'Opfer hat es irgendwie verdient',
    'niemand konnte Opfer leiden',
    'Witwe/r trauert zu 0%',
    'Mord während Telefonat',
    'jemandem wird eine Falle gestellt',
    'Mord vor dem Fernseher',
    'jemand wird eingesperrt',
    'jemand hat tatsächlich Suizid begangen',
    'die falsche Person wird umgebracht',
    'jemand überlebt einen Mordversuch',
    'alle Morde sind geplant',
    '"Unfall" war tatsächlich Mord',
    'extrem skurrile Mordmethode',
    'Showdown in der Kirche',
    'Gärtner*in ist Mörder*in',
    'Pfarrer*in ist Mörder*in',
    'Mord ist Familiensache',
    'alle sind kriminell',
    'min. 2 andere Straften ohne Bezug zum Mord',
    'jemand wird erstochen',
    'jemand wird erdrosselt',
    'jemand wird die Treppe runter geschubst',
    'Themen-Morde',
]

handlung_ermittlung = [
    'DS auf weltfalschester Fährte',
    'DS hat mit etwas recht',
    'DS macht Drecksarbeit',
    'DS flirtet mit Verdächtigen',
    'DS/DCI wird von Verdächtigen angegraben',
    'DS macht Notizen',
    'Gerichts-mediziner*in ist "lustig"',
    'Barnaby überlebt nur, weil die Autoren es so wollen',
    'Barnaby muss rennen (unfreiwillig)',
    'Durchsuchungs-beschluss optional',
    'notarielle Schweigepflicht gilt nicht für Barnaby',
    'Beweismittel-sicherung ist ein Fremdwort',
    'zufällige Lösung eines alten Falls',
    'Fall durch nebensächliches Ereignis gelöst',
    'Barnaby hat einen Heureka-Moment',
]

handlung_sonstiges = [
    'Pub während der Arbeitszeit',
    'Alkohol während der Arbeitszeit',
    'Joyce/Cully/Sarah sind aktiv beteiligt',
    'Joyce/Sarah hat ein neues Hobby = Mord',
    'freier Tag, was das?',
    'Feierabend = Alkohol',
    'Joyce kocht, Barnaby schafft es irgendwie, nichts essen zu müssen',
    'Barnaby auf Diät',
    'Cully hat ein Casting',
    'Cully hat einen neuen Job',
]

tatsachen = [
    'die Barnabys führen die einzig funktionierende Beziehung',
    'Paar mag sich, beide überleben, beide unschuldig',
    'niemand kann Auto fahren',
    'DS trägt sehr laute Krawatte',
]

meta = [
    'Mama kennt es nicht, ALLE anderen wissen wer es war',
    'Maria weiß wie alle sterben, aber nicht wers war',
    'erster Mord nach 30 Minuten',
    '3 1/2 Morde',
    'Flashback',
    'Mord-Kamera (schwarze Handschuhe, ...)',
    'Episodenende im Pub/Biergarten',
    'Szene endet vor Erklärung wichtiger Ereignisse',
    'jemand auf einem Fahrrad',
    'jemand macht nächtlichen Spaziergang',
    'offene Haustür',
    'Variation des Intros live gespielt',
    'schöne Szenerie',
    'recycelter Drehort',
    'berühmte Person',
    '100% weißer Cast',
]

meh = [
    'Familie beinahe ausgerottet',
]

terms = personen + orte + dinge + handlung_fall + handlung_ermittlung +  handlung_sonstiges + tatsachen + meta

for i in range(1,5):
    create_bingo_card(i, 5, terms)