
from metagpt.team import Team
import platform
import asyncio
import fire
from roles import leader

async def creatTeam(idea: str, investment: float = 3.0, n_round: int = 5):
    hire_roles = []     
    
    leaderProfile: str = 'leader 你是一位高效能的領導者，擁有出色的組織能力和溝通技巧。'    
    leaderRole = leader.Leader(name="leader", profile=leaderProfile, hire_roles=hire_roles, idea=idea)

    team = Team()
    team.hire([leaderRole])
    team.invest(investment)
    team.run_project(idea, send_to ="leader")
    await team.run(n_round=n_round)




def main(
    idea: str = "write a hello word with javascript",
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