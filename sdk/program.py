# program.py - This file contains the class for the Program commands.

# Section 1.5 - Program Commands

class Program:
    def __init__(self, parent, parameter):
        self.parent = parent

    # 1.5.1
    def run(self, progname: str, parameters: str):
        """Run the appointed program
        
        Command:
            PROGram:RUN <progname>[,<parameters>]
        
        Parameters:
            progname (str): The name of the program to run.
            parameters (str): The parameters of the program.
        """
        self.parent.send_command(f'PROGram:RUN "{progname}" "{parameters}"')

    # 1.5.2
    def exit(self, progname: str = ""):
        """Stop the program. without parameters
            means Stop program specified by
            PROGram:RUN
        
        Command:
            PROGram:EXIT [<progname>]
        """
        self.parent.send_command(f'PROGram:EXIT "{progname}"'.strip())
    
    # 1.5.3
    def state(self, progname: str = "") -> str:
        """Query the state of the program

        Status of interrogator , without
        parameters means to question the
        program specified by PROGram:RUN

        Command:
            PROGram:STATe [<progname>]
        
        Parameters:
            progname (str): The name of the program to query.
        
        Returns:
            str: The state of the program.
        """
        if response := self.parent.send_command(f'PROGram:STATe "{progname}"'):
            return response.strip()
        raise ValueError("No program state information returned.")
    