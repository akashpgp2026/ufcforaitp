import streamlit as st
import os
from markitdown import MarkItDown
from io import BytesIO

# Configuration and Page Setup
st.set_page_config(page_title="Universal Document Reader", page_icon="📄", layout="wide")

def main():
    st.title("📄 Universal Document Reader")
    st.markdown("Convert your Office docs, PDFs, and HTML files into clean Markdown instantly.")

    # Initialize the MarkItDown Engine
    # Note: MarkItDown handles internal requests; we pass configuration if needed
    mid = MarkItDown()

    # [2] Interface: Upload Area
    uploaded_files = st.file_uploader(
        "Drag and drop files here", 
        type=["docx", "xlsx", "pptx", "pdf", "html", "zip"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            base_name = os.path.splitext(uploaded_file.name)[0]
            
            with st.expander(f"📄 {uploaded_file.name}", expanded=True):
                try:
                    # Save uploaded file to a temporary location to process
                    # (MarkItDown works best with file paths or file-like objects)
                    with st.spinner(f"Processing {uploaded_file.name}..."):
                        # [1] The Engine: MarkItDown
                        result = mid.convert(uploaded_file)
                        content = result.text_content

                    # [2] Interface: Instant Preview
                    st.text_area(
                        label="Markdown Preview",
                        value=content,
                        height=300,
                        key=f"preview_{uploaded_file.name}"
                    )

                    # [2] Interface: Download Options
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.download_button(
                            label="Download as Markdown (.md)",
                            data=content,
                            file_name=f"{base_name}_converted.md",
                            mime="text/markdown",
                            key=f"md_{uploaded_file.name}"
                        )
                    
                    with col2:
                        st.download_button(
                            label="Download as Text (.txt)",
                            data=content,
                            file_name=f"{base_name}_converted.txt",
                            mime="text/plain",
                            key=f"txt_{uploaded_file.name}"
                        )

                except Exception as e:
                    # [3] Resilience: Error Handling
                    st.error(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")
                    # Optional: Log error for debugging
                    # st.exception(e)

if __name__ == "__main__":
    main()
