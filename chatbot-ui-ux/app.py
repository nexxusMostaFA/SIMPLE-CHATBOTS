from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# DeepSeek API Configuration
DEEPSEEK_API_KEY = "sk-d0d912aa295c4cc687bf6f608204c3c4"  
DEEPSEEK_API_URL = "https://platform.deepseek.com/api_keys"   

@app.route('/')
def home():
    """Serve the index.html page"""
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def chat():
    """Handle chat API requests"""
    try:
        # Get message from request
        data = request.json
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
        }

        payload = {
            "model": "deepseek-chat",  # استبدل بنموذج DeepSeek المناسب
            "messages": [{"role": "user", "content": user_message}],
            "temperature": 0.7,
            "max_tokens": 150
        }

        
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()  
 
        response_data = response.json()
        ai_response = response_data['choices'][0]['message']['content']

        return jsonify({'response': ai_response})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f"API Request Error: {str(e)}"}), 503
    except Exception as e:
        return jsonify({'error': f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)





    