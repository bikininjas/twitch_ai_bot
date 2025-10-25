# Dossier des Personnalités

Ce dossier contient les fichiers de configuration JSON pour chaque personnalité du bot nova_the_red_cat.
Ces fichiers restent la source de vérité par défaut même si un backend SQLite Cloud
est configuré (le bot revient automatiquement à ces JSON en cas d'erreur de base de données).

## Structure

Chaque fichier JSON représente une personnalité unique avec la structure suivante :

```json
{
  "schema_version": 1,
  "name": "nova_the_xxx_cat",
  "cultural_figure": "Figure culturelle inspirante",
  "description": "Description de la personnalité",
  "emoji": "🎭",
  "color": "couleur",
  "tone": "Quelques mots sur l'attitude générale",
  "iconic_phrases": [
    "Phrase 1",
    "Phrase 2",
    "..."
  ],
  "announcement_variants": [
    "Message de prise de contrôle #1",
    "Message de prise de contrôle #2"
  ],
  "signature": "- nova 🎭",
  "triggers": {
    "keywords": ["mot_clé", "..."],
    "commands": ["!commande", "..."]
  },
  "sample_prompts": [
    "Suggestion de prompt #1",
    "Suggestion de prompt #2"
  ],
  "cooldown_override": 180
}
```

## Personnalités disponibles

- **boomer.json** - nova_the_boomer_cat (Boomer générique) 📼
- **chirac.json** - nova_the_mayor_cat (Jacques Chirac) 🥖
- **diable.json** - nova_the_devil_cat (Le Diable) 😈
- **dictator.json** - nova_the_dictator_cat (Dictateur générique) ⚔️
- **jcvd.json** - nova_the_muscles_cat (Jean-Claude Van Damme) 🥋
- **jul.json** - nova_the_marseille_cat (Jul) 🎤
- **macron.json** - nova_the_president_cat (Emmanuel Macron) 🇫🇷
- **memelord.json** - nova_the_memelord_cat (Culture Internet) 🧠
- **melenchon.json** - nova_the_rebel_cat (Jean-Luc Mélenchon) 🚩
- **sarcastic.json** - nova_the_sarcastic_cat (Original) 😏
- **sarkozy.json** - nova_the_hyperactive_cat (Nicolas Sarkozy) 👔
- **taz.json** - nova_the_tornado_cat (Diable de Tasmanie) 🌪️

## Ajouter une nouvelle personnalité

1. Dupliquer un fichier existant comme modèle ou partir de la structure ci-dessus
2. Adapter les champs au personnage que vous souhaitez créer
3. S'assurer que la liste `iconic_phrases` contient au moins deux entrées
4. Définir au minimum un mot-clé ou une commande dans `triggers`
5. Redémarrer le bot pour recharger la personnalité

## Modifier une personnalité

1. Éditer le fichier JSON correspondant
2. Redémarrer le bot pour appliquer les changements

## Avantages de cette structure

- ✅ Maintenabilité : Un fichier par personnalité
- ✅ Facilité d'ajout/suppression de personnalités
- ✅ Validation automatique via le schéma Pydantic
- ✅ Configuration claire et lisible
- ✅ Possibilité de versioning individuel
- ✅ Réutilisabilité et partage facile