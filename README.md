# ZombieDungeon

## Einleitung
    - Kurzbeschreibung

## Spielkomponente
    - 2 Monster
        - Normal
        - Tank
    - 1 Spieler
    - Räume
    - diverse Waffen
        - Pistole
        - Shotgun
        - Sniper
        - Maschinenpistole
        - Sturmgewehr
        - Minigun
    - Geld (kein Sprite, wird direkt bei einem Kill gutgeschrieben)

## Spielprinzip
    - Spieler spawnt in einem Raum
    - Der Spieler spawnt mit einer Pistole (jede Waffe hat unendlich Munition, aber eine andere Feuerrate und Reichweite und Schaden)
    - Wenn Anfangsraum verlassen wird, werden Monster gespawnt, die ohne Sicht auf den Spieler nur herumirren
    - Ist der Spieler im Sichtradius des Monsters, läuft das Monster auf den Spieler zu
    - Der Spieler muss so viele Monster wie möglich töten.
    - Es gibt die Möglichkeit in einen Ruheraum zu gehen, sofern eines in der Nähe ist.
    - Dort werden seine Leben aufgefüllt und er kann in einem Art Shop eine neue Waffe oder einen Schild (teuer, aber sehr hilfreich) kaufen.
    - Verlässt der Spieler einen Raum wird dieser unzugänglich. Läuft der Spieler im Kreis werden die Räume ebenfalls jedes mal neu generiert
    - Für jedes Monster gibt es Punkte und Geld. Die Menge des gedroppten Geldes wird nach jedem Kill zufällig entschieden (Normal: 1-10 | Tank: 10-50 [Variabel])
    - Desto länger der Spieler überlebt, desto mehr Monster spawnen (pro Raum)
    - Tötet der Spieler Monster ohne Schaden zu nehmen (Streak) erhält er auf die Punkte einen Multiplier
    - Alle 10 Kills um 0.5x mehr

