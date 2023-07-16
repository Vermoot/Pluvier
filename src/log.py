class Log:
        activate = False

        def __init__(self, message, value = '') :
                if self.activate: 
                        print(message, value)
