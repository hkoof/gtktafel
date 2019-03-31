#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class TafelWindow(Gtk.Window):

    def __init__(self):
        # Een titel voor in de titelbalk van het window op het scherm
        # wordt hier meegegeven.
        #
        Gtk.Window.__init__(self, title="GTK Tafel")

        # GUI onderdelen aanmaken in het geheugen:
        #   - invulvakje voor welke tafel uitgerekend moet worden
        #   - invulvakje voor het aantal sommen (de lengte van de tafel)
        #   - knop om op te klikken om de tafel uit te laten rekenen
        #   - een lijst dinges om de tafel in te laten zien (GTK ListView)
        #
        self.invulvak_tafel = Gtk.Entry()
        self.invulvak_tot_en_met = Gtk.Entry()
        self.uitreken_knop = Gtk.Button(label="Reken uit")
        self.tafel_output_lijst = Gtk.TreeView()

        # Zet default waarden in de invulvakjes. Want als er op de knop geklikt
        # wordt terwijl deze vakjes nog leeg zijn dan crasht het programma omdat
        # lege strings niet om te zetten zijn naar int's (zie verderop)
        #
        self.invulvak_tafel.set_text("6")
        self.invulvak_tot_en_met.set_text("5")

        # Voor de output lijst is een Gtk.TreeView gebruikt. Dit is best een ingewikkeld
        # ding dat veel kan. Hier hoeft ie alleen maar een lijst met sommen (strings)
        # te laten zijn, maar er is wat extra werk nodig.
        #
        # Ten eerste heeft hij een "model" nodig waar hij de data uithaalt die hij moet laten
        # zien:
        #
        self.tafel_data = Gtk.ListStore(str)  # str geeft hier aan: 1 kolom met strings

        # En we moeten kolommen aanmaken, in ons geval maar 1.
        #
        kolom_definitie = Gtk.TreeViewColumn("Tafel", Gtk.CellRendererText(), text=0)
        self.tafel_output_lijst.append_column(kolom_definitie)

        # ... en we willen de kolom-header eigenlijk niet zien:
        #
        self.tafel_output_lijst.set_headers_visible(False)

        # Koppelen van het "ListStore" data-model aan de output-lijst:
        #
        tafel_output_lijst = self.tafel_output_lijst.set_model(self.tafel_data)

        # We moeten nog zorgen dat er wat gebeurt als er op de knop voor uitrekenen
        # geklikt wordt:
        #
        self.uitreken_knop.connect("clicked", self.op_uitreken_knop_geklikt)

        # Deze onderdelen moeten nog aan het window worden toegekend zodat ze er in
        # verschijnen. Dit gaat met een tussenstap: ze worden toegevoegd aan een onzichtbaar
        # object (een Gtk "container") dat de afmetingen en de plek  binnen het window
        # van alle onderdelen regelt. En die container wordt dan aan het window object
        # opgegeven als inhoud van het window.
        #
        # Dit lijkt misschien onnodig ingewikkeld, maar zo worden ze altijd netjes onder
        # elkaar gehouden en vergroot/verkleind naar gelang het window groter/kleiner
        # wordt gemaakt.
        #
        # De eenvoudigste container is een Gtk.Box:

        gtk_tafel_box = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL,  # vertikaal: de onderdelen onder elkaar
                spacing=10                             # ruimte tussen de onderdelen
                )

        # De GUI onderdelen aan gtk_tafel_box toevoegen in de volgorde waarin we willen
        # dat ze van boven naar beneden in het window verschijnen.
        #
        gtk_tafel_box.add(self.invulvak_tafel)
        gtk_tafel_box.add(self.invulvak_tot_en_met)
        gtk_tafel_box.add(self.uitreken_knop)
        gtk_tafel_box.add(self.tafel_output_lijst)

        # Dan de box als enige ding aan het window toewijzigen
        #
        self.add(gtk_tafel_box)

        # Window is nu klaar in het geheugen: laten zien en activeren:
        #
        self.show_all()

    def op_uitreken_knop_geklikt(self, button):
        # Eerst oude data uit de GUI output-list verwijderen.
        #
        self.tafel_data.clear()

        # Eerst de invulvakjes uitlezen, want daarin staat wat we precies moeten
        # uitrekenen.
        #
        tafel = self.invulvak_tafel.get_text()
        tot_en_met = self.invulvak_tot_en_met.get_text()

        # Let op: de variabelen tafel en tot_en_met zijn strings.
        # hier worden ze botweg omgezet naar getallen (int's) zonder
        # te checken of dat wel kan.
        #
        # Code om dit te checken of af te vangen is bewust weg gelaten
        # om dit simpele programma niet nog ingewikkelder te maken :-)
        #
        # Typ je dus bijv "aap" in plaats van een getal in een invulvak, dan gaat het
        # programma crashen op deze regels:
        #
        tafel = int(tafel)
        tot_en_met = int(tot_en_met)

        # Reken de tafel uit, som voor som en zet ze in een string die
        # we in de GUI output-lijst zetten zodat ze te zien zijn.

        # Een for-loop die één voor één de sommen aan de output lijst toevoegt
        #
        # "range" is een built-in class van Python die opeenvolgende getallen
        # genereert. Zie: https://docs.python.org/3/library/stdtypes.html#range
        #
        for tel in range(1, tot_en_met + 1):
            uitkomst = tel * tafel     # berekening

            # nette string maken van de hele som
            #
            som = "{} x {} = {}".format(tel, tafel, uitkomst)

            # Het had ook zo gekund:
            #   enkele_som = str(tel) + " x " + str(tafel) + " = " + str(tel * tafel)

            # De som toevoegen aan de list die ge-returned zal worden
            #
            self.tafel_data.append([som])

# Een GTK-window object aanmaken in het geheugen.
#
window = TafelWindow()

# Definieren dat als het window gesloten wordt, dit programma dan tevens stopt
#
window.connect("delete-event", Gtk.main_quit)

# Window actief maken
#
window.show_all()

# De GTK-mainloop opstarten.
# Dit is een while loop die wacht tot er een toets voor de window(s) van dit
# progamma is ingedrukt op met de muis is op geklikt. Of het window groter gemaakt
# door de gebruiker enz.
#
Gtk.main()

