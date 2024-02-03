import pygame
import os

# Initialisieren von Pygame-Funktionen
pygame.font.init()
pygame.mixer.init()

# Fenstergrösse und Initialisierung
BREITE, HÖHE = 900, 500
FENSTER = pygame.display.set_mode((BREITE, HÖHE))
pygame.display.set_caption("Space Fight")

# Farben
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
ROT = (255, 0, 0)
GELB = (255, 255, 0)

# Spielfeldgrenzen
RAHMEN = pygame.Rect(BREITE // 2 - 5, 0, 10, HÖHE)

# Soundeffekte
GESCHOSSTREFFER_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'explosion.wav'))
GESCHOSSE_ABFEUERN_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'laser.wav'))

# Schriftarten
GESUNDHEITS_SCHRIFT = pygame.font.SysFont('arial', 40)
GEWINNER_SCHRIFT = pygame.font.SysFont('arial', 100)

# Spielparameter
FPS = 60
GESCHWINDIGKEIT = 5
GESCHOSSE_GESCHWINDIGKEIT = 7
MAX_GESCHOSSE = 3
SCHIFFSBREITE = 80
SCHIFFSHÖHE = 60

GELB_TRIFFT = pygame.USEREVENT + 1
ROT_TRIFFT = pygame.USEREVENT + 2

GELBES_SCHIFF_BILD = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
GELBES_SCHIFF = pygame.transform.rotate(pygame.transform.scale(
    GELBES_SCHIFF_BILD, (SCHIFFSBREITE, SCHIFFSHÖHE)), 90)
ROTES_SCHIFF_BILD = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
ROTES_SCHIFF = pygame.transform.rotate(pygame.transform.scale(
    ROTES_SCHIFF_BILD, (SCHIFFSBREITE, SCHIFFSHÖHE)), 270)

HINTERGRUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (BREITE, HÖHE))


# Diese Funktion steuert das gelbe Raumschiff basierend auf den gedrückten Tasten.
def gelbe_steuerung(tasten_gedrückt, gelb):
    if tasten_gedrückt[pygame.K_a] and gelb.x - GESCHWINDIGKEIT > -15:  # Links
        gelb.x -= GESCHWINDIGKEIT
    if tasten_gedrückt[pygame.K_d] and gelb.x + GESCHWINDIGKEIT + gelb.height - 35 < RAHMEN.x:  # Rechts
        gelb.x += GESCHWINDIGKEIT
    if tasten_gedrückt[pygame.K_w] and gelb.y - GESCHWINDIGKEIT > -10:  # Hoch
        gelb.y -= GESCHWINDIGKEIT
    if tasten_gedrückt[pygame.K_s] and gelb.y + GESCHWINDIGKEIT + gelb.width < HÖHE:  # Runter
        gelb.y += GESCHWINDIGKEIT

# Diese Funktion steuert das rote Raumschiff basierend auf den gedrückten Tasten.
def rote_steuerung(tasten_gedrückt, rot):
    if tasten_gedrückt[pygame.K_LEFT] and rot.x - GESCHWINDIGKEIT + 15 > RAHMEN.x + RAHMEN.width:  # Links
        rot.x -= GESCHWINDIGKEIT
    if tasten_gedrückt[pygame.K_RIGHT] and rot.x + GESCHWINDIGKEIT + rot.height - 35 < BREITE:  # Rechts
        rot.x += GESCHWINDIGKEIT
    if tasten_gedrückt[pygame.K_UP] and rot.y - GESCHWINDIGKEIT > -10:  # Hoch
        rot.y -= GESCHWINDIGKEIT
    if tasten_gedrückt[pygame.K_DOWN] and rot.y + GESCHWINDIGKEIT + rot.width < HÖHE:  # Runter
        rot.y += GESCHWINDIGKEIT

# Diese Funktion zeichnet das Spielfenster mit den Raumschiffen, Lebenspunkten und Geschossen.
def zeichne_fenster(rot, gelb, rote_geschosse, gelbe_geschosse, rote_lebenspunkte, gelbe_lebenspunkte):
    FENSTER.blit(HINTERGRUND, (0, 0))
    pygame.draw.rect(FENSTER, SCHWARZ, RAHMEN)

    rote_lebenspunkte_text = GESUNDHEITS_SCHRIFT.render("Lebenspunkte: " + str(rote_lebenspunkte), True, WEISS)
    gelbe_lebenspunkte_text = GESUNDHEITS_SCHRIFT.render("Lebenspunkte: " + str(gelbe_lebenspunkte), True, WEISS)
    FENSTER.blit(rote_lebenspunkte_text, (BREITE - rote_lebenspunkte_text.get_width() - 10, 10))
    FENSTER.blit(gelbe_lebenspunkte_text, (10, 10))

    FENSTER.blit(GELBES_SCHIFF, (gelb.x, gelb.y))
    FENSTER.blit(ROTES_SCHIFF, (rot.x, rot.y))

    for geschoss in rote_geschosse:
        pygame.draw.rect(FENSTER, ROT, geschoss)
    for geschoss in gelbe_geschosse:
        pygame.draw.rect(FENSTER, GELB, geschoss)

    pygame.display.update()

