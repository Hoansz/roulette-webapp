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

# --- Wahrscheinlichkeiten berechnen ---
probs = calculate_probabilities(st.session_state.history)

# --- UI Buttons für Roulette Tisch ---
st.subheader("Roulette-Tisch")

# Zeile 1: 0 zentriert
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if st.button("0", key="btn_0"):
    add_number(0)
st.markdown("</div>", unsafe_allow_html=True)

# Weitere Zeilen: 3 Zahlen pro Zeile von links nach rechts
for row_start in range(1, 37, 3):
    row_numbers = [n for n in range(row_start, min(row_start + 3, 37))]
    cols = st.columns(len(row_numbers))
    for col, num in zip(cols, row_numbers):
        color = number_colors[num]
        with col:
            if st.button(f"{num}", key=f"btn_{num}"):
                add_number(num)

# --- Wahrscheinlich nächste Zahlen ---
st.subheader("Wahrscheinlich nächste Zahlen")
top = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:15]
top_cols = st.columns(5)
for i, (num, p) in enumerate(top):
    color = number_colors[num]
    with top_cols[i % 5]:
        st.markdown(f"""
            <div style='text-align: center;'>
                <b style='color:{color}; font-size: 18px'>{num}</b><br>
                <small>{p*100:.1f}%</small>
            </div>
        """, unsafe_allow_html=True)

# --- Letzte Zahlen anzeigen ---
st.subheader("Letzte Zahlen")
if st.session_state.history:
    reversed_history = list(reversed(st.session_state.history))
    max_per_row = 20
    rows = [reversed_history[i:i+max_per_row] for i in range(0, len(reversed_history), max_per_row)]
    for row_index, row in enumerate(rows):
        st.markdown("<div style='display: flex; gap: 2px;'>", unsafe_allow_html=True)
        for i, num in enumerate(row):
            color = number_colors[num]
            idx = len(st.session_state.history) - 1 - (row_index * max_per_row + i)
            if st.button(f"{num}", key=f"hist_{idx}"):
                remove_specific_instance(idx)
        st.markdown("</div>", unsafe_allow_html=True)
