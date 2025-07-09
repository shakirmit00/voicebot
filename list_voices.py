from elevenlabs.client import ElevenLabs

client = ElevenLabs(api_key="sk_7df99d5b0c6e4e151d08344a36cb1ecf4e0136e236f92c44")  # 🔁 Replace with your key

# Get all voices
voices = client.voices.get_all()

# Loop through actual list of voice objects
for voice in voices.voices:
    print(f"{voice.name} - {voice.voice_id}")
