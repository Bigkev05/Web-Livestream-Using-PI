from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Start stream on twitch or youtube
@app.route('/start_stream', methods=['POST'])
def start_stream():
    platform = request.form['platform']
    video_ip = request.form['video_ip']

    twitch_command = f'ffmpeg -i {video_ip} -f alsa -channels 1 -sample_rate 48000 -i hw:1,0 -vcodec libx264 -preset veryfast -tune zerolatency -r 60 -g 60 -maxrate 3000k -bufsize 3000k -vf "scale=1280:720" -acodec aac -b:a 160k -ar 48000 -f flv rtmp://live.twitch.tv/app/:stream Key"'
    
    youtube_command = f'ffmpeg -i {video_ip} -f alsa -channels 1 -sample_rate 48000 -i hw:1,0 -vcodec libx264 -preset veryfast -tune zerolatency -r 60 -g 60 -maxrate 3000k -bufsize 3000k -vf "scale=1280:720" -acodec aac -b:a 160k -ar 48000 -f flv rtmp://a.rtmp.youtube.com/live2/"stream key"

    command = twitch_command if platform == 'twitch' else youtube_command
    print(f"Executing command: {command}")

    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode == 0:
            return f"<h1>Streaming to {platform.capitalize()} started successfully!</h1><pre>{output.decode('utf-8')}</pre>"
        else:
            error_message = error.decode('utf-8') if error else "Unknown error"
            return f"<h1>Failed to start stream on {platform.capitalize()}</h1><pre>{error_message}</pre>"
    except Exception as e:
        return f"<h1>Error occurred: {str(e)}</h1>"

# Restart Flask Stream
@app.route('/restart_flask', methods=['POST'])
def restart_flask():
    try:
        subprocess.run(['sudo', 'systemctl', 'restart', 'flask_app.service'], check=True)
        run_python_script()  # Call the function to run the Python script
        return "<h1>Flask app restarted successfully and script executed!</h1>"
    except subprocess.CalledProcessError as e:
        return f"<h1>Failed to restart Flask app!</h1><pre>{str(e)}</pre>"

# Function to automatically run kevinpop.py
def run_python_script():
    file_path = '/home/kevin/kevinpop.py'

    if os.path.exists(file_path):
        print(f"File {file_path} exists, attempting to run it...")

        try:
            # Execute the Python script using Python 3
            process = subprocess.Popen(['python3', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()

            if process.returncode == 0:
                print(f"Script {file_path} executed successfully!")
                print(f"Output: {output.decode('utf-8')}")
            else:
                print(f"Error executing script: {error.decode('utf-8')}")
        except Exception as e:
            print(f"Error running script: {str(e)}")
    else:
        print(f"File {file_path} does not exist!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

