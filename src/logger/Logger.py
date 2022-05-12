#!/usr/bin/env python3

import logging


class Logger:
    """
    logger utility class

    allows creation of an arbitrary logger

    :global vars:
    __logger__

    :instance vars:
    name
    handlers
    format
    level

    :internal class methods:
    / none /

    :external class methods:
    create()
    get()
    set_and_add()
    destroy()
    """

    __logger__ = None

    def __init__(
        self,
        name: str = "default-logger",
        level=logging.DEBUG,
        output_dir: str = "logs",
        output_file: str = "output.log",
        handlers: dict = {"Stream": False, "File": True},
    ) -> None:
        """
        initialize the class
        """
        self.name = name
        self.level = level
        self.handlers = handlers
        self.output_dir = output_dir
        self.output_file = output_file
        self.format = logging.Formatter(
            fmt="[%(asctime)s] %(levelname)-8s :: %(name)-20s :: %(funcName)-12s :: %(message)s"
        )

        return None

    def create(self):
        self.__logger__ = logging.getLogger(self.name)
        self.__logger__.setLevel(self.level)

        if not self.__logger__.hasHandlers():
            if self.handlers.get("File"):
                self.set_and_add(logging.FileHandler(f"{self.output_dir}/{self.output_file}"))

            if self.handlers.get("Stream"):
                self.set_and_add(logging.StreamHandler())

        self.__logger__.debug("logger created")

        return self

    def get(self):
        if self.__logger__ == None:
            raise ValueError(
                f"logger {self.name} has no active logger. create one to continue."
            )

        return self.__logger__

    def set_and_add(self, handler):
        handler.setFormatter(self.format)
        self.__logger__.addHandler(handler)
        return self

    def destroy(self):
        self.__logger__ = None
        return self
