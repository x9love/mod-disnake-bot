import disnake
from disnake.ext import commands

class inrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description='Список пользователей с данной ролью')
    @commands.has_permissions(manage_messages=True)
    async def inrole(self, interaction, role: disnake.Role):
            people_with_role = [member.display_name for member in interaction.guild.members if role in member.roles]
            embed = disnake.Embed(
                 title='Модератор',
                 description=f'Люди с ролью {role.mention}: \n {", ".join(people_with_role)}'
            )
            await interaction.send(embed=embed)

def setup(bot):
    bot.add_cog(inrole(bot))