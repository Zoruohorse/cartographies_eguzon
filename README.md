# Cartographie interactive — Éguzon–Marmagne

Site statique pour GitHub Pages avec **même structure, taxonomie, design, physique et interactions** que le modèle Chaingy–Dambron / Celtic Interconnector. La seule adaptation d’interface est le titre de projet. La vue cartes et la vue réseau partagent les mêmes JSON.

## Installer dans un dépôt GitHub

1. Créer un dépôt vide, par exemple `cartographies_Eguzon_Marmagne`.
2. **Décompresser le ZIP** et importer **son contenu directement à la racine**. À la racine doivent figurer `index.html`, `apps/`, `assets/`, `data/`, `config/`, `audit/`, `README.md`, `validate.py` et `.nojekyll`.
3. Dans **Settings → Pages**, choisir **Deploy from a branch**, puis `main` et `/(root)`.
4. Vérifier localement avec `python validate.py` (PASS attendu), puis `python -m http.server 8000` avant d’ouvrir `http://localhost:8000`.

## Données et distinctions obligatoires

- Source **exclusivement** : `Cartographie Eguzon.xlsx`, feuille « Eguzon-Marmagne - Projet », **37 lignes de ressources** (lignes 2–38). Dernière **date de trouvaille** : **2026-11-02**, non nécessairement date de publication.
- Ligne nationale Éguzon–Marmagne : RTE, 400 kV à deux circuits, variantes 90–110 km, huit fuseaux, investissement **estimé** 300 M€, capacité de transit supplémentaire estimée **5 400 MW**. Concertation 28 septembre–22 novembre 2026, mise en service **au plus tôt en 2032** selon les documents.
- Campus Google/Ozans et son raccordement : **projet juridiquement distinct**, autre concertation du 2 novembre 2026 au 10 janvier 2027, première phase 225 kV 120 MW, extensions 400 kV conditionnelles. Les chiffres associés au centre de données ne sont pas des caractéristiques de la ligne nationale.
- Les actions locales d’opposition portent majoritairement sur Google/Ozans. Les acteurs sans position explicite sur la ligne RTE restent affichés en cartes avec *Position non qualifiée* et des preuves de fonction ou d’intervention ; aucune opinion transposée automatiquement.
- Le maire de Chouday défend le passage sur le tracé existant et la préservation de la fiscalité des pylônes. Cette préférence conditionnelle ne signifie pas refus de toute infrastructure électrique.
- Les montants de taxes, de coûts, emplois, eau et puissances sont qualifiés par périmètre et conditionnalité. Une date de consultation ne vaut ni DUP ni autorisation de construire.
- Les liens web proviennent du fichier Excel **sans nouvelle consultation des sites**. Les extraits via `news.google.com` sont marqués agrégateurs ; la ligne Excel 27 contient dans le corps une URL de partage du Monde, réutilisée explicitement.

## Fichiers

| Chemin | Usage |
|---|---|
| `data/actors.json` | Entités, catégories et preuves associées (positions optionnelles) |
| `data/claims.json` | Uniquement positions explicites sur **la ligne Éguzon–Marmagne** |
| `data/evidence.json` | Preuves datées et traçables à la ligne Excel et à l’URL du lot |
| `data/relations.json` | Liens attestés entre acteurs, institutions, enjeux et projets voisins |
| `data/sources.json` | Provenance des sources et statut des URL (agrégateur vs éditeur) |
| `data/meta.json` | Projet, évolutions techniques, synthèses documentées et vigilances |
| `config/taxonomy.json` | Taxonomie identique au dépôt modèle, sans extension |
| `apps/cards/`, `apps/network/`, `assets/` | Mêmes vues, styles et moteur physique que Chaingy |
| `audit/corpus-review.json` | Analyse **de chaque ligne**, y compris exclusions justifiées |
| `audit/validation.json` | Rapport de conformité JSON, sources, IDs et références |
| `audit/qa-report.json` | Tests de navigateur des deux vues |

## Mettre à jour

Conserver les identifiants des objets existants ; ajouter des preuves avec un identifiant séquentiel ; ne changer les positions que sur justification sourcée. `python validate.py` contrôle la cohérence. Les fiches présentent les preuves multiples ainsi que leurs liens.
