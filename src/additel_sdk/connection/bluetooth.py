import asyncio
from bleak import BleakClient, BleakScanner  # pip install bleak
from queue import Queue, Empty


class BluetoothConnection:
    """Class to handle Bluetooth connection to the device."""

    raise NotImplementedError("Bluetooth connection is not implemented yet.")

    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.device_name = kwargs.get("device_name")
        self.notification_uuid = kwargs.get("notification_uuid")
        self.write_uuid = kwargs.get("write_uuid")
        self.client = None
        self.response_queue = Queue()

        if not self.device_name:
            raise ValueError("Device name must be specified for Bluetooth connection.")

    def connect(self):
        """Establish a Bluetooth connection to the device."""
        asyncio.run(self._connect_async())

    async def _connect_async(self):
        devices = await BleakScanner.discover()
        for device in devices:
            if device.name == self.device_name:
                self.client = BleakClient(device)
                try:
                    await self.client.connect()
                    return
                except Exception as e:
                    raise ConnectionError(
                        f"Failed to connect to Bluetooth device '{self.device_name}' - {e}"
                    )
        raise ConnectionError(f"Bluetooth device '{self.device_name}' not found.")

    def disconnect(self):
        """Close the Bluetooth connection."""
        asyncio.run(self._disconnect_async())

    async def _disconnect_async(self):
        if self.client and self.client.is_connected:
            try:
                await self.client.disconnect()
                self.client = None
            except Exception as e:
                raise ConnectionError(
                    f"Failed to disconnect from Bluetooth device - {e}"
                )

    def send_command(self, command):
        """Send a command to the Bluetooth device."""
        asyncio.run(self._send_command_async(command))

    async def _send_command_async(self, command):
        if not self.client or not self.client.is_connected:
            raise ConnectionError("Bluetooth connection is not established.")

        try:
            command_in_bytes = bytes(command, "utf-8")
            await self.client.write_gatt_char(self.write_uuid, command_in_bytes)
        except Exception as e:
            raise IOError(f"Failed to send command '{command}' - {e}")

    def read_response(self, timeout=5):
        """Read response from the Bluetooth device."""
        try:
            response = self.response_queue.get(timeout=timeout)
            return response
        except Empty:
            raise TimeoutError("No response received within the timeout period.")

    async def _notification_handler(self, sender, data):
        """Handle incoming notifications from the device."""
        response = data.decode("utf-8")
        self.response_queue.put(response)

    def enable_notifications(self):
        """Enable notifications for reading responses."""
        asyncio.run(self._enable_notifications_async())

    async def _enable_notifications_async(self):
        if not self.client or not self.client.is_connected:
            raise ConnectionError("Bluetooth connection is not established.")

        try:
            await self.client.start_notify(
                self.notification_uuid, self._notification_handler
            )
        except Exception as e:
            raise IOError(f"Failed to enable notifications - {e}")

    def disable_notifications(self):
        """Disable notifications."""
        asyncio.run(self._disable_notifications_async())

    async def _disable_notifications_async(self):
        if not self.client or not self.client.is_connected:
            raise ConnectionError("Bluetooth connection is not established.")

        try:
            await self.client.stop_notify(self.notification_uuid)
        except Exception as e:
            raise IOError(f"Failed to disable notifications - {e}")
