# Système de Personnalités Nova

## 📁 Structure

```
personalities/
├── __init__.py          # Package principal et factory
├── base.py             # Classes de base (Personality, PersonalityType)
├── sarcastic.py        # Personnalité sarcastique (nova_the_sarcastic_cat)
├── macron.py           # Personnalité Macron (nova_the_president_cat)
├── jcvd.py             # Personnalité JCVD (nova_the_muscles_cat)
├── dictator.py         # Personnalité Dictateur (nova_the_dictator_cat)
├── melenchon.py        # Personnalité Mélenchon (nova_the_rebel_cat)
├── taz.py              # Personnalité Taz (nova_the_tornado_cat)
├── diable.py           # Personnalité Diable (nova_the_devil_cat)
└── jul.py              # Personnalité Jul (nova_the_marseille_cat)
```

## 🎭 Personnalités Disponibles

### 🔥 **Personnalités Françaises Authentiques**

1. **🇫🇷 Macron** - Le chat président
   - Expressions: "En même temps", "Poudre de perlimpinpin", "Start-up nation"
   - Style: Présidentiel avec références gaming

2. **🥋 Jean-Claude Van Damme** - Le chat philosophe-karatéka  
   - Expressions: "Moi je suis aware", "L'aigle", "Split !", "C'est ça !"
   - Style: Philosophie musclée déjantée

3. **⚔️ Dictateur** - Le chat autoritaire
   - Expressions: "Ordre et discipline !", "Pour la gloire !", "Vive l'empire !"
   - Style: Autorité humoristique

4. **🚩 Mélenchon** - Le chat révolutionnaire
   - Expressions: "Mes chers concitoyens !", "Peuple de France !", "L'oligarchie !"
   - Style: Rhétorique lyrique et passionnée

5. **🌪️ Taz** - Le chat tornade (Diable de Tasmanie)
   - Expressions: "BRRRRR !", "WOOOOSH !", "TORNADO !", "CHAOS !"
   - Style: Énergie chaotique complètement déjantée

6. **😈 Diable** - Le chat tentateur infernal
   - Expressions: "Muahahaha !", "Vends ton âme !", "Péché capital !"
   - Style: Diabolique mais amusant

7. **🎤 Jul** - Le chat rappeur marseillais
   - Expressions: "Wesh alors !", "C'est le S !", "Marseille bébé !"
   - Style: Rap marseillais unique

8. **😏 Sarcastique** - Le chat cynique original
   - Expressions: "Oh regarde qui parle...", "Tiens tiens...", "Eh bien bien bien..."
   - Style: Ironie et trolling bienveillant

## 🚀 Utilisation

```python
from src.gemini_ai.personality_manager import PersonalityManager
from src.gemini_ai.personalities import PersonalityType

# Créer le gestionnaire
pm = PersonalityManager()

# Forcer une personnalité spécifique
success, message = pm.force_personality(PersonalityType.MACRON)

# Changement aléatoire (avec cooldown)
success, message = pm.change_personality()

# Obtenir le prompt actuel
prompt = pm.get_current_prompt()
```

## ✨ Fonctionnalités

- **🎲 Changements aléatoires** avec système de cooldown (5 minutes)
- **⚡ Changements forcés** pour bypass le cooldown
- **📈 Historique** des 10 dernières personnalités
- **🎪 Messages d'annonce** variés pour chaque personnalité
- **🎯 Phrases d'accroche** spécifiques à chaque personnalité
- **🔧 Architecture modulaire** - un fichier par personnalité

## 🌟 Avantages de la Nouvelle Structure

1. **📂 Organisation claire** - Chaque personnalité dans son propre fichier
2. **🔧 Maintenance facile** - Ajout/modification de personnalités simplifié
3. **🎨 Personnalités authentiques** - Figures françaises reconnaissables
4. **🎭 Variété maximale** - 8 personnalités distinctes avec styles uniques
5. **🚀 Extensibilité** - Ajout de nouvelles personnalités sans impact sur l'existant