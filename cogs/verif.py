import disnake
from disnake.ext import commands
from disnake import TextInputStyle
from utils.databases import VerifDataBase


class GradeButt(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label='1', style=disnake.ButtonStyle.gray, custom_id='1')
    async def gr1(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.response.send_modal(ReviewModal(inter.author, 1, inter.bot))

    @disnake.ui.button(label='2', style=disnake.ButtonStyle.gray, custom_id='2')
    async def gr2(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.response.send_modal(ReviewModal(inter.author, 2, inter.bot))

    @disnake.ui.button(label='3', style=disnake.ButtonStyle.gray, custom_id='3')
    async def gr3(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.response.send_modal(ReviewModal(inter.author, 3, inter.bot))

    @disnake.ui.button(label='4', style=disnake.ButtonStyle.gray, custom_id='4')
    async def gr4(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.response.send_modal(ReviewModal(inter.author, 4, inter.bot))

    @disnake.ui.button(label='5', style=disnake.ButtonStyle.gray, custom_id='5')
    async def gr5(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.response.send_modal(ReviewModal(inter.author, 5, inter.bot))


class ReviewModal(disnake.ui.Modal):
    def __init__(self, member: disnake.Member, grade: int, bot: commands.Bot):
        self.member = member
        self.grade = grade
        self.bot = bot
        self.db = VerifDataBase()

        components = [
            disnake.ui.TextInput(label='Расскажите почему вы дали именно такую оценку', placeholder='Указывать не обязательно', custom_id='rev_modal',
                                style=TextInputStyle.paragraph, min_length=2, max_length=200, required=False)
        ]

        super().__init__(title='Оценка верификации', components=components, custom_id='reviewModal')

    async def callback(self, inter: disnake.ModalInteraction):


        rev_channels = self.bot.get_channel(1275053843406651422) #id канала с отзывами верификации

        rev_modal = inter.text_values['rev_modal']
        
        target_user = inter.author.name
        verificator = await self.db.get_user(target_user)

        embed = disnake.Embed(description=f'Оценка верификации от {inter.author.mention}:  **{self.grade}**\n\n{rev_modal}', color=0x2b2d31)
        embed.set_footer(text=f'Верефицировал: {verificator[1]}')
        await rev_channels.send(embed=embed)

        await inter.response.edit_message('Спасибо за вашу оценку! Она поможет нам стать еще лучше!', view=None)


class ButtGender(disnake.ui.View):
    def __init__(self, member: disnake.Member, name: str, age: int, bot: commands.Bot):
        super().__init__(timeout=None)
        self.member = member
        self.name = name
        self.age = age
        self.bot = bot
        self.db = VerifDataBase()

    @disnake.ui.button(label='Мужской', style=disnake.ButtonStyle.gray, custom_id='man_butt')
    async def man(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.response.defer(ephemeral=True)
        await inter.edit_original_response('<a:typing:1187808451259289741> Верифицирую пользователя...', components=[])

        man_role = inter.guild.get_role(1252615275573153835) # id роли мужской гендерки
        await self.member.add_roles(man_role)

        verif_log = inter.guild.get_channel(1262005303512272896) # id канала с логами верификации

        embed = disnake.Embed(description=f'{self.member.mention} был верифицирован {inter.author.mention}', color=0x2b2d31)

        await self.db.create_table()
        target_user = self.member.name
        verificator = inter.author.name
        await self.db.add_verif_user(target_user, verificator, reason=None)
        
        embed.add_field(name='>>> Имя:', value=f'```{self.name}```', inline=False)
        embed.add_field(name='>>> Возраст:', value=f'```{self.age}```', inline=False)
        embed.add_field(name='>>> Пол:', value=f'```Мужской```', inline=False)
        await verif_log.send(embed=embed)

        verif_role = inter.guild.get_role(1275053689312251946) #id роли верифицирован
        unverif_role = inter.guild.get_role(1274491445889466491) #id роли неверифицирован

        await self.member.add_roles(verif_role)
        await self.member.remove_roles(unverif_role, reason=f'{inter.author.name} верифицирует {self.member.name}')

        try:
            await self.member.send('**Оцените работу нашего состава, если есть недостатки или проблемы, напишите их**', view=GradeButt())

        except disnake.Forbidden:
            channel = inter.guild.get_channel(1274732200402878515) # id канала с отзывами верификации
            embed = disnake.Embed(description=f'У {self.member.mention} закрыты личные сообщения. Он не получил предложения оценить верификацию.', color=0xFF7B7B)

            await channel.send(embed=embed)
        await inter.edit_original_message('**Пользователь верифицирован!**')


    @disnake.ui.button(label='Женский', style=disnake.ButtonStyle.gray, custom_id='woman_butt')
    async def woman(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.response.defer(ephemeral=True)
        await inter.edit_original_response('<a:typing:1187808451259289741> Верифицирую пользователя...', components=[])

        woman_role = inter.guild.get_role(1274611885848657920) # id роли женской гендерки
        await self.member.add_roles(woman_role)

        verif_log = inter.guild.get_channel(1262005303512272896) # id канала с логами верификации

        embed = disnake.Embed(description=f'{self.member.mention} был верифицирован {inter.author.mention}', color=0x2b2d31)
        
        await self.db.create_table()
        target_user = self.member.name
        verificator = inter.author.name
        await self.db.add_verif_user(target_user, verificator, reason=None)
        
        embed.add_field(name='>>> Имя:', value=f'```{self.name}```', inline=False)
        embed.add_field(name='>>> Возраст:', value=f'```{self.age}```', inline=False)
        embed.add_field(name='>>> Пол:', value=f'```Женский```', inline=False)
        await verif_log.send(embed=embed)

        verif_role = inter.guild.get_role(...) #id роли верифицирован
        unverif_role = inter.guild.get_role(...) #id роли неверифицирован

        await self.member.add_roles(verif_role)
        await self.member.remove_roles(unverif_role, reason=f'{inter.author.name} верифицирует {self.member.name}')

        try:
            await self.member.send('**Оцените работу нашего состава, если есть недостатки или проблемы, напишите их**', view=GradeButt())

        except:
            channel = inter.guild.get_channel(...) #id канала с отзывами верификации
            embed = disnake.Embed(description=f'У {self.member.mention} закрыты личные сообщения. Она не получила предложения оценить верификацию.', color=0xFF7B7B)

            await channel.send(embed=embed)
        await inter.edit_original_message('**Пользователь верифицирован!**')


class VerifModal(disnake.ui.Modal):
    def __init__(self, member: disnake.Member, bot: commands.Bot):
        self.member = member
        self.bot = bot

        components = [
            disnake.ui.TextInput(label='Имя', placeholder='Как обращаться к пользователю', custom_id='name',
                                style=TextInputStyle.short, required=False),
            disnake.ui.TextInput(label='Возраст', placeholder='Возраст пользователя', custom_id='age',
                                style=TextInputStyle.short, required=False)
        ]

        super().__init__(title='Верификация', components=components, custom_id='verifModal')

    async def callback(self, inter: disnake.ModalInteraction):
        await inter.response.defer(ephemeral=True)

        name = inter.text_values['name']
        age = inter.text_values['age']

        if not name:
            name = 'Не указанно'
        if not age:
            age = 'Не указан'

        await inter.edit_original_response('Укажите пол', view=ButtGender(self.member, name, age, self.bot))


class Verif(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistents_views_added = False

    @commands.slash_command(name='verif', description='Верификация пользователей')
    async def verif(self, inter, member: disnake.Member = commands.Param(name='пользователь', description='Укажите пользователя для верификации')):
        role = inter.guild.get_role(...) #id роли верифицирован

        if member == inter.author:
            return await inter.response.send_message('Вы не можете верифицировать себя', ephemeral=True)
        
        if member.bot:
            return await inter.response.send_message('Вы не можете взаимодействовать с ботом', ephemeral=True)

        if role in member.roles:
            return await inter.response.send_message('Данный пользователь уже верифицирован', ephemeral=True)

        await inter.response.send_modal(VerifModal(member, self.bot))

    @commands.Cog.listener()
    async def on_ready(self):
        if self.persistents_views_added:
            return

        self.bot.add_view(GradeButt())


def setup(bot):
    bot.add_cog(Verif(bot))
