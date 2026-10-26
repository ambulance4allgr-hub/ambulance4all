import streamlit as st
import time
from datetime import datetime, timedelta
import uuid

st.set_page_config(page_title="Κέντρο Ελέγχου Εταιρείας", layout="wide")
st.sidebar.title("Μενού Εφαρμογής")
menu = st.sidebar.radio("Επιλέξτε Ενότητα:", ["🏠 Αρχική", "🚑 Live Παρακολούθηση", "📋 Πρόγραμμα Διακομιδών"])

# Αρχικοποίηση δεδομένων
if "names" not in st.session_state:
    st.session_state.names = ["Τ12", "Τ16", "Τ16Β", "Τ16Δ", "Ασθενοφόρο 5", "Ασθενοφόρο 6"]

if "amb" not in st.session_state:
    st.session_state.amb = {}
    for i in range(1, 7):
        st.session_state.amb[i] = {"crew": "", "origin": "", "dest": "", "target": None, "total_mins": 0, "active": False}

if "trips" not in st.session_state:
    st.session_state.trips = []

# ==========================================
# ΑΡΧΙΚΗ ΣΕΛΙΔΑ
# ==========================================
if menu == "🏠 Αρχική":
    st.markdown("<h1 style='text-align: center; color: #FF4B4B; font-size: 50px;'>🚑 Καλώς ήρθατε</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #555;'>Ηγετική Παρουσία στις Υπηρεσίες Υγείας και Διακομιδών</h3>", unsafe_allow_html=True)
    st.write("---")
    
    st.markdown("""
    ### 🏆 Το Όραμά μας
    Στην εταιρεία μας, δεσμευόμαστε στην παροχή υπηρεσιών διακομιδής και άμεσης ανταπόκρισης υψηλών προδιαγραφών. Θέτουμε ως προτεραιότητα την ασφάλεια, την αξιοπιστία και την άριστη εξυπηρέτηση των ασθενών, αποτελώντας τον αξιόπιστο συνεργάτη των νοσηλευτικών ιδρυμάτων και των οικογενειών.

    ### 🚑 Σύγχρονος Στόλος & Τεχνολογία
    Επενδύουμε διαρκώς στον εκσυγχρονισμό του εξοπλισμού μας. Ο στόλος των ασθενοφόρων μας τηρεί τις αυστηρότερες προδιαγραφές ασφαλείας και είναι εξοπλισμένος με προηγμένα συστήματα ιατρικής υποστήριξης. Κάθε μεταφορά πραγματοποιείται με γνώμονα τη μέγιστη δυνατή φροντίδα και άνεση για τον ασθενή.

    ### 👨‍⚕️ Εξειδικευμένο Ανθρώπινο Δυναμικό
    Η δύναμή μας έγκειται στους ανθρώπους μας. Τα πληρώματα των ασθενοφόρων στελεχώνονται αποκλειστικά από πιστοποιημένους διασώστες και έμπειρους οδηγούς. Με υψηλό αίσθημα ευθύνης και επαγγελματισμό, διαχειρίζονται κάθε περιστατικό με ακρίβεια, εχεμύθεια και σεβασμό προς τον άνθρωπο.

    ### ⏱️ Διαθεσιμότητα 24/7
    Αντιλαμβανόμαστε ότι οι ανάγκες για μεταφορά ασθενών δεν έχουν ωράριο. Γι' αυτόν τον λόγο, οι υπηρεσίες μας βρίσκονται σε πλήρη επιχειρησιακή ετοιμότητα **24 ώρες το 24ωρο, 365 ημέρες τον χρόνο**, έτοιμες να ανταποκριθούν άμεσα και αποτελεσματικά σε κάθε κάλεσμα.
    """)

