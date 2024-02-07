#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio

import fire

from metagpt.roles import (
    UserResearcher,
    NeedsAnalyst,
    DesignManager,
    SolutionEngineer,
    FeasibilityAnalyst,
    ExperienceAnalyst,
    Demonstrator,
)
from metagpt.team import Team


async def startup(
    idea: str,
    idea_dict: dict = None,
    investment: float = 0.01,
    n_round: int = 2,
):
    """Run a startup. Be a boss."""
    company = Team()
    company.hire(
        [
            UserResearcher(),
            NeedsAnalyst(),
            DesignManager(),
            SolutionEngineer(),
            FeasibilityAnalyst(),
            ExperienceAnalyst(),
            Demonstrator(),
        ]
    )

    company.invest(investment)
    company.start_project(idea, idea_dict)
    await company.run(n_round=n_round)


def main(
    idea: str = "",
    investment: float = 0.5,
    n_round: int = 8,
):
    def mandatory_input(prompt):
        while True:
            a = input(prompt)
            if a != "":
                return a
            print("You must fill in this section")

    def console_input():
        print("Background Information: ")
        company_name = mandatory_input("    Company Name: ")
        company_profile = mandatory_input("    Company Profile: ")
        company_mission = input("    Company Mission: ")
        product_range = input("    Current Product Range: ")
        print("Design Brief: ")
        topic = mandatory_input("    Topic: ")
        audience = input("    Target Audience: ")
        requirements = input("    Key Features and Requirements: ")
        print("Constraints: ")
        budget = mandatory_input("    Budget: ")
        timeframe = mandatory_input("    Timeframe: ")
        constraints = input("    Technical and Legal Constraints: ")
        return (
            ("Background Information: \n"
            "    Company Name: " + company_name + "\n"
            "    Company Profile: " + company_profile + "\n"
            "    Company Mission: " + company_mission + "\n"
            "    Current Product Range: " + product_range + "\n"
            "Design Brief: \n"
            "    Topic: " + topic + "\n"
            "    Target Audience: " + audience + "\n"
            "    Key Features and Requirements: " + requirements + "\n"
            "Constraints: \n"
            "    Budget: " + budget + "\n"
            "    Timeframe: " + timeframe + "\n"
            "    Technical and Legal Constraints: " + constraints),
                ({
                    "Company Name": company_name,
                    "Company Profile": company_profile,
                    "Company Mission": company_mission,
                    "Current Product Range": product_range,
                    "Topic": topic,
                    "Target Audience": audience,
                    "Key Features and Requirements": requirements,
                    "Budget": budget,
                    "Timeframe": timeframe,
                    "Technical and Legal Constraints": constraints
                })
        )
    
    # idea,idea_dict  = console_input()

    idea = '''Background Information:
            Company Name: Scarpa
            Company Profile: Scarpa, an esteemed Italian company founded in 1938, specializes in high-quality outdoor footwear. Initially focused on handcrafted shoes, it has expanded into mountaineering, skiing, rock climbing, and hiking footwear. Known for blending innovation, quality, and performance, Scarpa caters to both professional athletes and outdoor enthusiasts. The brand is globally recognized for its craftsmanship and advanced footwear technology, maintaining a strong position in the technical outdoor footwear market.
            Company Mission: Scarpa's mission centers on inspiring a connection with nature through innovative and quality footwear. Emphasizing Italian craftsmanship and technological advancement, Scarpa aims to enhance outdoor performance, comfort, and safety, encouraging exploration and enjoyment of the natural world.
            Current Product Range: Scarpa's product range includes mountaineering boots, ski boots, rock climbing shoes, and hiking footwear. Tailored for various expertise levels and terrains, their products range from lightweight approach shoes to advanced boots for extreme conditions. Constant innovation, athlete feedback incorporation, and a commitment to sustainability are hallmarks of their range, emphasizing eco-friendly materials and processes.
            Design Brief:
            Topic: Climbing accessories
            Target Audience: Intermediate boulder and sport climbers who have only ever climbed in an indoor gym and want to transition into the outdoors.
            Key Features and Requirements: The product must be a tangible item. It’s okay if it is only appropriate for only one of the two disciplines. It must be transportable in a backpack so it can be taken to the crag
            Constraints:
            Budget: £300000
            Timeframe: 3 years
            Technical and Legal Constraints: The product must be in agreement with respective safety laws and guidelines
            '''
    idea_dict = {
        "Company Name": "Scarpa",
        "Company Profile": "Scarpa, an esteemed Italian company founded in 1938, specializes in high-quality outdoor footwear. Initially focused on handcrafted shoes, it has expanded into mountaineering, skiing, rock climbing, and hiking footwear. Known for blending innovation, quality, and performance, Scarpa caters to both professional athletes and outdoor enthusiasts. The brand is globally recognized for its craftsmanship and advanced footwear technology, maintaining a strong position in the technical outdoor footwear market.",
        "Company Mission": "Scarpa's mission centers on inspiring a connection with nature through innovative and quality footwear. Emphasizing Italian craftsmanship and technological advancement, Scarpa aims to enhance outdoor performance, comfort, and safety, encouraging exploration and enjoyment of the natural world.",
        "Current Product Range": "Scarpa's product range includes mountaineering boots, ski boots, rock climbing shoes, and hiking footwear. Tailored for various expertise levels and terrains, their products range from lightweight approach shoes to advanced boots for extreme conditions. Constant innovation, athlete feedback incorporation, and a commitment to sustainability are hallmarks of their range, emphasizing eco-friendly materials and processes.",
        "Topic": "Climbing accessories",
        "Target Audience": "Intermediate boulder and sport climbers who have only ever climbed in an indoor gym and want to transition into the outdoors.",
        "Key Features and Requirements": "The product must be a tangible item. It’s okay if it is only appropriate for only one of the two disciplines. It must be transportable in a backpack so it can be taken to the crag",
        "Budget": "£300000",
        "Timeframe": "3 years",
        "Technical and Legal Constraints": "The product must be in agreement with respective safety laws and guidelines"
}

    asyncio.run(startup(idea, idea_dict, investment, n_round))


if __name__ == "__main__":
    fire.Fire(main)
 