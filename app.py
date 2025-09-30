import streamlit as st
import random
import pandas as pd

# --- Fonction pour simuler un lancer de dés ---
def lancer_de(delta, m):
    seuil = max(2, min(19, 11 - delta))  # borne 2..19
    d20 = random.randint(1, 20)
    total = d20 + delta + m  # Total inclut maintenant Δ + m + D20
    fate_faces = ["+", "+", "-", "-", "ѳ", "ѳ"]
    fate = random.choice(fate_faces)

    # Résultat de base
    if d20 == 1:
        base_result = "Échec [E]"
    elif d20 == 20:
        base_result = "Réussite [R]"
    elif total >= 11:  # seuil 11 pour la réussite
        base_result = "Réussite [R]"
    else:
        base_result = "Échec [E]"

    # Application du dé d’aléa
    if fate == "ѳ":
        final_result = base_result
    elif fate == "+":
        final_result = "R+ (Oui, et)" if "R" in base_result else "E+ (Non, mais)"
    elif fate == "-":
        final_result = "R- (Oui, mais)" if "R" in base_result else "E- (Non, et)"

    # Succès par rapport au seuil de 11
    succès_seuil = "Oui" if total >= 11 else "Non"

    return delta, d20, m, total, fate, final_result, succès_seuil

# --- Interface Streamlit ---
st.set_page_config(page_title="🎲 Lanceur de dés RPG", page_icon="🎲", layout="centered")
st.title("🎲 Lanceur de dés RPG (D20 + Δ + Dé d'aléa)")

# Explications des paramètres
st.info(
    """
    ℹ️ **Règles des paramètres :**
    - **Écart de niveau (Δ)** : entre **-10** et **+10** (0 inclus).  
    - **Variable (m)** : valeurs possibles **-4, -3, -2, -1, 0, 1, 2, 3, 4**.  
    """
)

# Explication du dé d'aléa
st.info(
    """
    🎲 **Dé d'aléa (Fate Die)** :
    - `ѳ` → pas de modification du résultat de base  
    - `+` → améliore la réussite ou atténue l’échec  
    - `-` → affaiblit la réussite ou aggrave l’échec  
    """
)

# Rappel de lecture des résultats
st.markdown(
    """
    ### 📝 Lecture des résultats :
    - **R** → Oui  
    - **E** → Non  
    - **R+** → Oui, et...  
    - **R-** → Oui, mais...  
    - **E+** → Non, mais...  
    - **E-** → Non, et...  
    """,
    unsafe_allow_html=True
)

# Entrées utilisateur
col1, col2, col3 = st.columns(3)
with col1:
    delta = st.number_input("Écart de niveau (Δ)", min_value=-10, max_value=10, value=0)
with col2:
    m = st.selectbox("Variable (m)", options=[-4, -3, -2, -1, 0, 1, 2, 3, 4], index=4)
with col3:
    n_lancers = st.number_input("Nombre de lancers", min_value=1, max_value=50, value=1)

# Bouton pour lancer les dés
if st.button("🎲 Lancer les dés !"):
    résultats = []
    for i in range(n_lancers):
        delta_val, d20_val, m_val, total_val, fate_val, final_result_val, succès_val = lancer_de(delta, m)
        résultats.append({
            "Δ": delta_val,
            "D20": d20_val,
            "m": m_val,
            "Total": total_val,
            "Succès Δ≥11": succès_val,
            "Fate": fate_val,
            "Résultat": final_result_val
        })

    df = pd.DataFrame(résultats)

    # Coloration réussites/échecs
    def color_result(val):
        if "R" in val:
            return "background-color: #c6f6d5"
        elif "E" in val:
            return "background-color: #fed7d7"
        return ""

    styled_df = df.style.applymap(color_result, subset=["Résultat"])

    st.subheader("📊 Résultats")
    st.dataframe(styled_df, use_container_width=True, height=400)

    # Bouton pour télécharger les résultats
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="💾 Télécharger les résultats en CSV",
        data=csv,
        file_name='resultats_lancers.csv',
        mime='text/csv'
    )
