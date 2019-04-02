#!/usr/bin/env python3

#
# Hieronder zijn de eerste 3 regels de voorgeschreven manier om de GTK module in
# je eigen programma beschikbaar te krijgen. Zie de officiële tutorial (link in
# de REAME.md file).
#

# "gi" is de overkoepelende, meta-module waar veel meer in zit dan alleen GTK.
#
import gi

# Vervolgens testen of we de bedoelde GTK versie beschikbaar hebben gekregen.
# Het kan wel zonder deze regel, maar dit zorgt voor een duidelijke error als
# je programma met de verkeerde module versie zoud worden gestart.
#
gi.require_version('Gtk', '3.0')

# Als laatste laden (importeren) we uit de overkoepelende module "gi" alleen het
# GTK-deel. Daarna kunnen we dingen uit de GTK-module gebruiken door er "Gtk."
# voor te zetten.
#
from gi.repository import Gtk

# Hier wordt een class gedefinieerd waarbij een lege Gtk.Window als basis wordt
# gebruikt. Een heel 'mechaniek' van wat een window in het X11 windows-systeem
# nodig heeft is in de Gtk.Window gecodeerd en hoeven we zelf niet te doen.
#
# Onze eigen TafelWindow erft dat allemaal over en we hoeven 'alleen maar' de
# dingen er bij in te programmeren wat we anders, of er bij willen t.o.v. een leeg
# GTK window.
#
# We definieren hier een class. Die code wordt hier nog niet uitgevoerd. Pas later
# als we een TafelWindow in het geheugen maken en aan een variabele toekennen (zie
# verderop)i, dan wordt (er iets van) de code uitgevoerd.
#
class TafelWindow(Gtk.Window):

    # "__init__()" is een functie die deel is van class, een z.g. "member function"
    # of "method".
    #
    # Speciale namen beginnen en eindigen in Python met 2 underscores. De naam
    # "__init__" is speciaal omdat die automatisch door python wordt gedraaid op
    # het moment dat een object van een class wordt aangemaakt.
    #
    def __init__(self):

        # De overgeërfde __init__() van de Gtk.Window wordt niet impliciet
        # aangeroepen (in bijv C++ gebeurt dat wel). Dat moeten we hier echter wel
        # doen, dus doen we dat hier eerst. Een titel voor in de titelbalk van het
        # window kan hier worden meegegeven.
        #
        Gtk.Window.__init__(self, title="GTK Tafel")

        # GUI onderdelen aanmaken in het geheugen:
        #   - invulvakje voor welke tafel uitgerekend moet worden
        #   - invulvakje voor het aantal sommen (de lengte van de tafel)
        #   - knop om op te klikken om de tafel uit te laten rekenen
        #   - een soort lijst waarin meerdere regels kunnen om de tafel in te laten
        #     zien (een GTK TreeView object is en beetje een overkill, maar er is niet
        #     veel anders in GTK wat er geschikt voor is)
        #
        self.invulvak_tafel = Gtk.Entry()
        self.invulvak_tot_en_met = Gtk.Entry()
        self.uitreken_knop = Gtk.Button(label="Reken uit!")
        self.tafel_output_lijst = Gtk.TreeView()

        # Zet default waarden in de invulvakjes. Want als er op de knop geklikt wordt
        # terwijl deze vakjes nog leeg zijn dan crasht het programma omdat lege strings
        # niet om te zetten zijn naar int's (zie verderop).
        #
        self.invulvak_tafel.set_text("1")
        self.invulvak_tot_en_met.set_text("4")

        # Voor de output lijst is een Gtk.TreeView gebruikt. Dit is best een ingewikkeld
        # ding dat veel kan. Hier hoeft ie alleen maar een lijst met sommen (strings)
        # te laten zijn, maar er is wat extra werk nodig.
        #
        # Ten eerste heeft hij een "model" nodig waar hij de data uithaalt die hij moet laten
        # zien. Omdat we een lijst willen (met slechts 1 kolom) maken we een ListStore en
        # hangen die aan de variabele tafel_data:
        #
        self.tafel_data = Gtk.ListStore(str)  # str geeft hier aan: 1 kolom met strings

        # En we moeten kolommen aanmaken, ook al hebben wij die eigenlijk niet nodig: wij
        # daarom maar 1 kolom.
        #
        kolom_definitie = Gtk.TreeViewColumn("Tafel", Gtk.CellRendererText(), text=0)
        self.tafel_output_lijst.append_column(kolom_definitie)

        # ... en we willen de kolom-header eigenlijk niet zien (dat gebeurt default wel):
        #
        self.tafel_output_lijst.set_headers_visible(False)

        # We koppelen het "ListStore" data-model aan de output-lijst:
        #
        self.tafel_output_lijst.set_model(self.tafel_data)

        # We moeten nog zorgen dat er wat gebeurt als er op de knop voor uitrekenen
        # geklikt wordt. We geven hier op dat onze member function ("method")
        # 'op_uitreken_knop_geklikt' uitgevoerd wordt als er op de knop 'uitreken_knop'
        # geklikt is:
        #
        self.uitreken_knop.connect("clicked", self.op_uitreken_knop_geklikt)

        # De GUI onderdelen moeten nog aan het window worden toegekend zodat ze er in
        # verschijnen. Dit gaat met een tussenstap: ze worden toegevoegd aan een onzichtbaar
        # object (een Gtk "container") dat de afmetingen en de plek binnen het window
        # van alle onderdelen regelt. En die container wordt dan op zijn beurt aan het window
        # object opgegeven als de inhoud van het window.
        #
        # Dit lijkt misschien onnodig ingewikkeld, maar zo worden ze altijd netjes onder
        # elkaar gehouden en vergroot/verkleind naar gelang het window groter/kleiner
        # wordt gemaakt. En dat gebeurt dan automatisch. Ook zorgt zo'n container ervoor
        # dat alle onderdelen een redelijk default formaat hebben en past automatisch het
        # formaat van het window zo aan dat het precies om de onderdelen past.
        #
        # De eenvoudigste container is een Gtk.Box:
        #
        gtk_tafel_box = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL,  # vertikaal: de onderdelen onder elkaar
                spacing=10                             # ruimte tussen de onderdelen 10 pixels
                )

        # De GUI onderdelen aan gtk_tafel_box toevoegen in de volgorde waarin we willen
        # dat ze van boven naar beneden in het window verschijnen.
        #
        gtk_tafel_box.add(self.invulvak_tafel)
        gtk_tafel_box.add(self.invulvak_tot_en_met)
        gtk_tafel_box.add(self.uitreken_knop)
        gtk_tafel_box.add(self.tafel_output_lijst)

        # Dan de box als enige inhoud aan het window toewijzigen:
        #
        self.add(gtk_tafel_box)

        # Window is nu klaar in het geheugen: laten zien en activeren:
        #
        self.show_all()


    # Deze method van TafelWindow wordt aangeroepen als er op de knop wordt geklikt. Dat
    # hebben we hierboven in __init__() ergens geregeld met connect().
    #
    def op_uitreken_knop_geklikt(self, button):

        # Eerst de invulvakjes uitlezen, want daarin staat wat we moeten uitrekenen.
        #
        tafel = self.invulvak_tafel.get_text()
        tot_en_met = self.invulvak_tot_en_met.get_text()

        # Let op: de variabelen tafel en tot_en_met zijn strings.
        #
        # Hieronder worden ze omgezet naar getallen (int's). Als we dat gewoon zouden
        # doen en de gebruiker typt iets in een invulvak dat niet om te zetten is
        # naar een int, dan zou het programma crashen met wat een "exception" heet.
        #
        # Een paar optie om dat te voorkomen:
        #
        #   - de invulvakjes (Gtk.Entry) overerven en dan iets toevoegen waarmee
        #     elk karakter dat er in wordt getypt gecontroleerd word: als het geen
        #     cijfer is wordt ie dan tegegehouden.
        #     Dit is best ingewikkeld, en er moet ook nog iets voor gemaakt worden
        #     Dat de Gtk.Entry nooit leeg kan zijn, want daar zou ie ook op crashen.
        #
        #   - Als er op de kop wordt geklikt eerst controleren of er cijfers in staan
        #     en de string er in niet leeg is. Als dat toch zo is, doen we gewoon
        #     net of er '0' in staat.
        #
        #   - De exception gewoon laten gebeuren, maar afvangen en '0' gebruiken.
        #
        # In plaats van net doen alsof er een '0' in stond zouden we ook kunnen
        # kiezen voor een mooi error-dialoog window. Maar we houden het hier nu
        # zo eenvoudig mogelijk en gebruiken '0'.
        #
        # Hieronder wordt de exception afgevangen. Een belangrijk concept in Python.
        #
        try:
            tafel = int(tafel)
        except ValueError:
            tafel = 0

        try:
            tot_en_met = int(tot_en_met)
        except ValueError:
            tot_en_met = 0

        # Oude data uit de GUI output-list verwijderen voordat we er nieuwe in gaan
        # zetten, anders krijgen we steeds meer tafels onder elkaar in de lijst.
        #
        self.tafel_data.clear()

        #
        # De tafel wordt som-voor-som uitgerekend. Elke som wordt in een string gezet
        # die vervolgens in de GUI output-lijst gezet wordt zodat ze te zien zijn.
        #

        # Hier wordt een for-loop gebruikt om één voor één de sommen uit te rekenen,
        # in een string te zetten en die string aan de output lijst toe te voegen.
        #
        # Opm: "range" is een built-in class van Python die opeenvolgende getallen
        # genereert. Zie: https://docs.python.org/3/library/stdtypes.html#range
        #
        for tel in range(1, tot_en_met + 1):
            uitkomst = tel * tafel     # berekening van een som

            # String maken van de hele som.
            # Dit had ook zo gekund:
            #     uitkomst = str(tel) + " x " + str(tafel) + " = " + str(tel * tafel)
            #
            som = "{} x {} = {}".format(tel, tafel, uitkomst)

            # Het ListStore datamodel verwacht dat we 1 regel per keer toevoegen
            # (append). Maar zo'n regel kan meerdere kolommen bevatten. Daarom
            # moet een regel als argument meegegeven worden in de vorm van een list.
            #
            # Voor elke kolom 1 waarde in de list. Wij hebben maar 1 kolom, en geven
            # dus een list met 1 waarde  mee: de uitgerekende som string.
            # Vandaar de rechte haken '[' en ']' hieronder: om er ee list van te
            # maken, met maar 1 element.
            #
            self.tafel_data.append([som])


