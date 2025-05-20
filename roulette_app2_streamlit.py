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

st.title("🎰 Roulette Quoten")

if "history" not in st.session_state:
    st.session_state.history = []

START_PROB = 1 / 37
MAX_HISTORY = 100

def calculate_probabilities():
    counts = {i: st.session_state.history.count(i) for i in range(37)}
    weights = {i: 1 / (counts[i] + 1)**2 for i in range(37)}
    total_weight = sum(weights.values())
    return {i: weights[i] / total_weight for i in range(37)}

def add_number(n):
    st.session_state.history.append(n)
    if len(st.session_state.history) > MAX_HISTORY:
        st.session_state.history = st.session_state.history[-MAX_HISTORY:]

def remove_last_instance(n):
    for i in range(len(st.session_state.history)):
        if st.session_state.history[i] == n:
            del st.session_state.history[i]
            break

probs = calculate_probabilities()

# --- Roulette-Tisch Darstellung ---
st.subheader("Roulette-Tisch")

# Zeile 1: 0 zentriert
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if st.button("0", key="btn_0"):
    add_number(0)
st.markdown("</div>", unsafe_allow_html=True)

# Weitere Zeilen: je 3 Zahlen nebeneinander
for row_start in range(1, 37, 3):
    cols = st.columns(3)
    for offset in range(3):
        num = row_start + offset
        if num <= 36:
            with cols[offset]:
                if st.button(str(num), key=f"btn_{num}"):
                    add_number(num)

# --- Wahrscheinlich nächste Zahlen ---
st.subheader("Wahrscheinlich nächste Zahlen")
top = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:15]
top_cols = st.columns(5)
for i, (num, p) in enumerate(top):
    color = number_colors[num]
    with top_cols[i % 5]:
        st.markdown(f"""
            <div style='text-align: center; border: 1px solid #ccc; border-radius: 5px; padding: 8px; margin: 4px;'>
                <b style='color:{color}; font-size: 18px'>{num}</b><br>
                <small>{p*100:.1f}%</small>
            </div>
        """, unsafe_allow_html=True)

# --- Letzte Zahlen anzeigen ---
st.subheader("Letzte Zahlen")
if st.session_state.history:
    cols = st.columns(min(len(st.session_state.history), 20))
    for i, num in enumerate(st.session_state.history):
        color = number_colors[num]
        with cols[i % 20]:
            if st.button(str(num), key=f"hist_{i}"):
                remove_last_instance(num)
