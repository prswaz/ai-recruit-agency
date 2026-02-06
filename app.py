import streamlit as st
from datetime import datetime
from pathlib import Path
from streamlit_option_menu import option_menu
from agents.orchestrator import OrchestratorAgent
from utils.logger import setup_logger
import asyncio

# Configure Streamlit page
st.set_page_config(
    page_title="AI Recruiter Agency",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize logger
logger = setup_logger()

# Adding CSS for the gradient background, typography, and button styles
st.markdown("""
    <style>
        /* General Styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            background: linear-gradient(135deg, #ff7f00, #00bfae);  /* Gradient: pink to teal */
            color: #fff;
        }

        a {
            text-decoration: none;
        }

        h1, h2, h3 {
            font-weight: 700;
        }

        p {
            font-weight: 400;
        }

        /* Hero Section */
        #hero {
            background: linear-gradient(135deg, #ff7f00, #00bfae);
            color: #fff;
            padding: 80px 20px;
            text-align: center;
        }

        #hero h1 {
            font-size: 48px;
            margin-bottom: 20px;
        }

        #hero p {
            font-size: 18px;
            margin-bottom: 40px;
        }

        /* Button Styling */
        .btn-primary, .btn-secondary {
            padding: 12px 24px;
            font-size: 16px;
            text-transform: uppercase;
            border-radius: 25px;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .btn-primary {
            background-color: #333;
            color: white;
        }

        .btn-primary:hover {
            background-color: #555;
        }

        .btn-secondary {
            background-color: white;
            color: #333;
            border: 2px solid #333;
        }

        .btn-secondary:hover {
            background-color: #f4f4f4;
        }

        /* About Section */
        #about {
            padding: 60px 20px;
            background-color: #f4f4f4;
            text-align: center;
        }

        #about h2 {
            font-size: 36px;
            margin-bottom: 20px;
        }

        #about p {
            font-size: 18px;
            max-width: 800px;
            margin: 0 auto;
        }

        /* Service Cards */
        .service-cards {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            padding: 40px 20px;
        }

        .service-card {
            background-color: #333;
            color: white;
            width: 30%;
            margin: 20px;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }

        .service-card:hover {
            transform: translateY(-10px);
        }

        .service-card h3 {
            font-size: 24px;
            margin-bottom: 10px;
        }

        .service-card p {
            font-size: 16px;
        }

        /* Footer Section */
        footer {
            padding: 20px;
            background-color: #333;
            color: white;
            text-align: center;
        }

        /* Job Listings */
        #jobs {
            padding: 60px 20px;
            background-color: #ffffff;
            text-align: center;
        }

        #jobs h2 {
            font-size: 36px;
            margin-bottom: 20px;
        }

        .job-listings {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }

        .job-card {
            background-color: #fff;
            width: 30%;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 15px;
            text-align: center;
            transition: transform 0.3s ease;
        }

        .job-card:hover {
            transform: translateY(-10px);
        }

        .job-card h3 {
            font-size: 24px;
            margin-bottom: 10px;
        }

        .job-card p {
            font-size: 16px;
            margin-bottom: 10px;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            #hero h1 {
                font-size: 36px;
            }

            #hero p {
                font-size: 16px;
            }

            .service-card {
                width: 100%;
                margin: 20px 0;
            }

            .job-card {
                width: 100%;
                margin: 20px 0;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Main async function to process the resume
async def process_resume(file_path: str) -> dict:
    try:
        orchestrator = OrchestratorAgent()
        resume_data = {
            "file_path": file_path,
            "submission_timestamp": datetime.now().isoformat(),
        }
        return await orchestrator.process_application(resume_data)
    except Exception as e:
        logger.error(f"Error processing resume: {str(e)}")
        raise

# Save the uploaded file
def save_uploaded_file(uploaded_file) -> str:
    try:
        save_dir = Path("uploads")
        save_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = save_dir / f"resume_{timestamp}_{uploaded_file.name}"

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return str(file_path)
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        raise

# Main app function
def main():
    # Navigation menu
    selected = option_menu(
        menu_title="Navigation",
        options=["Upload Resume", "About"],
        icons=["cloud-upload", "info-circle"],
        menu_icon="cast",
        default_index=0,
        styles={"nav-link": {"font-size": "1.2em", "color": "#00bcd4"}},
    )

    # Header section
    st.markdown('<header>', unsafe_allow_html=True)
    st.header("AI Recruiter Agency")
    st.subheader("Streamlined AI-powered recruitment process")
    st.markdown('</header>', unsafe_allow_html=True)

    # Main content area
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    if selected == "Upload Resume":
        uploaded_file = st.file_uploader(
            "Choose a PDF resume file",
            type=["pdf"],
            help="Upload a PDF resume for analysis",
            label_visibility="collapsed"
        )

        if uploaded_file:
            try:
                with st.spinner("Saving uploaded file..."):
                    file_path = save_uploaded_file(uploaded_file)

                st.info("Resume uploaded successfully! Processing...")

                # Create placeholder for progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()

                try:
                    status_text.text("Analyzing resume...")
                    progress_bar.progress(25)

                    result = asyncio.run(process_resume(file_path))

                    if result["status"] == "completed":
                        progress_bar.progress(100)
                        status_text.text("Analysis complete!")

                        # Display results in cards
                        st.markdown('<div class="card">', unsafe_allow_html=True)

                        st.subheader("Skills Analysis")
                        st.write(result["analysis_results"]["skills_analysis"])
                        st.metric("Confidence Score", f"{result['analysis_results']['confidence_score']:.0%}")

                        st.subheader("Matched Positions")
                        if not result["job_matches"]["matched_jobs"]:
                            st.warning("No suitable positions found.")
                        for job in result["job_matches"]["matched_jobs"]:
                            st.write(f"**{job['title']}**")
                            st.write(f"Match: {job.get('match_score', 'N/A')}")
                            st.write(f"📍 {job.get('location', 'N/A')}")
                            st.divider()

                        st.subheader("Screening Results")
                        st.metric("Screening Score", f"{result['screening_results']['screening_score']}%")
                        st.write(result["screening_results"]["screening_report"])

                        st.subheader("Final Recommendation")
                        st.info(result["final_recommendation"]["final_recommendation"], icon="💡")

                        st.markdown('</div>', unsafe_allow_html=True)

                        # Save results
                        output_dir = Path("results")
                        output_dir.mkdir(exist_ok=True)
                        output_file = output_dir / f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

                        with open(output_file, "w") as f:
                            f.write(str(result))

                        st.success(f"Results saved to: {output_file}")

                    else:
                        st.error(f"Process failed at stage: {result['current_stage']}")

                except Exception as e:
                    st.error(f"Error processing resume: {str(e)}")
                    logger.error(f"Processing error: {str(e)}", exc_info=True)

                finally:
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        logger.error(f"Error removing temporary file: {str(e)}")

            except Exception as e:
                st.error(f"Error handling file upload: {str(e)}")
                logger.error(f"Upload error: {str(e)}", exc_info=True)

    elif selected == "About":
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("About AI Recruiter Agency")
        st.write(
            """
            Welcome to **AI Recruiter Agency**, a cutting-edge recruitment analysis system powered by:
            
            - **Ollama (llama3.1)**: Advanced language model for natural language processing
            - **Streamlit**: Modern web interface for easy interaction
            
            Upload a resume to experience AI-powered recruitment analysis!
            """
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Footer section
    st.markdown('<footer>', unsafe_allow_html=True)
    st.write("AI Recruiter Agency &copy; 2025")
    st.markdown('</footer>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
