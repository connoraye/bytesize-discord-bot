import discord
import argparse
import os
import socket
import sys
import logging

def setup_logging(logger_level):
    the_logger = logging.getLogger()
    for old_handler in the_logger.handlers:
        the_logger.removeHandler(old_handler)

    new_handler = logging.StreamHandler(sys.stdout)

    hostname = socket.gethostname()

    json_format = (
        '{ "timestamp": "%(asctime)s", "log_level": "%(levelname)s", "message": "%(message)s", '
        f'"environment": "{args.environment}", "application": "{args.application}", '
        f'"module": "%(module)s", "process": "%(process)s", '
        f'"thread": "[%(thread)s]", "hostname": "{hostname}" }} '
    )

    new_handler.setFormatter(logging.Formatter(json_format))
    the_logger.addHandler(new_handler)
    new_level = logging.getLevelName(logger_level.upper())
    the_logger.setLevel(new_level)

    if the_logger.isEnabledFor(logging.DEBUG):
        boto3.set_stream_logger()
        the_logger.debug(f'Using boto3", "version": "{boto3.__version__}')

    return the_logger


def get_parameters():
    parser = argparse.ArgumentParser(
        description="A Discord bot"
    )

    # Parse command line inputs and set defaults
    parser.add_argument("--discord-bot-token")
    parser.add_argument("--log-level", default="INFO")
    parser.add_argument("--environment")
    parser.add_argument("--application")


    _args = parser.parse_args()

    # Override arguments with environment variables where set
    if "DISCORD_BOT_TOKEN" in os.environ:
        _args.discord_bot_token = os.environ["DISCORD_BOT_TOKEN"]
    if "LOG_LEVEL" in os.environ:
        _args.log_level = os.environ["LOG_LEVEL"]

    required_args = ["discord_bot_token"]

    missing_args = []
    for required_message_key in required_args:
        if required_message_key not in _args:
            missing_args.append(required_message_key)
    if missing_args:
        raise argparse.ArgumentError(
            None,
            "ArgumentError: The following required arguments are missing: {}".format(
                ", ".join(missing_args)
            ),
        )

    return _args

args = get_parameters()
logger = setup_logging(args.log_level)

client = discord.Client()

def main():
    logger.info(f'Discord bot token", "token": {args.discord_bot_token}')
    client.run(str(args.discord_bot_token))

@client.event
async def on_ready():
    logger.info(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    msg = message.content
    if message.author == client.user:
        return
    
    if msg.startswith("!hello"):
        logger.info(f"Received !hello command from {message.author}")
        await message.channel.send("Hello, I'm the ByteSize bot. People know me as Gigabyte.")

if __name__ == '__main__':
    main()
