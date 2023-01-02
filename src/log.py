class Log:
        activate = True

        def __init__(self, message, value = '') :
                if self.activate: 
                        print(message, value)