# ==========================================
# LIVE ΠΑΡΑΚΟΛΟΥΘΗΣΗ
# ==========================================
elif menu == "🚑 Live Παρακολούθηση":
    st.title("🚑 Κέντρο Παρακολούθησης Ασθενοφόρων")
    
    # Εδώ επιτρέπουμε την αλλαγή ονόματος με απλό τρόπο
    with st.expander("⚙️ Επεξεργασία Ονομάτων Στόλου (Πατήστε για άνοιγμα)"):
        c1, c2 = st.columns(2)
        with c1:
            st.session_state.names[0] = st.text_input("Όνομα 1ου", st.session_state.names[0])
            st.session_state.names[1] = st.text_input("Όνομα 2ου", st.session_state.names[1])
            st.session_state.names[2] = st.text_input("Όνομα 3ου", st.session_state.names[2])
        with c2:
            st.session_state.names[3] = st.text_input("Όνομα 4ου", st.session_state.names[3])
            st.session_state.names[4] = st.text_input("Όνομα 5ου", st.session_state.names[4])
            st.session_state.names[5] = st.text_input("Όνομα 6ου", st.session_state.names[5])
        st.info("Οι αλλαγές αποθηκεύονται αυτόματα.")

    @st.fragment(run_every=1.0)
    def draw_ambulances():
        for i in range(1, 7):
            a = st.session_state.amb[i]
            with st.container(border=True):
                if not a["active"]:
                    c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 0.8])
                    with c1:
                        a["crew"] = st.text_input("Πλήρωμα", value=a["crew"], key=f"c_{i}", placeholder="Ονόματα")
                    with c2:
                        a["origin"] = st.text_input("Από", key=f"o_{i}")
                    with c3:
                        a["dest"] = st.text_input("Προς", key=f"d_{i}")
                    with c4:
                        mins = st.number_input("Λεπτά", min_value=1, max_value=180, value=15, key=f"m_{i}")
                    with c5:
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
                    st.markdown(f"### 🚑 {st.session_state.names[i-1]}")
                else:
                    st.markdown(f"### 🚑 {st.session_state.names[i-1]}")
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

# ==========================================
# ΠΡΟΓΡΑΜΜΑ ΔΙΑΚΟΜΙΔΩΝ
# ==========================================
elif menu == "📋 Πρόγραμμα Διακομιδών":
    st.title("📋 Πρόγραμμα Διακομιδών")
    
    with st.form("trip_form", clear_on_submit=True):
        st.subheader("Καταχώρηση Νέας Διακομιδής")
        patient = st.text_input("Όνομα Ασθενούς")
        trip_date = st.date_input("Ημερομηνία")
        trip_time = st.text_input("Ώρα Έναρξης")
        trip_end = st.text_input("Ώρα Τέλους")
        from_loc = st.text_input("Από")
        to_loc = st.text_input("Προς")
        # Εδώ διαλέγεις από τα ονόματα που έφτιαξες
        amb_choice = st.selectbox("Επιλογή Ασθενοφόρου", st.session_state.names)
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
        st.subheader("Πρόγραμμα ανά Ασθενοφόρο")
        # 6 στήλες
        cols = st.columns(6)
        
        for idx, amb_name in enumerate(st.session_state.names):
            with cols[idx]:
                st.markdown(f"### 🚑 {amb_name}")
                amb_trips = [t for t in st.session_state.trips if t['amb'] == amb_name]
                amb_trips = sorted(amb_trips, key=lambda x: (str(x['date']), str(x['time'])))
                
                if not amb_trips:
                    st.write("Κενό.")
                else:
                    for trip in amb_trips:
                        st.text(f"📅 {trip['date']}")
                        st.text(f"🕒 {trip['time']} - {trip['end']}")
                        st.text(f"👤 {trip['patient']}")
                        st.text(f"📍 Από: {trip['from']}")
                        st.text(f"🏁 Προς: {trip['to']}")
                        
                        if trip.get('notes'):
                            st.text(f"📝 {trip['notes']}")
                            
                        if st.button("🗑️ Διαγραφή", key=f"del_{trip['id']}"):
                            st.session_state.trips = [t for t in st.session_state.trips if str(t['id']) != str(trip['id'])]
                            st.rerun()
                        st.write("---")
