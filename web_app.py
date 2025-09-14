"""Web-based SGDK Character Creator."""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import base64
import io
import traceback
from PIL import Image
from app.core.generator import CharacterGenerator
from app.core.exporter import SGDKExporter
from flask_cors import CORS

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = 'sgdk_character_creator_secret'
CORS(app)  # Enable CORS for all routes

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
        app.logger.error(f"Error generating character: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e),
            'details': traceback.format_exc()
        }), 500

@app.route('/api/export', methods=['POST'])
def export_character():
    """Export character to SGDK format."""
    try:
        data = request.json
        character_name = data.get('name', 'character')
        
        # Sanitize character name (remove special characters)
        character_name = ''.join(c for c in character_name if c.isalnum() or c == '_')
        if not character_name:
            character_name = 'character'
        
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
        
        # Add download links
        download_links = {
            'c_file': f'/download/{character_name}.c',
            'h_file': f'/download/{character_name}.h',
            'png_file': f'/download/{character_name}.png'
        }
        
        return jsonify({
            'success': True,
            'files': files,
            'download_links': download_links,
            'character_name': character_name
        })
    except Exception as e:
        app.logger.error(f"Error exporting character: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e),
            'details': traceback.format_exc()
        }), 500

@app.route('/api/random', methods=['GET'])
def random_character():
    """Generate random character parameters."""
    try:
        import random
        
        head_types = ["round", "square", "oval", "triangle"]
        body_types = ["normal", "muscular", "slim", "round"]
        arm_types = ["normal", "muscular", "thin", "long"]
        leg_types = ["normal", "muscular", "thin", "long"]
        
        # Extended color palette with more Mega Drive style colors
        colors = [
            # Skin tones
            "#FFDDAA", "#DDAA88", "#AA8866", "#886644", "#664422",
            # Primary colors
            "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF",
            # Mega Drive palette colors
            "#FF6666", "#66FF66", "#6666FF", "#FFFF66", "#FF66FF", "#66FFFF",
            "#0066CC", "#CC6600", "#CC0066", "#66CC00", "#6600CC", "#00CC66"
        ]
        
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
        
        # Make sure skin colors are consistent
        if random.random() < 0.7:  # 70% chance to have matching skin colors
            skin_color = random.choice(colors[:5])  # Choose from skin tones
            character_data["head_color"] = skin_color
            character_data["arm_color"] = skin_color
        
        return jsonify(character_data)
    except Exception as e:
        app.logger.error(f"Error generating random character: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e),
            'details': traceback.format_exc()
        }), 500

@app.route('/download/<path:filename>')
def download_file(filename):
    """Download a file."""
    try:
        return send_file(f'static/output/{filename}', as_attachment=True)
    except Exception as e:
        app.logger.error(f"Error downloading file: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12000, debug=True)