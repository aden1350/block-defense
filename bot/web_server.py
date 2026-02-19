#!/usr/bin/env python3
"""
Simple Web Server - Test Version
Serves AI Assistant via web interface
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os

# Import our AI assistant
from ai_assistant import answer_question

PORT = 8080

class AIHandler(SimpleHTTPRequestHandler):
    """Custom handler with AI assistant"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.path = '/index.html'
        return SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        """Handle POST requests - AI问答"""
        if self.path == '/api/ask':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                query = data.get('question', '')
                
                if query:
                    answer = answer_question(query)
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'answer': answer}).encode())
                else:
                    self.send_error(400, 'Missing question')
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        """Custom log"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def run_server(port=PORT):
    """Run the web server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, AIHandler)
    print(f"AI Assistant Web Server starting on port {port}...")
    print(f"Open http://localhost:{port} in your browser")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
