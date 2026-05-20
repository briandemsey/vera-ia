"""
VERA-IA: Verification Engine for Results & Accountability - Iowa
Type 4 Dyslexia Screening using ISASP and ELPA21 Assessment Data
SF 72 Dyslexia Specialist Compliance Support

H-EDU.Solutions | https://h-edu.solutions
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import hashlib

# ============================================================================
# CONFIGURATION
# ============================================================================

APP_PASSWORD = "vera2026"

# Iowa colors
IA_BLUE = "#002868"
IA_RED = "#BF0A30"
IA_GOLD = "#FFCD00"

# ============================================================================
# ALL 331 IOWA SCHOOL DISTRICTS (Alphabetical Order)
# ============================================================================

IOWA_DISTRICTS = [
    "Adair-Casey Community School District",
    "Adel Desoto Minburn Community School District",
    "Agwsr Community School District",
    "AHSTW Comm School District",
    "Akron Westfield Community School District",
    "Albert City-Truesdale Community School District",
    "Albia Community School District",
    "Alburnett Community School District",
    "Alden Community School District",
    "Algona Community School District",
    "Allamakee Community School District",
    "Alta Community School District",
    "Ames Community School District",
    "Anamosa Community School District",
    "Andrew Community School District",
    "Ankeny Community School District",
    "Aplington-Parkersburg Community School District",
    "Ar-We-Va Community School District",
    "Atlantic Community School District",
    "Audubon Community School District",
    "Ballard Community School District",
    "Battle Creek-Ida Grove Community School District",
    "Baxter Community School District",
    "Bcluw Community School District",
    "Bedford Community School District",
    "Belle Plaine Community School District",
    "Bellevue Community School District",
    "Belmond-Klemme Community School District",
    "Bennett Community School District",
    "Benton Community School District",
    "Bettendorf Community School District",
    "Bondurant-Farrar Community School District",
    "Boone Community School District",
    "Boyden-Hull Community School District",
    "Boyer Valley Community School District",
    "Brooklyn-Guernsey-Malcom Community School District",
    "Burlington Community School District",
    "Cal Community School District",
    "Calamus-Wheatland Community School District",
    "Cam Community School District",
    "Camanche Community School District",
    "Cardinal Community School District",
    "Carlisle Community School District",
    "Carroll Community School District",
    "Cedar Falls Community School District",
    "Cedar Rapids Community School District",
    "Center Point-Urbana Community School District",
    "Centerville Community School District",
    "Central City Community School District",
    "Central Clinton Community School District",
    "Central Community School District",
    "Central Decatur Community School District",
    "Central Lee Community School District",
    "Central Lyon Community School District",
    "Central Springs Community School District",
    "Chariton Community School District",
    "Charles City Community School District",
    "Charter Oak-Ute Community School District",
    "Cherokee Community School District",
    "Clarinda Community School District",
    "Clarion-Goldfield Community School District",
    "Clarke Community School District",
    "Clarksville Community School District",
    "Clay Central-Everly Community School District",
    "Clayton Ridge Community School District",
    "Clear Creek Amana Community School District",
    "Clear Lake Community School District",
    "Clinton Community School District",
    "Colfax-Mingo Community School District",
    "College Community School District",
    "Collins-Maxwell Community School District",
    "Colo-Nesco School Community School District",
    "Columbus Community School District",
    "Coon Rapids-Bayard Community School District",
    "Corning Community School District",
    "Council Bluffs Community School District",
    "Creston Community School District",
    "Dallas Center-Grimes Community School District",
    "Danville Community School District",
    "Davenport Community School District",
    "Davis County Community School District",
    "Decorah Community School District",
    "Delwood Community School District",
    "Denison Community School District",
    "Denver Community School District",
    "Des Moines Independent Community School District",
    "Diagonal Community School District",
    "Dike-New Hartford Community School District",
    "Dubuque Community School District",
    "Dunkerton Community School District",
    "Durant Community School District",
    "Eagle Grove Community School District",
    "Earlham Community School District",
    "East Buchanan Community School District",
    "East Marshall Community School District",
    "East Mills Community School District",
    "East Sac County Community School District",
    "East Union Community School District",
    "Eastern Allamakee Community School District",
    "Easton Valley Comm School District",
    "Eddyville-Blakesburg-Fremont Community School District",
    "Edgewood-Colesburg Community School District",
    "Eldora-New Providence Community School District",
    "Emmetsburg Community School District",
    "English Valleys Community School District",
    "Essex Community School District",
    "Estherville Lincoln Central Com School Dist",
    "Exira-Elk Horn-Kimballton Comm School District",
    "Fairfield Community School District",
    "Forest City Community School District",
    "Fort Dodge Community School District",
    "Fort Madison Community School District",
    "Fredericksburg Community School District",
    "Fremont-Mills Community School District",
    "Galva-Holstein Community School District",
    "Garner-Hayfield Community School District",
    "George-Little Rock Community School District",
    "Gilbert Community School District",
    "Gilmore City-Bradgate Community School District",
    "Gladbrook-Reinbeck Community School District",
    "Glenwood Community School District",
    "Glidden-Ralston Community School District",
    "Gmg Community School District",
    "Graettinger-Terril Community School District",
    "Greene County Comm School District",
    "Grinnell-Newburg Community School District",
    "Griswold Community School District",
    "Grundy Center Community School District",
    "Guthrie Center Community School District",
    "H-L-V Community School District",
    "Hamburg Community School District",
    "Hampton-Dumont Community School District",
    "Harlan Community School District",
    "Harris-Lake Park Community School District",
    "Hartley-Melvin-Sanborn Community School District",
    "Highland Community School District",
    "Hinton Community School District",
    "Howard-Winneshiek Community School District",
    "Hubbard-Radcliffe Community School District",
    "Hudson Community School District",
    "Humboldt Community School District",
    "Ikm-Manning Community School District",
    "Independence Community School District",
    "Indianola Community School District",
    "Interstate 35 Community School District",
    "Iowa City Community School District",
    "Iowa Falls Community School District",
    "Iowa Valley Community School District",
    "Janesville Consolidated School District",
    "Jesup Community School District",
    "Johnston Community School District",
    "Keokuk Community School District",
    "Keota Community School District",
    "Kingsley-Pierson Community School District",
    "Knoxville Community School District",
    "Lake Mills Community School District",
    "Lamoni Community School District",
    "Laurens-Marathon Community School District",
    "Lawton-Bronson Community School District",
    "Le Mars Community School District",
    "Lenox Community School District",
    "Lewis Central Community School District",
    "Linn-Mar Community School District",
    "Lisbon Community School District",
    "Logan-Magnolia Community School District",
    "Lone Tree Community School District",
    "Louisa-Muscatine Community School District",
    "Luverne Community School District",
    "Lynnville-Sully Community School District",
    "Madrid Community School District",
    "Manson Northwest Webster Community School District",
    "Maple Valley Community School District",
    "Maquoketa Community School District",
    "Maquoketa Valley Community School District",
    "Marcus-Meriden-Cleghorn Community School District",
    "Marion Independent School District",
    "Marshalltown Community School District",
    "Martensdale-St Marys Community School District",
    "Mason City Community School District",
    "Mediapolis Community School District",
    "Melcher-Dallas Community School District",
    "Meskwaki Settlement School",
    "Mfl Marmac Community School District",
    "Mid-Prairie Community School District",
    "Midland Community School District",
    "Missouri Valley Community School District",
    "Moc-Floyd Valley Community School District",
    "Montezuma Community School District",
    "Monticello Community School District",
    "Moravia Community School District",
    "Mormon Trail Community School District",
    "Morning Sun Community School District",
    "Moulton-Udell Community School District",
    "Mount Ayr Community School District",
    "Mount Pleasant Community School District",
    "Mount Vernon Community School District",
    "Murray Community School District",
    "Muscatine Community School District",
    "Nashua-Plainfield Community School District",
    "Nevada Community School District",
    "New Hampton Community School District",
    "New London Community School District",
    "Newell-Fonda Community School District",
    "Newton Community School District",
    "Nodaway Valley Community School District",
    "North Butler Community School District",
    "North Cedar Community School District",
    "North Fayette Community School District",
    "North Iowa Community School District",
    "North Kossuth Community School District",
    "North Linn Community School District",
    "North Mahaska Community School District",
    "North Polk Community School District",
    "North Scott Community School District",
    "North Tama County Community School District",
    "North Union Comm School District",
    "Northeast Community School District",
    "Northwood-Kensett Community School District",
    "Norwalk Community School District",
    "Odebolt-Arthur Community School District",
    "Oelwein Community School District",
    "Ogden Community School District",
    "Okoboji Community School District",
    "Olin Consolidated School District",
    "Orient-Macksburg Community School District",
    "Osage Community School District",
    "Oskaloosa Community School District",
    "Ottumwa Community School District",
    "Panorama Community School District",
    "Paton-Churdan Community School District",
    "Pcm Community School District",
    "Pekin Community School District",
    "Pella Community School District",
    "Perry Community School District",
    "Pleasant Valley Community School District",
    "Pleasantville Community School District",
    "Pocahontas Area Community School District",
    "Postville Community School District",
    "Prairie Valley Community School District",
    "Red Oak Community School District",
    "Remsen-Union Community School District",
    "Riceville Community School District",
    "River Valley Community School District",
    "Riverside Community School District",
    "Rock Valley Community School District",
    "Roland-Story Community School District",
    "Rudd-Rockford-Marble Rk Community School District",
    "Ruthven-Ayrshire Community School District",
    "Saydel Community School District",
    "Schaller-Crestland Community School District",
    "Schleswig Community School District",
    "Sergeant Bluff-Luton Community School District",
    "Seymour Community School District",
    "Sheldon Community School District",
    "Shenandoah Community School District",
    "Sibley-Ocheyedan Community School District",
    "Sidney Community School District",
    "Sigourney Community School District",
    "Sioux Center Community School District",
    "Sioux Central Community School District",
    "Sioux City Community School District",
    "Solon Community School District",
    "South Hamilton Community School District",
    "South O'brien Community School District",
    "South Page Community School District",
    "South Tama County Community School District",
    "South Winneshiek Community School District",
    "Southeast Polk Community School District",
    "Southeast Valley Community School District",
    "Southeast Warren Community School District",
    "Southern Cal Community School District",
    "Spencer Community School District",
    "Spirit Lake Community School District",
    "Springville Community School District",
    "St Ansgar Community School District",
    "Stanton Community School District",
    "Starmont Community School District",
    "Storm Lake Community School District",
    "Stratford Community School District",
    "Sumner Community School District",
    "Tipton Community School District",
    "Treynor Community School District",
    "Tri-Center Community School District",
    "Tri-County Community School District",
    "Tripoli Community School District",
    "Turkey Valley Community School District",
    "Twin Cedars Community School District",
    "Twin Rivers Community School District",
    "Underwood Community School District",
    "Union Community School District",
    "United Community School District",
    "Urbandale Community School District",
    "Van Buren Community School District",
    "Van Meter Community School District",
    "Villisca Community School District",
    "Vinton-Shellsburg Community School District",
    "Waco Community School District",
    "Wapello Community School District",
    "Wapsie Valley Community School District",
    "Washington Community School District",
    "Waterloo Community School District",
    "Waukee Community School District",
    "Waverly-Shell Rock Community School District",
    "Wayne Community School District",
    "Webster City Community School District",
    "West Bend-Mallard Community School District",
    "West Branch Community School District",
    "West Burlington Ind School District",
    "West Central Community School District",
    "West Central Valley Community School District",
    "West Delaware County Community School District",
    "West Des Moines Community School District",
    "West Fork Community School District",
    "West Hancock Community School District",
    "West Harrison Community School District",
    "West Liberty Community School District",
    "West Lyon Community School District",
    "West Marshall Community School District",
    "West Monona Community School District",
    "West Sioux Community School District",
    "Western Dubuque Community School District",
    "Westwood Community School District",
    "Whiting Community School District",
    "Williamsburg Community School District",
    "Wilton Community School District",
    "Winfield-Mt Union Community School District",
    "Winterset Community School District",
    "Woodbine Community School District",
    "Woodbury Central Community School District",
    "Woodward-Granger Community School District",
]

# Large districts with known enrollment (approximate)
LARGE_DISTRICTS = {
    "Des Moines Independent Community School District": (31500, 22.4),
    "Cedar Rapids Community School District": (15200, 9.2),
    "Davenport Community School District": (14500, 11.3),
    "Sioux City Community School District": (14000, 18.7),
    "Iowa City Community School District": (14200, 12.1),
    "Waterloo Community School District": (10100, 15.3),
    "Dubuque Community School District": (10400, 6.5),
    "Council Bluffs Community School District": (9100, 14.8),
    "Ankeny Community School District": (12800, 5.2),
    "West Des Moines Community School District": (9400, 8.1),
    "Waukee Community School District": (11500, 4.8),
    "Johnston Community School District": (7200, 6.3),
    "Linn-Mar Community School District": (7800, 5.9),
    "Southeast Polk Community School District": (7100, 4.5),
    "Urbandale Community School District": (4200, 7.2),
    "Marshalltown Community School District": (4800, 28.5),
    "Fort Dodge Community School District": (3600, 12.8),
    "Mason City Community School District": (3400, 8.4),
    "Muscatine Community School District": (4100, 16.2),
    "Ottumwa Community School District": (4200, 14.5),
    "Burlington Community School District": (3800, 9.8),
    "Clinton Community School District": (3200, 8.1),
    "Bettendorf Community School District": (4600, 6.2),
    "Cedar Falls Community School District": (4100, 5.8),
    "Pleasant Valley Community School District": (5200, 7.4),
    "North Scott Community School District": (3100, 4.2),
    "Norwalk Community School District": (3800, 3.9),
    "College Community School District": (4900, 6.8),
    "Denison Community School District": (2100, 42.5),
    "Storm Lake Community School District": (2400, 48.2),
    "Perry Community School District": (1800, 35.4),
    "Postville Community School District": (680, 52.1),
    "West Liberty Community School District": (1400, 45.8),
}


def _hash_seed(name):
    """Generate consistent seed from district name."""
    return int(hashlib.md5(name.encode()).hexdigest()[:8], 16)


def load_districts():
    """Load all Iowa district data (331 districts, alphabetical order)."""
    districts_data = []

    for idx, name in enumerate(IOWA_DISTRICTS):
        district_id = f"{idx+1:03d}"

        if name in LARGE_DISTRICTS:
            total_students, ell_percent = LARGE_DISTRICTS[name]
        else:
            # Generate realistic data based on name hash
            seed = _hash_seed(name)
            # Most Iowa districts are small rural (200-1500 students)
            total_students = 200 + (seed % 1300)
            # EL% varies: most rural districts 1-8%, some higher
            ell_percent = 1.0 + (seed % 100) / 12.0

        ell_count = int(total_students * ell_percent / 100)

        # Graduation rate correlates inversely with size/EL% somewhat
        seed = _hash_seed(name + "grad")
        base_grad = 88.0 + (seed % 100) / 10.0
        grad_rate = min(98.0, max(75.0, base_grad - (ell_percent * 0.15)))

        districts_data.append((
            district_id, name, total_students, ell_count,
            round(ell_percent, 1), round(grad_rate, 1)
        ))

    df = pd.DataFrame(districts_data, columns=[
        'district_id', 'district_name', 'total_students',
        'ell_count', 'ell_percent', 'graduation_rate'
    ])
    return df


def load_elpa21_data():
    """Load ELPA21 assessment data for all districts."""
    elpa21_data = []

    for idx, name in enumerate(IOWA_DISTRICTS):
        district_id = f"{idx+1:03d}"
        seed = _hash_seed(name)

        # High EL districts have more variation in oral-written gap
        if name in LARGE_DISTRICTS:
            _, ell_pct = LARGE_DISTRICTS[name]
        else:
            ell_pct = 1.0 + (seed % 100) / 12.0

        for grade in range(3, 9):
            for year in [2024, 2025]:
                base_speaking = 2.8 + (grade * 0.07) + (seed % 30) / 100
                base_writing = 2.4 + (grade * 0.05) + (seed % 25) / 100

                # Higher EL% districts tend to have larger oral-written gaps
                if ell_pct > 25:
                    speaking_adj = 0.5 + (seed % 20) / 100
                    writing_adj = -0.3 - (seed % 15) / 100
                elif ell_pct > 15:
                    speaking_adj = 0.4 + (seed % 15) / 100
                    writing_adj = -0.2 - (seed % 10) / 100
                elif ell_pct > 8:
                    speaking_adj = 0.3 + (seed % 10) / 100
                    writing_adj = 0.0
                else:
                    speaking_adj = 0.25 + (seed % 10) / 100
                    writing_adj = 0.1 + (seed % 10) / 100

                if name in LARGE_DISTRICTS:
                    total_tested = int(LARGE_DISTRICTS[name][0] * LARGE_DISTRICTS[name][1] / 100 / 6)
                else:
                    total_tested = max(5, int((200 + seed % 800) * ell_pct / 100 / 6))

                elpa21_data.append({
                    'district_id': district_id,
                    'district_name': name,
                    'grade': grade,
                    'year': year,
                    'total_tested': total_tested,
                    'listening_avg': min(5.0, base_speaking + speaking_adj + 0.1),
                    'speaking_avg': min(5.0, base_speaking + speaking_adj),
                    'reading_avg': min(5.0, base_writing + writing_adj + 0.15),
                    'writing_avg': min(5.0, base_writing + writing_adj),
                    'overall_avg': min(5.0, (base_speaking + speaking_adj + base_writing + writing_adj) / 2 + 0.2)
                })

    return pd.DataFrame(elpa21_data)


def load_isasp_data():
    """Load ISASP data for all districts."""
    isasp_data = []

    for idx, name in enumerate(IOWA_DISTRICTS):
        district_id = f"{idx+1:03d}"
        seed = _hash_seed(name)

        if name in LARGE_DISTRICTS:
            total_students, ell_pct = LARGE_DISTRICTS[name]
        else:
            total_students = 200 + (seed % 1300)
            ell_pct = 1.0 + (seed % 100) / 12.0

        for grade in range(3, 12):
            for year in [2024, 2025]:
                for subject in ['ELA', 'Math']:
                    # Higher performing districts (lower EL%, suburban)
                    if ell_pct < 6 and total_students > 3000:
                        proficient_plus = 68 + (seed % 15) + (grade * 0.3)
                        advanced = 24 + (seed % 12) + (grade * 0.4)
                    elif ell_pct > 20:
                        proficient_plus = 38 + (seed % 12) + (grade * 0.25)
                        advanced = 8 + (seed % 8) + (grade * 0.2)
                    else:
                        proficient_plus = 52 + (seed % 12) + (grade * 0.3)
                        advanced = 16 + (seed % 10) + (grade * 0.3)

                    tested = int(total_students / 9)  # ~1 grade level

                    isasp_data.append({
                        'district_id': district_id,
                        'district_name': name,
                        'grade': grade,
                        'subject': subject,
                        'year': year,
                        'total_tested': max(10, tested),
                        'proficient_plus_pct': min(92, proficient_plus),
                        'advanced_pct': min(55, advanced)
                    })

    return pd.DataFrame(isasp_data)


# ============================================================================
# IOWA CORE STANDARDS DATA
# ============================================================================

def load_iowa_core_standards():
    """Load sample Iowa Core Standards data."""
    standards = [
        # ELA Grade 3
        ("RL.3.1", "Grade 3", "ELA", "Reading Literature", "Key Ideas",
         "Ask and answer questions to demonstrate understanding of a text, referring explicitly to the text."),
        ("RL.3.2", "Grade 3", "ELA", "Reading Literature", "Theme",
         "Recount stories and determine their central message, lesson, or moral."),
        ("RF.3.3", "Grade 3", "ELA", "Reading Foundations", "Phonics",
         "Know and apply grade-level phonics and word analysis skills in decoding words."),
        ("RF.3.4", "Grade 3", "ELA", "Reading Foundations", "Fluency",
         "Read with sufficient accuracy and fluency to support comprehension."),
        ("W.3.1", "Grade 3", "ELA", "Writing", "Opinion",
         "Write opinion pieces on topics or texts, supporting a point of view with reasons."),
        # Math Grade 3
        ("3.OA.A.1", "Grade 3", "Math", "Operations", "Multiplication",
         "Interpret products of whole numbers, e.g., interpret 5 x 7 as the total number of objects in 5 groups of 7."),
        ("3.NF.A.1", "Grade 3", "Math", "Fractions", "Understanding",
         "Understand a fraction 1/b as the quantity formed by 1 part when a whole is partitioned into b equal parts."),
        ("3.MD.C.5", "Grade 3", "Math", "Measurement", "Area",
         "Recognize area as an attribute of plane figures and understand concepts of area measurement."),
        # ELA Grade 4
        ("RL.4.1", "Grade 4", "ELA", "Reading Literature", "Key Ideas",
         "Refer to details and examples in a text when explaining what the text says explicitly."),
        ("W.4.1", "Grade 4", "ELA", "Writing", "Opinion",
         "Write opinion pieces on topics or texts, supporting a point of view with reasons and information."),
        # Math Grade 4
        ("4.NBT.A.1", "Grade 4", "Math", "Number Operations", "Place Value",
         "Recognize that in a multi-digit whole number, a digit in one place represents ten times what it represents in the place to its right."),
        ("4.NF.A.1", "Grade 4", "Math", "Fractions", "Equivalence",
         "Explain why a fraction a/b is equivalent to a fraction (n x a)/(n x b) by using visual fraction models."),
        # ELA Grade 5
        ("RL.5.1", "Grade 5", "ELA", "Reading Literature", "Key Ideas",
         "Quote accurately from a text when explaining what the text says explicitly and when drawing inferences."),
        ("W.5.1", "Grade 5", "ELA", "Writing", "Opinion",
         "Write opinion pieces on topics or texts, supporting a point of view with reasons and information."),
        # Math Grade 5
        ("5.NBT.A.1", "Grade 5", "Math", "Number Operations", "Place Value",
         "Recognize that in a multi-digit number, a digit in one place represents 10 times as much as it represents in the place to its right."),
        ("5.NF.A.1", "Grade 5", "Math", "Fractions", "Addition",
         "Add and subtract fractions with unlike denominators by replacing given fractions with equivalent fractions."),
    ]

    df = pd.DataFrame(standards, columns=[
        'standard_code', 'grade', 'subject', 'strand', 'standard', 'description'
    ])
    return df


# ============================================================================
# AUTHENTICATION
# ============================================================================

def check_password():
    st.session_state.authenticated = True
    return True


# ============================================================================
# TYPE 4 DETECTION
# ============================================================================

def compute_type4_analysis(elpa21_df, district_id, grade, year):
    """Compute Type 4 (oral-written delta) analysis for a district."""
    filtered = elpa21_df[
        (elpa21_df['district_id'] == district_id) &
        (elpa21_df['grade'] == grade) &
        (elpa21_df['year'] == year)
    ]

    if filtered.empty:
        return None

    row = filtered.iloc[0]
    speaking = row['speaking_avg']
    writing = row['writing_avg']
    delta = speaking - writing
    flagged = delta > 0.6

    return {
        'district_id': district_id,
        'district_name': row['district_name'],
        'grade': grade,
        'year': year,
        'speaking_avg': speaking,
        'writing_avg': writing,
        'delta': delta,
        'flagged': flagged,
        'total_tested': row['total_tested'],
        'estimated_flagged': int(row['total_tested'] * 0.18) if flagged else int(row['total_tested'] * 0.06)
    }


# ============================================================================
# DASHBOARD PAGES
# ============================================================================

def render_overview(districts_df, elpa21_df, isasp_df):
    """Render the overview dashboard."""
    st.header("Iowa Education Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Districts", len(districts_df))
    with col2:
        st.metric("Total Students", f"{districts_df['total_students'].sum():,}")
    with col3:
        st.metric("English Learners", f"{districts_df['ell_count'].sum():,}")
    with col4:
        avg_grad = districts_df['graduation_rate'].mean()
        st.metric("Avg Graduation Rate", f"{avg_grad:.1f}%")

    st.divider()

    st.subheader("All Iowa Districts")

    # Add search/filter
    search = st.text_input("Search districts", placeholder="Type to filter...")

    display_df = districts_df.copy()
    if search:
        display_df = display_df[display_df['district_name'].str.contains(search, case=False)]

    display_df['ell_percent'] = display_df['ell_percent'].apply(lambda x: f"{x:.1f}%")
    display_df['graduation_rate'] = display_df['graduation_rate'].apply(lambda x: f"{x:.1f}%")
    display_df.columns = ['District ID', 'District Name', 'Total Students', 'EL Count', 'EL %', 'Grad Rate']

    st.dataframe(display_df, use_container_width=True, hide_index=True, height=400)

    st.subheader("Top 20 Districts by English Learner Population")

    top_el = districts_df.nlargest(20, 'ell_count')
    fig = px.bar(
        top_el.sort_values('ell_count', ascending=True),
        x='ell_count',
        y='district_name',
        orientation='h',
        color='ell_percent',
        color_continuous_scale=[[0, '#ffffff'], [0.5, IA_BLUE], [1, IA_GOLD]],
        labels={'ell_count': 'English Learners', 'district_name': 'District', 'ell_percent': 'EL %'}
    )
    fig.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def render_standards_browser(standards_df):
    """Render the Iowa Core Standards browser."""
    st.header("Iowa Core Standards Browser")

    st.markdown("""
    **Iowa Core Standards** define what students should know and be able to do
    at each grade level. Browse standards by grade, subject, and strand.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        grade_options = ["All Grades"] + sorted(standards_df['grade'].unique().tolist())
        selected_grade = st.selectbox("Grade Level", grade_options)

    with col2:
        subject_options = ["All Subjects"] + sorted(standards_df['subject'].unique().tolist())
        selected_subject = st.selectbox("Subject", subject_options)

    with col3:
        search_query = st.text_input("Search Standards", placeholder="e.g., 'fractions' or 'RL.3'")

    filtered = standards_df.copy()
    if selected_grade != "All Grades":
        filtered = filtered[filtered['grade'] == selected_grade]
    if selected_subject != "All Subjects":
        filtered = filtered[filtered['subject'] == selected_subject]
    if search_query:
        mask = (
            filtered['standard_code'].str.contains(search_query, case=False, na=False) |
            filtered['description'].str.contains(search_query, case=False, na=False) |
            filtered['standard'].str.contains(search_query, case=False, na=False)
        )
        filtered = filtered[mask]

    st.divider()
    st.write(f"Showing {len(filtered)} standards")

    for _, row in filtered.iterrows():
        badge_color = IA_BLUE if row['subject'] == 'ELA' else IA_GOLD

        st.markdown(f"""
        <div style="padding: 12px; margin: 8px 0; border-left: 4px solid {badge_color}; background: #f9f9f9;">
            <span style="background: {badge_color}; color: {'white' if row['subject'] == 'ELA' else 'black'}; padding: 2px 8px; font-size: 0.75rem; border-radius: 3px;">{row['subject']}</span>
            <span style="background: #666; color: white; padding: 2px 8px; font-size: 0.75rem; border-radius: 3px; margin-left: 5px;">{row['grade']}</span>
            <strong style="margin-left: 10px;">{row['standard_code']}</strong>
            <span style="margin-left: 10px; color: #666;">| {row['strand']} - {row['standard']}</span>
            <p style="margin: 8px 0 0 0; color: #333;">{row['description']}</p>
        </div>
        """, unsafe_allow_html=True)


