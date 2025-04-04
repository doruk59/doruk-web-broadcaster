from flask import Flask, render_template_string
import psutil
import subprocess
import json

app = Flask(__name__)

# HTML template for the streaming page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Doruk Web Broadcasting</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            font-family: Arial, sans-serif;
            background-color: #1a1a1a;
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .stream-container {
            position: relative;
            padding-bottom: 56.25%;
            height: 0;
            overflow: hidden;
            margin-bottom: 20px;
        }
        .stream-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }
        .status {
            background-color: #2a2a2a;
            padding: 20px;
            border-radius: 5px;
            margin-top: 20px;
        }
        .status-item {
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Doruk Web Broadcasting</h1>
        <div class="stream-container">
            <iframe src="https://www.youtube.com/embed/aPj0JpCh9TQ?autoplay=1" allowfullscreen></iframe>
        </div>
        <div class="status">
            <h2>Sistem Durumu</h2>
            <div class="status-item">
                <strong>CPU Kullanımı:</strong> {{ cpu }}%
            </div>
            <div class="status-item">
                <strong>RAM Kullanımı:</strong> {{ ram }}%
            </div>
            <div class="status-item">
                <strong>Sıcaklık:</strong> {{ temp }}°C
            </div>
            <div class="status-item">
                <strong>Sunucu Adresi:</strong> http://192.168.1.49:5000
            </div>
            <div class="status-item">
                <strong>Aktif Playlist:</strong> {{ playlist_name if playlist_name else 'Varsayılan' }}
            </div>
        </div>
    </div>
</body>
</html>
"""

def get_system_stats():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    
    # Get CPU temperature (specific to Raspberry Pi)
    try:
        temp = subprocess.check_output(['vcgencmd', 'measure_temp']).decode()
        temp = float(temp.replace('temp=', '').replace("'C", ''))
    except:
        temp = 0.0
    
    return cpu, ram, temp

def get_current_playlist():
    try:
        with open('playlists/current.json') as f:
            data = json.load(f)
            return data.get('name', 'Varsayılan')
    except:
        return 'Varsayılan'

@app.route('/')
def index():
    cpu, ram, temp = get_system_stats()
    playlist_name = get_current_playlist()
    return render_template_string(
        HTML_TEMPLATE,
        cpu=cpu,
        ram=ram,
        temp=temp,
        playlist_name=playlist_name
    )

@app.route('/status')
def status():
    cpu, ram, temp = get_system_stats()
    playlist_name = get_current_playlist()
    return {
        'cpu': cpu,
        'ram': ram,
        'temperature': temp,
        'playlist': playlist_name
    }

@app.route('/playlist')
def playlist_status():
    try:
        with open('playlists/current.json') as f:
            current_playlist = json.load(f)
        return {
            'name': current_playlist['name'],
            'current_video': current_playlist.get('current_video', ''),
            'next_video': current_playlist.get('next_video', ''),
            'play_mode': current_playlist['play_mode']
        }
    except:
        return {'error': 'No active playlist'}

if __name__ == '__main__':
    app.run(host='192.168.1.49', port=5000)
