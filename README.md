# Cabanes — disponibilités des cabanes de montagne

Application Android qui affiche, sur une carte, les places libres des cabanes de montagne (CAS et autres) pour des dates choisies. Chaque cabane porte un petit histogramme : une colonne par nuit, dont la hauteur est le nombre de places libres.

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
4. Touchez **Rechercher**, ou **Rechercher dans cette zone** sur la carte après l'avoir déplacée et zoomée.
5. Touchez une cabane pour voir le détail nuit par nuit et le lien vers sa page.

Le manuel d'utilisation détaillé est dans `Manuel_Cabanes.pdf`.

## Installation

1. Dans l'application GitHub ou dans Chrome, ouvrez **Releases** de ce dépôt, puis la version la plus récente.
2. Téléchargez `cabanes.apk` et ouvrez-le.
3. Autorisez l'installation depuis cette source si Android le demande, puis installez.

Si une ancienne version de l'application, signée avec une autre clé, est déjà installée, désinstallez-la d'abord.

## Fichiers du dépôt

| Fichier | Rôle |
| --- | --- |
| `index.html` | toute l'application : page, calendrier, carte et recherche |
| `.github/workflows/build.yml` | recette de compilation de l'APK par GitHub Actions |
| `debug.keystore` | clé de signature fixe, pour que chaque version s'installe par-dessus la précédente |
| `README.md` | ce fichier |

## Mise à jour

1. Remplacez `index.html` dans le dépôt (Chrome, page `upload/main` du dépôt, **Commit changes**).
2. GitHub Actions compile l'application. Suivez l'avancement dans l'onglet **Actions** (5 à 10 minutes).
3. Téléchargez `cabanes.apk` dans la nouvelle version de **Releases** et installez-le par-dessus l'ancienne.

## Fonctionnement

- L'application est une page web (`index.html`) emballée dans une application Android avec [Capacitor](https://capacitorjs.com). Les appels réseau sont faits par le code natif de l'application, ce qui évite le blocage que Chrome applique aux pages locales.
- Les disponibilités viennent du service public [Wodore](https://wodore.github.io/wodore-backend/api/), qui agrège les données du système de réservation des cabanes. Les requêtes sont espacées pour ménager le service.
- Le fond de carte est celui d'OpenStreetMap ou d'OpenTopoMap, affiché avec [Leaflet](https://leafletjs.com).
- La recette de compilation numérote chaque version (`versionCode`) avec le numéro d'exécution de GitHub Actions.

## Limites

- Seules les cabanes dont le service suit les disponibilités reçoivent un histogramme. Les autres se réservent par téléphone ou par e-mail.
- Une cabane fermée à la saison choisie n'a pas de donnée et n'apparaît pas avec des colonnes.
- Les rectangles de région sont approximatifs. La couverture des cabanes hors de Suisse dépend du service.
- Les chiffres sont indicatifs. Confirmez toujours la réservation auprès de la cabane ou sur le système de réservation officiel.
- Projet personnel, sans lien officiel avec le CAS ni avec le service Wodore. La clé `debug.keystore` est publique dans ce dépôt : elle ne convient pas à une publication sur le Play Store.
- 
