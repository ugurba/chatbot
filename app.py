import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Ugur Balci - Assistant IA",
    layout="centered"
)

# --- STYLE CSS (Look Portfolio) ---
st.markdown("""
    <style>
    .main {background-color: #f9f9f9;}
    h1 {color: #2C3E50;}
    .stChatMessage {border-radius: 15px;}
    /* Style pour les liens du sidebar */
    a {text-decoration: none; color: #2980b9; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (infos de contact) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=100) # Tu pourras mettre ta photo ici
    st.title("Ugur Balci")
    st.markdown("**Ingénieur Data & IA**")
    st.markdown("📍 Toulouse, France")
    st.markdown("📧 [ugur.balci@utoulouse.fr](mailto:ugur.balci@utoulouse.fr)")
    st.markdown("🔗 [LinkedIn](https://linkedin.com/in/ugur-balci84700)")
    st.markdown("🐙 [GitHub](https://github.com/ugurba)")
    st.divider()
    
    # Champ clé API
    api_key = st.text_input("Clé API Google Gemini:", type="password")
    if not api_key:
        st.warning("Entrez votre clé pour discuter.")

# --- CONTEXTE DU CV  ---
CV_CONTEXT = """
TU ES L'ASSISTANT VIRTUEL DE UGUR BALCI.
Ton but est de présenter son profil aux recruteurs de manière professionnelle et engageante.
Réponds aux questions en te basant UNIQUEMENT sur les informations ci-dessous.

--- PROFIL ---
Ugur Balci est un Ingénieur Data & IA, actuellement étudiant en Master "Interactions Informatique & Mathématiques pour l'IA" à l'Université de Toulouse (2024-2026).
Il recherche un stage de fin d'études (6 mois) ou un poste junior à partir d'Avril 2026.

--- COMPÉTENCES TECHNIQUES ---
- Langages : Python (Expert), C++, C#, Java, SQL, R.
- Machine Learning : XGBoost, Random Forest, SVM, LightGBM.
- Deep Learning : PyTorch, TensorFlow, CNN, RNN, LSTM, Transformers, GANs.
- NLP (Spécialité) : BERT, GPT, Tokenization, Embeddings, LLMs.
- Big Data / MLOps : Spark, Docker, GCP (Google Cloud), Azure, AWS, CI/CD.
- Visualisation : Power BI, Tableau, Matplotlib.

--- EXPÉRIENCES PROFESSIONNELLES ---
1. Stagiaire NLP & IA - IRIT / ENAC (Toulouse)
   - Sujet : Analyse des biais des LLMs (BERT, GPT) sur les expressions idiomatiques.
   - Réalisation : Création d'outils de visualisation pour interpréter le raisonnement de l'IA.

2. Stagiaire Data Scientist - IRIT (Toulouse, Juin-Août 2025)
   - Développement de modèles prédictifs pour séries temporelles.
   - Comparaison de modèles : Random Forest vs XGBoost vs LSTM.

3. Stagiaire Machine Learning - Université de Toulon (2024)
   - Conception de réseaux de neurones (CNN) pour la classification d'images sous PyTorch.
   - Utilisation de Data Augmentation et Transfer Learning.

4. Président & Co-fondateur - IMPHAIR (2021-Présent)
   - Création d'une startup (plateforme de comparaison cliniques/hôtels).
   - Développement d'algorithmes de matching et gestion stratégique.

--- FORMATION ---
- Master Interactions Informatique & Mathématiques pour l'IA - Université de Toulouse (En cours).
- Master Mathématiques Appliquées - Université de Toulon.
- Licence Mathématiques & Informatique - Avignon Université.
- CPGE (Prépa) PCSI/PSI - Lycée Frédéric Mistral.

--- LANGUES ---
- Français : Natif
- Turc : Natif
- Anglais : C1 (Avancé)
- Allemand : B1

--- CONTACT (Si demandé) ---
- Email : ugur.balci@utoulouse.fr
- Téléphone : +33 6 67 24 41 40
- LinkedIn : https://linkedin.com/in/ugur-balci
- GitHub : https://github.com/ugurba
- Portfolio Web : https://ugurba.github.io/Balci
- Localisation : Toulouse, France

"""

# --- INTERFACE DE CHAT ---
st.title("🤖 Chat with Ugur's Bot")
st.write("Bonjour ! Je suis l'assistant IA de Ugur. Posez-moi des questions sur son parcours, ses compétences ou ses projets.")

# Initialisation historique
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour ! Je peux vous parler de mes compétences, de mon expérience ou de mes projets personnels. Qu'est-ce qui vous intéresse ?"}]

# Affichage des messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Gestion de la saisie utilisateur
if prompt := st.chat_input("Ex: Quelles sont tes compétences en Python ?"):
    if not api_key:
        st.error("🔒 Veuillez entrer la clé API dans le menu à gauche pour activer le bot.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        try:
            # Configuration du modèle
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash') 
            
            with st.spinner("Ugur est en train de réfléchir..."):
                response = model.generate_content(f"{CV_CONTEXT}\n\nQuestion du recruteur: {prompt}")
                
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.chat_message("assistant").write(response.text)

        except Exception as e:
            st.error(f"Erreur : {e}")

            st.info("Astuce : Vérifiez que le nom du modèle (ligne 85) est bien celui qui fonctionne pour votre clé.")
