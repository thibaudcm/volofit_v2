# ✈️ VoloFit

**VoloFit** est une application interactive développée avec **Streamlit** qui aide à choisir la meilleure combinaison d'avions pour répondre à une demande passager et cargo sur un trajet de 24 heures maximum, pour le jeu Airlines Manager.  
Elle prend en compte les capacités des avions, les vitesses de croisière et les préférences (vitesse minimale, remplissage optimal...).

Teste le ici : volofit.streamlit.app

---

## 🚀 Fonctionnalités

- 🎯 Entrée personnalisée de la demande : Éco, Affaires, Première, Cargo  
- 📊 Calcul automatique des équivalents sièges  
- 🧠 Sélection optimisée de 1 ou 2 avions pour répondre au mieux à la demande  
- 📦 Affichage clair de la combinaison retenue  
- 📱 Responsive : fonctionne sur téléphone, tablette ou PC  
- 💡 Mode "Planning serré" pour privilégier les avions rapides

---

## ⚙️ Lancer l'application

### Prérequis

- Python ≥ 3.8
- Streamlit
- Pandas

### Installation

```bash
git clone https://github.com/thibaudcm/volofit.git
cd volofit
pip install -r requirements.txt
