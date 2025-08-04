"""Character generator for SGDK sprites."""

from PIL import Image, ImageDraw
import math


class CharacterGenerator:
    """Generates character sprites based on user specifications."""
    
    def __init__(self):
        self.base_size = 32
    
    def generate_character(self, character_data, frame=0):
        """Generate a character sprite based on the given data.
        
        Args:
            character_data (dict): Character specification
            frame (int): Animation frame number
            
        Returns:
            PIL.Image: Generated character sprite
        """
        size = character_data.get("size", 32)
        
        # Create image with transparency
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Animation offset for walking
        total_frames = character_data.get("animation_frames", 1)
        if total_frames > 1:
            walk_offset = math.sin(frame * 2 * math.pi / total_frames) * 2
            bob_offset = abs(math.sin(frame * 2 * math.pi / total_frames)) * 1
        else:
            walk_offset = 0
            bob_offset = 0
        
        # Draw character parts
        self._draw_legs(draw, character_data, size, walk_offset)
        self._draw_body(draw, character_data, size, bob_offset)
        self._draw_arms(draw, character_data, size, walk_offset, bob_offset)
        self._draw_head(draw, character_data, size, bob_offset)
        
        return image
    
    def _draw_head(self, draw, data, size, bob_offset):
        """Draw the character's head."""
        head_type = data.get("head_type", "round")
        color = data.get("head_color", "#FFDDAA")
        
        # Head position and size
        head_size = size // 4
        head_x = size // 2 - head_size // 2
        head_y = size // 6 - int(bob_offset)
        
        if head_type == "round":
            draw.ellipse([head_x, head_y, head_x + head_size, head_y + head_size], 
                        fill=color, outline="#000000", width=1)
        elif head_type == "square":
            draw.rectangle([head_x, head_y, head_x + head_size, head_y + head_size], 
                          fill=color, outline="#000000", width=1)
        elif head_type == "oval":
            draw.ellipse([head_x, head_y, head_x + head_size, head_y + head_size + 4], 
                        fill=color, outline="#000000", width=1)
        elif head_type == "triangle":
            points = [
                (head_x + head_size // 2, head_y),
                (head_x, head_y + head_size),
                (head_x + head_size, head_y + head_size)
            ]
            draw.polygon(points, fill=color, outline="#000000")
        
        # Draw simple face
        eye_size = max(1, head_size // 8)
        eye_y = head_y + head_size // 3
        
        # Eyes
        draw.ellipse([head_x + head_size // 3 - eye_size, eye_y, 
                     head_x + head_size // 3 + eye_size, eye_y + eye_size * 2], 
                    fill="#000000")
        draw.ellipse([head_x + 2 * head_size // 3 - eye_size, eye_y, 
                     head_x + 2 * head_size // 3 + eye_size, eye_y + eye_size * 2], 
                    fill="#000000")
        
        # Mouth
        mouth_y = head_y + 2 * head_size // 3
        draw.arc([head_x + head_size // 4, mouth_y, 
                 head_x + 3 * head_size // 4, mouth_y + head_size // 4], 
                0, 180, fill="#000000", width=1)
    
    def _draw_body(self, draw, data, size, bob_offset):
        """Draw the character's body."""
        body_type = data.get("body_type", "normal")
        color = data.get("body_color", "#0066CC")
        
        # Body position and size
        body_width = size // 3
        body_height = size // 2
        body_x = size // 2 - body_width // 2
        body_y = size // 3 - int(bob_offset)
        
        if body_type == "normal":
            draw.rectangle([body_x, body_y, body_x + body_width, body_y + body_height], 
                          fill=color, outline="#000000", width=1)
        elif body_type == "muscular":
            body_width = int(body_width * 1.3)
            body_x = size // 2 - body_width // 2
            draw.rectangle([body_x, body_y, body_x + body_width, body_y + body_height], 
                          fill=color, outline="#000000", width=1)
        elif body_type == "slim":
            body_width = int(body_width * 0.7)
            body_x = size // 2 - body_width // 2
            draw.rectangle([body_x, body_y, body_x + body_width, body_y + body_height], 
                          fill=color, outline="#000000", width=1)
        elif body_type == "round":
            draw.ellipse([body_x, body_y, body_x + body_width, body_y + body_height], 
                        fill=color, outline="#000000", width=1)
    
    def _draw_arms(self, draw, data, size, walk_offset, bob_offset):
        """Draw the character's arms."""
        arm_type = data.get("arm_type", "normal")
        color = data.get("arm_color", "#FFDDAA")
        
        # Arm dimensions
        arm_width = size // 8
        arm_length = size // 3
        
        # Left arm
        left_arm_x = size // 2 - size // 3 - arm_width
        arm_y = size // 3 + size // 12 - int(bob_offset)
        
        # Right arm  
        right_arm_x = size // 2 + size // 3
        
        # Arm swing animation
        left_swing = int(walk_offset)
        right_swing = -int(walk_offset)
        
        if arm_type == "normal":
            # Left arm
            draw.rectangle([left_arm_x, arm_y + left_swing, 
                          left_arm_x + arm_width, arm_y + arm_length + left_swing], 
                         fill=color, outline="#000000", width=1)
            # Right arm
            draw.rectangle([right_arm_x, arm_y + right_swing, 
                          right_arm_x + arm_width, arm_y + arm_length + right_swing], 
                         fill=color, outline="#000000", width=1)
        elif arm_type == "muscular":
            arm_width = int(arm_width * 1.5)
            # Left arm
            draw.rectangle([left_arm_x, arm_y + left_swing, 
                          left_arm_x + arm_width, arm_y + arm_length + left_swing], 
                         fill=color, outline="#000000", width=1)
            # Right arm
            draw.rectangle([right_arm_x, arm_y + right_swing, 
                          right_arm_x + arm_width, arm_y + arm_length + right_swing], 
                         fill=color, outline="#000000", width=1)
        elif arm_type == "thin":
            arm_width = max(1, int(arm_width * 0.6))
            # Left arm
            draw.rectangle([left_arm_x, arm_y + left_swing, 
                          left_arm_x + arm_width, arm_y + arm_length + left_swing], 
                         fill=color, outline="#000000", width=1)
            # Right arm
            draw.rectangle([right_arm_x, arm_y + right_swing, 
                          right_arm_x + arm_width, arm_y + arm_length + right_swing], 
                         fill=color, outline="#000000", width=1)
        elif arm_type == "long":
            arm_length = int(arm_length * 1.3)
            # Left arm
            draw.rectangle([left_arm_x, arm_y + left_swing, 
                          left_arm_x + arm_width, arm_y + arm_length + left_swing], 
                         fill=color, outline="#000000", width=1)
            # Right arm
            draw.rectangle([right_arm_x, arm_y + right_swing, 
                          right_arm_x + arm_width, arm_y + arm_length + right_swing], 
                         fill=color, outline="#000000", width=1)
    
    def _draw_legs(self, draw, data, size, walk_offset):
        """Draw the character's legs."""
        leg_type = data.get("leg_type", "normal")
        color = data.get("leg_color", "#0066CC")
        
        # Leg dimensions
        leg_width = size // 8
        leg_length = size // 3
        
        # Leg positions
        left_leg_x = size // 2 - size // 6 - leg_width // 2
        right_leg_x = size // 2 + size // 6 - leg_width // 2
        leg_y = size // 2 + size // 6
        
        # Walking animation
        left_step = int(walk_offset)
        right_step = -int(walk_offset)
        
        if leg_type == "normal":
            # Left leg
            draw.rectangle([left_leg_x, leg_y, 
                          left_leg_x + leg_width, leg_y + leg_length + left_step], 
                         fill=color, outline="#000000", width=1)
            # Right leg
            draw.rectangle([right_leg_x, leg_y, 
                          right_leg_x + leg_width, leg_y + leg_length + right_step], 
                         fill=color, outline="#000000", width=1)
        elif leg_type == "muscular":
            leg_width = int(leg_width * 1.5)
            left_leg_x = size // 2 - size // 6 - leg_width // 2
            right_leg_x = size // 2 + size // 6 - leg_width // 2
            # Left leg
            draw.rectangle([left_leg_x, leg_y, 
                          left_leg_x + leg_width, leg_y + leg_length + left_step], 
                         fill=color, outline="#000000", width=1)
            # Right leg
            draw.rectangle([right_leg_x, leg_y, 
                          right_leg_x + leg_width, leg_y + leg_length + right_step], 
                         fill=color, outline="#000000", width=1)
        elif leg_type == "thin":
            leg_width = max(1, int(leg_width * 0.6))
            left_leg_x = size // 2 - size // 6 - leg_width // 2
            right_leg_x = size // 2 + size // 6 - leg_width // 2
            # Left leg
            draw.rectangle([left_leg_x, leg_y, 
                          left_leg_x + leg_width, leg_y + leg_length + left_step], 
                         fill=color, outline="#000000", width=1)
            # Right leg
            draw.rectangle([right_leg_x, leg_y, 
                          right_leg_x + leg_width, leg_y + leg_length + right_step], 
                         fill=color, outline="#000000", width=1)
        elif leg_type == "long":
            leg_length = int(leg_length * 1.3)
            # Left leg
            draw.rectangle([left_leg_x, leg_y, 
                          left_leg_x + leg_width, leg_y + leg_length + left_step], 
                         fill=color, outline="#000000", width=1)
            # Right leg
            draw.rectangle([right_leg_x, leg_y, 
                          right_leg_x + leg_width, leg_y + leg_length + right_step], 
                         fill=color, outline="#000000", width=1)


def generate():
    """Legacy function for compatibility."""
    generator = CharacterGenerator()
    return generator

