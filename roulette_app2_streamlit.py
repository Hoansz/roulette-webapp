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
        .number-grid {
            display: grid;
            grid-template-columns: repeat(3, 50px);
            gap: 4px;
            justify-content: center;
        }
        .number-box {
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 6px;
            text-align: center;
            font-size: 14px;
            cursor: pointer;
            background-color: white;
        }
        .number-box:hover {
            background-color: #eee;
        }
        .history-box {
            display: inline-block;
            width: 32px;
            height: 32px;
            line-height: 32px;
            margin: 2px;
            text-align: center;
            border-radius: 4px;
            font-size: 13px;
            font-weight: bold;
            color: white;
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

st.subheader("Roulette Tisch")

# 0 in der Mitte über den restlichen Zahlen
st.markdown("<div style='text-align:center'><b>0</b></div>", unsafe_allow_html=True)
if st.button("0", key="btn_0"):
    add_number(0)
st.caption(f"{probs[0]*100:.1f}%")

# Zahlen 1–36 in 3 Spalten von unten nach oben
st.markdown("<div class='number-grid'>", unsafe_allow_html=True)
for row in range(12):
    for col in range(3):
        num = row * 3 + col + 1
        if num <= 36:
            if st.button(str(num), key=f"btn_{num}"):
                add_number(num)
            st.markdown(f"<div class='number-box'>{num}<br><small>{probs[num]*100:.1f}%</small></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.subheader("Wahrscheinlich nächste Zahlen")
top = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:15]
top_cols = st.columns(5)
for i, (num, p) in enumerate(top):
    color = number_colors[num]
    with top_cols[i % 5]:
        st.markdown(f"""
            <div class='number-box' style='background-color:{color}; color:white;'>
                <b>{num}</b><br><small>{p*100:.1f}%</small>
            </div>
        """, unsafe_allow_html=True)

st.subheader("Letzte Zahlen")
reversed_hist = list(reversed(st.session_state.history))
rows = [reversed_hist[i:i+20] for i in range(0, len(reversed_hist), 20)]
for row in rows:
    for num in row:
        color = number_colors[num]
        st.markdown(f"<span class='history-box' style='background-color:{color};'>{num}</span>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)