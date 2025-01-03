# display.py - This file contains the display commands for the SDK.

# Section 1.6 - Display commands

class Display:
    def __init__(self, parent):
        self.parent = parent

    # 1.6.1
    def setBrightness(self, type, level):
        """Set the brightness of the display

        Command:
            DISPaly:BRIGHTness <type>,<level>

        Args:
            type (float): The type of display (Percentage)
            level (int): The value of brightness

        Returns:
            None
        """
        self.parent.cmd(f'DISPaly:BRIGHTness {type},{level}')

    # 1.6.2
    def getBrightness(self, type) -> int:
        """Query the brightness of the display

        Command:
            DISPaly:BRIGHTness? <type>

        Args:
            type (float): The type of display (Percentage)

        Returns:
            int: The value of brightness
        """
        if response := self.parent.cmd(f'DISPaly:BRIGHTness? {type}'):
            return int(response.strip())
        raise ValueError("No brightness information returned.")


    # 1.6.3
    def getLanguage(self) -> str:
        """Query the language of the display

        Command:
            DISPaly:LANGuage?

        Returns:
            str: The language of the display
        """
        if response := self.parent.cmd("DISPaly:LANGuage?"):
            return response.strip()
        raise ValueError("No language information returned.")

    # 1.6.5
    def Messagebox(self, message):
        """Display dialog box

        Command:
            DISPlay:MESSagebox < "Message ">

        Args:
            message (_type_): _description_

        Returns:
            None
        """
        self.parent.cmd(f'DISPlay:MESSagebox "{message}"')

    # 1.6.6
    def getHome(self) -> str:
        """Query the home page of the display

        Command:
            DISPaly:HOME?

        Returns:
            str: The home page of the display
        """
        if response := self.parent.cmd("DISPaly:HOME?"):
            return response.strip()
        raise ValueError("No home page information returned.")

    # 1.6.7
    def getTheme(self) -> str:
        """Query the theme of the display

        Command:
            DISPaly:THEMe?

        Returns:
            str: The theme of the display
        """
        if response := self.parent.cmd("DISPaly:THEMe?"):
            return response.strip()
        raise ValueError("No theme information returned.")

    # 1.6.9
    def themeAllNames(self) -> str:
        """Query all the names of the theme

        Command:
            DISPaly:THEMe:ALLNames?

        Returns:
            str: All the names of the theme
        """
        if response := self.parent.cmd("DISPaly:THEMe:ALLNames?"):
            return response.strip()
        raise ValueError("No theme information returned.")

    # 1.6.10
    def setTheme(self, theme):
        """Set system theme( work after restarting)

        Command:
            DISPaly:THEMe <theme>

        Args:
            theme (str): A supported theme name.

        Returns:
            None
        """
        self.parent.cmd(f'DISPaly:THEMe {theme}')

class Diagnostic:
    def __init__(self, parent):
        self.parent = parent

    # 1.6.4
    def setLanguage(self, lcid, reboot: bool = False):
        """Set the language of the display

        Command:
            DIAGnostic:LANGuage <lcid>[,<reboot>]

        Args:
            lcid (str): The language of the display
            reboot (bool): Set to True to reboot the display

        Returns:
            None
        """
        self.parent.cmd(f'DISPaly:LANGuage {lcid},{int(reboot)}')