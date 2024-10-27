# 🎥 **Livestream Application Project** 🎥

Welcome to the **Livestream Application Project**! This project is a custom-built livestreaming setup that lets you connect with a global audience in real-time, share personal experiences, and interact with viewers through text-to-speech functionality, all powered by a Raspberry Pi. Let's dive in!

---

## 🏆 **Project Goals**

The main objective is to create a fully functional livestreaming setup that:
- Streams live video and audio using Raspberry Pi and basic hardware.
- Converts chat messages into spoken words with Google Text-to-Speech.
- Provides an intuitive web interface to manage livestream settings.

---

## 🧰 **Tech Stack and Tools**

### 🗣️ gTTS (Google Text-to-Speech)
- **Purpose**: Converts Twitch chat text into spoken audio.
- **Implementation**:
  ```python
  tts = gTTS(text="Hello, World!", lang='en')
  tts.save("output.mp3")
