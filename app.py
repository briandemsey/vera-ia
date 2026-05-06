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
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

APP_PASSWORD = "vera2026"

# Iowa colors
IA_BLUE = "#002868"
IA_RED = "#BF0A30"
IA_GOLD = "#FFCD00"

# ============================================================================
# SAMPLE DATA - Iowa Districts (Alphabetical Order)
# ============================================================================

def load_districts():
    """Load Iowa district data (alphabetical order)."""
    districts_data = [
        ("01", "Cedar Rapids Community", 15200, 1398, 9.2, 91.2),
        ("02", "Council Bluffs Community", 9100, 1347, 14.8, 87.5),
        ("03", "Davenport Community", 14500, 1639, 11.3, 88.1),
        ("04", "Des Moines Independent", 31500, 7056, 22.4, 84.3),
        ("05", "Dubuque Community", 10400, 676, 6.5, 93.4),
        ("06", "Iowa City Community", 14200, 1718, 12.1, 94.8),
        ("07", "Sioux City Community", 14000, 2618, 18.7, 85.9),
        ("08", "Waterloo Community", 10100, 1545, 15.3, 83.7),
    ]

    df = pd.DataFrame(districts_data, columns=[
        'district_id', 'district_name', 'total_students',
        'ell_count', 'ell_percent', 'graduation_rate'
    ])
    return df


def load_elpa21_data():
    """Load sample ELPA21 assessment data."""
    elpa21_data = []

    districts = [
        ("01", "Cedar Rapids Community"),
        ("02", "Council Bluffs Community"),
        ("03", "Davenport Community"),
        ("04", "Des Moines Independent"),
        ("05", "Dubuque Community"),
        ("06", "Iowa City Community"),
        ("07", "Sioux City Community"),
        ("08", "Waterloo Community"),
    ]

    for district_id, district_name in districts:
        for grade in range(3, 9):
            for year in [2024, 2025]:
                # Generate realistic ELPA21 scores (scale 1-5: Emerging to Proficient)
                base_speaking = 2.9 + (grade * 0.07)
                base_writing = 2.5 + (grade * 0.05)

                # District-specific variation
                if district_id == "04":  # Des Moines - highest EL%, larger delta
                    speaking_adj = 0.5
                    writing_adj = -0.3
                elif district_id == "07":  # Sioux City
                    speaking_adj = 0.45
                    writing_adj = -0.25
                elif district_id in ["05", "06"]:  # Higher performing
                    speaking_adj = 0.3
                    writing_adj = 0.2
                else:
                    speaking_adj = 0.35
                    writing_adj = 0.0

                elpa21_data.append({
                    'district_id': district_id,
                    'district_name': district_name,
                    'grade': grade,
                    'year': year,
                    'total_tested': 600 + (grade * 40) if district_id in ["04", "07"] else 200 + (grade * 25),
                    'listening_avg': min(5.0, base_speaking + speaking_adj + 0.1),
                    'speaking_avg': min(5.0, base_speaking + speaking_adj),
                    'reading_avg': min(5.0, base_writing + writing_adj + 0.15),
                    'writing_avg': min(5.0, base_writing + writing_adj),
                    'overall_avg': min(5.0, (base_speaking + speaking_adj + base_writing + writing_adj) / 2 + 0.2)
                })

    return pd.DataFrame(elpa21_data)


