
from metagpt.team import Team
import platform
import asyncio
import fire

async def creatTeam(idea: str, investment: float = 3.0, n_round: int = 5):
    hire_roles = [PythonCoder(),JavaScriptCoder()]     

    team = Team()
    team.hire([leader] + hire_roles)
    team.invest(investment)
    team.run_project(idea, send_to ="leader")
    await team.run(n_round=n_round)




def main(
    idea: str = "",
    investment: float = 3.0,
    n_round: int = 5,
):
    """
    :param idea: Debate topic, such as "Topic: The U.S. should commit more in climate change fighting"
                 or "Trump: Climate change is a hoax"
    :param investment: contribute a certain dollar amount to watch the debate
    :param n_round: maximum rounds of the debate
    :return:
    """
    
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(creatTeam(idea, investment, n_round))


if __name__ == "__main__":
    fire.Fire(main)