# DeepSeek Excel Data Analysis Chatbot

## Overview

This LLM-based chatbot is an intelligent AI-powered application that allows users to interact with Excel files using natural language questions. The bot is designed to run completely locally with the state-of-the-art DeepSeek R1 model or may take in an API key for another model of your choice.

## Features

- 🔍 Upload Excel files for interactive analysis
- 💬 Ask questions about your data in natural language
- 🤖 Compatible with the tate-of-the art DeepSeek R1 reasoning model
- 🗃️ Vector database storage for enhanced context retrieval
- 🔧 Configurable AI model and API key support

## Prerequisites

- Python 3.8+
- Required Python libraries:
  - huggingface_hub
  - gradio
  - pandas
  - openai
  - openpyxl
  - chromadb

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sayujshah/DeepSeekExcelAnalyzer.git
cd DeepSeekExcelAnalyzer
```

2. Install required dependencies:
```bash
pip install huggingface_hub openai gradio pandas openpyxl chromadb
```
or run:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python app.py
```

This will launch a Gradio web interface where you can:
- Upload an Excel file
- Ask questions about the data
- Optionally configure the AI model and provide an API key
- Optionally store the Excel file into the ChromaDB memory for future retrieval

### Advanced Features

#### Model Configuration
- Default Model: `deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B`
- You can specify a different model in the "Advanced Settings" section
- Supports both HuggingFace and OpenAI-compatible APIs
- Supports all HuggingFace inferences

#### ChromaDB Storage
- Use the "Store file contents in memory" button to save Excel data in a local vector database
- Enables more contextual and relevant AI responses in future requests

## Additional Scripts

### `ExcelAnalyzer.py`
The functions under-the-hood that load, embed, and prompt the chatbot with instructions on how to answer user questions.

### `add_to_chromadb.py`
A utility script to bulk add Excel files to the ChromaDB collection. This is useful for adding common reports that you can refer back to or compare current reports to via the chatbot. Modify the `folder_path` variable to point to your Excel files directory.

## Limitations

- Performance may vary based on data complexity, local disk space, and CPU performance (highly recommend to use virtual GPUs or an API key)
- Requires structured Excel files with clear column names
- Response quality depends on the chosen AI model

## License

MIT License

Copyright (c) 2025 sayujshah

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.