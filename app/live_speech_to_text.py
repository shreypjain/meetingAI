import time
import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone):
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # format the instructions string
    instructions = (
        "Hello!"
    )

    # show instructions and wait 3 seconds before starting
    print(instructions)
    time.sleep(3)

    question = input('Do you want to speak? (y/n): ')    
    while question.lower() != 'n':
        i = 0
        print('Instance {}. Speak!'.format(i+1))
        
        guess = recognize_speech_from_mic(recognizer, microphone)
            
        if not guess["success"]:
            print("I didn't catch that. What did you say?\n")

        # if there was an error, stop the game
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break
    
        # show the user the transcription
        print("You said: {}".format(guess["transcription"]))
        
        question = input('Do you want to speak? (y/n): ')
        i += 1