#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 14:43
@Author  : alexanderwu
@File    : __init__.py
"""

from metagpt.roles.role import Role
from metagpt.roles.user_researcher import UserResearcher
from metagpt.roles.analyst import Analyst
from metagpt.roles.innovator import Innovator
from metagpt.roles.evaluator import Evaluator
from metagpt.roles.demonstator import Demonstrator


__all__ = [
    "Role",
    "UserResearcher",
    "Analyst",
    "Innovator",
    "Evaluator",
    "Demonstrator",
]
