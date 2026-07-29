import streamlit as st
from youtube_analyzer import build_youtube_agent
import re

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI YouTube Analyzer",
    page_icon="🎥",
    layout="wide"
)

# -----------------------------
# CSS STYLING
# -----------------------------
st.markdown("""
<style>
html, body, [class*="css"]{
    font-family: 'Segoe UI', sans-serif;
}

.main{
    background: #0E1117;
}

.hero{
    text-align: center;
    padding: 20px;
}

.hero h1{
    color: #ff4b4b;
    font-size: 55px;
    margin-bottom: 5px;
}

.hero p{
    color: #BBBBBB;
    font-size: 20px;
}

.metric-card{
    background: #1B1F2A;
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid #2C313C;
}

.metric-title{
    color: #BBBBBB;
    font-size: 16px;
}

.metric-value{
    color: white;
    font-size: 22px;
    font-weight: bold;
}

.stButton>button{
    width: 100%;
    background: #ff4b4b;
    color: white;
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
}

.stButton>button:hover{
    background: #ff2222;
}

.footer{
    text-align: center;
    color: gray;
    padding: 30px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.title("🎥 AI YouTube Analyzer")
    st.markdown("---")
    st.success("### Features")
    st.write("""
    ✅ AI Summary  
    ✅ Key Insights  
    ✅ Important Topics  
    ✅ Action Points  
    ✅ Fast Analysis  
    ✅ Markdown Report  
    """)
    st.markdown("---")
    st.info("""
    Built using:
    • Agno AI  
    • Groq LLM  
    • Streamlit  
    • Python  
    """)
    st.markdown("---")
    st.caption("Made ❤️ by Prince Yadav")

# -----------------------------
# HERO SECTION
# -----------------------------
st.markdown("""
<div class='hero'>
    <h1>🎥 AI YouTube Video Analyzer</h1>
    <p>Get an AI-generated summary, insights, and action points from any YouTube video.</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# METRICS SECTION
# -----------------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">⚡ Speed</div>
        <div class="metric-value">10-30 sec</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">🤖 AI Model</div>
        <div class="metric-value">Groq</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">📄 Output</div>
        <div class="metric-value">Markdown Report</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# -----------------------------
# AGENT INITIALIZATION
# -----------------------------
@st.cache_resource
def get_agent():
    return build_youtube_agent()

agent = get_agent()

# -----------------------------
# URL INPUT
# -----------------------------
video_url = st.text_input(
    "📺 Enter YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=..."
)

# -----------------------------
# THUMBNAIL PREVIEW FUNCTION
# -----------------------------
def get_thumbnail(url):
    match = re.search(r"(?:v=|youtu\.be/)([\w-]+)", url)
    if match:
        return f"https://img.youtube.com/vi/{match.group(1)}/maxresdefault.jpg"
    return None

if video_url:
    thumb = get_thumbnail(video_url)
    if thumb:
        st.image(thumb, use_container_width=True)

# -----------------------------
# EXAMPLE URL EXPANDER
# -----------------------------
with st.expander("📌 Example YouTube URL"):
    st.code("https://youtu.be/JkaxUblCGz0?si=BbstJGieMKx-ldVg")

# Initialize session state for holding analysis results
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# -----------------------------
# ANALYZE BUTTON & LOGIC
# -----------------------------
if st.button("🚀 Analyze Video"):
    if not video_url or video_url.strip() == "":
        st.warning("Please enter a valid YouTube URL.")
    else:
        try:
            progress = st.progress(0)
            with st.spinner("Analyzing Video..."):
                progress.progress(20)
                
                # Run AI Agent
                response = agent.run(f"Analyze this YouTube video:\n{video_url}")
                progress.progress(70)
                
                # Store output in session state
                st.session_state.analysis_result = response.content
                progress.progress(100)

            st.success("✅ Analysis Completed")
            st.balloons()
            
        except Exception as e:
            st.error(f"An error occurred during analysis: {e}")

# Display results if available in session state
if st.session_state.analysis_result:
    st.divider()
    st.subheader("📑 AI Analysis Report")
    st.markdown(st.session_state.analysis_result)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.download_button(
            label="📥 Download Report",
            data=st.session_state.analysis_result,
            file_name="youtube_analysis.md",
            mime="text/markdown"
        )

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("""
<hr>
<div class='footer'>
    Made with ❤️ by <b>Prince Yadav</b>
    <br><br>
    AI Powered YouTube Video Analysis
</div>
""", unsafe_allow_html=True)