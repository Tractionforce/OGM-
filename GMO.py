import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="GMO Declaration Manager", layout="wide")

st.title("🧬 GMO Regulatory Declaration Manager")
st.markdown("Fill out the forms below to automatically populate the required French regulatory GMO declaration sheets.")

# ------------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# ------------------------------------------------------------------------------
if "df_cell_commercial" not in st.session_state:
    st.session_state.df_cell_commercial = pd.DataFrame(columns=[
        "Réf #",
        "Nom de la lignée", 
        "Espèce et origine tissulaire", 
        "Classement initial", 
        "Type de modification", 
        "Type de vecteur", 
        "Nom du transgène / gène modifié", 
        "N° DUO et classe de confinement"
    ])

if "df_mgm_2_2_1" not in st.session_state:
    st.session_state.df_mgm_2_2_1 = pd.DataFrame(columns=[
        "MGM Nom & Souche", 
        "Classe d'origine", 
        "Méthode d'obtention et vecteurs", 
        "Hôtes intermédiaires", 
        "Type de modification", 
        "Organisme donneur & Classe", 
        "Transgènes / Inserts", 
        "Effet attendu", 
        "Classe proposée", 
        "Hôtes cibles (Lien Tableau 3.5.2)"
    ])

if "df_cell_stables_3_5_1" not in st.session_state:
    st.session_state.df_cell_stables_3_5_1 = pd.DataFrame(columns=[
        "OGM final : Espèce & Lignée", 
        "Type de modification", 
        "Méthode d'obtention", 
        "Vecteurs utilisés", 
        "Stabilité", 
        "Gènes mutés / délétés", 
        "Organisme donneur & Classe", 
        "Transgènes & Fonctions", 
        "Confinement proposé"
    ])

if "df_exposure_3_5_2" not in st.session_state:
    st.session_state.df_exposure_3_5_2 = pd.DataFrame(columns=[
        "Réf MGM (Ligne Tab 2.2.1)", 
        "Nom du micro-organisme", 
        "Gène modifié / Transgène et (n° GenBank)", 
        "Pathogène humain ?", 
        "Classe MGM", 
        "Lignée cellulaire hôte & modifications", 
        "Cellule de référence (Tab 1.1 / 3.5.2)", 
        "Classe de confinement finale"
    ])

if "df_animaux" not in st.session_state:
    st.session_state.df_animaux = pd.DataFrame(columns=[
        "Genre et espèce", 
        "Nom de la lignée / réf. bibliographique", 
        "Type de modification génétique", 
        "Nom et espèce d’origine du transgène/gène modifié (n° GenBank)", 
        "N° DUO et classe de confinement"
    ])

# ------------------------------------------------------------------------------
# ROUTING / SELECTION
# ------------------------------------------------------------------------------
st.sidebar.header("Navigation & Options")
project_type = st.sidebar.selectbox(
    "Select the type of GMO workflow to register:",
    [
        "Lentivirus / Viral GMM (Table 2.2.1 + Table 3.5.2)",
        "Stable Cell Lines without Lentivirus (Table 3.5.1)",
        "Existing / Commercial Cell Lines (Table 1.1)",
        "GM Animals (Table 1.2)"
    ]
)

st.subheader(f"Workflow: {project_type}")

