import streamlit as st

# Farben wie im Roulette
number_colors = {
    0: 'green', 1: 'red', 2: 'black', 3: 'red', 4: 'black', 5: 'red', 6: 'black',
    7: 'red', 8: 'black', 9: 'red', 10: 'black', 11: 'black', 12: 'red', 13: 'black',
    14: 'red', 15: 'black', 16: 'red', 17: 'black', 18: 'red', 19: 'red', 20: 'black',
    21: 'red', 22: 'black', 23: 'red', 24: 'black', 25: 'red', 26: 'black', 27: 'red',
    28: 'black', 29: 'black', 30: 'red', 31: 'black', 32: 'red', 33: 'black', 34: 'red',
    35: 'black', 36: 'red'
}

st.set_page_config(layout="wide")

# Reset-Funktion
col1, col2 = st.columns([10, 1])
with col2:
    if st.button("🗑️", key="reset"):
        st.session_state.history = []

st.title("🎰 Roulette Quoten")

if "history" not in st.session_state:
    st.session_state.history = []

START_PROB = 1 / 37
MAX_HISTORY = 100

def calculate_probabilities(history):
    counts = {i: history.count(i) for i in range(37)}
    weights = {i: 1 / (counts[i] + 1)**2 for i in range(37)}
    total_weight = sum(weights.values())
    return {i: weights[i] / total_weight for i in range(37)}

def add_number(n):
    st.session_state.history.append(n)
    if len(st.session_state.history) > MAX_HISTORY:
        st.session_state.history = st.session_state.history[-MAX_HISTORY:]

def remove_specific_instance(index):
    if 0 <= index < len(st.session_state.history):
        del st.session_state.history[index]

# --- UI Buttons für Roulette Tisch ---
st.subheader("Roulette-Tisch")

# Zeile 1: 0 zentriert
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
color_0 = number_colors[0]
st.markdown(f"""
    <button style='background-color:{color_0}; color:white; font-weight:bold; font-size:16px; padding:10px; border:none; border-radius:4px;' onclick="document.querySelector('[name=btn_0]').click();">0</button>
""", unsafe_allow_html=True)
if st.button("", key="btn_0"):
    add_number(0)
st.markdown("</div>", unsafe_allow_html=True)

# Weitere Zeilen: je 3 Zahlen nebeneinander
for row_start in range(1, 37, 3):
    cols = st.columns(3)
    for offset in range(3):
        num = row_start + offset
        if num <= 36:
            with cols[offset]:
                color = number_colors[num]
                st.markdown(f"""
                    <button style='background-color:{color}; color:white; font-weight:bold; font-size:16px; width:100%; padding:10px; border:none; border-radius:4px;' onclick="document.querySelector('[name=btn_{num}]').click();">{num}</button>
                """, unsafe_allow_html=True)
                if st.button("", key=f"btn_{num}"):
                    add_number(num)

# --- Wahrscheinlichkeiten berechnen ---
probs = calculate_probabilities(st.session_state.history)

# --- Wahrscheinlich nächste Zahlen ---
st.subheader("Wahrscheinlich nächste Zahlen")
top = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:15]
top_cols = st.columns(5)
for i, (num, p) in enumerate(top):
    color = number_colors[num]
    with top_cols[i % 5]:
        st.markdown(f"""
            <div style='text-align: center; border: 1px solid #ccc; border-radius: 5px; padding: 8px; margin: 4px; background-color:{color}; color:white;'>
                <b style='font-size: 18px'>{num}</b><br>
                <small>{p*100:.1f}%</small>
            </div>
        """, unsafe_allow_html=True)

# --- Letzte Zahlen anzeigen ---
st.subheader("Letzte Zahlen")
if st.session_state.history:
    reversed_history = list(reversed(st.session_state.history))
    cols = st.columns(min(len(reversed_history), 20))
    for i, num in enumerate(reversed_history):
        color = number_colors[num]
        with cols[i % 20]:
            if st.button(f"{num}", key=f"hist_{len(st.session_state.history) - 1 - i}"):
                remove_specific_instance(len(st.session_state.history) - 1 - i)
