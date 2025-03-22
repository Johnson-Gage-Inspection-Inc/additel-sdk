# program.py - This file contains the class for the Program commands.

# Section 1.5 - Program Commands


class Program:
    def __init__(self, parent):
        self.parent = parent

    # 1.5.1
    def run(self, progname: str, parameters = None) -> None:
        """Run the appointed program

        Command:
            PROGram:RUN <progname>[,<parameters>]

        Args:
            progname (str): The name of the program to run.
            parameters (_type_, optional): The parameters of the program. Defaults to None.
        """
        self.parent.send_command(f'PROGram:RUN "{progname}" "{parameters}"')

    # 1.5.2
    def exit(self, progname: str = "") -> None:
        """Stop the program. without parameters
            means Stop program specified by
            PROGram:RUN

        Command:
            PROGram:EXIT [<progname>]
        """
        exit_cmd = f'PROGram:EXIT "{progname}"' if progname else "PROGram:EXIT"
        self.parent.send_command(exit_cmd)

    # 1.5.3
    def state(self, progname: str = "") -> str:
        """Query the state of the program

        Status of interrogator , without
        parameters means to question the
        program specified by PROGram:RUN

        Command:
            PROGram:STATe [<progname>]

        Args:
            progname (str): The name of the program to query.

        Returns:
            str: The state of the program.
        """
        state_query = f'PROGram:STATe "{progname}"' if progname else "PROGram:STATe"
        if response := self.parent.cmd(state_query):
            return response.strip()
        raise ValueError("No program state information returned.")