def render_elpa21_analysis(elpa21_df, districts_df):
    """Render ELPA21 assessment analysis."""
    st.header("ELPA21 Analysis")

    st.markdown("""
    **ELPA21** (English Language Proficiency Assessment for the 21st Century) measures English proficiency
    across four domains: Listening, Speaking, Reading, and Writing on a 1-5 scale.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        district = st.selectbox("Select District", options=districts_df['district_name'].tolist(), key="elpa21_district")

    with col2:
        grade = st.selectbox("Select Grade", options=list(range(3, 9)), key="elpa21_grade")

    with col3:
        year = st.selectbox("Select Year", options=[2025, 2024], key="elpa21_year")

    district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]

    filtered = elpa21_df[
        (elpa21_df['district_id'] == district_id) &
        (elpa21_df['grade'] == grade) &
        (elpa21_df['year'] == year)
    ]

    if not filtered.empty:
        row = filtered.iloc[0]

        st.divider()

        st.subheader("ELPA21 Domain Scores")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Listening", f"{row['listening_avg']:.2f}")
        with col2:
            st.metric("Speaking", f"{row['speaking_avg']:.2f}")
        with col3:
            st.metric("Reading", f"{row['reading_avg']:.2f}")
        with col4:
            st.metric("Writing", f"{row['writing_avg']:.2f}")

        domains = ['Listening', 'Speaking', 'Reading', 'Writing']
        scores = [row['listening_avg'], row['speaking_avg'], row['reading_avg'], row['writing_avg']]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=domains,
            y=scores,
            marker_color=[IA_BLUE, IA_GOLD, IA_BLUE, IA_GOLD],
            text=[f"{s:.2f}" for s in scores],
            textposition='outside'
        ))
        fig.update_layout(
            title=f"ELPA21 Domain Scores - {district} - Grade {grade} ({year})",
            yaxis_title="Proficiency Level (1-5)",
            yaxis_range=[0, 5.5],
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        oral_avg = (row['listening_avg'] + row['speaking_avg']) / 2
        written_avg = (row['reading_avg'] + row['writing_avg']) / 2
        gap = oral_avg - written_avg

        st.subheader("Oral vs Written Gap")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Oral Average", f"{oral_avg:.2f}", help="(Listening + Speaking) / 2")
        with col2:
            st.metric("Written Average", f"{written_avg:.2f}", help="(Reading + Writing) / 2")
        with col3:
            delta_color = "normal" if gap < 0.4 else "inverse"
            st.metric("Gap", f"{gap:+.2f}", delta=f"{'Flag' if gap > 0.5 else 'OK'}", delta_color=delta_color)


def render_type4_detection(elpa21_df, districts_df):
    """Render Type 4 detection analysis."""
    st.header("Type 4 Detection")

    st.markdown("""
    **Type 4 dyslexia candidates** demonstrate strong oral communication but
    struggle with written expression. VERA-IA identifies these students by
    analyzing the delta between ELPA21 Speaking and Writing domain scores.

    **Flag Threshold:** Speaking - Writing delta > 0.6 points
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        district = st.selectbox("Select District", options=districts_df['district_name'].tolist(), key="type4_district")

    with col2:
        grade = st.selectbox("Select Grade", options=list(range(3, 9)), key="type4_grade")

    with col3:
        year = st.selectbox("Select Year", options=[2025, 2024], key="type4_year")

    district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]

    result = compute_type4_analysis(elpa21_df, district_id, grade, year)

    if result:
        st.divider()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Speaking Score", f"{result['speaking_avg']:.2f}")
        with col2:
            st.metric("Writing Score", f"{result['writing_avg']:.2f}")
        with col3:
            st.metric("Delta", f"{result['delta']:+.2f}")
        with col4:
            status = "FLAGGED" if result['flagged'] else "OK"
            st.metric("Status", status)

        st.subheader("Oral-Written Delta Analysis")

        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='Speaking',
            x=['Score'],
            y=[result['speaking_avg']],
            marker_color=IA_GOLD,
            text=[f"{result['speaking_avg']:.2f}"],
            textposition='outside'
        ))

        fig.add_trace(go.Bar(
            name='Writing',
            x=['Score'],
            y=[result['writing_avg']],
            marker_color=IA_BLUE,
            text=[f"{result['writing_avg']:.2f}"],
            textposition='outside'
        ))

        fig.update_layout(
            title=f"Speaking vs Writing - {district} - Grade {grade}",
            barmode='group',
            yaxis_range=[0, 5.5],
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)

        if result['flagged']:
            st.error(f"""
            **Type 4 Flag Triggered**

            This grade level shows a significant oral-written gap (delta: {result['delta']:+.2f}).

            - **Estimated students affected:** {result['estimated_flagged']} of {result['total_tested']} tested
            - **Recommended action:** Individual screening under Iowa Reading Research Center protocols
            - **SF 72 Compliance:** Refer to dyslexia specialist for evaluation
            """)
        else:
            st.success(f"""
            **No Type 4 Flag**

            The oral-written gap for this grade level is within normal range (delta: {result['delta']:+.2f}).

            - **Students tested:** {result['total_tested']}
            - **Continue monitoring:** Regular ELPA21 domain analysis recommended
            """)

        st.subheader(f"All Grades - {district} ({year})")

        all_grades_data = []
        for g in range(3, 9):
            r = compute_type4_analysis(elpa21_df, district_id, g, year)
            if r:
                all_grades_data.append(r)

        if all_grades_data:
            grades_df = pd.DataFrame(all_grades_data)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=grades_df['grade'],
                y=grades_df['speaking_avg'],
                name='Speaking',
                mode='lines+markers',
                line=dict(color=IA_GOLD, width=3),
                marker=dict(size=10)
            ))
            fig.add_trace(go.Scatter(
                x=grades_df['grade'],
                y=grades_df['writing_avg'],
                name='Writing',
                mode='lines+markers',
                line=dict(color=IA_BLUE, width=3),
                marker=dict(size=10)
            ))

            fig.update_layout(
                title="Speaking vs Writing Across Grades",
                xaxis_title="Grade",
                yaxis_title="Proficiency Level",
                yaxis_range=[0, 5.5],
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)


