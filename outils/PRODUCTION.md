# Production des aides-mémoire Espace 19 – mode d'emploi pour Claude

À lire en entier, avec `consignes_aides_memoire.md` (même dossier), avant chaque séance de production.
Michel Féviliyé : bénévole, non-développeur, vouvoiement, français simple. Il dort ou travaille pendant les séances : ne lui pose pas de question, décide, explique dans le compte rendu.

## Repères Google Drive (identifiants)
- Aide-Mémoire : 17XU4TqbUGWylvKa2JgQi1a1IDBt7Ae-T (contient `logo_espace19.png` : 1NY49OpR-wG4SMMRS4C3gP78jOc3Oz5A_)
  - Téléchargements voix off : 100Fy3UxDGMYTvRXyi56GAvivcdRJRTLb
  - Formation Débutant : 1qAlva7-s4S5EeweIjSlGO-DqWD1WkP9J
    - Plan : 1agjSXEzsxN45UD8-KDIeiR4p0ATq-RCL (lire les 3 .docx)
    - Traitement (PRIVÉ) : 1L2K8sLsspXgOoQ1erK5QcnEqojTdeU6x — contient `plan_de_travail.md` et un sous-dossier « NN - Titre » par sujet
    - Aide-mémoire Participants (PARTAGÉ par lien, lecture seule) : 1SoPnXajuQBltxh0qk0jCj8DAaghjYEoY — un sous-dossier « NN - Titre » par sujet, avec UNIQUEMENT la vidéo finale avec voix et la fiche PDF finale
    - Archives : 1cdjyGMua_A8D5Ow0Wll3v5UOWFzIJNN8
