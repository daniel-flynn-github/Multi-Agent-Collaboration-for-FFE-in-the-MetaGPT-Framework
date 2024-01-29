#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 14:43
@Author  : alexanderwu
@File    : __init__.py
"""

from metagpt.roles.role import Role
from metagpt.roles.architect import Architect
from metagpt.roles.project_manager import ProjectManager
from metagpt.roles.product_manager import ProductManager
from metagpt.roles.engineer import Engineer
from metagpt.roles.qa_engineer import QaEngineer
from metagpt.roles.seacher import Searcher
from metagpt.roles.sales import Sales
from metagpt.roles.customer_service import CustomerService
from metagpt.roles.user_researcher import UserResearcher
from metagpt.roles.needs_analyst import NeedsAnalyst
from metagpt.roles.design_manager import DesignManager
from metagpt.roles.innovator import Innovator
from metagpt.roles.solution_engineer import SolutionEngineer
from metagpt.roles.feasability_analyst import FeasibilityAnalyst
from metagpt.roles.market_analyst import MarketAnalyst
from metagpt.roles.experience_analyst import ExperienceAnalyst


__all__ = [
    "Role",
    "Architect",
    "ProjectManager",
    "ProductManager",
    "Engineer",
    "QaEngineer",
    "Searcher",
    "Sales",
    "CustomerService",
    "Test1Role",
    "Test2Role",
    "UserResearcher",
    "NeedsAnalyst",
    "DesignManager",
    "Innovator",
    "SolutionEngineer",
    "FeasibilityAnalyst",
    "MarketAnalyst",
    "ExperienceAnalyst",
]
