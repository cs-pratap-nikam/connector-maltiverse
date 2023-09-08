""" Copyright start
  Copyright (C) 2008 - 2023 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """
from connectors.core.connector import Connector, get_logger, ConnectorError
from .operations import _check_health, operations
from django.conf import settings 
from integrations.crudhub import make_request
logger = get_logger('maltiverse')

MACRO_LIST = ["IP_Enrichment_Playbooks_IRIs", 
              "URL_Enrichment_Playbooks_IRIs", 
              "Domain_Enrichment_Playbooks_IRIs", 
              "FileHash_Enrichment_Playbooks_IRIs"]

class MaltiverseConn(Connector):
    def execute(self, config, operation, params, **kwargs):
        try:
            action = operations.get(operation)
            result = action(config, params)
            return result
        except Exception as err:
            logger.error(str(err))
            raise ConnectorError(str(err))

    def check_health(self, config):
        return _check_health(config)
    
    def del_micro(self, config): 
        if not settings.LW_AGENT: 
            for macro in MACRO_LIST: 
                try: 
                    resp = make_request(f'/api/wf/api/dynamic-variable/?name={macro}', 'GET') 
                    if resp['hydra:member']: 
                        logger.info("resetting global variable '%s'" % macro) 
                        macro_id = resp['hydra:member'][0]['id'] 
                        resp = make_request(f'/api/wf/api/dynamic-variable/{macro_id}/?format=json', 'DELETE') 
                except Exception as e: 
                    logger.error(e) 
 
    def on_deactivate(self, config): 
        self.del_micro(config) 
    
    def on_activate(self, config): 
        self.del_micro(config) 
    
    def on_add_config(self, config, active): 
        self.del_micro(config) 
    
    def on_delete_config(self, config): 
        self.del_micro(config) 