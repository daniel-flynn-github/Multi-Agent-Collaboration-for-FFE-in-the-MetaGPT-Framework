#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio

import fire

from metagpt.roles import (
    Architect,
    Engineer,
    ProductManager,
    ProjectManager,
    QaEngineer,
    UserResearcher,
    NeedsAnalyst,
    DesignManager,
    Innovator,
    SolutionEngineer,
    FeasibilityAnalyst,
    MarketAnalyst
)
from metagpt.team import Team


async def startup(
    idea: str,
    investment: float = 0.01,
    n_round: int = 2,
):
    """Run a startup. Be a boss."""
    company = Team()
    company.hire(
        [
            FeasibilityAnalyst(),
        ]
    )


    company.invest(investment)
    company.start_project(idea)
    await company.run(n_round=n_round)


def main(
    idea: str = "",
    investment: float = 0.2,
    n_round: int = 8,
):
    company_description = input("Give a brief description of your company: \n")
    topic = input("Give a description of the topic or issue you want product ideas for: \n")
    budget = input("What is the budget you are willing to allocate to the project?: \n")
    timeframe = input("In what timeframe does the product need to reach the market?: \n")
    idea = "Company Description: " + company_description + "\nTopic: " + topic + "\nBudget: " + budget + "\nTimeframe: " + timeframe

    asyncio.run(startup(idea, investment, n_round))


if __name__ == "__main__":
    fire.Fire(main)