# ------------------------------------------------------------------------------
# 1. LENTIVIRUS WORKFLOW (TABLE 2.2.1 + TABLE 3.5.2)
# ------------------------------------------------------------------------------
if project_type == "Lentivirus / Viral GMM (Table 2.2.1 + Table 3.5.2)":
    st.info("ℹ️ Registering a viral vector requires declaring the GMM vector (Table 2.2.1) and linking it to the target host cell exposures (Table 3.5.2).")
    
    with st.form("form_lentivirus_workflow", clear_on_submit=True):
        
        # --- SECTION 1: TABLE 2.2.1 (MGM) ---
        st.markdown("### 🦠 1. Viral Vector / GMM Information (Table 2.2.1)")
        col1, col2 = st.columns(2)
        
        gmm_name = col1.text_input("Final GMM Name & Strain", placeholder="e.g., Lentivirus Cas9_GEN1KO")
        gmm_orig_class = col2.selectbox("Original Microorganism Class", [1, 2, 3], index=1)
        gmm_method = col1.text_input("Method & Vectors Used", value="Transfection multi-plasmidique")
        gmm_inter_host = col2.text_input("Intermediate Hosts", value="HEK 293T")
        
        gmm_mod_type = col1.selectbox("Modification Type", [
            "Combinaison de modifications",
            "Insertion de transgènes",
            "Délétion de gènes"
        ])
        gmm_donor = col2.text_input("Donor Organism & Class", value="S. pyogenes (C2)")
        gmm_transgenes = st.text_area("Transgenes / Inserts (Name & Function)", placeholder="Insert A: Cas9 recombinante, sgRNA anti-GEN1")
        gmm_effect = col1.text_input("Expected Effect", value="Non-réplicatif")
        gmm_prop_class = col2.selectbox("Proposed Vector Class", ["C1", "C2", "C3"])
        
        target_hosts_link = st.text_input("Target Hosts Reference", value="Tableau 3.5.2")

        st.markdown("---")

        # --- SECTION 2: TABLE 3.5.2 (EXPOSURE) ---
        st.markdown("### 🧫 2. Target Cell Exposure Information (Table 3.5.2)")
        col3, col4 = st.columns(2)
        
        mgm_ref_id = col3.text_input("MGM Reference (Table 2.2.1 line)", value="Tableau 2.2.1, ligne 1")
        microorg_name = col4.text_input("Microorganism Name", value="Lentivirus HIV-1")
        
        # Champ de saisie mis à jour
        transgene_target = col3.text_input("Modified Gene / Transgene and (GenBank#)", placeholder="e.g., GEN1 (NM_00123), Cas9")
        
        is_pathogen = col4.selectbox("Is Human Pathogen?", ["Non", "Oui"], index=0)
        mgm_class = col3.selectbox("MGM Class (Table 3.5.2)", [1, 2, 3], index=1)
        host_cell_desc = col4.text_input("Host Cell Line & Modifications", placeholder="e.g., Cellule humaine HCT-116")
        ref_cell_link = col3.text_input("Reference Cell Line Link", placeholder="e.g., Tableau 1.1, ligne 2")
        final_containment = col4.selectbox("Final Containment Class", ["C1", "C2", "C3"])

        if st.form_submit_button("💾 Save Lentivirus & Exposure Declaration"):
            row_2_2_1 = {
                "MGM Nom & Souche": gmm_name,
                "Classe d'origine": gmm_orig_class,
                "Méthode d'obtention et vecteurs": gmm_method,
                "Hôtes intermédiaires": gmm_inter_host,
                "Type de modification": gmm_mod_type,
                "Organisme donneur & Classe": gmm_donor,
                "Transgènes / Inserts": gmm_transgenes,
                "Effet attendu": gmm_effect,
                "Classe proposée": gmm_prop_class,
                "Hôtes cibles (Lien Tableau 3.5.2)": target_hosts_link
            }
            st.session_state.df_mgm_2_2_1 = pd.concat([st.session_state.df_mgm_2_2_1, pd.DataFrame([row_2_2_1])], ignore_index=True)

            row_3_5_2 = {
                "Réf MGM (Ligne Tab 2.2.1)": mgm_ref_id,
                "Nom du micro-organisme": microorg_name,
                "Gène modifié / Transgène et (n° GenBank)": transgene_target,
                "Pathogène humain ?": is_pathogen,
                "Classe MGM": mgm_class,
                "Lignée cellulaire hôte & modifications": host_cell_desc,
                "Cellule de référence (Tab 1.1 / 3.5.2)": ref_cell_link,
                "Classe de confinement finale": final_containment
            }
            st.session_state.df_exposure_3_5_2 = pd.concat([st.session_state.df_exposure_3_5_2, pd.DataFrame([row_3_5_2])], ignore_index=True)

            st.success("✅ Successfully registered into Table 2.2.1 (GMM) and Table 3.5.2 (Cell Exposure)!")

