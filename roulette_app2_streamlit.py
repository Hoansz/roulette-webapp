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
st.markdown("""
    <style>
        .grid-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 20px;
        }
        .grid-row {
            display: flex;
            gap: 8px;
            margin: 4px 0;
        }
        .number-button {
            width: 60px;
            height: 60px;
            font-size: 16px;
            font-weight: bold;
            border: 1px solid #ccc;
            border-radius: 6px;
            background-color: white;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

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
    for i in reversed(range(len(st.session_state.history))):
        if st.session_state.history[i] == n:
            del st.session_state.history[i]
            break

probs = calculate_probabilities()

# --- Roulette-Tisch Darstellung ---
st.subheader("Roulette-Tisch")
st.markdown("<div class='grid-container'>", unsafe_allow_html=True)

# Zeile 1: 0 zentriert
st.markdown("<div class='grid-row' style='justify-content: center;'>", unsafe_allow_html=True)
col_zero = st.columns(1)
with col_zero[0]:
    if st.button("0", key="btn_0"):
        add_number(0)
    st.markdown("<div class='number-button'>0</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Weitere Zeilen: je 3 Zahlen nebeneinander
for row_start in range(1, 37, 3):
    st.markdown("<div class='grid-row'>", unsafe_allow_html=True)
    row_cols = st.columns(3)
    for offset in range(3):
        num = row_start + offset
        if num <= 36:
            with row_cols[offset]:
                if st.button(str(num), key=f"btn_{num}"):
                    add_number(num)
                st.markdown(f"<div class='number-button'>{num}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- Wahrscheinlich nächste Zahlen ---
st.subheader("Wahrscheinlich nächste Zahlen")
top = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:15]
top_cols = st.columns(5)
for i, (num, p) in enumerate(top):
    color = number_colors[num]
    with top_cols[i % 5]:
        st.markdown(f"""
            <div class='number-button' style='background-color:{color}; color:white;'>
                <b>{num}</b><br><small>{p*100:.1f}%</small>
            </div>
        """, unsafe_allow_html=True)

# --- Verlauf anzeigen ---
st.subheader("Letzte Zahlen")
reversed_hist = list(reversed(st.session_state.history))
rows = [reversed_hist[i:i+20] for i in range(0, len(reversed_hist), 20)]
for row in rows:
    st.write(" ".join(str(n) for n in row))
