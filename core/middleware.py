from django.conf import settings
import mimetypes
import os

class CacheControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Ensure proper MIME types are registered
        mimetypes.add_type('font/woff2', '.woff2')
        mimetypes.add_type('font/woff', '.woff')
        mimetypes.add_type('font/ttf', '.ttf')
        mimetypes.add_type('image/svg+xml', '.svg')
        mimetypes.add_type('image/x-icon', '.ico')

    def __call__(self, request):
        response = self.get_response(request)
        
        # Handle static and media files
        if request.path.startswith(('/static/', '/media/')):
            file_path = request.path.split('?')[0]  # Remove query parameters
            content_type = self._get_content_type(file_path)
            
            if content_type:
                response['Content-Type'] = content_type
            
            # Set cache control headers for static files
            response['Cache-Control'] = 'public, max-age=31536000, immutable'
            
            # Remove Expires header if present
            if 'Expires' in response:
                del response['Expires']
        
        # Handle HTML responses
        elif not response.get('Content-Type'):
            if response.get('content-type', '').startswith('text/html'):
                response['Content-Type'] = 'text/html; charset=utf-8'
        
        return response

    def _get_content_type(self, file_path):
        """Determine the content type based on file extension."""
        ext = os.path.splitext(file_path)[1].lower()
        
        # Special handling for common file types
        content_types = {
            '.css': 'text/css; charset=utf-8',
            '.js': 'text/javascript; charset=utf-8',
            '.woff2': 'font/woff2',
            '.woff': 'font/woff',
            '.ttf': 'font/ttf',
            '.svg': 'image/svg+xml',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.ico': 'image/x-icon',
            '.webp': 'image/webp',
        }
        
        if ext in content_types:
            return content_types[ext]
        
        # Fallback to system MIME types
        mime_type, encoding = mimetypes.guess_type(file_path)
        if mime_type:
            if mime_type.startswith('text/'):
                return f'{mime_type}; charset=utf-8'
            return mime_type
        
        return None