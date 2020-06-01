from .logger import logging

class LongMessage:
    """Class to handle long message sending in chunks"""
    def __init__(self, channel, block=False):
        self.limit = 1994 # to allow ``` before and after
        self.parts = []
        self.channel = channel
        self.block = block

    def add(self, part):
        """Adds part of long message"""
        self.parts.append(part)

    async def send(self):
        """sends the message to channel in limit chunks"""
        for chunk in self.chunks():
            await self.channel.send(chunk)
        logger.info("Response:\n%s", '\n'.join(self.lines()))

    def lines(self):
        """transforms the message to lines"""
        lines = []
        for part in self.parts:
            lines.extend(part.split("\n"))
        return lines

    def chunks(self):
        """Transform the lines to limit sized chunks"""
        lines = self.lines()
        while True:
            msg = "```asciidoc\n" if self.block else ""
            if not lines:
                break
            while lines and len(msg + lines[0]) < self.limit:
                msg += lines.pop(0) + "\n"
            if self.block:
                msg += '```'
            yield msg
