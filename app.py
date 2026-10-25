import streamlit as st
import pandas as pd

# Ορισμός βασικών πληροφοριών σελίδας
st.set_page_config(page_title="Ambulance 4 All", layout="wide")

# Προσομοίωση δεδομένων (αργότερα μπορούν να αντικατασταθούν με πραγματική βάση δεδομένων)
if 'vehicles' not in st.session_state:
    st.session_state.vehicles = pd.DataFrame({
        "Πινακίδα": ["ΙΧΑ-1234", "ΙΧΑ-5678", "ΙΧΑ-9012", "ΙΧΑ-3456"],
        "Μοντέλο": ["Mercedes Sprinter", "Ford Transit", "Fiat Ducato", "Peugeot Boxer"],
        "Κατάσταση": ["Διαθέσιμο", "Σε Αποστολή", "Διαθέσιμο", "Συντήρηση"]
    })

if 'dispatchers' not in st.session_state:
    st.session_state.dispatchers = pd.DataFrame({
        "Ονοματεπώνυμο": ["Γιώργος Παπαδόπουλος", "Μαρία Νικολάου", "Κώστας Γεωργίου"],
        "Τηλέφωνο": ["6900000001", "6900000002", "6900000003"],
        "Βάρδια": ["Πρωινή", "Απογευματινή", "Βραδινή"]
    })

# Πλαϊνό μενού
st.sidebar.title("🚑 Ambulance 4 All")
menu = st.sidebar.radio("Επιλογή Λειτουργίας", ["Αρχική", "Οχήματα", "Διασώστες", "Καταγραφή Αποστολής"])

# --- Σελίδα Αρχικής ---
if menu == "Αρχική":
    st.title("Καλώς ήρθατε στο Σύστημα Διαχείρισης Ambulance 4 All")
    st.write("Εδώ μπορείτε να διαχειριστείτε τα οχήματα, το προσωπικό και τις καθημερινές αποστολές σας.")
    st.image("https://cdn-icons-png.flaticon.com/512/2967/2967368.png", width=150) # Ένα εικονίδιο ασθενοφόρου

# --- Σελίδα Οχημάτων ---
elif menu == "Οχήματα":
    st.title("🚑 Διαχείριση Στόλου")
    st.dataframe(st.session_state.vehicles, use_container_width=True)
    st.info("Συμβουλή: Μπορείτε να επεξεργαστείτε απευθείας τα δεδομένα στον πίνακα παραπάνω.")

# --- Σελίδα Διασωστών ---
elif menu == "Διασώστες":
    st.title("👨‍⚕️ Διαχείριση Προσωπικού")
    st.dataframe(st.session_state.dispatchers, use_container_width=True)

# --- Σελίδα Καταγραφής Αποστολής ---
elif menu == "Καταγραφή Αποστολής":
    st.title("📝 Νέα Αποστολή")
    with st.form("dispatch_form"):
        col1, col2 = st.columns(2)
        with col1:
            patient = st.text_input("Όνομα Ασθενούς")
            origin = st.text_input("Σημείο Παραλαβής")
        with col2:
            destination = st.text_input("Προορισμός")
            vehicle = st.selectbox("Επιλογή Οχήματος", st.session_state.vehicles["Πινακίδα"])
        
        submitted = st.form_submit_button("Καταγραφή")
        if submitted:
            st.success(f"Η αποστολή για τον/την {patient} καταγράφηκε! (Όχημα: {vehicle})")
            # Εδώ μπορείτε να προσθέσετε κώδικα για αποθήκευση σε αρχείο ή βάση δεδομένων