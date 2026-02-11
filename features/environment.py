"""Behave hooks — setup / teardown lifecycle."""

from core.api_client import APIClient
from utils.logger import setup_logging


def before_all(context):
    setup_logging()
    context.client = APIClient()


def after_all(context):
    APIClient.reset()


def before_scenario(context, scenario):
    context.response = None
    context.validator = None
