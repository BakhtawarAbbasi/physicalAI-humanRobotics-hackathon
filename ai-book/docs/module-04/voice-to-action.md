---
title: Voice-to-Action
sidebar_position: 1
---

# Voice-to-Action

## Introduction

This chapter covers voice recognition and processing techniques for robotics applications, focusing on speech-to-text conversion in ROS 2 environments. Voice-to-action systems enable natural human-robot interaction by allowing users to control robots through spoken commands.

## Prerequisites

Before starting with voice-to-action processing, ensure you have:
- Working ROS 2 environment (Humble Hawksbill or later)
- Microphone for voice input
- Speech recognition libraries installed (e.g., speech_recognition, pocketsphinx)
- Understanding of basic ROS 2 concepts (topics, services, nodes)
- Basic knowledge of audio processing concepts

## Speech Recognition Concepts

Speech recognition is the process of converting spoken language into text. In robotics applications, this enables natural human-robot interaction through voice commands. The system typically involves several key components:

### Key Components

1. **Audio Input**: Capturing sound from the environment using microphones
2. **Feature Extraction**: Processing audio signals to identify phonetic features
3. **Acoustic Model**: Mapping acoustic features to phonemes
4. **Language Model**: Determining the most likely word sequence
5. **Decoder**: Combining models to produce recognized text
6. **Command Parser**: Interpreting recognized text for robotic action

### Types of Speech Recognition

- **Offline Recognition**: Uses locally stored models, privacy-preserving but limited vocabulary
- **Online Recognition**: Uses cloud-based services, better accuracy but requires internet
- **Hybrid Approach**: Combines both approaches for optimal performance

## Voice Command Processing Pipeline

The voice command processing pipeline handles the complete flow from audio input to command execution:

### Pipeline Stages

1. **Audio Capture**: Recording audio from microphone or other input source
2. **Preprocessing**: Filtering noise and enhancing signal quality
3. **Feature Extraction**: Converting audio to feature vectors suitable for recognition
4. **Speech Recognition**: Converting audio to text using acoustic and language models
5. **Natural Language Processing**: Extracting intent and entities from recognized text
6. **Command Mapping**: Converting parsed commands to ROS 2 actions
7. **Action Execution**: Executing commands in the robotic system
8. **Feedback Generation**: Providing confirmation or error feedback to the user

### Implementation Considerations

- **Real-time Processing**: Low-latency recognition for responsive interaction
- **Noise Robustness**: Filtering background noise for accurate recognition
- **Speaker Adaptation**: Adjusting to individual speaker characteristics
- **Keyword Spotting**: Detecting wake words or command triggers

## Speech-to-Text Conversion Examples

### Python Implementation with SpeechRecognition Library

```python
import speech_recognition as sr
import rospy
from std_msgs.msg import String

class VoiceToActionNode:
    def __init__(self):
        rospy.init_node('voice_to_action')
        self.pub = rospy.Publisher('/voice_command', String, queue_size=10)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

    def listen_for_commands(self):
        with self.microphone as source:
            print("Listening for commands...")
            audio = self.recognizer.listen(source)

        try:
            # Recognize speech using Google's service
            command_text = self.recognizer.recognize_google(audio)
            print(f"Recognized: {command_text}")

            # Publish command to ROS topic
            self.pub.publish(command_text)
            return command_text
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error with recognition service: {e}")

        return None

    def run(self):
        rate = rospy.Rate(1)  # Check for commands once per second
        while not rospy.is_shutdown():
            self.listen_for_commands()
            rate.sleep()

if __name__ == '__main__':
    node = VoiceToActionNode()
    node.run()
```

### Advanced Configuration for Robotics

```python
# Configuration for robotics voice control
VOICE_CONFIG = {
    'sample_rate': 16000,  # Hz
    'chunk_size': 1024,    # Samples per chunk
    'energy_threshold': 3000,  # Silence threshold
    'phrase_time_limit': 5,    # Max seconds for a phrase
    'dynamic_energy_threshold': True,
    'pause_threshold': 0.8,    # Seconds of silence before phrase ends
    'phrase_threshold': 0.3,   # Minimum seconds of speaking to start phrase
    'non_speaking_duration': 0.5  # Silence duration to consider phrase complete
}
```

## Practical Exercises

### Exercise 1: Basic Voice Command Recognition

1. Set up a microphone with your ROS 2 system
2. Install speech recognition libraries: `pip install speechrecognition pyaudio`
3. Create a simple node that listens for basic commands like "move forward", "turn left", "stop"
4. Test recognition accuracy in quiet and noisy environments
5. Implement a basic command parser to convert recognized text to robot actions

### Exercise 2: Keyword Spotting Implementation

1. Implement a keyword spotting system that wakes up only when hearing a specific word (e.g., "robot")
2. Use the `recognize_google()` method with a specific phrase bias
3. Add hysteresis to prevent rapid triggering
4. Test the system with different speakers and accents

### Exercise 3: Robust Command Processing

1. Create a robust command processing pipeline that handles common recognition errors
2. Implement fuzzy matching for similar-sounding commands
3. Add confirmation prompts for critical actions
4. Test with various background noise conditions

## Troubleshooting Voice Recognition Issues

### Common Problems and Solutions

1. **Poor Recognition Accuracy**:
   - Solution: Adjust energy threshold, use noise cancellation, improve microphone placement
   - Check: `recognizer.energy_threshold` value, ambient noise levels

2. **Microphone Not Detected**:
   - Solution: Check audio device permissions, install proper drivers
   - Command: `arecord -l` to list audio devices

3. **High CPU Usage**:
   - Solution: Reduce sampling rate, implement periodic listening instead of constant monitoring
   - Alternative: Use lighter acoustic models

4. **Background Noise Interference**:
   - Solution: Use noise suppression filters, directional microphones
   - Technique: `recognizer.adjust_for_ambient_noise()` with calibration

5. **Latency Issues**:
   - Solution: Optimize audio buffer sizes, use streaming recognition
   - Consider: Offline recognition models for faster response

### Performance Optimization Tips

- Use appropriate sample rates (16kHz is often sufficient)
- Implement wake word detection to reduce processing
- Cache acoustic models in memory
- Use threading for non-blocking audio processing
- Implement timeout mechanisms to prevent hanging

## Summary

This chapter provided an introduction to voice-to-action processing for robotics applications. You learned about:
- Speech recognition concepts and key components
- Voice command processing pipeline implementation
- Speech-to-text conversion techniques in ROS 2 environments
- Practical exercises to reinforce learning
- Troubleshooting techniques for common issues

The next chapter will cover cognitive planning with Large Language Models (LLMs) to translate natural language goals into ROS 2 action sequences.

## Next Steps

Continue to the next chapter to learn about [Cognitive Planning with LLMs](./cognitive-planning).