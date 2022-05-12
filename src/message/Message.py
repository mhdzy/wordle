#!/usr/bin/env python3

import os


class Message:

    msg_path = "src/message/"

    def __init__(self, mode: str) -> None:
        self.mode: str = mode
        if self.mode not in ["phone", "group"]:
            raise ValueError("Class variable 'mode' must be either 'phone' or 'group'.")
        return None

    def send_message(self, phone_number: str, message: str) -> None:
        program: str = "osascript"
        mode: str = self.msg_path + (
            "message.app" if self.mode == "phone" else "groupmessage.app"
        )
        cmd: str = " ".join([program, mode, f'"{phone_number}"', f'"{message}"'])

        os.system(cmd)

        return None
