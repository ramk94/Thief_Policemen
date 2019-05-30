#!/usr/bin/env python

"""
Last updated by Emma Smith
06 December 2018
"""

i# Impports
import rospy
from std_msgs.msg import Int32
from std_msgs.msg import String
import dialogflow_v2 as dialogflow
import os

# Define globals
global current_directory # Directory where node is stored
global done # flag to indicate that the processing is done
global finish_dialog # publisher used to send the done flag
global response_dialog # publisher to send the text response from dialogflow
global intent_dialog # publisher to send the intent from dialogflow


# set globals
# change this to your current machine
# this needs to be the directory where the json file is located
current_directory = '/home/pi/catkin_ws/src/lynxmotion_package/scripts'
print (current_directory)
done = 0


def detect_intent_audio(project_id, session_id, audio_file_path, language_code):
    """
    Returns response to audio file
    """
    global done
	
    # Sets session for dialogflow. This is used to create a continuing conversation and essentially save your place
    # Not used currently
    session_client = dialogflow.SessionsClient()

    # Paramaters for the file
    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = 44100

    # Associates session with the project on dialogflow
    session = session_client.session_path(project_id, session_id)

    # Opens audio file and reads it
    with open(audio_file_path, 'rb') as audio_file:
        input_audio = audio_file.read()

    # Decodes audo file based off the encodinng before
    audio_config = dialogflow.types.InputAudioConfig(
        audio_encoding=audio_encoding, language_code=language_code,
        sample_rate_hertz=sample_rate_hertz)
    # Lets dialogflow know that we're sending a decoded audio file
    query_input = dialogflow.types.QueryInput(audio_config=audio_config)

    # Response from dialogflow
    response = session_client.detect_intent(
        session=session, query_input=query_input,
        input_audio=input_audio)
    print ('-' * 20)
    print ('Query text: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print ('Response: {}\n'.format(
        response.query_result.fulfillment_text))
    done += 1

    # Publish response and confirmation of completion
    finish_dialog.publish(done)
    response_dialog.publish(response.query_result.fulfillment_text)
    intent_dialog.publish(response.query_result.intent.display_name)
    
    
def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    # Sets the client
    session_client = dialogflow.SessionsClient()

    # Session
    session = session_client.session_path(project_id, session_id)

    # Processes all text strings from the input array
    for text in texts:
        # Configures text input settings
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        # Sends text to dialogflow for procesing
        query_input = dialogflow.types.QueryInput(text=text_input)

        # Response from dialogflow
        response = session_client.detect_intent(
            session=session, query_input=query_input)

        return response.query_result.fulfillment_text


def dialog_command_callback (data):
    global current_directory

    user_input = data.data
    result = detect_intent_audio("feelings-a1c4f", "1-1", user_input, 'en-US')


def node_setup():
    # Declare globals
    global current_directory
    global finish_dialog
    global response_dialog
    global intent_dialog
    
    environment = os.path.join(current_directory, 'Feelings-0b93d9f44df2.json')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = environment

    # Initialize node, publishers, and subscriber
    rospy.init_node('dialog', anonymous=True)
    rospy.Subscriber('dialog_command', String, dialog_command_callback)
    finish_dialog = rospy.Publisher('dialog_finished', Int32, queue_size=1)
    response_dialog = rospy.Publisher('dialog_response', String, queue_size=1)
    intent_dialog = rospy.Publisher('dialog_intent', String, queue_size=1)

    print ("Dialog node has been initialized")
    rospy.spin()


if __name__ == "__main__":
    try:
        print("Starting dialog node setup")
        node_setup()
    except rospy.ROSInterruptException as e:
        print(e)
    
