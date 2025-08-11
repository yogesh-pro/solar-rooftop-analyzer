from flask import Flask, request, render_template, jsonify, flash, redirect, url_for
import torch
import torchvision.transforms as T
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import io
import base64
from openai import OpenAI
import os
import re
import json
from model_loader import load_model_with_fallback
from werkzeug.utils import secure_filename
import secrets
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # For flash messages

# Configure upload settings
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static/results', exist_ok=True)

# Load model and initialize transform (gracefully handle missing model for development)
print("Loading model...")
try:
    model, device = load_model_with_fallback()
    MODEL_AVAILABLE = True
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"⚠️  Model not available: {e}")
    print("🔧 Running in development mode - UI testing only")
    model, device = None, None
    MODEL_AVAILABLE = False

transform = T.Compose([
    T.Resize((256, 256)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Initialize OpenAI client
def get_openai_client():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OpenRouter API key not found in environment variables")
    
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ask_openrouter(prompt, model_name="google/gemma-3-12b-it:free"):
    try:
        client = get_openai_client()
        
        # Validate API key format
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key or not api_key.startswith("sk-or-v1-"):
            raise ValueError("Invalid API Key Format: OpenRouter API keys should start with 'sk-or-v1-'")
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "authentication" in error_msg.lower():
            raise ValueError("API Authentication Failed - Check your OpenRouter API key and account credits")
        elif "429" in error_msg:
            raise ValueError("Rate Limited - Too many requests. Please wait a moment and try again.")
        elif "quota" in error_msg.lower():
            raise ValueError("Quota Exceeded - Your OpenRouter account is out of credits.")
        else:
            raise ValueError(f"API Error: {error_msg}")

def get_prompt(area_m2):
    prompt = f"""You are a solar energy advisor AI. Analyze the given rooftop area in square meters and return installation suggestions and financial assessment.
    Rooftop area: {area_m2:.2f}
    Avg solar panel size: 1.6 m²
    Power Output: 250W to 400W.
    remember the avg household power consumption in India is 1,395 kWh/month.
    Respond ONLY in JSON with the following keys:
    {{
  "recommended_panels": int,
  "recommended_panels_explanation": str,
  "total_capacity_kw": float,
  "total_capacity_kw_explanation": str,
  "yearly_production_kwh": float,
  "yearly_production_explanation": str,
  "installation_cost_inr": float,
  "installation_cost_explanation": str,
  "yearly_savings_inr": float,
  "yearly_savings_explanation": str,
  "payback_period_years": float,
  "payback_period_explanation": str
}}"""
    return prompt.strip()

def parse_json_from_text(text):
    try:
        json_str = re.search(r"\{.*\}", text, re.DOTALL).group(0)
        data = json.loads(json_str)
        return data
    except Exception as e:
        raise ValueError(f"Failed to parse JSON from AI response: {e}")

def create_bill_comparison_chart(metrics):
    """Create a chart comparing electricity bills with and without solar"""
    try:
        # Calculate monthly values
        monthly_production_kwh = metrics['yearly_production_kwh'] / 12
        monthly_savings = metrics['yearly_savings_inr'] / 12
        
        # Assuming average electricity rate in India (₹5-8 per kWh)
        avg_electricity_rate = 6.5  # ₹ per kWh
        
        # Calculate monthly consumption based on average Indian household (1,395 kWh/month)
        avg_monthly_consumption = 1395  # kWh
        monthly_bill_without_solar = avg_monthly_consumption * avg_electricity_rate
        
        # Calculate bill with solar (reduced consumption from grid)
        grid_consumption_with_solar = max(0, avg_monthly_consumption - monthly_production_kwh)
        monthly_bill_with_solar = grid_consumption_with_solar * avg_electricity_rate
        
        # Create data for single month comparison
        categories = ['Without Solar', 'With Solar']
        bills = [monthly_bill_without_solar, monthly_bill_with_solar]
        colors = ['#ff6b6b', '#4ecdc4']
        
        # Create the chart
        fig, ax = plt.subplots(figsize=(8, 6))
        
        bars = ax.bar(categories, bills, color=colors, alpha=0.8, width=0.6)
        
        # Customize the chart
        ax.set_ylabel('Monthly Bill (₹)', fontweight='bold', fontsize=12)
        ax.set_title('Monthly Electricity Bill Comparison', fontweight='bold', fontsize=14)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, bill in zip(bars, bills):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 50,
                   f'₹{int(bill)}', ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # Add savings annotation in the middle
        savings = monthly_bill_without_solar - monthly_bill_with_solar
        savings_percentage = (savings / monthly_bill_without_solar) * 100
        
        # Add savings text between bars
        ax.text(0.5, max(bills) * 0.5, f'Monthly Savings\n₹{int(savings)}\n({savings_percentage:.1f}% reduction)', 
                ha='center', va='center', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.8),
                transform=ax.transData)
        
        # Add consumption details
        ax.text(0.02, 0.98, f'Monthly Consumption: {avg_monthly_consumption} kWh\nSolar Production: {int(monthly_production_kwh)} kWh', 
                transform=ax.transAxes, fontsize=10,
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7),
                verticalalignment='top')
        
        plt.tight_layout()
        
        # Convert to base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        chart_data = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return chart_data
        
    except Exception as e:
        raise ValueError(f"Error creating bill comparison chart: {str(e)}")

def process_image(image_path):
    """Process uploaded image and return rooftop analysis"""
    if not MODEL_AVAILABLE:
        # Return mock data for development mode
        return 150.0, "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    try:
        # Load and process image
        image = Image.open(image_path).convert("RGB")
        input_tensor = transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            output = model(input_tensor)
            predicted_mask = torch.argmax(output, dim=1).squeeze().cpu().numpy()

        # Calculate rooftop area
        rooftop_pixels = np.sum(predicted_mask == 1)
        area_per_pixel_m2 = 0.01
        estimated_area = rooftop_pixels * area_per_pixel_m2

        # Create visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Original image
        ax1.imshow(image)
        ax1.set_title("Original Image")
        ax1.axis("off")
        
        # Predicted mask
        ax2.imshow(predicted_mask, cmap="viridis")
        ax2.set_title("Predicted Rooftop Mask")
        ax2.axis("off")
        
        plt.tight_layout()
        
        # Save plot to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plot_data = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return estimated_area, plot_data
        
    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Check if this is image upload method
        method = request.form.get('method', 'image')
        
        if method == 'image':
            # Original image upload logic
            if 'file' not in request.files:
                flash('No file uploaded')
                return redirect(url_for('index'))
            
            file = request.files['file']
            
            if file.filename == '':
                flash('No file selected')
                return redirect(url_for('index'))
            
            if not allowed_file(file.filename):
                flash('Invalid file type. Please upload JPG, JPEG, or PNG files only.')
                return redirect(url_for('index'))
            
            # Save uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Process image
            estimated_area, plot_data = process_image(file_path)
            
            # Check minimum area
            if estimated_area < 10:
                flash(f'Estimated rooftop area ({estimated_area:.2f} m²) is too small. Please ensure the image is clear and the rooftop is visible.')
                return redirect(url_for('index'))
            
            # Get AI analysis
            prompt = get_prompt(estimated_area)
            ai_response = ask_openrouter(prompt)
            metrics = parse_json_from_text(ai_response)
            
            # Generate bill comparison chart
            bill_chart_data = create_bill_comparison_chart(metrics)
            
            # Clean up uploaded file
            os.remove(file_path)
            
            return render_template('results.html', 
                                 area=estimated_area,
                                 plot_data=plot_data,
                                 metrics=metrics,
                                 ai_response=ai_response,
                                 bill_chart_data=bill_chart_data,
                                 method='image')
        
    except ValueError as e:
        flash(f'Error: {str(e)}')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Unexpected error: {str(e)}')
        return redirect(url_for('index'))

@app.route('/analyze-manual', methods=['POST'])
def analyze_manual():
    try:
        # Get manually entered area
        area_str = request.form.get('area')
        if not area_str:
            flash('Please enter a rooftop area')
            return redirect(url_for('index'))
        
        try:
            estimated_area = float(area_str)
        except ValueError:
            flash('Please enter a valid number for rooftop area')
            return redirect(url_for('index'))
        
        # Validate area
        if estimated_area < 10:
            flash('Rooftop area must be at least 10 m²')
            return redirect(url_for('index'))
        
        if estimated_area > 10000:
            flash('Rooftop area seems too large. Please check your input.')
            return redirect(url_for('index'))
        
        # Get AI analysis
        prompt = get_prompt(estimated_area)
        ai_response = ask_openrouter(prompt)
        metrics = parse_json_from_text(ai_response)
        
        # Generate bill comparison chart
        bill_chart_data = create_bill_comparison_chart(metrics)
        
        return render_template('results.html', 
                             area=estimated_area,
                             plot_data=None,  # No image analysis for manual entry
                             metrics=metrics,
                             ai_response=ai_response,
                             bill_chart_data=bill_chart_data,
                             method='manual')
        
    except ValueError as e:
        flash(f'Error: {str(e)}')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Unexpected error: {str(e)}')
        return redirect(url_for('index'))

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for programmatic access"""
    try:
        # Check if this is a manual area entry or file upload
        if 'area' in request.form or 'area' in request.json if request.json else False:
            # Manual area entry via API
            if request.json:
                area_data = request.json.get('area')
            else:
                area_data = request.form.get('area')
            
            try:
                estimated_area = float(area_data)
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid area value'}), 400
            
            if estimated_area < 10:
                return jsonify({'error': 'Area must be at least 10 m²'}), 400
            
            if estimated_area > 10000:
                return jsonify({'error': 'Area seems too large'}), 400
                
        else:
            # File upload method
            if 'file' not in request.files:
                return jsonify({'error': 'No file uploaded'}), 400
            
            file = request.files['file']
            
            if not allowed_file(file.filename):
                return jsonify({'error': 'Invalid file type'}), 400
            
            # Save and process file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            estimated_area, _ = process_image(file_path)
            
            if estimated_area < 10:
                os.remove(file_path)
                return jsonify({'error': 'Rooftop area too small'}), 400
            
            # Clean up file
            os.remove(file_path)
        
        # Get AI analysis
        prompt = get_prompt(estimated_area)
        ai_response = ask_openrouter(prompt)
        metrics = parse_json_from_text(ai_response)
        
        # Generate bill comparison chart
        bill_chart_data = create_bill_comparison_chart(metrics)
        
        return jsonify({
            'estimated_area': estimated_area,
            'metrics': metrics,
            'bill_chart_data': bill_chart_data,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(413)
def too_large(e):
    flash('File is too large. Maximum size is 16MB.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Check for API key
    if not os.getenv("OPENROUTER_API_KEY"):
        print("WARNING: OPENROUTER_API_KEY environment variable not set!")
        print("Set it with: export OPENROUTER_API_KEY='your-api-key-here'")
    
    app.run(debug=True, host='0.0.0.0', port=8080)