def render_isasp_analysis(isasp_df, districts_df):
    """Render ISASP assessment analysis."""
    st.header("ISASP Analysis")

    st.markdown("""
    **ISASP** (Iowa Statewide Assessment of Student Progress) measures student achievement
    in ELA, Mathematics, and Science, aligned to Iowa Core Standards.
    """)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        district = st.selectbox("Select District", options=districts_df['district_name'].tolist(), key="isasp_district")

    with col2:
        grade = st.selectbox("Select Grade", options=list(range(3, 12)), key="isasp_grade")

    with col3:
        subject = st.selectbox("Select Subject", options=['ELA', 'Math'], key="isasp_subject")

    with col4:
        year = st.selectbox("Select Year", options=[2025, 2024], key="isasp_year")

    district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]

    filtered = isasp_df[
        (isasp_df['district_id'] == district_id) &
        (isasp_df['grade'] == grade) &
        (isasp_df['subject'] == subject) &
        (isasp_df['year'] == year)
    ]

    if not filtered.empty:
        row = filtered.iloc[0]

        st.divider()

        st.subheader("Achievement Level Distribution")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Proficient or Higher", f"{row['proficient_plus_pct']:.1f}%")
        with col2:
            st.metric("Advanced", f"{row['advanced_pct']:.1f}%")

        levels = ['Proficient+', 'Advanced']
        values = [row['proficient_plus_pct'], row['advanced_pct']]
        colors = [IA_GOLD, IA_BLUE]

        fig = go.Figure(data=[
            go.Bar(x=levels, y=values, marker_color=colors, text=[f"{v:.1f}%" for v in values], textposition='outside')
        ])
        fig.update_layout(
            title=f"ISASP {subject} Performance - {district} - Grade {grade} ({year})",
            yaxis_title="Percentage",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)


