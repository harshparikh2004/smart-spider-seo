import streamlit as st
import pandas as pd
# Import our custom logic
from crawler import crawl_url

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

st.markdown("Enter a website URL below to generate a real-time technical audit report.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Configuration")
    target_url = st.text_input("Target URL", "https://www.emblus.com")
    run_btn = st.button("🚀 Run Audit", type="primary")
    
    st.divider()
    st.info("Built for Emblus Internship\nDeveloper: Harsh Parikh")

# --- MAIN LOGIC ---
if run_btn and target_url:
    with st.spinner(f"Crawling {target_url}... Please wait."):
        # Call our crawler script
        data = crawl_url(target_url)

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
                st.caption(f"Length: {len(data['title'])} characters")
            else:
                st.error("Page Title is Missing!")

            # Description Check
            if data["meta_desc"] != "Missing":
                st.success(f"**Meta Description:** {data['meta_desc']}")
                st.caption(f"Length: {len(data['meta_desc'])} characters")
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
            
            # Convert list of dicts to DataFrame for display
            if data["images"]:
                df_img = pd.DataFrame(data["images"])
                
                # Filter for missing alt text
                missing_alt = df_img[df_img['alt'] == '']
                
                c_a, c_b = st.columns(2)
                c_a.metric("Total Images", len(df_img))
                c_b.metric("Missing Alt Text", len(missing_alt), delta_color="inverse")

                if not missing_alt.empty:
                    st.error(f"⚠️ {len(missing_alt)} images are missing Alt Text.")
                    st.dataframe(missing_alt, use_container_width=True)
                else:
                    st.success("✅ All images have Alt Text!")
            else:
                st.info("No images found on this page.")

        with tab3:
            st.subheader("Audit Findings")
            # Logic to generate warnings dynamically
            if data["load_time"] > 2.0:
                st.warning(f"🐢 **Slow Load Time:** The page took {data['load_time']}s to load. Google recommends under 2.5s.")
            
            if len(data["h1"]) > 1:
                st.warning("⚠️ **Multiple H1 Tags:** It is recommended to have only one H1 per page.")
            
            if data["status_code"] != 200:
                st.error("🚨 **Broken Page:** The server returned a non-200 status code.")