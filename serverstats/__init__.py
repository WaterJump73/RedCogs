from .serverstats import ServerStats

async def setup(bot):
    await bot.add_cog(ServerStats(bot))