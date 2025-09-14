"""Web-based SGDK Character Creator."""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import base64
import io
from PIL import Image
from app.core.generator import CharacterGenerator
from app.core.exporter import SGDKExporter

app = Flask(__name__)
app.secret_key = 'sgdk_character_creator_secret'

# Initialize components
generator = CharacterGenerator()
exporter = SGDKExporter()

# Create output directory
os.makedirs('static/output', exist_ok=True)
os.makedirs('templates', exist_ok=True)

@app.route('/')
def index():
    """Main character creator page."""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_character():
    """Generate character sprite based on parameters."""
    try:
        data = request.json
        frame = data.get('frame', 0)
        
        # Generate character
        sprite = generator.generate_character(data, frame)
        
        # Convert to base64 for web display
        img_buffer = io.BytesIO()
        sprite.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{img_base64}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/export', methods=['POST'])
def export_character():
    """Export character to SGDK format."""
    try:
        data = request.json
        character_name = data.get('name', 'character')
        
        # Create output files
        output_path = f'static/output/{character_name}.c'
        exporter.export_character(data, output_path)
        
        # Read generated files
        files = {}
        
        # C file
        if os.path.exists(output_path):
            with open(output_path, 'r') as f:
                files['c_file'] = f.read()
        
        # Header file
        header_path = f'static/output/{character_name}.h'
        if os.path.exists(header_path):
            with open(header_path, 'r') as f:
                files['h_file'] = f.read()
        
        # PNG file (as base64)
        png_path = f'static/output/{character_name}.png'
        if os.path.exists(png_path):
            with open(png_path, 'rb') as f:
                png_base64 = base64.b64encode(f.read()).decode()
                files['png_file'] = f'data:image/png;base64,{png_base64}'
        
        return jsonify({
            'success': True,
            'files': files
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/random', methods=['GET'])
def random_character():
    """Generate random character parameters."""
    import random
    
    head_types = ["round", "square", "oval", "triangle"]
    body_types = ["normal", "muscular", "slim", "round"]
    arm_types = ["normal", "muscular", "thin", "long"]
    leg_types = ["normal", "muscular", "thin", "long"]
    
    colors = ["#FFDDAA", "#DDAA88", "#AA8866", "#886644", "#664422",
             "#FF6666", "#66FF66", "#6666FF", "#FFFF66", "#FF66FF", "#66FFFF"]
    
    character_data = {
        "head_type": random.choice(head_types),
        "body_type": random.choice(body_types),
        "arm_type": random.choice(arm_types),
        "leg_type": random.choice(leg_types),
        "head_color": random.choice(colors),
        "body_color": random.choice(colors),
        "arm_color": random.choice(colors),
        "leg_color": random.choice(colors),
        "size": random.randint(24, 48),
        "animation_frames": random.randint(2, 6)
    }
    
    return jsonify(character_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12000, debug=True)