# Diese Funktion aktualisiert die Position der Geschosse und überprüft Kollisionen.
def behandle_geschosse(gelbe_geschosse, rote_geschosse, gelb, rot):
    for geschoss in gelbe_geschosse:
        geschoss.x += GESCHOSSE_GESCHWINDIGKEIT
        if rot.colliderect(geschoss):
            pygame.event.post(pygame.event.Event(ROT_TRIFFT))
            gelbe_geschosse.remove(geschoss)
        elif geschoss.x > BREITE:
            gelbe_geschosse.remove(geschoss)

    for geschoss in rote_geschosse:
        geschoss.x -= GESCHOSSE_GESCHWINDIGKEIT
        if gelb.colliderect(geschoss):
            pygame.event.post(pygame.event.Event(GELB_TRIFFT))
            rote_geschosse.remove(geschoss)
        elif geschoss.x < 0:
            rote_geschosse.remove(geschoss)

# Diese Funktion zeigt den Gewinnertext im Spiel an und verzögert das Spiel für 5 Sekunden.
def zeichne_gewinner(text):
    draw_text = GEWINNER_SCHRIFT.render(text, True, WEISS)
    FENSTER.blit(draw_text, (BREITE / 2 - draw_text.get_width() / 2, HÖHE / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)

# Hauptfunktion, die das Spiel steuert.
def main():
    # Initialisierung der Spielfiguren, Meteoriten und anderer Variablen
    rot = pygame.Rect(700, 300, SCHIFFSBREITE, SCHIFFSHÖHE)
    gelb = pygame.Rect(100, 300, SCHIFFSBREITE, SCHIFFSHÖHE)

    rote_geschosse = []
    gelbe_geschosse = []

    rote_lebenspunkte = 10
    gelbe_lebenspunkte = 10

    uhr = pygame.time.Clock()
    spiel_läuft = True
    while spiel_läuft:
        uhr.tick(FPS)
        for ereignis in pygame.event.get():
            if ereignis.type == pygame.QUIT:
                spiel_läuft = False
                pygame.quit()

            if ereignis.type == pygame.KEYDOWN:
                # Überprüfen der Tastendrücke zum Abfeuern von Geschossen
                if ereignis.key == pygame.K_LCTRL and len(gelbe_geschosse) < MAX_GESCHOSSE:
                    geschoss = pygame.Rect(gelb.x + gelb.height, gelb.y + gelb.width // 2, 10, 5)
                    gelbe_geschosse.append(geschoss)
                    GESCHOSSE_ABFEUERN_SOUND.play()
                if ereignis.key == pygame.K_RCTRL and len(rote_geschosse) < MAX_GESCHOSSE:
                    geschoss = pygame.Rect(rot.x, rot.y + rot.width // 2, 10, 5)
                    rote_geschosse.append(geschoss)
                    GESCHOSSE_ABFEUERN_SOUND.play()
            if ereignis.type == ROT_TRIFFT:
                # Reduzieren der Lebenspunkte bei Treffer auf das rote Raumschiff
                rote_lebenspunkte -= 1
                GESCHOSSTREFFER_SOUND.play()
            if ereignis.type == GELB_TRIFFT:
                # Reduzieren der Lebenspunkte bei Treffer auf das gelbe Raumschiff
                gelbe_lebenspunkte -= 1
                GESCHOSSTREFFER_SOUND.play()

        # Festlegen des Gewinnertextes
        gewinner_text = ""
        if rote_lebenspunkte <= 0:
            gewinner_text = "Gelb gewinnt!"
        if gelbe_lebenspunkte <= 0:
            gewinner_text = "Rot gewinnt!"
        if gewinner_text != "":
            zeichne_gewinner(gewinner_text)
            break

        # Aktualisierung der Tastendrücke, Steuerung der Raumschiffe
        tasten_gedrückt = pygame.key.get_pressed()
        gelbe_steuerung(tasten_gedrückt, gelb)
        rote_steuerung(tasten_gedrückt, rot)

        # Behandlung von Geschossen und Aktualisierung des Spielfensters
        behandle_geschosse(gelbe_geschosse, rote_geschosse, gelb, rot)

        zeichne_fenster(rot, gelb, rote_geschosse, gelbe_geschosse, rote_lebenspunkte, gelbe_lebenspunkte)

    main()

# Startet das Spiel, wenn dieses Skript ausgeführt wird.
if __name__ == "__main__":
    main()
