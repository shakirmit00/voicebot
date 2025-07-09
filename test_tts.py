from elevenlabs import generate, play, set_api_key

set_api_key("sk_7df99d5b0c6e4e151d08344a36cb1ecf4e0136e236f92c44")

audio = generate(
    text="Hello, this is a test from ElevenLabs.",
    voice="P7vsEyTOpZ6YUTulin8m",
    model="eleven_multilingual_v1"
)
play(audio)