def load_isasp_data():
    """Load sample ISASP (Iowa Statewide Assessment of Student Progress) data."""
    isasp_data = []

    districts = [
        ("01", "Cedar Rapids Community"),
        ("02", "Council Bluffs Community"),
        ("03", "Davenport Community"),
        ("04", "Des Moines Independent"),
        ("05", "Dubuque Community"),
        ("06", "Iowa City Community"),
        ("07", "Sioux City Community"),
        ("08", "Waterloo Community"),
    ]

    for district_id, district_name in districts:
        for grade in range(3, 12):
            for year in [2024, 2025]:
                for subject in ['ELA', 'Math']:
                    # Generate realistic ISASP proficiency
                    if district_id in ["05", "06"]:  # High performing
                        proficient_plus = 68 + (grade * 0.4)
                        advanced = 24 + (grade * 0.5)
                    elif district_id in ["04", "08"]:  # Lower performing
                        proficient_plus = 42 + (grade * 0.3)
                        advanced = 10 + (grade * 0.25)
                    else:  # Average
                        proficient_plus = 52 + (grade * 0.35)
                        advanced = 16 + (grade * 0.35)

                    isasp_data.append({
                        'district_id': district_id,
                        'district_name': district_name,
                        'grade': grade,
                        'subject': subject,
                        'year': year,
                        'total_tested': 3000 + (grade * 150) if district_id == "04" else 1200 + (grade * 80),
                        'proficient_plus_pct': min(90, proficient_plus),
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
    ]

    df = pd.DataFrame(standards, columns=[
        'standard_code', 'grade', 'subject', 'strand', 'standard', 'description'
    ])
    return df


# ============================================================================
# AUTHENTICATION
# ============================================================================

def check_password():
    """Simple password authentication."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.markdown(f"""
    <div style="text-align: center; padding: 60px 20px;">
        <h1 style="color: {IA_BLUE}; font-size: 3rem; margin-bottom: 10px;">VERA-IA</h1>
        <p style="color: #666; font-size: 1.1rem; margin-bottom: 40px;">
            Verification Engine for Results & Accountability<br>Iowa Implementation
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("Enter access code:", type="password", key="password_input")
        if st.button("Access VERA-IA", use_container_width=True):
            if password == APP_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid access code")

    st.markdown("""
    <div style="text-align: center; margin-top: 60px; color: #999; font-size: 0.85rem;">
        <p>VERA-IA analyzes ISASP and ELPA21 data to identify Type 4 dyslexia candidates.</p>
        <p style="margin-top: 10px;">SF 72 Dyslexia Specialist Compliance Support</p>
        <p style="margin-top: 10px;">Contact: brian@h-edu.solutions</p>
    </div>
    """, unsafe_allow_html=True)

    return False


# ============================================================================
# TYPE 4 DETECTION
# ============================================================================

def compute_type4_analysis(elpa21_df, district_id, grade, year):
    """
    Compute Type 4 (oral-written delta) analysis for a district.
    Delta = Speaking Score - Writing Score
    Flag threshold: Delta > 0.6 points (on ELPA21 1-5 scale)
    """
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

    st.subheader("Pilot Districts")

    display_df = districts_df.copy()
    display_df['ell_percent'] = display_df['ell_percent'].apply(lambda x: f"{x:.1f}%")
    display_df['graduation_rate'] = display_df['graduation_rate'].apply(lambda x: f"{x:.1f}%")
    display_df.columns = ['District ID', 'District Name', 'Total Students', 'EL Count', 'EL %', 'Grad Rate']

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.subheader("English Learner Population by District")

    fig = px.bar(
        districts_df.sort_values('ell_count', ascending=True),
        x='ell_count',
        y='district_name',
        orientation='h',
        color='ell_percent',
        color_continuous_scale=[[0, '#ffffff'], [0.5, IA_BLUE], [1, IA_GOLD]],
        labels={'ell_count': 'English Learners', 'district_name': 'District', 'ell_percent': 'EL %'}
    )
    fig.update_layout(height=400, showlegend=False)
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

        st.dataframe(export_elpa21, use_container_width=True, hide_index=True)

        csv_elpa21 = export_elpa21.to_csv(index=False)
        st.download_button("Download ELPA21 CSV", csv_elpa21, f"vera_ia_elpa21_{year}.csv", "text/csv", use_container_width=True)

    with col2:
        st.subheader("ISASP Data")
        if district == "All Districts":
            export_isasp = isasp_df[isasp_df['year'] == year]
        else:
            district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]
            export_isasp = isasp_df[(isasp_df['district_id'] == district_id) & (isasp_df['year'] == year)]

        st.dataframe(export_isasp, use_container_width=True, hide_index=True)

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
