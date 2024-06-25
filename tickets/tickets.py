from typing import Optional
import discord

from .common.buttons import TicketButton

from redbot.core import commands, app_commands, Config
from zammad_py import ZammadAPI

embedSuccess = discord.Embed(description="# Erfolgreich\n**Es wurden folgende Werte gesetzt:**", color=0x0ffc03)
embedFailure = discord.Embed(color=0xff0000)
embedLog = discord.Embed(color=0xfc7f03)

class Tickets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=518963742)
        self.config.register_guild(
            host="None",
            user="None",
            password="None",
            embedTitle="Ticket",
            embedDescription="Drücke auf den Button um ein neues Ticket zu erstellen",
            embedFooter="None",
            embedFooterURL="None",
            buttonLabel="Neues Ticket erstellen",
            modalTitle="Ticket",
            modalNameLabel="Name",
            modalNamePlaceholder="Max Mustermann",
            modalMailLabel="E-Mail",
            modalMailPlaceholder="max@mustermann.de",
            modalSubjectLabel="Subject",
            modalSubjectPlaceholder="Trollen im Chat",
            modalMessageLabel="Message",
            modalMessagePlaceholder="Der User XXX trollt sämtliche User im Chat",
            ticketCategory=0,
            tickets={}
    )

    tickets = app_commands.Group(name="ticket", description="Ticket commands")

    @tickets.command(name="setup", description="Konfiguriere das System")
    @app_commands.describe(option="Welche Option soll geändert werden?", wert="Der Wert welcher gesetzt werden soll")
    @app_commands.choices(option=[
        app_commands.Choice(name="Hostname", value="host"),
        app_commands.Choice(name="Username", value="user"),
        app_commands.Choice(name="Password", value="password"),
        app_commands.Choice(name="Embed Title", value="embedTitle"),
        app_commands.Choice(name="Embed Description", value="embedDescription"),
        app_commands.Choice(name="Embed Footer", value="embedFooter"),
        app_commands.Choice(name="Embed Footer URL", value="embedFooterURL"),
        app_commands.Choice(name="Modal Title", value="modalTitle"),
        app_commands.Choice(name="Modal Name Label", value="modalNameLabel"),
        app_commands.Choice(name="Modal Name Placeholder", value="modalNamePlaceholder"),
        app_commands.Choice(name="Modal Mail Label", value="modalMailLabel"),
        app_commands.Choice(name="Modal Mail Placeholder", value="modalMailPlaceholder"),
        app_commands.Choice(name="Modal Subject Label", value="modalSubjectLabel"),
        app_commands.Choice(name="Modal Subject Placeholder", value="modalSubjectPlaceholder"),
        app_commands.Choice(name="Modal Message Label", value="modalMessageLabel"),
        app_commands.Choice(name="Modal Message Placeholder", value="modalMessagePlaceholder"),
        app_commands.Choice(name="Button Label", value="buttonLabel"),
        app_commands.Choice(name="Ticket Kategorie", value="ticketCategory")
    ])
    async def setup(self, interaction: discord.Interaction, option: app_commands.Choice[str], wert: str):
        try:

            match option.value:

                case "host":

                    await self.config.guild(interaction.guild).host.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Host__**\n* {wert}"

                case "user":

                    await self.config.guild(interaction.guild).user.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Username__**\n* {wert}"

                case "password":

                    await self.config.guild(interaction.guild).password.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Password__**\n* {wert}"

                case "embedTitle":

                    await self.config.guild(interaction.guild).embedTitle.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Embed Title__**\n* {wert}"

                case "embedDescription":

                    await self.config.guild(interaction.guild).embedDescription.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Embed Description__**\n* {wert}"

                case "embedFooter":

                    await self.config.guild(interaction.guild).embedFooter.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Embed Footer__**\n* {wert}"

                case "embedFooterURL":

                    await self.config.guild(interaction.guild).embedFooterURL.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Embed Footer URL__**\n* {wert}"

                case "modalTitle":

                    await self.config.guild(interaction.guild).modalTitle.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Modal Title__**\n* {wert}"

                case "modalNameLabel":

                    await self.config.guild(interaction.guild).modalNameLabel.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**Modal Name Label**\n* {wert}"

                case "modalNamePlaceholder":

                    await self.config.guild(interaction.guild).modalNamePlaceholder.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Modal Name Placeholder__**\n* {wert}"

                case "modalMailLabel":

                    await self.config.guild(interaction.guild).modalMailLabel.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Modal Mail Label__**\n* {wert}"

                case "modalMailPlaceholder":

                    await self.config.guild(interaction.guild).modalMailPlaceholder.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Modal Mail Placeholder__**\n* {wert}"

                case "modalSubjectLabel":

                    await self.config.guild(interaction.guild).modalSubjectLabel.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Modal Subject Label__**\n* {wert}"

                case "modalSubjectPlaceholder":

                    await self.config.guild(interaction.guild).modalSubjectPlaceholder.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Modal Subject Placeholder__**\n* {wert}"

                case "modalMessageLabel":

                    await self.config.guild(interaction.guild).modalMessageLabel.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Modal Message Label__**\n* {wert}"

                case "modalMessagePlaceholder":

                    await self.config.guild(interaction.guild).modalMessagePlaceholder.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Modal Message Placeholder__**\n* {wert}"

                case "buttonLabel":

                    await self.config.guild(interaction.guild).embedFooterURL.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Button Label__**\n* {wert}"

                case "ticketCategory":
                    
                    if(wert.isnumeric() == False):
                        raise Exception("Die ID darf nur aus Zahlen bestehen")
                    if(discord.utils.get(interaction.guild.categories, id=int(wert))) is None:
                        raise Exception("Keine Kategorie gefunden")
                    await self.config.guild(interaction.guild).ticketCategory.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Ticket Kategorie__**\n* {wert}"
                    
            await interaction.response.send_message(embed=embedSuccess, ephemeral=True)

        except Exception as error:
            embedFailure.description = f"# Fehler\n### Es ist folgender Fehler aufgetreten:\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)

    @tickets.command(name="getconfig", description="Zeigt die gesammte Konfiguration")
    @app_commands.checks.has_permissions(administrator=True)
    async def getconfig(self, interaction: discord.Interaction):
        try:
            embedLog.description = (f"# Ticketsystem Konfiguration\n"
                                    f"### System\n"
                                    f"* Host: **{await self.config.guild(interaction.guild).host()}**\n"
                                    f"* User: **{await self.config.guild(interaction.guild).user()}**\n"
                                    f"* Password: **{await self.config.guild(interaction.guild).password()}**\n"
                                    f"### Embed\n"
                                    f"* Title: **{await self.config.guild(interaction.guild).embedTitle()}**\n"
                                    f"* Description: **{await self.config.guild(interaction.guild).embedDescription()}**\n"
                                    f"* Footer: **{await self.config.guild(interaction.guild).embedFooter()}**\n"
                                    f"* Footer URL: **{await self.config.guild(interaction.guild).embedFooterURL()}**\n"
                                    f"### Button\n"
                                    f"* Label: **{await self.config.guild(interaction.guild).buttonLabel()}**\n"
                                    f"### Modal\n"
                                    f"* Title: **{await self.config.guild(interaction.guild).modalTitle()}**\n"
                                    f"* Name Label: **{await self.config.guild(interaction.guild).modalNameLabel()}**\n"
                                    f"* Name Placeholder: **{await self.config.guild(interaction.guild).modalNamePlaceholder()}**\n"
                                    f"* E-Mail Label: **{await self.config.guild(interaction.guild).modalMailLabel()}**\n"
                                    f"* E-Mail Placeholder: **{await self.config.guild(interaction.guild).modalMailPlaceholder()}**\n"
                                    f"* Subject Label: **{await self.config.guild(interaction.guild).modalSubjectLabel()}**\n"
                                    f"* Subject Placeholder: **{await self.config.guild(interaction.guild).modalSubjectPlaceholder()}**\n"
                                    f"* Description Label: **{await self.config.guild(interaction.guild).modalMessageLabel()}**\n"
                                    f"* Description Placeholder: **{await self.config.guild(interaction.guild).modalDescriptionPlaceholder()}**\n"
                                    f"### Tickets\n"
                                    f"* Ticket Category: **{discord.utils.get(interaction.guild.categories, id=int(await self.config.guild(interaction.guild).ticketCategory()))}**")
            await interaction.response.send_message(embed=embedLog)
        except Exception as error:
            embedFailure.description = f"# Fehler\n### Es ist folgender Fehler aufgetreten:\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)

    @tickets.command(name="create", description="Erstelle ein neues Ticket")
    async def create(self, interaction: discord.Interaction):
        try:

            embed = discord.Embed(title=await self.config.guild(interaction.guild).embedTitle(), description=await self.config.guild(interaction.guild).embedDescription())

            await interaction.response.send_message(embed=embed, view=TicketButton(await self.config.guild(interaction.guild).buttonLabel(),
                                                                      discord.ButtonStyle.green, await self.config.guild(interaction.guild).modalTitle(),
                                                                      await self.config.guild(interaction.guild).modalNameLabel(),
                                                                      await self.config.guild(interaction.guild).modalNamePlaceholder(),
                                                                      await self.config.guild(interaction.guild).modalMailLabel(),
                                                                      await self.config.guild(interaction.guild).modalMailPlaceholder(),
                                                                      await self.config.guild(interaction.guild).modalSubjectLabel(),
                                                                      await self.config.guild(interaction.guild).modalSubjectPlaceholder(),
                                                                      await self.config.guild(interaction.guild).modalMessageLabel(),
                                                                      await self.config.guild(interaction.guild).modalMessagePlaceholder(),
                                                                      discord.TextStyle.long))

        except Exception as error:
            print(error)

    async def create_text_channel(self, interaction: discord.Interaction, ticketID: int):
        try:
            channelname=f"ticket-{interaction.user}"
            permissionOverwrite = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True)
            }
            channel = await interaction.guild.create_text_channel(name=channelname, category=int(await self.config.guild(interaction.guild).ticketCategory()), overwrites=permissionOverwrite)
            await self.config.guild(interaction.guild).tickets.set_raw(interaction.user.id, value={'channel': channel.id, 'zammadID': ticketID})
        except Exception as error:
            embedFailure.description = f"# Fehler\n### Es ist folgender Fehler aufgetreten:\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)