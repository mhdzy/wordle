import os


class Message:
    def __init__(self, mode: str) -> None:
        self.mode = mode
        if self.mode not in ["phone", "group"]:
            raise ValueError("Class variable 'mode' must be either 'phone' or 'group'.")
        return None

    def send_message(self, phone_number: str, message: str) -> None:
        program = "osascript"
        mode = (
            "message/" + ("message.app" if self.mode == "phone" else "groupmessage.app")
        )
        phone_number = f'"{phone_number}"'
        message = f'"{message}"'
        cmd = " ".join([program, mode, phone_number, message])

        os.system(cmd)

        return None
