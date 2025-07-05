from enum import StrEnum;

class RegexPattern(StrEnum):

    DiscordMessageReference: str = r"https:\/\/(?:canary\.|ptb\.)?discord(?:app)?\.com\/channels\/(\d+)\/(\d+)\/(\d+)";

    DiscordCustomEmoji: str = r'<a?:\w+:(\d+)>';
