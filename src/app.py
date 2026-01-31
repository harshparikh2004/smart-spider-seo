import streamlit as st
import pandas as pd
from crawler import crawl_url
from utils import generate_ai_caption

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Smart-Spider Auditor",
    page_icon="🕷️",
    layout="wide"
)

# --- HEADER ---
st.title("🕷️ Smart-Spider: Technical SEO Auditor")
st.markdown("""
<style>
    .metric-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("Configuration")
    target_url = st.text_input("Target URL", "https://www.emblus.com")
    run_btn = st.button("🚀 Run Audit", type="primary")
    
    st.divider()
    st.info("Built for Emblus Internship\nDeveloper: Harsh Parikh")

# --- SESSION STATE MANAGEMENT (The Fix) ---
# This keeps the data alive even when you click other buttons
if "audit_data" not in st.session_state:
    st.session_state.audit_data = None

# Only run the crawler if the "Run Audit" button is clicked
if run_btn and target_url:
    with st.spinner(f"Crawling {target_url}... Please wait."):
        # Save result to session state
        st.session_state.audit_data = crawl_url(target_url)

# --- MAIN LOGIC ---
# Now we check if data exists in session state, not just if the button was clicked
if st.session_state.audit_data:
    data = st.session_state.audit_data

    # Error Handling
    if data["error"]:
        st.error(f"❌ Audit Failed: {data['error']}")
    else:
        # --- DASHBOARD UI ---
        
        # 1. Top Metrics Row
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Status Code", data["status_code"], delta="200 OK" if data["status_code"]==200 else "Error")
        c2.metric("Load Time", f"{data['load_time']}s", delta="-0.5s Goal")
        c3.metric("Internal Links", data["internal_links"])
        c4.metric("External Links", data["external_links"])

        st.divider()

        # 2. Detailed Tabs
        tab1, tab2, tab3 = st.tabs(["📄 Content & Meta", "🖼️ Image Analysis", "⚠️ Warnings"])

        with tab1:
            st.subheader("Meta Data Health")
            
            # Title Check
            if data["title"] != "Missing":
                st.success(f"**Page Title:** {data['title']}")
            else:
                st.error("Page Title is Missing!")

            # Description Check
            if data["meta_desc"] != "Missing":
                st.success(f"**Meta Description:** {data['meta_desc']}")
            else:
                st.warning("Meta Description is Missing!")

            # H1 Check
            st.markdown("### Header Hierarchy")
            if data["h1"]:
                for h1 in data["h1"]:
                    st.markdown(f"**H1:** {h1}")
            else:
                st.error("Missing H1 Tag! (Critical for SEO)")

        with tab2:
            st.subheader(f"Found {len(data['images'])} Images")
            
            if data["images"]:
                df_img = pd.DataFrame(data["images"])
                missing_alt = df_img[df_img['alt'] == '']
                
                c_a, c_b = st.columns(2)
                c_a.metric("Total Images", len(df_img))
                c_b.metric("Missing Alt Text", len(missing_alt), delta_color="inverse")

                if not missing_alt.empty:
                    st.error(f"⚠️ {len(missing_alt)} images are missing Alt Text.")
                    
                    st.markdown("### 🤖 AI Auto-Fixer")
                    st.info("Select an image below to generate Alt-Text using Computer Vision.")
                    
                    # Create a dropdown to select a broken image
                    img_option = st.selectbox(
                        "Select Image to Fix:", 
                        missing_alt['src'].tolist(),
                        format_func=lambda x: x[:60] + "..." # Shorten long URLs
                    )
                    
                    # Display selected image and Generate Button
                    if img_option:
                        col_left, col_right = st.columns([1, 2])
                        with col_left:
                            st.image(img_option, width=200, caption="Preview")
                        
                        with col_right:
                            # Unique key is crucial here
                            if st.button("✨ Generate AI Alt-Text", key="gen_btn"):
                                with st.spinner("Analyzing pixels..."):
                                    ai_text = generate_ai_caption(img_option)
                                    
                                    if "Error" in ai_text:
                                        st.error(ai_text)
                                    else:
                                        st.success("✅ Suggested Alt-Text:")
                                        st.code(ai_text, language="text")
                                        st.caption("Copy this text and paste it into your CMS.")
                else:
                    st.success("✅ All images have Alt Text!")
            else:
                st.info("No images found on this page.")

        with tab3:
            st.subheader("Audit Findings")
            if data["load_time"] > 2.0:
                st.warning(f"🐢 **Slow Load Time:** The page took {data['load_time']}s to load.")
            if len(data["h1"]) > 1:
                st.warning("⚠️ **Multiple H1 Tags:** Recommended to have only one H1.")
            if data["status_code"] != 200:
                st.error("🚨 **Broken Page:** Server returned non-200 status.")

else:
    # Initial State
    st.info("👈 Enter a URL in the sidebar and click 'Run Audit' to start.")