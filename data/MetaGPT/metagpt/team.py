#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/12 00:30
@Author  : alexanderwu
@File    : software_company.py
"""
from pydantic import BaseModel, Field, create_model
from typing import Dict

from metagpt.actions import BossRequirement, SynthesiseNeed
from metagpt.config import CONFIG
from metagpt.environment import Environment
from metagpt.logs import logger
from metagpt.roles import Role, FeasibilityAnalyst
from metagpt.schema import Message
from metagpt.utils.common import NoMoneyException


class Team(BaseModel):
    """
    Team: Possesses one or more roles (agents), SOP (Standard Operating Procedures), and a platform for instant messaging,
    dedicated to perform any multi-agent activity, such as collaboratively writing executable code.
    """
    environment: Environment = Field(default_factory=Environment)
    investment: float = Field(default=10.0)
    idea: str = Field(default="")

    class Config:
        arbitrary_types_allowed = True

    def hire(self, roles: list[Role]):
        """Hire roles to cooperate"""
        self.environment.add_roles(roles)

    def invest(self, investment: float):
        """Invest company. raise NoMoneyException when exceed max_budget."""
        self.investment = investment
        CONFIG.max_budget = investment
        logger.info(f'Investment: ${investment}.')

    def _check_balance(self):
        if CONFIG.total_cost > CONFIG.max_budget:
            raise NoMoneyException(CONFIG.total_cost, f'Insufficient funds: {CONFIG.max_budget}')
        

    def start_project(self, idea, idea_dict: dict = None, send_to: str = ""):

        def generate_model_from_dict(data) -> BaseModel:
            fields = {key: (type(value), ...) for key, value in data.items()}
            return create_model('DynamicModel', **fields)
        """Start a project from publishing boss requirement."""
        
        self.idea = idea
        if idea_dict == None:
            print("DID NOT GENERATE AT ALL")
            self.environment.publish_message(Message(role="Human", content=idea, cause_by=BossRequirement, send_to=send_to))
        else:
            print("GENERATED DICT")
            DynamicModel = generate_model_from_dict(data=idea_dict)
            self.environment.publish_message(Message(role="Human", content=idea, instruct_content = DynamicModel(**idea_dict), cause_by=BossRequirement, send_to=send_to))
        ### TEST REMOVE WHEN DONE
        #self.environment.publish_message(Message(role="Design Manager", content = """[Human: Company Description: A fourth year student at Glasgow University studying Product Design. Have access to various workshops throughout the university, such as metalworks, woodworks, etc...Topic: Ideas for a product I can manually make 10 of for a final year project Budget: 100 pounds Timeframe: 3 months,"Solution Engineer": { "Project name": "music_project", "Solutions": [{"Product name": "MelodyMatch", "Description": "MelodyMatch is an AI-powered music recommendation platform that provides personalized recommendations based on individual preferences and needs. It analyzes users' listening habits, favorite genres, and artists to curate a tailored list of music suggestions. MelodyMatch also takes into account users' moods, activities, and specific requirements, such as budget constraints and the need for affordable solutions. With MelodyMatch, users can discover new and innovative music-related products that align with their specific requirements."},{"Product name": "TuneTrove","Description": "TuneTrove is a music discovery app that offers personalized recommendations based on individual preferences and needs. It utilizes advanced algorithms to analyze users' music libraries, favorite songs, and artists to generate a curated list of music suggestions. TuneTrove also takes into consideration users' budget constraints and the need for affordable solutions. With TuneTrove, users can explore new and innovative music-related products that cater to their specific requirements."},{"Product name": "HarmonyHub","Description": "HarmonyHub is a smart music recommendation system that provides personalized suggestions based on individual preferences and needs. It incorporates machine learning algorithms to analyze users' listening patterns, favorite genres, and artists to generate a customized list of music recommendations. HarmonyHub also considers users' budget limitations and the need for affordable solutions. With HarmonyHub, users can easily discover new and innovative music-related products that match their specific requirements."},{"Product name": "RhythmRecommender","Description": "RhythmRecommender is an intelligent music recommendation platform that offers personalized suggestions based on individual preferences and needs. It employs advanced algorithms to analyze users' music preferences, favorite songs, and artists to curate a tailored list of music recommendations. RhythmRecommender also takes into account users' budget constraints and the need for affordable solutions. With RhythmRecommender, users can explore new and innovative music-related products that align with their specific requirements."},{"Product name": "MusicMate","Description": "MusicMate is a comprehensive music recommendation app that provides personalized suggestions based on individual preferences and needs. It utilizes artificial intelligence to analyze users' music listening habits, favorite genres, and artists to generate a curated list of music recommendations. MusicMate also considers users' budget limitations and the need for affordable solutions. With MusicMate, users can easily discover new and innovative music-related products that cater to their specific requirements."}]}]""", cause_by = BossRequirement, send_to = FeasibilityAnalyst))
        
    def _save(self):
        logger.info(self.json())

    async def run(self, n_round=3):
        """Run company until target round or no money"""
        while n_round > 0:
            # self._save()
            n_round -= 1
            logger.debug(f"{n_round=}")
            self._check_balance()
            await self.environment.run()
        return self.environment.history
    