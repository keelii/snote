# -*- coding: utf-8 -*-
from development import DevelopmentConfig
from production import ProductionConfig
from testing import TestingConfig

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}