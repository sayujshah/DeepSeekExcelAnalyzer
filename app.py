import gradio as gr
from Scripts.ExcelAnalyzer import ExcelAnalyzer

DEFAULT_MODEL = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"

def process_file_and_question(file, question, model_name, api_key):
    """Process the file and question with configurable model settings"""
    if file is None:
        return "Please upload an Excel file first."
    
    final_key = api_key if api_key.strip() else None
    # Use provided model name if available, otherwise use default
    final_model = model_name if model_name.strip() else DEFAULT_MODEL

    analyzer = ExcelAnalyzer(model_name=final_model, api_key=final_key)
    
    # Load file if not already loaded
    load_result = analyzer.load_excel(file)
    if "Error" in load_result:
        return load_result
    
    # Process question
    return analyzer.generate_response(question)

with gr.Blocks(title="Excel Data Analyzer") as app:
    gr.Markdown("""
    # Excel Data Analyzer
    Upload your Excel file then ask questions about the data.
    The AI will analyze your data and provide answers. Make sure your Excel file has clear column names and structured data.
    """)
    
    with gr.Row():
        with gr.Column():
            file_input = gr.File(label="Upload Excel File")
            question_input = gr.Textbox(
                label="Enter your question about the data"
            )
    
    with gr.Accordion("Advanced Settings", open=False):
        model_input = gr.Textbox(
            label="Model Name (optional)",
            placeholder=f"Default: {DEFAULT_MODEL}",
            value=""
        )
        api_key_input = gr.Textbox(
                label="API Key (optional)",
                placeholder="Enter your API key here (if needed)",
                value="",
                type="password"
        )

    with gr.Row():
        submit_btn = gr.Button("Analyze")
        store_btn = gr.Button("Store file contents in memory")
    
    output = gr.Textbox(label="Analysis Result", lines=10)
    status_output = gr.Textbox(label="Status message", lines=2)
    
    submit_btn.click(
        fn=process_file_and_question,
        inputs=[file_input, question_input, model_input, api_key_input],
        outputs=output
    )

    # Click event for storing data in ChromaDB
    store_in_chromadb=True
    store_btn.click(
        fn=ExcelAnalyzer().store_in_chroma_db,
        inputs=[file_input],
        outputs=status_output
    )

if __name__ == "__main__":
    app.launch()