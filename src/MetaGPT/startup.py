#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio

import fire

from metagpt.roles import (
    UserResearcher,
    NeedsAnalyst,
    Innovator,
    Evaluator,
    Demonstrator,
)
from metagpt.team import Team


async def startup(
    idea: str,
    idea_dict: dict = None,
    investment: float = 0.01,
    n_round: int = 2,
    human_ideas: bool = False,
):
    """Run a startup. Be a boss."""
    company = Team()
    company.human_ideas(human_ideas)
    company.hire(
        [
            UserResearcher(),
            NeedsAnalyst(),
            Innovator(),
            Evaluator(),
            Demonstrator(),
        ]
    )

    company.invest(investment)
    company.start_project(idea, idea_dict)
    await company.run(n_round=n_round)


def main(
    idea: str = "",
    investment: float = 1.5,
    n_round: int = 8,
    idea_evaluator: bool = False,
    example_scenario: bool = False,
):
    

    def console_idea_input():
        human_ideas = []
        print("Enter 'done' to end the input")
        i = 0
        while True:
            i += 1
            idea_name = input(f"Enter Idea {i} Name: ")
            if idea_name == "done":
                 break
            idea_description = input(f"Enter Idea {i} Description: ")
            if idea_description == "done":
                 break
            human_ideas.append((idea_name, idea_description))
        return human_ideas

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
        product = mandatory_input("    Original Product: ")
        audience = input("    Target Audience: ")
        suggested = input("    Suggested Features: ")
        requirements = input("    Requirements: ")
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
            "    Product: " + product + "\n"
            "    Target Audience: " + audience + "\n"
            "    Suggested Features: " + suggested + "\n"
            "    Requirements: " + requirements + "\n"
            "Constraints: \n"
            "    Budget: " + budget + "\n"
            "    Timeframe: " + timeframe + "\n"
            "    Technical and Legal Constraints: " + constraints),
                ({
                    "Company Name": company_name,
                    "Company Profile": company_profile,
                    "Company Mission": company_mission,
                    "Current Product Range": product_range,
                    "Product": product,
                    "Target Audience": audience,
                    "Suggested Features": suggested,
                    "Requirements": requirements,
                    "Budget": budget,
                    "Timeframe": timeframe,
                    "Technical and Legal Constraints": constraints
                })
        )
    

    idea = '''Background Information:
            Company Name: Scarpa
            Company Profile: Scarpa, an esteemed Italian company founded in 1938, specializes in high-quality outdoor footwear. Initially focused on handcrafted shoes, it has expanded into mountaineering, skiing, rock climbing, and hiking footwear. Known for blending innovation, quality, and performance, Scarpa caters to both professional athletes and outdoor enthusiasts. The brand is globally recognized for its craftsmanship and advanced footwear technology, maintaining a strong position in the technical outdoor footwear market.
            Company Mission: Scarpa's mission centers on inspiring a connection with nature through innovative and quality footwear. Emphasizing Italian craftsmanship and technological advancement, Scarpa aims to enhance outdoor performance, comfort, and safety, encouraging exploration and enjoyment of the natural world.
            Current Product Range: Scarpa's product range includes mountaineering boots, ski boots, rock climbing shoes, and hiking footwear. Tailored for various expertise levels and terrains, their products range from lightweight approach shoes to advanced boots for extreme conditions. Constant innovation, athlete feedback incorporation, and a commitment to sustainability are hallmarks of their range, emphasizing eco-friendly materials and processes.
            Design Brief:
            Product: ""Walking backpack""
            Target Audience: New walkers who are still getting to grips with the outdoors.
            Suggested Features: Lightweight
            Requirements: Reasonably affordable
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
        "Product": "Walking backpack",
        "Target Audience": "New walkers who are still getting to grips with the outdoors.",
        "Suggested Features": "Lightweight.",
        "Requirements": "Reasonably affordable",
        "Budget": "£300000",
        "Timeframe": "3 years",
        "Technical and Legal Constraints": "The product must be in agreement with respective safety laws and guidelines"
    }
    if idea_evaluator == True:
        human_ideas_list = console_idea_input()
        idea = ""
        idea_dict = {}
        for i in range(len(human_ideas_list)):
            idea += f"Idea {i+1} Name: {human_ideas_list[i][0]}\nIdea {i+1} Description: {human_ideas_list[i][1]}\n"
            idea_dict[f"Idea {i+1}"] = "Name: " + human_ideas_list[i][0] + "\nDescription: " + human_ideas_list[i][1]
    
    elif example_scenario == False:
        idea,idea_dict  = console_input()
    elif example_scenario == False and idea_evaluator == False:
        print("EXAMPLE SCENARIO:\n\n" + idea)

    asyncio.run(startup(idea, idea_dict, investment, n_round, idea_evaluator))


if __name__ == "__main__":
    fire.Fire(main)
 