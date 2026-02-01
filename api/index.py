from http.server import BaseHTTPRequestHandler
from openai import OpenAI
import json
import os

# Initialize OpenAI with the secure environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Setup Headers (Handle CORS so your frontend can talk to this backend)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        # 2. Read the memory sent from Frontend
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        memory = data.get('memory', '')

        try:
            # 3. Call OpenAI (The Magic)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a romantic poet. Write a short, passionate love letter (max 3 sentences) based on the user's memory."},
                    {"role": "user", "content": f"Memory: {memory}"}
                ]
            )
            result = response.choices[0].message.content
            
            # 4. Send result back to Frontend
            self.wfile.write(json.dumps({'message': result}).encode('utf-8'))
            
        except Exception as e:
            self.wfile.write(json.dumps({'message': f"Error: {str(e)}"}).encode('utf-8'))

    # Handle Preflight requests (CORS handshake)
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

        self.end_headers()
