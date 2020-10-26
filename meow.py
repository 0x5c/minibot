"""
Static variables that power the bot to meow at you.
---
"""

#informational

author = "@Mad Ice Tea#6497"
# not actually called during the meow command, would ruin the experience. Only for those who read the code.
license = "MIT"
# again, not actually called, but more because this is assumed from mb?info + source repository to begin with

#translations of the command

meowEnglish = ""mew", "miao", "mao""
meowSpanish = ""miau""
meowJapanese = ""ミュ", "マオ""

#functional

fileLocation = "das_katzchen.png"
# Might need dynamic changes if we move this file to a resources folder; such cases are better handled/changed from a helper file than in the main.py
fileDiscordName = image.png
fileDiscordNameQuotes = """ + image.png + """
# Based on documentation: https://discordpy.readthedocs.io/en/latest/faq.html#how-do-i-use-a-local-image-file-for-an-embed-image
# DiscordNameQuotes is creating a string from the raw filename input. The default appears to be image.png, but this could probably be changed?
fileEmbedName = ""attachment://" + fileName + """
# For the embed line.
