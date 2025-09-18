# Dossier des Personnalités

Ce dossier contient les fichiers de configuration JSON pour chaque personnalité du bot nova_the_red_cat.

## Structure

Chaque fichier JSON représente une personnalité unique avec la structure suivante :

```json
{
  "name": "nova_the_xxx_cat",
  "cultural_figure": "Figure culturelle inspirante",
  "iconic_phrases": [
    "Phrase 1",
    "Phrase 2",
    "..."
  ],
  "emoji": "🎭",
  "color": "couleur",
  "description": "Description de la personnalité"
}
```

## Personnalités disponibles

- **macron.json** - nova_the_president_cat (Emmanuel Macron) 🇫🇷
- **jcvd.json** - nova_the_muscles_cat (Jean-Claude Van Damme) 🥋
- **melenchon.json** - nova_the_rebel_cat (Jean-Luc Mélenchon) 🚩
- **dictator.json** - nova_the_dictator_cat (Dictateur générique) ⚔️
- **taz.json** - nova_the_tornado_cat (Diable de Tasmanie) 🌪️
- **diable.json** - nova_the_devil_cat (Le Diable) 😈
- **jul.json** - nova_the_marseille_cat (Jul rappeur) 🎤
- **sarcastic.json** - nova_the_sarcastic_cat (Original) 😏

## Ajouter une nouvelle personnalité

1. Créer un nouveau fichier JSON avec le nom de la personnalité
2. Suivre la structure décrite ci-dessus
3. Le bot chargera automatiquement la nouvelle personnalité au redémarrage

## Modifier une personnalité

1. Éditer le fichier JSON correspondant
2. Redémarrer le bot pour appliquer les changements

## Avantages de cette structure

- ✅ Maintenabilité : Un fichier par personnalité
- ✅ Facilité d'ajout/suppression de personnalités
- ✅ Configuration claire et lisible
- ✅ Possibilité de versioning individuel
- ✅ Réutilisabilité et partage facile