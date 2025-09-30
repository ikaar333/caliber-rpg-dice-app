import streamlit as st
import random
import pandas as pd

# --- Fonction pour simuler un lancer de dés ---
def lancer_de(delta, m):
    seuil = max(2, min(19, 11 - delta))  # borne 2..19
    d20 = random.randint(1, 20)
    fate_faces = ["+", "+", "-", "-", "ѳ", "ѳ"]
    fate = random.choice(fate_faces)

    # Résultat de base
    if d20 == 1:
        base_result = "Échec [E]"
    elif d20 == 20:
        base_result = "Réussite [R]"
    elif (d20 + m) >= seuil:
        base_result = "Réussite [R]"
    else:
        base_result = "Échec [E]"

    # Application du dé d’aléa
    if fate == "ѳ":
        final_result = base_result
    elif fate == "+":
        final_result = "Réussite améliorée [R+] (Oui, et)" if "R" in base_result else "Échec atténué [E+] (Non, mais)"
    elif fate == "-":
        final_result = "Réussite affaiblie [R-] (Oui, mais)" if "R" in base_result else "Échec aggravé [E-] (Non, et)"

    return d20, m, seuil, fate, final_result

# --- Interface Streamlit ---
st.set_page_config(page_title="🎲 Lanceur de dés RPG", page_icon="🎲", layout="centered")
st.title("🎲 Lanceur de dés RPG (D20 + Dé d'aléa)")

# Info sur les bornes des paramètres
st.info(
    """
    ℹ️ **Règles des paramètres :**
    - **Écart de niveau (Δ)** : entre **-10** et **+10** (incluant 0).  
    - **Variable (m)** : valeurs possibles **-4, -3, -2, -1, 0, 1, 2, 3, 4**.  
    """
)

# Rappel de lecture des résultats
st.markdown(
    """
    ### 📝 Guide de lecture des résultats :
    - **Réussite [R]** → Oui  
    - **Échec [E]** → Non  
    - **Réussite améliorée [R+]** → Oui, et...  
    - **Réussite affaiblie [R-]** → Oui, mais...  
    - **Échec atténué [E+]** → Non, mais...  
    - **Échec aggravé [E-]** → Non, et...  
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
        d20_val, m_val, seuil_val, fate_val, final_result_val = lancer_de(delta, m)
        résultats.append({
            "Lancer #": i + 1,
            "D20": d20_val,
            "Variable (m)": m_val,
            "Seuil": seuil_val,
            "Dé d'aléa": fate_val,
            "Résultat final": final_result_val
        })

    df = pd.DataFrame(résultats)

    # Coloration réussites/échecs
    def color_result(val):
        if "Réussite" in val:
            return "background-color: #c6f6d5"
        elif "Échec" in val:
            return "background-color: #fed7d7"
        return ""

    styled_df = df.style.applymap(color_result, subset=["Résultat final"])
    st.subheader("📊 Résultats")
    st.dataframe(styled_df, use_container_width=True)
