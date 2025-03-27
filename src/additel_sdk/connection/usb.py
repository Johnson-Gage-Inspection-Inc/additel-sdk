import usb.core
import usb.util
from usb.backend import libusb1
import logging
from . import Connection


class USBConnection(Connection):
    """Class to handle USB connection to the device."""

    type = "usb"

    def __init__(self, parent, **kwargs):
        self.vendor_id = kwargs.get("vendor_id")
        self.product_id = kwargs.get("product_id")
        self.backend_path = kwargs.get("backend_path")  # Optional, for custom backend
        self.device = None
        self.endpoint_out = None
        self.endpoint_in = None

        if not self.vendor_id or not self.product_id:
            raise ValueError(
                "Both 'vendor_id' and 'product_id' required for USB connection."
            )

        self.backend = (
            libusb1.get_backend(find_library=lambda x: self.backend_path)
            if self.backend_path
            else None
        )

    def __enter__(self):
        """Establish connection to the USB device."""
        try:
            self.device = usb.core.find(
                idVendor=self.vendor_id, idProduct=self.product_id, backend=self.backend
            )
            if self.device is None:
                raise ConnectionError(
                    "USB device not found. Ensure it's connected and IDs are correct."
                )

            self.device.set_configuration()
            configuration = self.device.get_active_configuration()
            interface = configuration[(0, 0)]

            self.endpoint_out = usb.util.find_descriptor(
                interface,
                custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)
                == usb.util.ENDPOINT_OUT,
            )
            self.endpoint_in = usb.util.find_descriptor(
                interface,
                custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)
                == usb.util.ENDPOINT_IN,
            )

            if self.endpoint_out is None or self.endpoint_in is None:
                raise ConnectionError(
                    "Endpoints for USB communication could not be established."
                )

        except usb.core.USBError as e:
            raise ConnectionError(f"Failed to establish USB connection: {e}") from e

    def __exit__(self):
        """Release the USB device."""
        try:
            if self.device:
                usb.util.dispose_resources(self.device)
                self.device = None
        except usb.core.USBError as e:
            logging.error(f"Failed to release USB device: {e}")
            raise ConnectionError(f"Failed to disconnect USB device: {e}") from e

    def send_command(self, command):
        """Send a command to the USB device."""
        if not self.device or not self.endpoint_out:
            raise ConnectionError(
                "USB device is not connected or output endpoint is unavailable."
            )

        try:
            self.endpoint_out.write(command)
        except usb.core.USBError as e:
            raise IOError(f"Failed to send command '{command}': {e}") from e

    def read_response(self, timeout=5000):
        """Read response from the USB device."""
        if not self.device or not self.endpoint_in:
            raise ConnectionError(
                "USB device is not connected or input endpoint is unavailable."
            )

        try:
            response = self.device.read(
                self.endpoint_in.bEndpointAddress,
                self.endpoint_in.wMaxPacketSize,
                timeout=timeout,
            )
            return response.tobytes().decode("utf-8").strip()
        except usb.core.USBError as e:
            raise IOError(f"Failed to read response: {e}") from e

    def list_available_devices():
        """Utility method to list all connected USB devices."""
        devices = []
        for device in usb.core.find(find_all=True):
            devices.append(
                {
                    "vendor_id": hex(device.idVendor),
                    "product_id": hex(device.idProduct),
                    "manufacturer": (
                        usb.util.get_string(device, device.iManufacturer)
                        if device.iManufacturer
                        else "Unknown"
                    ),
                    "product": (
                        usb.util.get_string(device, device.iProduct)
                        if device.iProduct
                        else "Unknown"
                    ),
                }
            )
        return devices
