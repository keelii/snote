# -*- coding: utf-8 -*-
from development import Config as DevelopmentConfig
from testing import Config as TestingConfig
try:
    from production import Config as ProductionConfig
except (RuntimeError, NameError, ImportError):
    print 'Production config not found, please run install shell'
finally:
    ProductionConfig = None

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}