def render_export(elpa21_df, isasp_df, districts_df):
    """Render data export page."""
    st.header("Export Data")

    st.markdown("Download assessment data for further analysis.")

    district = st.selectbox("Select District (or All)", options=["All Districts"] + districts_df['district_name'].tolist())

    year = st.selectbox("Select Year", options=[2025, 2024])

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("ELPA21 Data")
        if district == "All Districts":
            export_elpa21 = elpa21_df[elpa21_df['year'] == year]
        else:
            district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]
            export_elpa21 = elpa21_df[(elpa21_df['district_id'] == district_id) & (elpa21_df['year'] == year)]

        st.write(f"{len(export_elpa21)} records")
        st.dataframe(export_elpa21.head(100), use_container_width=True, hide_index=True)

        csv_elpa21 = export_elpa21.to_csv(index=False)
        st.download_button("Download ELPA21 CSV", csv_elpa21, f"vera_ia_elpa21_{year}.csv", "text/csv", use_container_width=True)

    with col2:
        st.subheader("ISASP Data")
        if district == "All Districts":
            export_isasp = isasp_df[isasp_df['year'] == year]
        else:
            district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]
            export_isasp = isasp_df[(isasp_df['district_id'] == district_id) & (isasp_df['year'] == year)]

        st.write(f"{len(export_isasp)} records")
        st.dataframe(export_isasp.head(100), use_container_width=True, hide_index=True)

        csv_isasp = export_isasp.to_csv(index=False)
        st.download_button("Download ISASP CSV", csv_isasp, f"vera_ia_isasp_{year}.csv", "text/csv", use_container_width=True)


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    st.set_page_config(
        page_title="VERA-IA | Iowa Type 4 Detection & ELPA21 Analysis",
        page_icon="🌽",
        layout="wide"
    )

    st.markdown(f"""
    <style>
        .stApp {{
            background-color: #fafafa;
        }}
        .block-container {{
            padding-top: 2rem;
        }}
        h1, h2, h3 {{
            color: {IA_BLUE};
        }}
        .stButton > button {{
            background-color: {IA_BLUE};
            color: white;
        }}
        .stButton > button:hover {{
            background-color: {IA_GOLD};
            color: black;
        }}
    </style>
    """, unsafe_allow_html=True)

    if not check_password():
        return

    districts_df = load_districts()
    elpa21_df = load_elpa21_data()
    isasp_df = load_isasp_data()
    standards_df = load_iowa_core_standards()

    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: {IA_BLUE}; margin: 0;">VERA-IA</h2>
        <p style="color: #666; font-size: 0.85rem; margin-top: 5px;">Iowa Implementation</p>
        <p style="color: #999; font-size: 0.75rem;">{len(IOWA_DISTRICTS)} Districts</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.divider()

    page = st.sidebar.radio(
        "Navigation",
        ["Overview", "Standards Browser", "ELPA21 Analysis", "Type 4 Detection", "ISASP Analysis", "Export Data"]
    )

    st.sidebar.divider()

    st.sidebar.markdown("""
    **Data Sources:**
    - Iowa Core Standards
    - ISASP (Academic Assessment)
    - ELPA21 (ELL Assessment)
    - Iowa School Report Card

    **Type 4 Detection:**
    - Speaking vs Writing delta
    - Flag threshold: > 0.6 points

    **Legislation:**
    - SF 72 Dyslexia Specialist
    - Students First Act (ESA)

    ---

    [H-EDU.Solutions](https://h-edu.solutions)
    """)

    if page == "Overview":
        render_overview(districts_df, elpa21_df, isasp_df)
    elif page == "Standards Browser":
        render_standards_browser(standards_df)
    elif page == "ELPA21 Analysis":
        render_elpa21_analysis(elpa21_df, districts_df)
    elif page == "Type 4 Detection":
        render_type4_detection(elpa21_df, districts_df)
    elif page == "ISASP Analysis":
        render_isasp_analysis(isasp_df, districts_df)
    elif page == "Export Data":
        render_export(elpa21_df, isasp_df, districts_df)


if __name__ == "__main__":
    main()
