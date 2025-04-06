# Final Enhanced Smart Data Analyzer
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
from fpdf import FPDF
from PIL import Image
import base64
import qrcode

# --- Styling and Initial Setup ---
st.set_page_config(page_title="Smart Data Analyzer", layout="wide")
st.markdown("<h1 style='text-align: center;'>📊 Smart Data Analyzer</h1>", unsafe_allow_html=True)

# --- Welcome Message ---
with st.expander("👋 Welcome Message", expanded=True):
    st.markdown("""
    <div style='font-size:18px;'>
        🎉 <strong>Welcome!</strong> I'm <strong>Zain</strong>, your assistant for cleaning and exploring datasets. <br>
        Upload a <strong>CSV</strong> or <strong>Excel</strong> file below and let's uncover insights together!
    </div>
    """, unsafe_allow_html=True)

# --- File Upload ---
with st.sidebar:
    st.image("https://img.freepik.com/free-vector/data-visualization_52683-7355.jpg?ga=GA1.1.1443411147.1730915938&semt=ais_hybrid&w=740", width=100,)
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

# --- Load Dataset ---
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📄 Raw Dataset")
    st.dataframe(df.head(10))

    # --- Data Summary ---
    st.subheader("📊 Data Summary")
    st.markdown(f"**Shape:** {df.shape}")
    st.markdown("**Null Values:**")
    st.dataframe(df.isnull().sum()[df.isnull().sum() > 0])

    st.markdown("**Data Types:**")
    st.dataframe(df.dtypes)

    # --- New: Cardinality Check ---
    st.markdown("**High Cardinality Columns (Unique > 30):**")
    high_card_cols = df.nunique()[df.nunique() > 30]
    st.dataframe(high_card_cols)

    # --- New: Duplicate Rows ---
    duplicate_rows = df[df.duplicated()]
    if not duplicate_rows.empty:
        st.markdown(f"**🚨 Duplicate Rows Found:** {duplicate_rows.shape[0]}")
        st.dataframe(duplicate_rows)

    # --- New: AI Column Cleaning Suggestion (Simple Heuristic) ---
    st.markdown("**🧠 Suggested Columns for Cleaning:**")
    suggestions = df.columns[df.isnull().any() | (df.nunique() > 50)]
    st.write(list(suggestions))

    # --- Distributions ---
    st.subheader("📈 Column Distributions")
    num_cols = df.select_dtypes(include=['float64', 'int64'])
    for col in num_cols.columns:
        fig, ax = plt.subplots()
        sns.histplot(df[col], kde=True, ax=ax)
        st.pyplot(fig)

    # --- PDF Report Generator ---
    class PDF(FPDF):
        def header(self):
            if hasattr(self, 'profile_img'):
                self.image(self.profile_img, 10, 8, 20)
            self.set_font('Arial', 'B', 14)
            self.cell(0, 10, 'Smart Data Analyzer Report', ln=1, align='C')
            self.set_font('Arial', '', 12)
            self.cell(0, 10, 'Email: zainalvi552@gmail.com', ln=1, align='C')
            self.ln(10)

    def generate_pdf():
        pdf = PDF()
        pdf.add_page()
        pdf.profile_img = 'mylogo.png'

        # Summary
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, f"Data Shape: {df.shape}", ln=1)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, "Null Values:", ln=1)
        pdf.set_font('Arial', '', 11)
        for col, val in df.isnull().sum().items():
            if val > 0:
                pdf.cell(0, 8, f"{col}: {val}", ln=1)

        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, "Data Types:", ln=1)
        pdf.set_font('Arial', '', 11)
        for col, dtype in df.dtypes.items():
            pdf.cell(0, 8, f"{col}: {dtype}", ln=1)

        # QR Code
        qr = qrcode.make("https://linkedin.com/in/zainalvi552")
        qr_path = "qr_code.png"
        qr.save(qr_path)
        pdf.image(qr_path, x=160, y=240, w=30)

        # Footer
        pdf.set_y(-30)
        pdf.set_font("Arial", size=9)
        pdf.set_text_color(100)
        pdf.multi_cell(0, 5, "© Zain Alvi | Aspiring Data Engineer\nProject: Smart Data Analyzer | Built with Python & Streamlit\nLinkedIn: linkedin.com/in/zainalvi552 | GitHub: github.com/zainalvi")

        return pdf.output(dest='S').encode('latin1')

    # --- Download Button ---
    st.download_button(
        label="⬇️ Download Full Report (PDF)",
        data=generate_pdf(),
        file_name="SmartDataReport.pdf",
        mime='application/pdf'
    )
