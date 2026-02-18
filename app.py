import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import datetime

# --- 1. CONFIGURATION (The Brain) ---
# Replace with your actual key from Step 1
GEMINI_KEY = "AIzaSyCWX5JvVMUMGAL2708P1dKtBsUJ5hXvuCU" 
genai.configure(api_key=GEMINI_KEY)

# --- 2. THE SECRET DATABASE (Your Moat) ---
# This is what makes your tool valuable. Add more companies later.
nodal_officers = {
    "IndiGo": "nodal@goindigo.in",
    "Air India": "commerce@airindia.in",
    "Zomato": "grievance@zomato.com",
    "Swiggy": "grievance@swiggy.in",
    "HDFC Bank": "grievance.redressal@hdfcbank.com",
    "SBI": "customercare@sbi.co.in",
    "Amazon": "grievance-officer@amazon.in",
    "Flipkart": "grievance.officer@flipkart.com"
}

# --- 3. THE APP UI ---
st.set_page_config(page_title="Wassool AI", page_icon="⚖️")

st.title("⚖️ Wassool AI: The Consumer Fighter")
st.markdown("""
**Did a company cheat you?** Don't just complain. Send a **Legal Notice**.
*Instant. Professional. Cited with Indian Laws.*
""")

# Input Form
with st.form("notice_form"):
    col1, col2 = st.columns(2)
    user_name = col1.text_input("Your Name")
    company_name = col2.selectbox("Select Company (or type below)", ["IndiGo", "Zomato", "HDFC Bank", "Amazon", "Other"])
    
    if company_name == "Other":
        company_name = st.text_input("Type Company Name")
        
    issue_type = st.selectbox("What is the issue?", 
        ["Flight Refund Denied", "Defective Product", "Service Not Delivered", "Security Deposit Not Returned", "Hidden Charges"])
    
    amount = st.number_input("Amount to Recover (₹)", min_value=0, step=500)
    details = st.text_area("Details (Date, Order ID, What they said)", placeholder="e.g., I ordered a phone on 12th Jan, Order #123. It arrived broken. Support closed my ticket.")
    
    submit = st.form_submit_button("Draft My Legal Notice")

# --- 4. THE AI LOGIC ---
if submit and user_name and details:
    with st.spinner("Consulting the AI Lawyer..."):
        # The "Lawyer" Prompt
        prompt = f"""
        You are a fierce Consumer Rights Lawyer in India.
        Draft a 'Final Legal Notice' from {user_name} to {company_name}.
        
        Context:
        - Issue: {issue_type}
        - Amount Involved: ₹{amount}
        - Facts: {details}
        - Date: {datetime.date.today()}
        
        Requirements:
        1. Cite relevant Indian Laws strictly:
           - If Flight: Cite 'DGCA CAR Section 3, Series M, Part IV'.
           - If Product/Service: Cite 'Consumer Protection Act 2019 (Section 35)'.
           - If Bank: Cite 'RBI Ombudsman Scheme'.
        2. Tone: Professional, Intimidating, Demand Immediate Payment within 7 days.
        3. Threaten to file a formal complaint with the National Consumer Helpline (NCH) and Consumer Forum.
        4. Keep it concise (1 page). Do not use placeholders like [Your Name], use the real data provided.
        """
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        notice_text = response.text
        
        st.success("✅ Notice Generated!")
        
        # Display Text
        st.text_area("Copy Text", notice_text, height=300)
        
        # --- 5. PDF GENERATION (The Value) ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=11)
        
        # Simple Header
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "LEGAL NOTICE", ln=True, align='C')
        pdf.ln(10)
        
        # Body
        pdf.set_font("Arial", size=11)
        # Encoding fix for FPDF (Standard Latin-1)
        clean_text = notice_text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 6, clean_text)
        
        # Footer
        pdf.ln(10)
        pdf.set_font("Arial", 'I', 8)
        pdf.cell(0, 10, "Generated via Wassool AI - Consumer Rights Automation", align='C')
        
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        
        st.download_button(
            label="📄 Download Official PDF (For Email/WhatsApp)",
            data=pdf_bytes,
            file_name=f"Legal_Notice_{company_name}.pdf",
            mime="application/pdf"
        )
        
        # --- 6. THE UPSELL (Monetization) ---
        st.divider()
        st.subheader("🚀 Send it to the RIGHT person")
        
        if company_name in nodal_officers:
            st.error(f"🔒 **Locked Info:** The Direct Nodal Officer Email for {company_name} is available.")
            st.write("Most support emails (support@...) ignore you. Nodal Officers are legally required to reply.")
            st.write(f"**Pay ₹29 to unlock the Direct Email for {company_name} + 5 others.**")
            
            # Simple UPI logic (Manual for now)
            with st.expander("Unlock Now (UPI)"):
                st.image("https://upload.wikimedia.org/wikipedia/commons/d/d0/QR_code_for_mobile_English_Wikipedia.svg", width=200, caption="Scan to Pay ₹29") # REPLACE WITH YOUR UPI QR
                st.write("1. Pay ₹29")
                st.write("2. Send screenshot to (Your WhatsApp)")
                st.write("3. Get the list instantly.")
        else:
            st.info("Tip: Always find the 'Grievance Officer' email for faster replies.")