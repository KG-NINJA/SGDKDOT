"""SGDK exporter for character sprites."""

import os
from PIL import Image
from .generator import CharacterGenerator


class SGDKExporter:
    """Exports character sprites to SGDK format."""
    
    def __init__(self):
        self.generator = CharacterGenerator()
    
    def export_character(self, character_data, output_path):
        """Export character to SGDK format.
        
        Args:
            character_data (dict): Character specification
            output_path (str): Output file path (.c file)
        """
        base_name = os.path.splitext(os.path.basename(output_path))[0]
        output_dir = os.path.dirname(output_path)
        
        # Generate all animation frames
        frames = []
        frame_count = character_data.get("animation_frames", 1)
        size = character_data.get("size", 32)
        
        for frame in range(frame_count):
            sprite = self.generator.generate_character(character_data, frame)
            frames.append(sprite)
        
        # Convert to indexed color (Mega Drive palette)
        indexed_frames = []
        palette = self._create_megadrive_palette(character_data)
        
        for frame in frames:
            indexed_frame = self._convert_to_indexed(frame, palette)
            indexed_frames.append(indexed_frame)
        
        # Generate sprite data
        sprite_data = self._generate_sprite_data(indexed_frames, size)
        
        # Generate palette data
        palette_data = self._generate_palette_data(palette)
        
        # Write C file
        self._write_c_file(output_path, base_name, sprite_data, palette_data, 
                          size, frame_count)
        
        # Write header file
        header_path = os.path.join(output_dir, base_name + ".h")
        self._write_header_file(header_path, base_name, size, frame_count)
        
        # Save PNG reference
        png_path = os.path.join(output_dir, base_name + ".png")
        self._save_sprite_sheet(indexed_frames, png_path, size)
    
    def _create_megadrive_palette(self, character_data):
        """Create a Mega Drive compatible palette."""
        # Extract colors from character data
        colors = [
            "#000000",  # Black (transparent)
            character_data.get("head_color", "#FFDDAA"),
            character_data.get("body_color", "#0066CC"),
            character_data.get("arm_color", "#FFDDAA"),
            character_data.get("leg_color", "#0066CC"),
            "#000000",  # Black for outlines
            "#FFFFFF",  # White for highlights
            "#808080",  # Gray for shadows
        ]
        
        # Pad to 16 colors (Mega Drive palette size)
        while len(colors) < 16:
            colors.append("#000000")
        
        return colors[:16]
    
    def _convert_to_indexed(self, image, palette):
        """Convert RGBA image to indexed color using the given palette."""
        # Convert to RGB
        rgb_image = Image.new("RGB", image.size, (0, 0, 0))
        rgb_image.paste(image, mask=image.split()[-1])  # Use alpha as mask
        
        # Create palette image
        palette_image = Image.new("P", (1, 1))
        palette_colors = []
        for color in palette:
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            palette_colors.extend([r, g, b])
        
        # Pad palette to 768 bytes (256 colors * 3 components)
        while len(palette_colors) < 768:
            palette_colors.append(0)
        
        palette_image.putpalette(palette_colors)
        
        # Quantize to palette
        quantized = rgb_image.quantize(palette=palette_image)
        
        return quantized
    
    def _generate_sprite_data(self, frames, size):
        """Generate sprite data in SGDK format."""
        sprite_data = []
        
        for frame_idx, frame in enumerate(frames):
            frame_data = []
            
            # Convert to 4bpp (4 bits per pixel) format
            pixels = list(frame.getdata())
            
            # Group pixels in pairs (2 pixels per byte)
            for i in range(0, len(pixels), 2):
                pixel1 = pixels[i] & 0x0F
                pixel2 = pixels[i + 1] & 0x0F if i + 1 < len(pixels) else 0
                byte_value = (pixel1 << 4) | pixel2
                frame_data.append(byte_value)
            
            sprite_data.append(frame_data)
        
        return sprite_data
    
    def _generate_palette_data(self, palette):
        """Generate palette data in SGDK format."""
        palette_data = []
        
        for color in palette:
            # Convert to Mega Drive RGB format (4 bits per component)
            r = int(color[1:3], 16) >> 4
            g = int(color[3:5], 16) >> 4
            b = int(color[5:7], 16) >> 4
            
            # Mega Drive color format: 0000BBB0GGG0RRR0
            md_color = (b << 9) | (g << 5) | (r << 1)
            palette_data.append(md_color)
        
        return palette_data
    
    def _write_c_file(self, output_path, name, sprite_data, palette_data, 
                     size, frame_count):
        """Write the C source file."""
        with open(output_path, 'w') as f:
            f.write(f'#include "{name}.h"\n\n')
            
            # Write palette data
            f.write(f"const u16 {name}_palette[16] = {{\n")
            for i, color in enumerate(palette_data):
                if i % 8 == 0:
                    f.write("    ")
                f.write(f"0x{color:04X}")
                if i < len(palette_data) - 1:
                    f.write(", ")
                if i % 8 == 7:
                    f.write("\n")
            f.write("\n};\n\n")
            
            # Write sprite data for each frame
            for frame_idx, frame_data in enumerate(sprite_data):
                f.write(f"const u8 {name}_frame{frame_idx}_data[{len(frame_data)}] = {{\n")
                for i, byte in enumerate(frame_data):
                    if i % 16 == 0:
                        f.write("    ")
                    f.write(f"0x{byte:02X}")
                    if i < len(frame_data) - 1:
                        f.write(", ")
                    if i % 16 == 15:
                        f.write("\n")
                f.write("\n};\n\n")
            
            # Write sprite definitions
            for frame_idx in range(frame_count):
                tiles_w = (size + 7) // 8  # Round up to nearest tile
                tiles_h = (size + 7) // 8
                f.write(f"const SpriteDefinition {name}_frame{frame_idx} = {{\n")
                f.write(f"    .w = {tiles_w},\n")
                f.write(f"    .h = {tiles_h},\n")
                f.write(f"    .tiles = {name}_frame{frame_idx}_data,\n")
                f.write(f"    .palette = {name}_palette,\n")
                f.write(f"    .numTile = {tiles_w * tiles_h}\n")
                f.write("};\n\n")
            
            # Write animation array
            if frame_count > 1:
                f.write(f"const SpriteDefinition* {name}_animation[{frame_count}] = {{\n")
                for frame_idx in range(frame_count):
                    f.write(f"    &{name}_frame{frame_idx}")
                    if frame_idx < frame_count - 1:
                        f.write(",")
                    f.write("\n")
                f.write("};\n\n")
    
    def _write_header_file(self, output_path, name, size, frame_count):
        """Write the header file."""
        with open(output_path, 'w') as f:
            guard = f"{name.upper()}_H"
            f.write(f"#ifndef {guard}\n")
            f.write(f"#define {guard}\n\n")
            f.write("#include <genesis.h>\n\n")
            
            # Declarations
            f.write(f"extern const u16 {name}_palette[16];\n")
            
            for frame_idx in range(frame_count):
                f.write(f"extern const u8 {name}_frame{frame_idx}_data[];\n")
                f.write(f"extern const SpriteDefinition {name}_frame{frame_idx};\n")
            
            if frame_count > 1:
                f.write(f"extern const SpriteDefinition* {name}_animation[{frame_count}];\n")
            
            f.write(f"\n#define {name.upper()}_FRAME_COUNT {frame_count}\n")
            f.write(f"#define {name.upper()}_SIZE {size}\n")
            
            f.write(f"\n#endif // {guard}\n")
    
    def _save_sprite_sheet(self, frames, output_path, size):
        """Save a sprite sheet PNG for reference."""
        if not frames:
            return
        
        # Create sprite sheet
        sheet_width = len(frames) * size
        sheet_height = size
        
        sheet = Image.new("RGB", (sheet_width, sheet_height), (0, 0, 0))
        
        for i, frame in enumerate(frames):
            # Convert indexed to RGB
            rgb_frame = frame.convert("RGB")
            sheet.paste(rgb_frame, (i * size, 0))
        
        sheet.save(output_path)


def export():
    """Legacy function for compatibility."""
    return SGDKExporter()

