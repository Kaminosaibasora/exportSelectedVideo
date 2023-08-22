# exportSelectedVideo
Exporte une vidéo MP4 "simple" selon la piste audio et de sous-titre choisie.

## Effected :
+ récupérer les informations de langue
+ préparer une interface graphique
+ mettre en place un système de copie vers dossier file_in des vidéos traités via interface graphique
+ remettre tous les paths à partir du même point
+ gérer les noms des fichiers exporté finaux
+ une pop up de validation à la fin 
* mettre en place une animation loading
+ mettre en place l'affichage d'information
+ passage de vidéo en mkv : automatiser la selection de piste
+ généraliser le traitement de infovideo() (parsing mkmerge)
+ utilisation des threads pour exporter le traitement et rendre le tout dynamique
+ ajouter un bouton pour ouvrir le dossier file_out directement
+ revoir la disposition de l'interface
+ metttre en place un système de gestion des erreures
- empécher la fenêtre de ne pas répondre
<!-- https://www.developpez.net/forums/d1333235/c-cpp/bibliotheques/qt/debuter/programme-ne-repond-pendant-chargement-d-qprogressbar/ -->
<!-- https://www.developpez.net/forums/d1331300/c-cpp/bibliotheques/qt/debuter/lecture-d-fichier-lourd/#post7232463 -->
<!-- https://qt-quarterly.developpez.com/qq-27/conserver-reactivite-ihm/ -->
<!-- https://www.pythonguis.com/tutorials/multithreading-pyqt-applications-qthreadpool/ -->

## TODO
- mettre en place des logs
- mettre en place un installateur pour importer toutes les dépendances