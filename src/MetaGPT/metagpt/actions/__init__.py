#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 17:44
@Author  : alexanderwu
@File    : __init__.py
"""
from enum import Enum

from metagpt.actions.action import Action
from metagpt.actions.action_output import ActionOutput
from metagpt.actions.add_requirement import BossRequirement
from metagpt.actions.create_personas import CreatePersonas
from metagpt.actions.create_pain_points import CreatePainPoints
from metagpt.actions.ideas import CreateIdeas
from metagpt.actions.create_journey_maps import CreateJourneyMaps
from metagpt.actions.summarise import Summarise
from metagpt.actions.evaluate_technical_value import EvaluateTechnicalValue
from metagpt.actions.evaluate_financial_value import EvaluateFinancialValue
from metagpt.actions.evaluate_customer_value import EvaluateCustomerValue
from metagpt.actions.evaluate_social_value import EvaluateSocialValue
from metagpt.actions.evaluate_market_value import EvaluateMarketValue
from metagpt.actions.create_design_principles import CreateDesignPrinciples



class ActionType(Enum):
    """All types of Actions, used for indexing."""

    ADD_REQUIREMENT = BossRequirement
    CREATE_PERSONAS = CreatePersonas
    CREATE_PAIN_POINTS = CreatePainPoints
    CREATE_IDEAS = CreateIdeas
    CREATE_JOURNEY_MAPS = CreateJourneyMaps
    SUMMARISE = Summarise
    EVALUATE_TECHNICAL_VALUE = EvaluateTechnicalValue
    EVALUATE_FINANCIAL_VALUE = EvaluateFinancialValue
    EVALUATE_CUSTOMER_VALUE = EvaluateCustomerValue
    EVALUATE_SOCIAL_VALUE = EvaluateSocialValue
    EVALUATE_MARKET_VALUE = EvaluateMarketValue
    CREATE_DESIGN_PRINCIPLES = CreateDesignPrinciples


__all__ = [
    "ActionType",
    "Action",
    "ActionOutput",
]
