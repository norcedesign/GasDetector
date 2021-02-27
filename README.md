# Gas detector
Application temps réel pour la détection de fuite de gaz en milieu industriel. Cette logiciel développé en pythnon est embarqué sur un Raspberry Pi.

## Système de détection
a) Ce programme détecte la présence de 3 type de gaz (qui peuvent être CO2, CO, O3, CH4, etc.)

b) Le système affiche un niveau d'alerte (Low, Medium, High) en fonction de la concentration de gaz

## Système de commande
c) Le système réagit à la fuite de gaz par 3 types d'action:
  - Aération à trois niveaux
  - Ventilation à deux niveaux
  - Injection de gaz