####
#### Hier begint de code pas die niet ingesprongen is in een functie of class
#### definitie. De uitvoering van code van deze file begint dus hier.
####

# Ons GTK-window object aanmaken in het geheugen:
#
window = TafelWindow()

# Ervoor zorgen dat als het window gesloten wordt, dit programma dan tevens stopt.
#
window.connect("delete-event", Gtk.main_quit)

# Window actief maken
#
window.show_all()

# De GTK-mainloop opstarten.
#
# Dit is een while loop in de GTK module die wacht tot er een toets voor de window(s)
# van dit progamma is ingedrukt of met de muis is op geklikt of het window groter
# gemaakt door de gebruiker enz. ("events" genoemd). Als er zulke events zich
# voordoen wordt veel automatisch intern door GTK afgehandeld.
#
# Een event is bijvoorbeeld dat de tekst die de gebruiker in de invulvakjes typt ook
# verschijnt op het scherm in het invulvakje en dat daarin ook wat basis
# edit-mogelijkheden gewoon werken zoals backspace en pijltjestoetsen, dat het
# geselecteerd kan worden en naar het clipboard gekopiëerd enz. Voor die events
# hoeven we helemaal niets anders te doen dat GTK's GUI onderdelen gebruiken en
# aan variabelen toekennen.
#
# Maar ook automatische dingen die wij hebben voorbereid, zoals het stoppen van het
# programma als het window wordt gesloten, is zo'n event dat door de GTK-main-loop
# wordt afgehandeld, maar na slechts één regel code van onze kant.
#
# En verder natuurlijk dat onze eigen code wordt uitgevoerd als er op de knop wordt
# geklikt is ook zo'n event.
#
# Nadat gedaan is wat bij een event moet gebeuren, moet het systeem gewoon op het
# volgende event wachten. Vandaar een loop. En als die loopstopt (door Gtk.main_quit())
# doet de hele GUI niks meer.
#
# We hoeven die loop eigenlijk nooit te zien, dat is intern mechaniek van GTK en de
# desktop environment. We moeten hem echter wel zelf draaien zodra we alles hebben
# klaargezet in variabele, dus in het geheugen. Dat draaien van de main-loop
# is simpelweg:
#
Gtk.main()

# Eventuele code hier wordt pas uitgevoerd als het hele GTK-deel van ons programma
# (de main-loop dus) is gestopt. Danzij de de regel met connect("delete-event"...)
# een stukje hierboven, gebeurt dat als ons window is gesloten.
#
# Hadden we die connect(..) niet gedaan dan zou de code hieronder waarschijnlijk
# nooit uitgevoerd worden. Want dat zou het programma alleen ophouden als het wordt
# ge-kill-ed.
#
print("GTK programma geëindigd!")

