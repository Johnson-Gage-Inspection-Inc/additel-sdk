# pattern.py - This file contains the Pattern class which contains the commands for the Pattern module.

# Section 1.7 - Function module commands


class Pattern:
    def __init__(self, parent):
        self.parent = parent

        # 1.7.1
        def patterns(self, function, otherParams):
            """Switch main interface function

            Command:
                PATTern:MAIN:PATTerns Dual|SCMM|SConn[,<”otherParams”>]

            Args:
                function (str): The function to switch to.
                otherParams (str): Other parameters.

            Returns:
                None
            """
            self.parent.cmd(f"PATTern:MAIN:PATTerns {function},{otherParams}")

        # 1.7.2
        def setMatch(self, paramIndex, matchStr: str = ""):
            """Set the match ing conditions of the intelligent wiring base

            Command:
                PATTern:MAIN:MATCH <paramIndex>[,<” matchStr” >]

            Args:
                paramIndex (int): The parameter index corresponding to:
                    1 = ChannelInfo1
                    2 = ChannelInfo2
                    3 = ChannelInfo3
                    other = close match;
                matchStr (str):  A matching string with quotes.

            Returns:
                None
            """
            if matchStr:
                self.parent.cmd(f"PATTern:MAIN:MATCH {paramIndex},{matchStr}")
            else:
                self.parent.cmd(f"PATTern:MAIN:MATCH {paramIndex}")
