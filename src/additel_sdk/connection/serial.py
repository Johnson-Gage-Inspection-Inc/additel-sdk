import serial  # pip install pyserial


class SerialConnection:
    """Class to handle Serial connection to the device."""
    raise NotImplementedError("Serial connection is not implemented yet.")
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.port = kwargs.get("port")
        self.baudrate = kwargs.get("baudrate", 9600)
        self.bytesize = kwargs.get("bytesize", serial.EIGHTBITS)
        self.parity = kwargs.get("parity", serial.PARITY_NONE)
        self.stopbits = kwargs.get("stopbits", serial.STOPBITS_ONE)
        self.timeout = kwargs.get("timeout", 1)
        self.serial_port = None

        if not self.port:
            raise ValueError("Serial port must be specified.")

    def connect(self):
        """Establish a serial connection to the device."""
        try:
            self.serial_port = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=self.bytesize,
                parity=self.parity,
                stopbits=self.stopbits,
                timeout=self.timeout,
            )
        except serial.SerialException as e:
            raise ConnectionError(f"Failed to open serial port {self.port} - {e}")

    def disconnect(self):
        """Close the serial connection."""
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.close()
                self.serial_port = None
            except serial.SerialException as e:
                raise ConnectionError(f"Failed to close serial port {self.port} - {e}")

    def send_command(self, command):
        """Send a command to the device over the serial connection."""
        if not self.serial_port or not self.serial_port.is_open:
            raise ConnectionError("Serial connection is not established.")

        try:
            self.serial_port.write(f"{command}\r\n".encode())
        except serial.SerialException as e:
            raise IOError(f"Failed to send command '{command}' - {e}")

    def read_response(self):
        """Read a response from the device over the serial connection."""
        if not self.serial_port or not self.serial_port.is_open:
            raise ConnectionError("Serial connection is not established.")

        try:
            response = self.serial_port.read(1024).decode().strip()
            return response
        except serial.SerialException as e:
            raise IOError(f"Failed to read response - {e}")
