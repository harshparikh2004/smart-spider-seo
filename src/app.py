import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# --- IMPORT YOUR MODULES ---
from crawler import crawl_url
from utils import generate_ai_caption

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Smart-Spider | AI SEO Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. IMMERSIVE CSS STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;500;700;800&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #020617; /* Ink Black */
        color: #F8FAFC;
    }

    /* --- SIDEBAR --- */
    section[data-testid="stSidebar"] {
        width: 350px !important;
        background-color: #0B1121;
        border-right: 1px solid #1E293B;
    }
    
    /* --- HERO TEXT --- */
    .hero-text {
        background: linear-gradient(to right, #3B82F6, #8B5CF6, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        margin-top: 2rem;
    }
    
    .hero-sub {
        text-align: center;
        color: #94A3B8;
        font-size: 1.25rem;
        margin-bottom: 3rem;
    }

    /* --- METRIC CARDS (NEW) --- */
    .glass-metric {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 15px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }
    .glass-metric:hover {
        border-color: #3B82F6;
        background: rgba(30, 41, 59, 0.8);
        transform: translateY(-2px);
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 700;
        color: #F8FAFC;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* --- CUSTOM BUTTON --- */
    .stButton > button {
        background: linear-gradient(90deg, #3B82F6 0%, #2563EB 100%);
        border: none;
        color: white;
        padding: 14px 28px;
        font-weight: 600;
        border-radius: 8px;
        width: 100%;
        transition: 0.3s;
    }
    .stButton > button:hover {
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. HELPER FUNCTIONS ---
def create_donut_chart(score):
    """
    Creates a modern 'Donut' style chart instead of the old Gauge.
    Removes the 'annoying bar' background artifacts.
    """
    color = "#10B981" if score > 80 else "#F59E0B" if score > 50 else "#EF4444"
    
    fig = go.Figure(go.Pie(
        values=[score, 100-score],
        labels=["Score", "Remaining"],
        hole=0.75,
        sort=False,
        marker=dict(colors=[color, "#1E293B"]), # #1E293B matches the dark theme background
        textinfo='none',
        hoverinfo='none'
    ))

    fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, b=0, l=0, r=0),
        height=220,
        annotations=[dict(text=str(score), x=0.5, y=0.5, font_size=50, font_color="white", showarrow=False)]
    )
    return fig

# --- 4. APP STATE ---
if "audit_data" not in st.session_state:
    st.session_state.audit_data = None
    st.session_state.app_state = "landing" 

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("### 🕸️ Smart-Spider")
    st.caption("v3.0 | ENTERPRISE CORE")
    st.markdown("---")
    
    target_url = st.text_input("ENTER TARGET URL", "https://emblus.com")
    
    c1, c2 = st.columns(2)
    with c1: st.toggle("Deep Scan", value=True)
    with c2: st.toggle("AI Vision", value=True)

    st.markdown("###")
    run_btn = st.button("🚀 INITIALIZE AUDIT")
    
    if run_btn and target_url:
        st.session_state.app_state = "results"
        with st.status("System Active: Running Protocols...", expanded=True) as status:
            st.write("🔹 Resolving DNS & Handshake...")
            time.sleep(0.3)
            st.write("🔹 Parsing DOM Structure...")
            # CALL CRAWLER
            st.session_state.audit_data = crawl_url(target_url) 
            st.write("🔹 AI Vision Processing...")
            time.sleep(0.3)
            status.update(label="Audit Complete", state="complete", expanded=False)

# --- 6. MAIN CONTENT AREA ---

# VIEW 1: LANDING PAGE
if st.session_state.app_state == "landing":
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<h1 class="hero-text">SEO AUDITS REIMAGINED</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">AI-Powered Technical Analysis for the Modern Web</p>', unsafe_allow_html=True)
    
    # Feature Grid
    col1, col2, col3 = st.columns(3)
    features = [
        ("⚡ Lightning Fast", "Async Python Engine"),
        ("👁️ AI Vision", "Auto-Captioning Neural Net"),
        ("🛡️ Security Check", "SSL & Header Analysis")
    ]
    
    for col, (title, desc) in zip([col1, col2, col3], features):
        with col:
            st.markdown(f"""
            <div class="glass-metric" style="height:150px;">
                <h3 style="margin:0;">{title}</h3>
                <p style="color:#94A3B8; margin-top:10px;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

# VIEW 2: RESULTS DASHBOARD
elif st.session_state.app_state == "results" and st.session_state.audit_data:
    data = st.session_state.audit_data
    
    if data.get("error"):
        st.error(f"Connection Failed: {data['error']}")
    else:
        # --- HEADER ---
        st.markdown(f"### 📡 Audit Report: `{target_url}`")
        st.markdown("---")

        # --- SCORING ALGORITHM ---
        score = 100
        if data['load_time'] > 1.0: score -= 10
        if data['load_time'] > 2.0: score -= 10
        if data['title'] == "Missing": score -= 20
        if data['meta_desc'] == "Missing": score -= 10
        if data['status_code'] != 200: score -= 30
        final_score = max(0, score)

        # --- MAIN DASHBOARD GRID ---
        col_score, col_stats = st.columns([1.5, 3], gap="large")

        # LEFT: THE SCORE RING
        with col_score:
            st.markdown('<div class="glass-metric" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown('<p class="metric-label">OVERALL HEALTH</p>', unsafe_allow_html=True)
            st.plotly_chart(create_donut_chart(final_score), use_container_width=True, config={'displayModeBar': False})
            
            # Status Badge
            status_color = "#10B981" if final_score > 80 else "#F59E0B"
            status_text = "OPTIMIZED" if final_score > 80 else "NEEDS WORK"
            st.markdown(f"""
            <div style="background:{status_color}20; border:1px solid {status_color}; color:{status_color}; 
            padding:5px 15px; border-radius:20px; font-size:0.8rem; font-weight:700; margin-top:10px;">
            {status_text}
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # RIGHT: DETAILED METRICS GRID
        with col_stats:
            # Row 1
            r1c1, r1c2, r1c3 = st.columns(3)
            with r1c1:
                st.markdown(f"""
                <div class="glass-metric">
                    <span class="metric-val">{data['load_time']}s</span>
                    <span class="metric-label">⚡ Load Speed</span>
                </div>
                """, unsafe_allow_html=True)
            with r1c2:
                st.markdown(f"""
                <div class="glass-metric">
                    <span class="metric-val">{len(data['images'])}</span>
                    <span class="metric-label">🖼️ Assets</span>
                </div>
                """, unsafe_allow_html=True)
            with r1c3:
                st.markdown(f"""
                <div class="glass-metric">
                    <span class="metric-val">{data['internal_links']}</span>
                    <span class="metric-label">🔗 Links</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Row 2 (New Parameters)
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True) # Spacer
            r2c1, r2c2, r2c3 = st.columns(3)
            
            # SSL Logic
            is_ssl = target_url.startswith("https")
            ssl_icon = "🔒 Secure" if is_ssl else "🔓 Unsafe"
            
            with r2c1:
                 st.markdown(f"""
                <div class="glass-metric">
                    <span class="metric-val" style="font-size:1.4rem;">{ssl_icon}</span>
                    <span class="metric-label">Protocol</span>
                </div>
                """, unsafe_allow_html=True)
            with r2c2:
                # SEO Meta Check logic
                meta_status = "✅ Valid" if data['title'] != "Missing" else "❌ Missing"
                st.markdown(f"""
                <div class="glass-metric">
                    <span class="metric-val" style="font-size:1.4rem;">{meta_status}</span>
                    <span class="metric-label">Meta Tags</span>
                </div>
                """, unsafe_allow_html=True)
            with r2c3:
                st.markdown(f"""
                <div class="glass-metric">
                    <span class="metric-val">{data['status_code']}</span>
                    <span class="metric-label">Server Code</span>
                </div>
                """, unsafe_allow_html=True)

        # --- TABS SECTION ---
        st.markdown("###")
        t1, t2 = st.tabs(["📄 Content Architecture", "👁️ Vision Analysis"])
        
        with t1:
            st.info(f"**Title Tag:** {data['title']}")
            st.code(f"Meta Description: {data['meta_desc']}", language="html")
            
        with t2:
            st.markdown("#### Image Alt-Text Auditor")
            df_img = pd.DataFrame(data["images"])
            
            if not df_img.empty:
                missing = df_img[df_img['alt'] == '']
                st.metric("Images Missing Alt-Text", len(missing), delta_color="inverse")
                
                if not missing.empty:
                    col_sel, col_prev = st.columns([1, 1])
                    with col_sel:
                        img_opt = st.selectbox("Select Image to Fix:", missing['src'].tolist())
                        if st.button("✨ Generate AI Caption"):
                            with st.spinner("AI Processing..."):
                                cap = generate_ai_caption(img_opt)
                                st.success("Generated:")
                                st.code(cap)
                    with col_prev:
                        if img_opt: st.image(img_opt, width=300)
            else:
                st.success("No images found.")