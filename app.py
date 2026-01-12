# app.py
import streamlit as st
from models import SchuldEintrag, BezahlterEintrag
from database import (
    load_schulden, add_schuld, delete_schuld,
    load_bezahlt, add_bezahlt, save_bezahlt
)
from logic import berechne_monatsschulden, berechne_jahresschulden, berechne_betrag
from datetime import datetime
# ---------------------------------------------------------
# CSS laden
# ---------------------------------------------------------
def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception:
        st.warning("Konnte style.css nicht laden.")

load_css()

# ---------------------------------------------------------
# SESSION STATE FÜR FORMULAR
# ---------------------------------------------------------
if "show_form" not in st.session_state:
    st.session_state.show_form = True

# ---------------------------------------------------------
# PWA EINBINDUNG
# ---------------------------------------------------------

st.markdown("""
<link rel="manifest" href="/manifest.json">

<script>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/service-worker.js")
      .then(reg => console.log("Service Worker registriert:", reg))
      .catch(err => console.log("Service Worker Fehler:", err));
  });
}
</script>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# TITEL
# ---------------------------------------------------------

st.title("💰 Dayn maareeye Schuldenverwaltung – Schuldner & Schuldgeber")

# ---------------------------------------------------------
# OBERER BEREICH – STATISTIKEN
# ---------------------------------------------------------

schulden = load_schulden()
bezahlt = load_bezahlt()

anzahl_offen = len(schulden)
anzahl_bezahlt = len(bezahlt)

st.subheader(f"📌 Daymaha wali lagudin Offene Schulden: **{anzahl_offen} Schuldner**")
st.subheader(f"📌 Daymaha laguday Bezahlte Schulden: **{anzahl_bezahlt} Einträge**")

monat = datetime.now().month
jahr = datetime.now().year

offen_monat = berechne_monatsschulden(schulden, monat, jahr)
offen_jahr = berechne_jahresschulden(schulden, jahr)

bezahlt_monat = berechne_monatsschulden(bezahlt, monat, jahr)
bezahlt_jahr = berechne_jahresschulden(bezahlt, jahr)

st.info(f"📅 **Offene Schulden im Monat:** {offen_monat} €")
st.info(f"📅 **Offene Schulden im Jahr:** {offen_jahr} €")
st.success(f"💼 **Bezahlte Schulden im Monat:** {bezahlt_monat} €")
st.success(f"💼 **Bezahlte Schulden im Jahr:** {bezahlt_jahr} €")

# ---------------------------------------------------------
# NEUEN SCHULDNER HINZUFÜGEN
# ---------------------------------------------------------

with st.expander("➕ dayn cusub kudar Neuen Schuldner hinzufügen", expanded=st.session_state.show_form):
    schuldner = st.text_input("magaca dayn qaataha Name des Schuldners")
    schuldgeber = st.text_input("magaca dayn bixiyaha Name des Schuldgebers")
    art = st.text_input("nuuca dayntu tahay Art der Schulden")

    betrag_raw = st.text_input(
        "Qiimaha daynta Betrag (Rechnung erlaubt, z.B. 2,00 + 1,99)"
    )

    if st.button("kaydi Speichern"):
        betrag = berechne_betrag(betrag_raw)

        if schuldner and schuldgeber and art and betrag is not None and betrag > 0:
            eintrag = SchuldEintrag(
                schuldner=schuldner,
                schuldgeber=schuldgeber,
                art=art,
                betrag=betrag
            )
            add_schuld(eintrag)
            st.success(f"Schuld erfolgreich gespeichert ({betrag} €)")

            # 🔥 Formular automatisch schließen
            st.session_state.show_form = False
            st.rerun()

        else:
            st.error("Bitte alle Felder korrekt ausfüllen. Betrag muss eine gültige Rechnung sein.")

# ---------------------------------------------------------
# LISTE DER SCHULDNER
# ---------------------------------------------------------

with st.expander("📋 Daymaha wali lagudin Liste der offenen Schulden"):
    schulden = load_schulden()

    if schulden:
        for i, s in enumerate(schulden):
            st.write(f"### {i+1}. {s['schuldner']} schuldet {s['betrag']} €")
            st.write(f"Schuldgeber: {s['schuldgeber']}")
            st.write(f"Art: {s['art']}")
            st.write(f"Datum: {s['datum']}")

            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"❌ tuur Löschen {i}", key=f"del_{i}"):
                    delete_schuld(i)
                    st.warning("Eintrag gelöscht")
                    st.rerun()

            with col2:
                if st.button(f"✔️ in laguday dayntan cadee Als bezahlt markieren {i}", key=f"pay_{i}"):
                    bezahlt_eintrag = BezahlterEintrag(
                        schuldner=s["schuldner"],
                        betrag=s["betrag"]
                    )
                    add_bezahlt(bezahlt_eintrag)
                    delete_schuld(i)
                    st.success("Schuld als bezahlt gespeichert")
                    st.rerun()
    else:
        st.info("Keine offenen Schulden vorhanden")

# ---------------------------------------------------------
# BEZAHLTE SCHULDEN – ANZEIGEN, BEARBEITEN, LÖSCHEN
# ---------------------------------------------------------

with st.expander("💼 Daymaha laguday Bezahlte Schulden anzeigen / bearbeiten / löschen"):
    bezahlt = load_bezahlt()

    if bezahlt:
        for i, b in enumerate(bezahlt):
            st.write(f"### {i+1}. {b['schuldner']} hat {b['betrag']} € bezahlt")
            st.write(f"Datum: {b['datum']}")

            neuer_betrag = st.number_input(
                f"Neuer Betrag für {b['schuldner']}",
                value=float(b["betrag"]),
                key=f"edit_betrag_{i}"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"💾 Speichern {i}", key=f"save_paid_{i}"):
                    b["betrag"] = neuer_betrag
                    save_bezahlt(bezahlt)
                    st.success("Eintrag aktualisiert")
                    st.rerun()

            with col2:
                if st.button(f"❌ Löschen bezahlt {i}", key=f"del_paid_{i}"):
                    bezahlt.pop(i)
                    save_bezahlt(bezahlt)
                    st.warning("Bezahlter Eintrag gelöscht")
                    st.rerun()

    else:
        st.info("Noch keine Schulden bezahlt")

# ---------------------------------------------------------
# BERECHNUNGEN MANUELL
# ---------------------------------------------------------

with st.expander("📊 Berechnungen manuell auswählen"):
    schulden = load_schulden()
    bezahlt = load_bezahlt()

    monat = st.number_input("Monat", min_value=1, max_value=12, step=1)
    jahr = st.number_input("Jahr", min_value=2000, max_value=2100, step=1)

    if st.button("Berechnen"):
        offen_monat = berechne_monatsschulden(schulden, monat, jahr)
        offen_jahr = berechne_jahresschulden(schulden, jahr)

        bezahlt_monat = berechne_monatsschulden(bezahlt, monat, jahr)
        bezahlt_jahr = berechne_jahresschulden(bezahlt, jahr)

        st.write(f"📌 **Offene Schulden im Monat {monat}/{jahr}: {offen_monat} €**")
        st.write(f"📌 **Offene Schulden im Jahr {jahr}: {offen_jahr} €**")
        st.write(f"💼 **Bezahlte Schulden im Monat {monat}/{jahr}: {bezahlt_monat} €**")
        st.write(f"💼 **Bezahlte Schulden im Jahr {jahr}: {bezahlt_jahr} €**")
