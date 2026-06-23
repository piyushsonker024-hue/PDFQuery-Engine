import streamlit as st
import requests
import pandas as pd
import json

st.set_page_config(page_title="PDFQueryEngine")
st.title("PDFQueryEngine")
st.write("Upload a PDF with text, tables, or images, and ask anything about its content.")

UPLOAD_URL = "http://localhost:800/upload"
ASK_URL = "http://localhost:800/ask"

pdf_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if pdf_file:
    st.success(f"File '{pdf_file.name}' uploaded successfully!")
    if st.button("Process PDF"):
        with st.spinner("Uploading and processing PDF..."):
            files = {'pdf': pdf_file}
            try:
                response = requests.post(UPLOAD_URL, files=files)
                result = response.json()
                if response.status_code == 200:
                    pdf_id = result["pdf_id"]
                    st.session_state["pdf_id"] = pdf_id
                    st.success("PDF processed successfully!")
                    st.info(f"PDF ID: {pdf_id}")
                else:
                    st.error(result.get("error", "Something went wrong during processing."))
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")

if "pdf_id" in st.session_state:
    st.markdown("---")
    st.subheader("Ask a question about the uploaded PDF")
    question = st.text_input("Enter your question here")

    if st.button("Get Answer") and question:
        with st.spinner("Thinking..."):
            try:
                data = {
                    "pdf_id": st.session_state["pdf_id"],
                    "question": question
                }
                response = requests.post(ASK_URL, json=data)
                result = response.json()

                if response.status_code == 200:
                    answer = result["answer"]
                    st.success("Answer:")
                    st.write(answer)

                    output_data = {
                        "pdf_id": st.session_state["pdf_id"],
                        "question": question,
                        "answer": answer
                    }

                    json_str = json.dumps(output_data, indent=2)
                    st.download_button(
                        label="Download as JSON",
                        data=json_str,
                        file_name="pdf_query_result.json",
                        mime="application/json"
                    )

                    csv_data = pd.DataFrame([output_data]).to_csv(index=False)
                    st.download_button(
                        label="Download as CSV",
                        data=csv_data,
                        file_name="pdf_query_result.csv",
                        mime="text/csv"
                    )
                else:
                    st.error(result.get("error", "Failed to get an answer."))
            except Exception as e:
                st.error(f"Error calling API: {e}")
    
    
