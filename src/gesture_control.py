import tflearn


class GestureControl:
    def __init__(self):
        """
        load the model and keep the model during the game
        """
        self.model = tflearn.DNN(...)
        self.model.load("...")

    def get_gesture(self):
        """
        Every time open a window and close it after recognition.
        
        workflow:
        1. open a named window with opencv
        2. recognize the current gesture
        3. close the window
        4. return the predicted categories
        :return:
        """
        self.model.predict(...)
        result = 'Swing'
        return result
