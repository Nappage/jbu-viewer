# JBU Viewer

Interactive viewer for Joint Bilateral Upsampling (JBU) using Streamlit.

## Overview

This project provides a web-based interface for experimenting with Joint Bilateral Upsampling (JBU), allowing users to:
- Upload high-resolution guidance images and low-resolution solutions
- Adjust JBU parameters in real-time
- Visualize results and compare different parameter settings
- Analyze upsampling quality through various metrics

## Installation

```bash
# Clone the repository
git clone https://github.com/Nappage/jbu-viewer.git
cd jbu-viewer

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

Then open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501).

## Features

- Interactive parameter adjustment
- Real-time visualization
- Support for various image formats
- Error metrics visualization
- Side-by-side comparison view

## Dependencies

- Python 3.8+
- Streamlit
- NumPy
- OpenCV
- SciPy
- Matplotlib

## License

MIT License - see LICENSE file for details