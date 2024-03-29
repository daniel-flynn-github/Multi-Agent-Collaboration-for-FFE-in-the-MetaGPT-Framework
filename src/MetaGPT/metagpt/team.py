#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/12 00:30
@Author  : alexanderwu
@File    : software_company.py
"""
from pydantic import BaseModel, Field, create_model
from typing import Dict

from metagpt.actions import BossRequirement
from metagpt.config import CONFIG
from metagpt.environment import Environment
from metagpt.logs import logger
from metagpt.roles import Role
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

    def human_ideas(self, human_idea: bool):
        CONFIG.human_ideas = human_idea
        logger.info(f'Human Ideas: ${human_idea}.')

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
    