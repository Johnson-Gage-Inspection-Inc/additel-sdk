import socket
from typing import List, Optional
from customTypes import DIModuleInfo, DIFunctionChannelConfig, DIScanInfo
import time
import json

class Additel:
    def __init__(self, ip: str, port: int = 8000, timeout: int = 10, retries: int = 1):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.retries = retries
        self.connection = None
        self.module = self.Module(self)
        self.scan = self.Scan(self)
        self.channel = self.Channel(self)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def connect(self):
        try:
            self.connection = socket.create_connection((self.ip, self.port), timeout=self.timeout)
        except Exception as e:
            print(f"Error connecting to Additel device: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def send_command(self, command: str) -> Optional[str]:
        for attempt in range(self.retries):
            try:
                if not self.connection:
                    self.connect()
                self.connection.sendall(f"{command}\n".encode())
                return self.connection.recv(4096).decode().strip()
            except socket.timeout:
                print(f"Timeout on attempt {attempt + 1} for command '{command}'. Retrying...")
                time.sleep(1)
            except Exception as e:
                print(f"Error sending command '{command}': {e}")
                break
        return None

    def parse_json(self, response: str) -> dict:
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
        return {}

    def clear_status(self):
        self.send_command("*CLS")

    def identify(self) -> Optional[str]:
        return self.send_command("*IDN?")

    def reset(self):
        self.send_command("*RST")

    class Module:
        def __init__(self, parent):
            self.parent = parent

        def info(self) -> List[DIModuleInfo]:
            response = self.parent.send_command("JSON:MODule:INFormation?")
            if response:
                return [DIModuleInfo(**module) for module in json.loads(response)]
            return []

        def set_label(self, index: int, label: str):
            command = f'MODule:LABel {index},"{label}"'
            self.parent.send_command(command)

        def get_configuration(self, module_index: int) -> List[DIFunctionChannelConfig]:
            response = self.parent.send_command(f"JSON:MODule:CONFig? {module_index}")
            if response:
                return [DIFunctionChannelConfig(**config) for config in json.loads(response)]
            return []

        def configure(self, module_index: int, params: List[DIFunctionChannelConfig]):
            json_params = json.dumps([param.__dict__ for param in params])
            command = f'JSON:MODule:CONFig {module_index},{json_params}'
            self.parent.send_command(command)

    class Scan:
        def __init__(self, parent):
            self.parent = parent

        def start(self, scan_info: DIScanInfo):
            json_params = json.dumps(scan_info.__dict__)
            command = f'JSON:SCAN:STARt {json_params}'
            self.parent.send_command(command)

        def get_configuration(self) -> DIScanInfo:
            response = self.parent.send_command("JSON:SCAN:STARt?")
            if response:
                return DIScanInfo(**json.loads(response))
            return None

        def stop(self):
            self.parent.send_command("SCAN:STOP")

        def get_latest_data(self, time_format: Optional[str] = None) -> Optional[str]:
            command = "SCAN:DATA:Last?"
            if time_format:
                command += f" {time_format}"
            return self.parent.send_command(command)

        def get_data_json(self, count: int) -> List[dict]:
            command = f"JSON:SCAN:DATA? {count}"
            response = self.parent.send_command(command)
            if response:
                return json.loads(response)
            return []

    class Channel:
        def __init__(self, parent):
            self.parent = parent

        def get_configuration(self, channel_name: str) -> DIFunctionChannelConfig:
            response = self.parent.send_command(f'JSON:CHANnel:CONFig? "{channel_name}"')
            if response:
                return DIFunctionChannelConfig(**json.loads(response))
            return None

        def configure(self, channel_config: DIFunctionChannelConfig):
            json_params = json.dumps(channel_config.__dict__)
            command = f'JSON:CHANnel:CONFig {json_params}'
            self.parent.send_command(command)

        def set_zero(self, enable: bool):
            command = f"CHANnel:ZERo {int(enable)}"
            self.parent.send_command(command)

    class Calibration:
        def __init__(self, parent):
            self.parent = parent
            self.electricity = self.Electricity(self)

        class Electricity:
            def __init__(self, parent):
                self.parent = parent

            def start_scan(self, mode: int, function: int, range_: int):
                """
                Start an electrical calibration scan.
            
                This method initiates a calibration scan for electrical parameters
                based on the specified mode, function, and range.
            
                Parameters:
                    mode (int): The mode of calibration. Only `0` (active calibration) is supported.
                    function (int): The function type for calibration:
                        - 0: Voltage
                        - 1: Current
                        - 2: Resistance
                        - 3: PRT (Platinum Resistance Thermometer)
                        - 4: Thermistor
                    range_ (int): The range of calibration specific to the function type:
                        - Voltage: 0 (100 mV), 1 (1 V), 2 (10 V), 3 (50 V)
                        - Current: 0 (100 µA), 1 (1 mA), 2 (10 mA), 3 (100 mA)
                        - Resistance: 0 (100 Ω), 1 (1 kΩ), 2 (10 kΩ), 3 (100 kΩ),
                        4 (1 MΩ), 5 (10 MΩ), 6 (100 MΩ)
                        - PRT: 0 (100 Ω), 1 (400 Ω), 2 (4 kΩ)
                        - Thermistor: 0 (0–10 kΩ), 1 (10–100 kΩ), 2 (0.1–1 MΩ)
            
                Raises:
                    ValueError: If `mode` is not 0, or if invalid parameters are provided.
            
                Returns:
                    None
                """
            
                if mode != 0:
                    raise ValueError("Only mode 0 (active calibration) is supported")
                command = f'CALibration:ElECtricity:SCAN {mode},{function},{range_}'
                self.parent.parent.send_command(command)

            def 