# ------------------------------------------------------------------------------
# 2. STABLE CELL LINES WITHOUT LENTIVIRUS (TABLE 3.5.1)
# ------------------------------------------------------------------------------
elif project_type == "Stable Cell Lines without Lentivirus (Table 3.5.1)":
    st.info("ℹ️ Declaration form for non-viral, stable cell line generation (Table 3.5.1).")
    
    with st.form("form_stables_non_viral", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        final_gmo = col1.text_input("Final GMO (Species & Cell Line)", placeholder="e.g., RPE-1 RNA Pol2")
        mod_type = col2.selectbox("Modification Type", [
            "Ajout de transgènes",
            "Délétion de gènes",
            "Substitution de gènes"
        ])
        gen_method = col1.text_input("Method of Generation", placeholder="e.g., Transfection + sélection G418")
        vectors_used = col2.text_input("Vectors Used", placeholder="e.g., PB533-42B3mutAC2-sfGFP")
        stability = col1.selectbox("Stability", ["Stable", "Transitoire"], index=0)
        mutated_genes = col2.text_input("Mutated / Deleted Genes", placeholder="e.g., 42B3mutAC2-scFv")
        donor_org = col1.text_input("Donor Organism & Class", value="Humain (C1)")
        transgenes_desc = st.text_area("Transgenes & Functions", placeholder="Insert A: scFv anti-RNA Pol II, sfGFP")
        proposed_containment = col2.selectbox("Proposed Containment Class", ["C1", "C2", "C3"])

        if st.form_submit_button("➕ Add to Table 3.5.1"):
            row_3_5_1 = {
                "OGM final : Espèce & Lignée": final_gmo,
                "Type de modification": mod_type,
                "Méthode d'obtention": gen_method,
                "Vecteurs utilisés": vectors_used,
                "Stabilité": stability,
                "Gènes mutés / délétés": mutated_genes,
                "Organisme donneur & Classe": donor_org,
                "Transgènes & Fonctions": transgenes_desc,
                "Confinement proposé": proposed_containment
            }
            st.session_state.df_cell_stables_3_5_1 = pd.concat([st.session_state.df_cell_stables_3_5_1, pd.DataFrame([row_3_5_1])], ignore_index=True)
            st.success("✅ Added to Table 3.5.1!")

# ------------------------------------------------------------------------------
# 3. EXISTING / COMMERCIAL CELL LINES (TABLE 1.1)
# ------------------------------------------------------------------------------
elif project_type == "Existing / Commercial Cell Lines (Table 1.1)":
    st.info("ℹ️ Declaration form for existing genetically modified cell lines (Table 1.1).")
    
    with st.form("form_commercial_cells", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        ref_id = col1.text_input("Ref #", value=str(len(st.session_state.df_cell_commercial) + 1))
        line_name = col2.text_input("Cell Line Name", placeholder="e.g., HEK 293T, HCT-116")
        species_tissue = col1.text_input("Species & Tissue Origin", placeholder="e.g., Homo sapiens, embryonic kidney")
        init_class = col2.selectbox("Initial Classification", ["C1", "C2", "C3"], index=0)
        
        mod_type = col1.text_input("Modification Type", value="NA")
        vector_type = col2.text_input("Vector Type", value="NA")
        transgene_name = col1.text_input("Gene / Transgene Name", value="NA")
        duo_reg = col2.text_input("DUO Registration & Class", placeholder="e.g., 8892 (C1)")

        if st.form_submit_button("➕ Add to Table 1.1"):
            row_1_1 = {
                "Réf #": ref_id,
                "Nom de la lignée": line_name,
                "Espèce et origine tissulaire": species_tissue,
                "Classement initial": init_class,
                "Type de modification": mod_type,
                "Type de vecteur": vector_type,
                "Nom du transgène / gène modifié": transgene_name,
                "N° DUO et classe de confinement": duo_reg
            }
            st.session_state.df_cell_commercial = pd.concat([st.session_state.df_cell_commercial, pd.DataFrame([row_1_1])], ignore_index=True)
            st.success("✅ Added to Table 1.1!")

# ------------------------------------------------------------------------------
# 4. GM ANIMALS (TABLE 1.2)
# ------------------------------------------------------------------------------
elif project_type == "GM Animals (Table 1.2)":
    with st.form("form_animals", clear_on_submit=True):
        col1, col2 = st.columns(2)
        genus_species = col1.text_input("Genus & Species", value="Drosophila melanogaster")
        strain_ref = col2.text_input("Line Name & Bibliographic Ref")
        mod_type = col1.selectbox("Genetic Modification Type", ["transgénèse", "knock-in", "knock-out", "transfection"])
        gene_info = col2.text_area("Gene / Transgene Name & Origin (GenBank #)")
        duo_class = col1.text_input("DUO Registration & Containment Class", value="8892 C1")
        
        if st.form_submit_button("➕ Add to Table 1.2"):
            new_row = {
                "Genre et espèce": genus_species,
                "Nom de la lignée / réf. bibliographique": strain_ref,
                "Type de modification génétique": mod_type,
                "Nom et espèce d’origine du transgène/gène modifié (n° GenBank)": gene_info,
                "N° DUO et classe de confinement": duo_class
            }
            st.session_state.df_animaux = pd.concat([st.session_state.df_animaux, pd.DataFrame([new_row])], ignore_index=True)
            st.success("✅ Added to Table 1.2!")

# ------------------------------------------------------------------------------
# DATA PREVIEW & MULTI-TAB EXCEL EXPORT
# ------------------------------------------------------------------------------
st.markdown("---")
st.header("📊 Recorded Regulatory Data Overview")

tab_1_1, tab_2_2_1, tab_3_5_1, tab_3_5_2, tab_1_2 = st.tabs([
    "Table 1.1 (Commercial Cells)", 
    "Table 2.2.1 (GMM / Lentivirus)", 
    "Table 3.5.1 (Stable Cells Non-Viral)", 
    "Table 3.5.2 (Cell Exposures)",
    "Table 1.2 (GM Animals)"
])

with tab_1_1:
    st.dataframe(st.session_state.df_cell_commercial, use_container_width=True)

with tab_2_2_1:
    st.dataframe(st.session_state.df_mgm_2_2_1, use_container_width=True)

with tab_3_5_1:
    st.dataframe(st.session_state.df_cell_stables_3_5_1, use_container_width=True)

with tab_3_5_2:
    st.dataframe(st.session_state.df_exposure_3_5_2, use_container_width=True)

with tab_1_2:
    st.dataframe(st.session_state.df_animaux, use_container_width=True)

# Generate multi-sheet Excel file compliant with regulator expectations
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    st.session_state.df_cell_commercial.to_excel(writer, sheet_name='Tableau_1_1', index=False)
    st.session_state.df_mgm_2_2_1.to_excel(writer, sheet_name='Tableau_2_2_1', index=False)
    st.session_state.df_cell_stables_3_5_1.to_excel(writer, sheet_name='Tableau_3_5_1', index=False)
    st.session_state.df_exposure_3_5_2.to_excel(writer, sheet_name='Tableau_3_5_2', index=False)
    st.session_state.df_animaux.to_excel(writer, sheet_name='Tableau_1_2', index=False)

st.download_button(
    label="📥 Download Complete Regulatory Excel Workbook (.xlsx)",
    data=buffer.getvalue(),
    file_name="declaration_OGM_officielle.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
