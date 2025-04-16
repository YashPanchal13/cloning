from flask import Flask, request, render_template, send_file, url_for
from TTS.api import TTS
import os
import uuid

app = Flask(__name__)

# Define folder paths for sample voices and output folder
app.config['UPLOAD_FOLDER'] = "uploads"
app.config['OUTPUT_FOLDER'] = "outputs"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Load the TTS model once when the app starts
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

@app.route("/")
def index():
    # List available speakers dynamically from the speaker_samples folder
    speakers = [f.split('.')[0] for f in os.listdir('speaker_samples') if f.endswith('.wav')]
    return render_template("index.html", speakers=speakers)

@app.route("/speak_form", methods=["POST"])
def speak_form():
    text = request.form.get("text", "")
    language = request.form.get("language", "en")
    selected_speaker = request.form.get("speaker_choice")

    if not selected_speaker or not text.strip():
        return "Please provide both text and choose a speaker."

    # Get the correct speaker sample path
    speaker_path = os.path.join("speaker_samples", f"{selected_speaker}.wav")
    if not os.path.exists(speaker_path):
        return f"Speaker sample not found: {selected_speaker}"

    # Generate cloned speech
    output_filename = f"{uuid.uuid4().hex}_cloned.wav"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    try:
        tts.tts_to_file(
            text=text,
            speaker_wav=speaker_path,
            language=language,
            file_path=output_path
        )
        return render_template("index.html",
                               cloned_audio=url_for('serve_file', folder='outputs', filename=output_filename),
                               original_audio=url_for('serve_file', folder='speaker_samples', filename=f"{selected_speaker}.wav"))
    except Exception as e:
        return f"Error during TTS generation: {e}"

@app.route("/<folder>/<filename>")
def serve_file(folder, filename):
    file_path = os.path.join(app.root_path, folder, filename)
    return send_file(file_path)

if __name__ == "__main__":
    app.run(debug=True)



# from flask import Flask, request, render_template, send_file, url_for, redirect
# from TTS.api import TTS
# import os
# import uuid

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = "uploads"
# app.config['OUTPUT_FOLDER'] = "outputs"
# app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB max upload size

# # Ensure folders exist
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
# os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# # Load TTS model once
# tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/speak_form", methods=["POST"])
# def speak_form():
#     text = request.form.get("text", "")
#     language = request.form.get("language", "en")
#     speaker_file = request.files.get("speaker_wav")

#     if not speaker_file or not text.strip():
#         return "Please provide both a speaker voice and some text."

#     # Save uploaded speaker voice
#     speaker_filename = f"{uuid.uuid4().hex}.wav"
#     speaker_path = os.path.join(app.config['UPLOAD_FOLDER'], speaker_filename)
#     speaker_file.save(speaker_path)

#     # Generate cloned speech
#     output_filename = f"{uuid.uuid4().hex}_cloned.wav"
#     output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

#     try:
#         tts.tts_to_file(
#             text=text,
#             speaker_wav=speaker_path,
#             language=language,
#             file_path=output_path
#         )
#         return render_template("index.html",
#                                cloned_audio=url_for('serve_file', folder='outputs', filename=output_filename),
#                                original_audio=url_for('serve_file', folder='uploads', filename=speaker_filename))
#     except Exception as e:
#         return f"Error during TTS generation: {e}"

# @app.route("/<folder>/<filename>")
# def serve_file(folder, filename):
#     file_path = os.path.join(app.root_path, folder, filename)
#     return send_file(file_path)
    
# if __name__ == "__main__":
#     app.run(debug=True)






# from flask import Flask, request, render_template, send_file, redirect, url_for
# from TTS.api import TTS
# import os
# import uuid

# app = Flask(__name__)
# tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

# SPEAKER_WAV = "/Users/par/Desktop/Yash/Bark/bark_voices/salman/speaker.wav"
# OUTPUT_DIR = "outputs"
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/speak_form", methods=["POST"])
# def speak_form():
#     text = request.form["text"]
#     file_name = f"{uuid.uuid4().hex}.wav"
#     output_path = os.path.join(OUTPUT_DIR, file_name)

#     try:
#         tts.tts_to_file(
#             text=text,
#             speaker_wav=SPEAKER_WAV,
#             language="en",
#             file_path=output_path
#         )
#         return render_template("index.html", audio_url=url_for('download_file', filename=file_name))
#     except Exception as e:
#         return f"Error: {e}"

# @app.route("/download/<filename>")
# def download_file(filename):
#     file_path = os.path.join(OUTPUT_DIR, filename)
#     return send_file(file_path, as_attachment=True)

# if __name__ == "__main__":
#     app.run(debug=True)
