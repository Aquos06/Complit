import datetime
import streamlit as st
from type.page import PageType
from utils.database.graph import Neo4Graph
import uuid

def make_new(full_name, birth_date, gender, address, phone_number, email_addr, current_medications,family_medical_history):
    patient_id = uuid.uuid4()
    cypher =[
        f"""CREATE (p:Patient {{
            patient_id: "{patient_id}",
            full_name: "{full_name}",
            birth_date: date("{birth_date.isoformat()}"),
            gender: "{gender}",
            address: "{address}",
            phone_number: "{phone_number}",
            email_addr: "{email_addr}"
        }})""",

        f"""CREATE (cm:CurrentMedications {{
            details: "{current_medications}",
            patient_id: "{patient_id}"
        }})""",

        f"""CREATE (fmh:FamilyMedicalHistory {{
            details: "{family_medical_history}",
            patient_id: "{patient_id}" 
        }})""",

        f"""MATCH (p:Patient {{patient_id: "{patient_id}"}}),
            (cm:CurrentMedications {{patient_id: "{patient_id}"}})
            CREATE (p)-[:HAS_CURRENT_MEDICATIONS]->(cm)""",
        f"""MATCH (p:Patient {{patient_id: "{patient_id}"}}),
            (fmh:FamilyMedicalHistory {{patient_id: "{patient_id}"}})
            CREATE (p)-[:HAS_FAMILY_MEDICAL_HISTORY]->(fmh)"""
    ]
    
    graph = Neo4Graph()
    graph.execute_query(queries=cypher)
    
    

def create_new_member_ui():
    full_name = st.text_input("Full Name")
    birthday = st.date_input("Birth Date", datetime.date(2000,9,18))
    gender = st.selectbox("Gender",('Men','Women'))
    address = st.text_input("Address")
    phone_number = st.text_input("Phone Number")
    email_addr = st.text_input("Email Address")
    current_medications = st.text_area("Current Medication")
    family_medical_history = st.text_area("Family Medical History")
    
    if st.button("Save"):
        make_new(
            full_name=full_name,
            birth_date=birthday,
            gender=gender,
            address=address,
            phone_number=phone_number,
            email_addr=email_addr,
            current_medications=current_medications,
            family_medical_history=family_medical_history
            )
    
        st.session_state.mode = PageType.NULL
        st.rerun()