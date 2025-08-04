# ☀️ Solar Rooftop Analysis App

An intelligent system that analyzes rooftop images to estimate usable solar panel area and uses AI (via OpenRouter) to calculate installation metrics, energy production, and ROI estimates for homeowners and solar professionals.

🚀 **Live Demo**: [Click Me!](https://solar-rooftop-analyzer-vphpoef7w8xi6dx27jqq3z.streamlit.app/)

---

## 📌 Features

- 🔼 Upload a rooftop image via the web interface
- 🧠 ML-based rooftop segmentation using a deep learning model
- 📏 Automated rooftop area estimation in square meters
- 🧮 AI-powered solar metric generation:
  - 📦 Recommended number of solar panels
  - ⚡ System capacity (kW)
  - 🌞 Annual energy production (kWh)
  - 💰 Installation cost
  - 🪙 Yearly savings
  - ⏳ Payback period
  - 📘 Detailed explanation for each metric (via LLM)

---

## 🛠️ Project Setup Instructions

### 1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/solar-rooftop-analyzer.git
cd solar-rooftop-analyzer
```

### 2. **Create and Activate a Virtual Environment**
```bash
# For Unix/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

### 3. **Install Required Packages**
```bash
pip install -r requirements.txt
```

### 4. **Download Model from [HERE](https://github.com/yogesh-pro/solar-rooftop-analyzer/releases/tag/Model)**


### 5. **🚀 Run the Streamlit App**
```bash
streamlit run app.py
```
- Then open your browser at http://localhost:8501

### **📂 Project Structure**
```bash
├── app.py                      # Streamlit web app
├── model.ipynb                 # Model training or inference notebook
├── requirements.txt            # Python dependencies
├── rooftop_best_model.pt       # Your trained segmentation model
├── README.md                   # This file
```

### **🌟 Future Scope**
- Roof tilt & direction consideration
- Shadow detection
- Real-time ROI tracking with dynamic electricity pricing

