import streamlit as st
import torch
import torchvision.transforms as T
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from openai import OpenAI
import os
import re
import json
from model_loader import load_model_with_fallback

# Load model (same as before)
@st.cache_resource
def load_model():
    return load_model_with_fallback()

model, device = load_model()

transform = T.Compose([
    T.Resize((256, 256)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY", "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"),
)

def ask_openrouter(prompt, model="google/gemma-3-12b-it:free"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


def get_prompt(area_m2):
    # Prompt requests a JSON with all fields based on rooftop area only
    prompt =  f"""You are a solar energy advisor AI. Analyze the given rooftop area in square meters and return installation suggestions and financial assessment.
    Rooftop area: {area_m2:.2f}""" +"""
    Avg solar panel size: 1.6 m²
    Power Output: 250W to 400W.
    remember the avg houshold power consumption in India is 1,395 kWh kWh/month.
    Respond ONLY in JSON with the following keys:{
    {
  "recommended_panels": int,                // Recommended number of panels
  "recommended_panels_explanation": str,      // Explanation for panel recommendation
  "total_capacity_kw": float,               // Total system capacity in kilowatts
    "total_capacity_kw_explanation": str,        // Explanation for capacity recommendation
  "yearly_production_kwh": float,           // Annual energy production in kWh
    "yearly_production_explanation": str,        // Explanation for production estimate
  "installation_cost_inr": float,           // Estimated cost in Indian Rupees
    "installation_cost_explanation": str,        // Explanation for cost estimate
  "yearly_savings_inr": float,              // Estimated annual savings in Indian Rupees
    "yearly_savings_explanation": str,         // Explanation for savings estimate
  "payback_period_years": float             // ROI / Payback period in years
    "payback_period_explanation": str         // Explanation for payback period estimate
}
    } 
    """.strip()
    return prompt


def parse_json_from_text(text):
    try:
        # Extract JSON substring from text (if any extra text)
        json_str = re.search(r"\{.*\}", text, re.DOTALL).group(0)
        data = json.loads(json_str)
        return data
    except Exception as e:
        st.error(f"Failed to parse JSON from AI response: {e}")
        return None

st.title("☀️ Rooftop Solar Analysis with AI-generated Metrics")

uploaded_file = st.file_uploader("Upload rooftop image (jpg, png)", type=["jpg","jpeg","png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_tensor)
        predicted_mask = torch.argmax(output, dim=1).squeeze().cpu().numpy()

    rooftop_pixels = np.sum(predicted_mask == 1)
    area_per_pixel_m2 = 0.01
    estimated_area = rooftop_pixels * area_per_pixel_m2

    st.subheader("🏠 Estimated Rooftop Area")
    st.success(f"{estimated_area:.2f} m² usable rooftop")

    # Side-by-side images
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Original Image", use_container_width=True)
    with col2:
        fig, ax = plt.subplots()
        ax.imshow(predicted_mask, cmap="viridis")
        ax.set_title("Predicted Rooftop Mask")
        ax.axis("off")
        st.pyplot(fig)
    if estimated_area < 10:
        st.warning("Estimated rooftop area is less than 10 m². Please ensure the image is clear and the rooftop is visible.")
        st.stop()
    st.subheader("🤖 Fetching solar potential metrics from AI...")
    with st.spinner("Contacting AI model..."):
        prompt = get_prompt(estimated_area)
        ai_response = ask_openrouter(prompt)
        st.markdown("**Raw AI response:**")
        st.code(ai_response)

        try:
            metrics = parse_json_from_text(ai_response)
            if not metrics:
                st.error("PLEASE RETRY : No valid JSON response received from AI.")
        except json.JSONDecodeError as e:
            st.error(f"PLEASE RETRY : Failed to decode JSON from AI response: {e}")
            metrics = None
        except Exception as e:
            st.error(f"PLEASE RETRY : An unexpected error occurred: {e}")
            metrics = None
        st.markdown("---")
    # Display AI-generated metrics

        if metrics:
            st.subheader("🔆 AI Generated Solar Metrics")

            st.markdown(f"<div style='font-size:20px; font-weight:bold;'>🔹 Recommended Panels: {metrics.get('recommended_panels', 'N/A')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-left:20px;'>📝 {metrics.get('recommended_panels_explanation', 'N/A')}</div>", unsafe_allow_html=True)

            st.markdown(f"<div style='font-size:20px; font-weight:bold;'>🔹 Total Capacity: {metrics.get('total_capacity_kw', 'N/A')} kW</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-left:20px;'>📝 {metrics.get('total_capacity_kw_explanation', 'N/A')}</div>", unsafe_allow_html=True)

            st.markdown(f"<div style='font-size:20px; font-weight:bold;'>🔹 Yearly Production: {metrics.get('yearly_production_kwh', 'N/A')} kWh</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-left:20px;'>📝 {metrics.get('yearly_production_explanation', 'N/A')}</div>", unsafe_allow_html=True)

            st.markdown(f"<div style='font-size:20px; font-weight:bold;'>🔹 Installation Cost: ₹{metrics.get('installation_cost_inr', 'N/A')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-left:20px;'>📝 {metrics.get('installation_cost_explanation', 'N/A')}</div>", unsafe_allow_html=True)

            st.markdown(f"<div style='font-size:20px; font-weight:bold;'>🔹 Yearly Savings: ₹{metrics.get('yearly_savings_inr', 'N/A')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-left:20px;'>📝 {metrics.get('yearly_savings_explanation', 'N/A')}</div>", unsafe_allow_html=True)

            st.markdown(f"<div style='font-size:20px; font-weight:bold;'>🔹 Payback Period: {metrics.get('payback_period_years', 'N/A')} years</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-left:20px;'>📝 {metrics.get('payback_period_explanation', 'N/A')}</div>", unsafe_allow_html=True)
