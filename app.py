import streamlit as st
import time
from datetime import datetime, timedelta
import uuid
import json
import os

st.set_page_config(page_title="Κέντρο Ελέγχου Εταιρείας", layout="wide")
st.sidebar.title("Μενού Εφαρμογής")
menu = st.sidebar.radio("Επιλέξτε Ενότητα:", ["🏠 Αρχική", "🚑 Live Παρακολούθηση", "📋 Πρόγραμμα Διακομιδών"])

NAMES_FILE = "names.json"

# --- ΣΥΣΤΗΜΑ ΑΠΟΘΗΚΕΥΣΗΣ ΟΝΟΜΑΤΩΝ ---
def load_names():
    default_names = ["Τ12", "Τ16", "Τ16Β", "Τ16Δ", "Νέο 5", "Νέο 6"]
    if os.path.exists(NAMES_FILE):
        try:
            with open(NAMES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if len(data) == 6:
                    return data
                else:
                    return default_names
        except:
            return default_names
    return default_names

def save_names(names):
    with open(NAMES_FILE, "w", encoding="utf-8") as f:
        json.dump(names, f, ensure_ascii=False)

if "amb_names" not in st.session_state:
    st.session_state.amb_names = load_names()

if "amb" not in st.session_state:
    st.session_state.amb = {}
    for i in range(1, 7):
        st.session_state.amb[i] = {"crew": "", "origin": "", "dest": "", "target": None, "total_mins": 0, "active": False}

if "trips" not in st.session_state:
    st.session_state.trips = []

if menu == "🏠 Αρχική":
    st.markdown("<h1 style='text-align: center; color: #FF4B4B; font-size: 50px;'>🚑 Καλώς ήρθατε στην Εταιρεία μας</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #555;'>Η Νούμερο 1 Επιλογή στην Άμεση Ανταπόκριση και τις Διακομιδές</h3>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("""
    ### 🏆 Η Αριστεία είναι ο Πρότυπό μας
    Στην **Εταιρεία μας**, δεν κάνουμε απλώς τη δουλειά μας· θέτουμε τα πρότυπα της αγοράς. Είμαστε περήφανοι που θεωρούμαστε οι **απόλυτοι ηγέτες** στον τομέα των υπηρεσιών υγείας και διακομιδών.
    Διαθέτουμε τον **πιο σύγχρονο και άρτια εξοπλισμένο στόλο ασθενοφόρων** στην περιοχή. Κάθε όχημά μας είναι ένα κινούμενο κέντρο εντατικής φροντίδας.
    Πίσω από το τιμόνι βρίσκονται τα **πιο έμπειρα και καταρτισμένα πληρώματα**. Λειτουργούμε **24 ώρες το 24ωρο, 7 ημέρες την εβδομάδα**.
    """)
    st.write("---")
    st.success("👈 Χρησιμοποιήστε το μενού στα αριστερά για να μεταβείτε στις άλλες ενότητες.")

elif menu == "🚑 Live Παρακολούθηση":
    st.title("🚑 Κέντρο Παρακολούθησης Ασθενοφόρων")
    
    @st.fragment(run_every=1.0)
    def draw_ambulances():
        for i in range(1, 7):
            a = st.session_state.amb[i]
            with st.container(border=True):
                if not a["active"]:
                    c1, c2, c3, c4, c5, c6 = st.columns([1.2, 1, 1, 1, 0.8, 0.5])
                    with c1:
                        new_name = st.text_input("Όνομα", value=st.session_state.amb_names[i-1], key=f"n_{i}")
                        if new_name != st.session_state.amb_names[i-1]:
                            st.session_state.amb_names[i-1] = new_name
                            save_names(st.session_state.amb_names)
                    with c2:
                        a["crew"] = st.text_input("Πλήρωμα", value=a["crew"], key=f"c_{i}", placeholder="Ονόματα")
                    with c3:
                        a["origin"] = st.text_input("Από", key=f"o_{i}")
                    with c4:
                        a["dest"] = st.text_input("Προς", key=f"d_{i}")
                    with c5:
                        mins = st.number_input("Λεπτά", min_value=1, max_value=180, value=15, key=f"m_{i}")
                    with c6:
                        st.write("")
                        st.write("")
                        if st.button("▶", key=f"b_{i}", use_container_width=True, type="primary"):
                            if a["origin"] and a["dest"]:
                                a["total_mins"] = mins
                                a["target"] = datetime.now() + timedelta(minutes=mins)
                                a["active"] = True
                                st.rerun()
                            else:
                                st.warning("Συμπλήρωσε διαδρομή.")
                    st.markdown(f"### 🚑 {st.session_state.amb_names[i-1]}")
                else:
                    st.markdown(f"### 🚑 {st.session_state.amb_names[i-1]}")
                    col_info, col_prog, col_timer, col_btn = st.columns([2, 1.5, 1.2, 0.8])
                    with col_info:
                        if a["crew"]:
                            st.caption(f"👥 {a['crew']}")
                        st.caption(f"📍 {a['origin']} ➔ {a['dest']}")
                    with col_prog:
                        st.write("") 
                        remaining = max(0, int((a["target"] - datetime.now()).total_seconds()))
                        total_secs = a["total_mins"] * 60
                        prog = 1 - (remaining / total_secs) if total_secs > 0 else 0
                        st.progress(min(max(prog, 0.0), 1.0))
                    with col_timer:
                        if remaining > 0:
                            m, s = divmod(remaining, 60)
                            st.markdown(f"<div style='font-size: 35px; font-weight: bold; text-align: center; color: #FF4B4B; font-family: monospace;'>{m:02d}:{s:02d}</div>", unsafe_allow_html=True)
                        else:
                            st.success("✅ Έφτασε!")
                    with col_btn:
                        st.write("")
                        if st.button("⏹", key=f"s_{i}", use_container_width=True):
                            a["active"] = False
                            a["target"] = None
                            st.rerun()
    draw_ambulances()

elif menu == "📋 Πρόγραμμα Διακομιδών":
    st.title("📋 Πρόγραμμα Διακομιδών")
    st.subheader("Καταχώρηση Νέας Διακομιδής")
    
    with st.form("trip_form", clear_on_submit=True):
        patient = st.text_input("Όνομα Ασθενούς")
        trip_date = st.date_input("Ημερομηνία")
        trip_time = st.text_input("Ώρα Έναρξης")
        trip_end = st.text_input("Ώρα Τέλους")
        from_loc = st.text_input("Από")
        to_loc = st.text_input("Προς")
        amb_choice = st.selectbox("Επιλογή Ασθενοφόρου", st.session_state.amb_names)
        notes = st.text_input("Σημειώσεις")
        
        if st.form_submit_button("Καταχώρηση", type="primary"):
            if patient and from_loc and to_loc:
                new_trip = {"id": str(uuid.uuid4()), "date": str(trip_date), "time": trip_time, "end": trip_end, "patient": patient, "from": from_loc, "to": to_loc, "amb": amb_choice, "notes": notes}
                st.session_state.trips.append(new_trip)
                st.success(f"Καταχωρήθηκε για το {amb_choice}!")
            else:
                st.error("Συμπλήρωσε Ασθενή, Από και Προς.")

    st.divider()
    
    if not st.session_state.trips:
        st.info("Δεν υπάρχουν προγραμματισμένες διακομιδές.")
    else:
        st.subhe
