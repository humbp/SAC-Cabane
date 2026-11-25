# Cabanes — disponibilités des cabanes de montagne

Application Android (icône : une cabane rouge) qui affiche, sur une carte, les places libres des cabanes de montagne (CAS et autres) pour des dates choisies. Chaque cabane porte un petit histogramme : une colonne par nuit, dont la hauteur est le nombre de places libres.

| Couleur de la colonne | Signification |
| --- | --- |
| Rouge | moins de places libres que de personnes dans le groupe |
| Jaune | juste assez : au plus 2 places de marge |
| Vert | confortable |
| Gris | pas de donnée pour cette nuit |

Un cercle gris sur la carte marque une cabane connue du service mais dont les places libres ne sont pas suivies (par exemple la Cabane des Audannes). Il faut alors se renseigner directement auprès de la cabane.

## Utilisation

1. Touchez le bouton des dates, puis l'arrivée et le départ dans le même calendrier. Les nuits vont de l'arrivée à la veille du départ (31 nuits au maximum).
2. Choisissez une région dans la liste (26 régions de Suisse, France, Italie, Autriche, Allemagne et Slovénie), ou « Zone visible de la carte ».
3. Réglez le nombre de personnes (4 par défaut). Les couleurs se recalculent tout de suite.
4. Les dates proposées au lancement sont toujours celles du prochain week-end (samedi suivant la date du jour, une nuit).
5. Dans **Légende et filtres**, réglez si besoin la taille des cabanes avec les deux curseurs (places minimum et maximum).
6. Touchez **Rechercher**, ou **Rechercher dans cette zone** sur la carte après l'avoir déplacée et zoomée.
7. Touchez une cabane pour voir le détail nuit par nuit et le lien vers sa page.

Le manuel d'utilisation détaillé est dans `Manuel_Cabanes.pdf`.

## Installation (utilisateurs)

Les utilisateurs reçoivent un lien et n'ont pas besoin de GitHub : ouvrir le lien dans Chrome, ouvrir le fichier `cabanes.apk` téléchargé, autoriser l'installation si demandé.
Lien fixe : `https://github.com/humbp/SAC-Cabane/releases/latest/download/cabanes.apk` (dépôt public requis).

Détails dans `Manuel_Cabanes.pdf` (français) et `Gebruuchsalyitig_Cabanes_Berndeutsch.pdf` (bernois).

## Diffusion (mainteneur)

Voir `Guide_Diffusion_Cabanes.pdf`. La compilation tourne à chaque modification. La clé de signature est dans le secret `ANDROID_KEYSTORE_B64`.

## Fichiers du dépôt

| Fichier | Rôle |
| --- | --- |
| `index.html` | toute l'application : page, calendrier, carte et recherche |
| `make_icons.py` | dessine l'icône (cabane rouge) pour Android |
| `.github/workflows/build.yml` | compilation de l'APK par GitHub Actions |
| `README.md` | ce fichier |

## Mise à jour

1. Remplacez `index.html` dans le dépôt (Chrome, page `upload/main` du dépôt, **Commit changes**).
2. GitHub Actions compile et publie une nouvelle version dans **Releases** (5 à 10 minutes). Le lien fixe pointe vers elle.

## Fonctionnement

- L'application est une page web (`index.html`) emballée dans une application Android avec [Capacitor](https://capacitorjs.com). Les appels réseau sont faits par le code natif de l'application, ce qui évite le blocage que Chrome applique aux pages locales.
- Les disponibilités viennent du service public [Wodore](https://wodore.github.io/wodore-backend/api/), qui agrège les données du système de réservation des cabanes. Les requêtes sont espacées pour ménager le service.
- Le fond de carte est celui d'OpenStreetMap ou d'OpenTopoMap, affiché avec [Leaflet](https://leafletjs.com).
- Les recettes de compilation numérotent chaque version avec le numéro d'exécution de GitHub Actions.

## Limites

- Seules les cabanes dont le service suit les disponibilités reçoivent un histogramme. Les autres se réservent par téléphone ou par e-mail.
- France (FFCAM), Italie (CAI) et Slovénie (PZS) n'offrent pas d'accès public aux places libres : ces cabanes apparaissent en cercle gris avec le lien du système de réservation du pays (pays estimé d'après la position, approximatif près des frontières). L'Autriche, l'Allemagne et le Haut-Adige passent par Hut-Reservation, lu par le service quand il suit la cabane.
- Le filtre de taille s'appuie sur la capacité annoncée par le service ; les cercles gris, sans capacité connue, sont masqués dès que la plage est réduite.
- Une cabane fermée à la saison choisie n'a pas de donnée et n'apparaît pas avec des colonnes.
- Les rectangles de région sont approximatifs. La couverture des cabanes hors de Suisse dépend du service.
- Les chiffres sont indicatifs. Confirmez toujours la réservation auprès de la cabane ou sur le système de réservation officiel.
- Projet personnel, sans lien officiel avec le CAS ni avec le service Wodore. La clé de signature Android est une clé de test (secret GitHub) : elle ne convient pas à une publication sur le Play Store.