- Mettre à jour un fichier .md dans Drive : créer le nouveau, puis déplacer l'ancien dans Archives (renommé « … (ancienne version AAAA-MM-JJ HHhMM) »). Ne jamais supprimer.
- Téléverser un fichier local : `create_file` avec `base64Content = sha256:<hash>:<chemin absolu>` et `disableConversionToGoogleType: true`. Le fichier doit être dans le dossier scratchpad de la session, avec un nom simple (sans accent ni apostrophe). Limite : environ 3,1 Mo par fichier (au-delà, l'envoi est refusé).

## Outils (ce dossier)
- `render_01.py` : bibliothèque et exemple complet de vidéo du sujet 08 « Créer un dossier personnel » (nom historique). Les outils propres à chaque sujet vont dans `outils/NN-motcle/` (ex. `outils/01-ordinateur/`). Fonctions réutilisables : `screen`, `cursor`, `ripple`, `highlight` (cadre jaune clignotant), `arrow`, `loupe`, `caption` (titre d'étape en haut), `subtitle` + `sub_at` (sous-titres en bas), `card`, rendu ffmpeg 1280×720 à 12 i/s. Pour un nouveau sujet : copier en `render_NN.py` et réécrire les écrans (`screen`, `rect_of`) et `frame()` scène par scène. Écrans DESSINÉS (pas de capture), fidèles à Windows 11 ou au site, sans reproduire de logo de site officiel.
- `script_01.json` : modèle de script (scènes : id, narration, caption). Paragraphes de narration = scènes.
- `crops_01.py` : images zoomées des étapes pour la fiche.
- `fiche_v3.py` : fiche PDF 4 pages (modèle validé par Michel le 25/11). Copier en `fiche_NN.py` et réécrire le contenu ; garder CSS, en-tête avec logo, pieds de page, QR SÉPARÉS (grand « Revoir la vidéo » en page 3, petit « Tous les aide-mémoire » en bas de la page 4), page « Mes notes ». Le script vérifie qu'aucun bloc ne déborde : corriger jusqu'à « deborde » < 0 sur les 4 pages.
- `assemble_v2.py` (à utiliser) : vidéo + voix. Usage : `python3 assemble_v2.py script_NN.json NN.mp3 sortie.mp4 chemin/du/render_NN.py`. Il trouve la fin de chaque phrase avec `aligne.py` (débit en syllabes : la voix fait aussi des pauses aux virgules, on ne peut pas se fier aux seules pauses), cale chaque paragraphe au début de sa scène, et affiche chaque sous-titre exactement pendant que la phrase est dite. Il s'arrête si une phrase est douteuse (rapport hors 0,70–1,40). Il écrit `sortie.mp4.rapport.json` (début/fin de chaque phrase, contrôle par scène : environ 0,07 s par caractère + 1,3 s par phrase). Voix en mono 64 kbit/s. Marges propres à un sujet : clé `"marges"` dans le script.
- `assemble.py` : ANCIENNE version, ne plus l'utiliser (elle s'est trompée de phrase sur le 08 et le 01, découvert le 25/11 séance B).
- Contrôle après assemblage : planche d'images prise au MILIEU de chaque phrase (sous-titre = phrase attendue = image), et niveau sonore non nul pendant chaque phrase.
- Page interactive : modèle `../08-creer-un-dossier/index.html` (démonstration, exercice vérifié, 3 échecs → solution animée, « Recommencer » / « Terminer la leçon »). Une page par sujet quand `plan_de_travail.md` l'indique ; ajouter le lien dans `../index.html`.
- Installer si besoin : `pip install --break-system-packages playwright qrcode python-docx` ; `python3 -m playwright install chromium` si Chromium manque.

## Production continue (depuis le 25/11/2026 15h, décision de Michel)
Une séance par heure. Chaque séance traite UN sujet DE BOUT EN BOUT (séance A puis séance B ci-dessous, à la suite, sans attendre le lendemain), puis s'arrête. La séance suivante prend le sujet suivant. On continue jusqu'à ce que tout le plan soit publié.

### Verrou anti-doublon (obligatoire, en tout premier)
1. Chercher dans Traitement un fichier dont le titre commence par `VERROU_production`.
   - S'il existe et a été créé il y a MOINS de 3 heures : une autre séance travaille. S'arrêter immédiatement, sans rien modifier et sans envoyer de mail.
   - S'il existe et a plus de 3 heures : la séance précédente s'est interrompue. Le déplacer dans Archives (renommé « … (abandonné) »), le signaler dans le compte rendu, puis continuer.
2. Créer `VERROU_production.md` dans Traitement (contenu : date, heure, numéro du sujet choisi).
3. À la fin de la séance (même en cas d'échec) : déplacer le verrou dans Archives, renommé « VERROU_production (libéré AAAA-MM-JJ HHhMM).md ».

### Choix du sujet
- D'abord, un sujet dont tout est prêt sauf la publication (voix produite, non publié) : le terminer (séance B).
- Sinon, le premier sujet dont les sources sont « ⬜ » : séance A puis séance B.
- Avant de publier : si Participants › « NN - Titre » contient déjà la vidéo finale, ne rien refaire (marquer « Publié »).
- Si tous les sujets sont « Publié » : déplacer les fichiers du dossier Plan dans Archives, envoyer un dernier compte rendu « Production terminée » (une seule fois : écrire « Production terminée » en tête de plan_de_travail.md ; si c'est déjà écrit, s'arrêter sans mail).

## Séance A (préparer un sujet)
1. Lire `plan_de_travail.md` (Drive › Traitement). Prendre le PREMIER sujet dont « Sources » est ⬜. Si aucun : séance terminée, le dire dans le compte rendu.
2. Vérifier : aide officielle d'abord (support.microsoft.com, support.google.com, sites officiels), puis 2-3 guides datés. Un libellé de bouton n'est écrit tel quel que s'il est confirmé. Écrire `sources_NN.md`.
3. Écrire `script_NN.json` (ton des consignes : rassurant, phrases courtes, analogies), puis la vidéo sans voix sous-titrée (2 à 3 min, lente, cadres jaunes, flèches, loupe, pause, exercice + solution, résumé). Contrôler une planche d'images (ffmpeg tile) : rien de masqué, textes lisibles.
4. Fiche PDF 4 pages (lien du sous-dossier Participants pour le grand QR : créer « NN - Titre » dans Participants s'il n'existe pas ; il hérite du partage par lien — le vérifier avec get_file_permissions).
5. Page interactive si prévue : la coder, la tester avec Playwright (réussite, 3 échecs → solution, aucune erreur JavaScript), commit + push sur `main` (lignes de fin de commit : Co-Authored-By: Claude <noreply@anthropic.com>). Si le push est refusé : le noter, ne pas contourner.
6. Voix off Higgsfield : narration complète (paragraphes séparés par une ligne vide), modèle `text2speech_v2`, variant `elevenlabs`, voice_type `preset`, voice_id `8b95a259-62fd-545d-b0f0-7b521a972b6b` (Elodie), `use_unlim: false`. D'abord `estimate_audio_cost` puis `balance` ; lancer UNE génération seulement si coût ≤ 6 crédits et ≤ solde ; générer via le `quote_ref`. `jobs_wait` jusqu'au résultat. Ne jamais acheter de crédits, ni changer d'abonnement.
7. Récupérer le mp3 tout de suite (le serveur Claude ne peut pas le télécharger lui-même) : Make (zone eu2, organisation 5418420, équipe 2791712). Scénario Make « Espace 19 – récupérer voix off » (id 10234106, actif, connexion « Google Drive Espace 19 » id 14760273, valable jusqu'au 25/05/2027) : `scenarios_run` avec `responsive: true` et `data = {url: <URL du mp3>, nom: "NN.mp3", dossier: <ID du dossier Traitement › NN>}`, puis vérifier dans Drive que `NN.mp3` est arrivé. Ensuite `download_file_content` sur ce fichier pour l'avoir dans la session. Si aucune connexion : noter l'URL du mp3 dans `plan_de_travail.md` et dans le compte rendu.
8. Déposer dans Traitement › « NN - Titre » : sources, script, vidéo sans voix sous-titrée, fiche PDF (brouillon), images. Mettre à jour `plan_de_travail.md`.

## Séance B (assembler et publier, juste après la séance A)
0. Avant tout : si Participants › « NN - Titre » contient déjà la vidéo finale avec voix, le sujet est déjà publié : marquer « Publié » dans le plan et ne rien refaire.
1. Pour chaque sujet dont la voix est « ⏳ » : chercher `NN.mp3` dans Traitement › NN (ou un mp3 récent dans « Téléchargements voix off » ; le ranger dans Traitement › NN). S'il manque et que Make est connecté : relancer le scénario avec l'URL notée. Sinon : le signaler.
2. Avec le mp3 : `download_file_content`, `assemble_v2.py script_NN.json NN.mp3 sortie.mp4 render_NN.py`, vérifier durée, taille (< 3,1 Mo pour l'envoi) et la planche d'images (sous-titres = phrase dite). Si trop lourd : augmenter le crf vidéo du module de rendu ; découper en 2 parties seulement en dernier recours.
3. Publier dans Participants › « NN - Titre » : `NN - Titre.mp4` (avec voix) et `NN - Titre.pdf` (fiche finale). Rien d'autre dans ce dossier.
4. Archiver : déplacer dans Archives les fichiers de travail du sujet devenus inutiles (vidéo sans voix, anciennes versions), APRÈS la publication. Garder sources et script dans Traitement.
5. `plan_de_travail.md` : passer le sujet à « Publié ». Quand tout est publié : déplacer les fichiers du dossier Plan dans Archives et l'écrire dans le compte rendu.

## Compte rendu (chaque séance)
Un mail par sujet publié (pas de mail quand la séance s'arrête à cause du verrou). Mail à michel.feviliye@gmail.com uniquement (Gmail send_message, HTML simple, objet « Aides-mémoire Espace 19 – n° NN publié »), en français simple : résultat d'abord, preuves (liens Drive, tailles, durées, commit), ce qui n'a pas pu être vérifié (écoute de la voix), crédits dépensés et solde, puis « À faire de votre côté » numéroté (ex. valider l'autorisation Make si elle manque). Fiches publiées en pièce jointe si possible. Si Gmail échoue : tout mettre dans SendUserMessage.

## Règles impératives
Aucun secret dans les messages ou le dépôt (dépôt PUBLIC). Aucun autre appel payant que la voix ci-dessus. Ne jamais partager un dossier de travail ; ne pas modifier le partage du dossier Participants. Ne jamais réécrire l'historique git publié. Rien n'est « terminé » sans preuve.
