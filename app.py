from flask import Flask, request, send_file
import edge_tts
import asyncio
import tempfile

app = Flask(__name__)

async def tts_to_wav(text, path):
    tts = edge_tts.Communicate(text, voice="en-US-AriaNeural")
    await tts.save(path)

def generate_wav(text):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    asyncio.run(tts_to_wav(text, tmp.name))
    return tmp.name

@app.route("/speak")
def speak():
    text = request.args.get("text", "")
    if not text:
        return "No text", 400
    wav = generate_wav(text)
    return send_file(wav, mimetype="audio/wav")
