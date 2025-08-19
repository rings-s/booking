"""
Management command to test media file handling and QR code generation
"""
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from base.models import Business
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw
import os


class Command(BaseCommand):
    help = 'Test media file handling and QR code generation'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing media file handling and QR code generation...'))
        
        # Test QR code generation for existing businesses
        self.test_qr_code_generation()
        
        # Test sample image creation
        self.create_sample_images()
        
        self.stdout.write(self.style.SUCCESS('Media and QR code tests completed successfully!'))
    
    def test_qr_code_generation(self):
        """Test QR code generation for businesses"""
        self.stdout.write('Testing QR code generation...')
        
        businesses = Business.objects.all()
        if not businesses.exists():
            self.stdout.write(self.style.WARNING('No businesses found. Load fixtures first.'))
            return
            
        for business in businesses:
            try:
                # Clear existing QR code to force regeneration
                if business.qr_code:
                    business.qr_code.delete()
                business.qr_code = None
                
                # Generate new QR code
                business.generate_qr_code()
                business.save()
                
                if business.qr_code and business.qr_code.name:
                    self.stdout.write(f'✓ QR code generated for {business.name}: {business.qr_code.name}')
                else:
                    self.stdout.write(self.style.ERROR(f'✗ Failed to generate QR code for {business.name}'))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Error generating QR code for {business.name}: {str(e)}'))
    
    def create_sample_images(self):
        """Create sample logo and cover images"""
        self.stdout.write('Creating sample images...')
        
        businesses = Business.objects.all()
        
        for business in businesses:
            try:
                # Create sample logo
                logo_img = self.create_sample_logo(business.name)
                logo_content = ContentFile(logo_img.getvalue())
                logo_filename = f"logo_{business.slug}.png"
                
                if business.logo:
                    business.logo.delete()
                business.logo.save(logo_filename, logo_content, save=False)
                
                # Create sample cover image
                cover_img = self.create_sample_cover(business.name)
                cover_content = ContentFile(cover_img.getvalue())
                cover_filename = f"cover_{business.slug}.png"
                
                if business.cover_image:
                    business.cover_image.delete()
                business.cover_image.save(cover_filename, cover_content, save=False)
                
                business.save()
                
                self.stdout.write(f'✓ Sample images created for {business.name}')
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Error creating images for {business.name}: {str(e)}'))
    
    def create_sample_logo(self, business_name):
        """Create a simple sample logo"""
        # Create a 200x200 image with a colored background
        img = Image.new('RGB', (200, 200), color='#3B82F6')
        draw = ImageDraw.Draw(img)
        
        # Add business initials
        initials = ''.join([word[0].upper() for word in business_name.split()[:2]])
        
        # Draw initials in white
        bbox = draw.textbbox((0, 0), initials)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (200 - text_width) // 2
        y = (200 - text_height) // 2
        
        draw.text((x, y), initials, fill='white')
        
        # Save to BytesIO
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer
    
    def create_sample_cover(self, business_name):
        """Create a simple sample cover image"""
        # Create a 800x400 image with a gradient-like effect
        img = Image.new('RGB', (800, 400), color='#6B7280')
        draw = ImageDraw.Draw(img)
        
        # Add business name
        bbox = draw.textbbox((0, 0), business_name)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (800 - text_width) // 2
        y = (400 - text_height) // 2
        
        draw.text((x, y), business_name, fill='white')
        
        # Save to BytesIO
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer