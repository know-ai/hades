# -*- coding: utf-8 -*-
"""pyhades/utils/other.py

This module implements other Use Utility Functions.
"""
import os
import re
import yaml
import logging
import requests
import functools
from ._errors import RequestDecorationError


def get_headers(auth_service_host:str="127.0.0.1", auth_service_port:int=5000, auth_endpoint:str='/api/healthcheck/key'):
    r"""
    Documentation here
    """
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-API-KEY": None
    } 
    try:
        url = f"http://{auth_service_host}:{auth_service_port}{auth_endpoint}"
        response = requests.get(url)
        if response and response.status_code==200:
            
            response = response.json()
            key = response['message']
            headers["X-API-KEY"] = key
        
        return headers
    
    except requests.ConnectionError as ex:

        trace = []
        tb = ex.__traceback__
        while tb is not None:
            trace.append({
                "filename": tb.tb_frame.f_code.co_filename,
                "name": tb.tb_frame.f_code.co_name,
                "lineno": tb.tb_lineno
            })
            tb = tb.tb_next
        msg = str({
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        })
        logging.warning(msg=msg)

        return headers

def decorator(declared_decorator):
    """
    Create a decorator out of a function, which will be used as a wrapper
    """

    @functools.wraps(declared_decorator)
    def final_decorator(func=None, **kwargs):
        # This will be exposed to the rest of your application as a decorator
        def decorated(func):
            # This will be exposed to the rest of your application as a decorated
            # function, regardless how it was called
            @functools.wraps(func)
            def wrapper(*a, **kw):
                # This is used when actually executing the function that was decorated

                return declared_decorator(func, a, kw, **kwargs)
            
            return wrapper
        
        if func is None:
            
            return decorated
        
        else:
            # The decorator was called without arguments, so the function should be
            # decorated immediately
            return decorated(func)

    return final_decorator

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def parse_config(config_file, tag='!ENV'):
    """
    Load a yaml configuration file and resolve any environment variables
    The environment variables must have !ENV before them and be in this format
    to be parsed: ${VAR_NAME}.
    E.g.:

    database:
        host: !ENV ${HOST}
        port: !ENV ${PORT}
    app:
        log_path: !ENV '/var/${LOG_PATH}'
        something_else: !ENV '${AWESOME_ENV_VAR}/var/${A_SECOND_AWESOME_VAR}'

    :param str path: the path to the yaml file
    :param str data: the yaml data itself as a stream
    :param str tag: the tag to look for
    :return: the dict configuration
    :rtype: dict[str, T]
    """
    # pattern for global vars: look for ${word}
    pattern = re.compile('.*?\${(\w+)}.*?')
    loader = yaml.SafeLoader

    # the tag will be used to mark where to start searching for the pattern
    # e.g. somekey: !ENV somestring${MYENVVAR}blah blah blah
    loader.add_implicit_resolver(tag, pattern, None)

    def constructor_env_variables(loader, node):
        """
        Extracts the environment variable from the node's value
        :param yaml.Loader loader: the yaml loader
        :param node: the current node in the yaml
        :return: the parsed string that contains the value of the environment
        variable
        """
        value = loader.construct_scalar(node)
        match = pattern.findall(value)  # to find all env variables in line
        if match:
            full_value = value
            for g in match:
                full_value = full_value.replace(
                    f'${{{g}}}', os.environ.get(g, g)
                )
            return full_value
        return value

    loader.add_constructor(tag, constructor_env_variables)

    with open(config_file) as f:
                
            return yaml.load(f, Loader=loader)

def env_var_not_defined(target):
    r"""
    Documentation here
    """
    regexStr = r"(?<={)[^}]*(?=})"
    mo = re.search(regexStr,target)
    if not mo:
        return False
    else:
        
        return True

def check_key_in_dict(_dict, key):
    r"""
    Documentation here
    """
    if key in _dict.keys():

        value = _dict[key]

        if env_var_not_defined(value):

            return False

        return True
    
    return False

@decorator
def notify_state(func, args, kwargs):
    """

    :param args:
    :return:
    """
    result = func(*args, **kwargs)
    state_machine = args[0]
    current_transition = func.__name__.replace('on_','')
    current_destination = current_transition.split('_to_')[-1]
    active_transitions = state_machine._get_active_transitions()

    for transition in active_transitions:

        if transition.identifier==current_transition:
            
            for destination in transition.destinations:
                
                if destination.name==current_destination:

                    engine_state = destination.value
                    info = state_machine.serialize()
                    info["state"] = engine_state
                    
                    if state_machine.sio: 
                        
                        state_machine.sio.emit(state_machine.event_name, info)

    return result


@decorator
def request_redirected(func, args, kwargs):
    """

    :param args:
    :return:
    """
    try:
        response = func(*args, **kwargs)

        if isinstance(response, requests.models.Response):
    
            status_code = response.status_code

            if status_code==requests.codes.ok:

                return response.json(), status_code

            return None, status_code

        else:

            raise RequestDecorationError(f"Func: {func.__name__} not return a {requests.models.Response} response")

    except requests.ConnectionError as err:

        return {'message': str(err)}, requests.codes.timeout
    


def system_log_transition(
    log:bool=False,
    event_service_host:str="127.0.0.1",
    event_service_port:int=5000, 
    event_endpoint:str='/api/healthcheck/key',
    auth_service_host:str="127.0.0.1",
    auth_service_port:int=5004, 
    auth_endpoint:str='/api/events/add'
    ):
    
    @decorator
    def _system_log_transition(func, args, kwargs):
        r"""

        :param args:
        :return:
        """
        result = func(*args, **kwargs)
        event_url = f"http://{event_service_host}:{event_service_port}{event_endpoint}"

        if log:
            
            state_machine = args[0]
            current_transition = func.__name__.replace('on_','')
            current_destination = current_transition.split('_to_')[-1]
            active_transitions = state_machine._get_active_transitions()

            for transition in active_transitions:

                if transition.identifier==current_transition:
                    
                    for destination in transition.destinations:
                        
                        if destination.name==current_destination:
                            _current_transition = current_transition.replace("_", " ")
                            engine_state = destination.value
                            info = state_machine.serialize()
                            info["state"] = engine_state
                            payload = {
                                'user': "SYS.KnowAI",
                                'message': f"{info['name']} was switched from {_current_transition}",
                                'description': info['description'],
                                'classification': info['classification'],
                                'priority': info['priority'],
                                'criticity': info['criticity']
                            }
                            try:
                                requests.post(
                                    event_url, 
                                    headers=get_headers(auth_service_host, auth_service_port, auth_endpoint), 
                                    json=payload
                                    )
                            except requests.ConnectionError as ex:
                                trace = []
                                tb = ex.__traceback__
                                while tb is not None:
                                    trace.append({
                                        "filename": tb.tb_frame.f_code.co_filename,
                                        "name": tb.tb_frame.f_code.co_name,
                                        "lineno": tb.tb_lineno
                                    })
                                    tb = tb.tb_next
                                msg = str({
                                    'type': type(ex).__name__,
                                    'message': str(ex),
                                    'trace': trace
                                })
                                logging.warning(msg=msg)

        return result

    return _system_log_transition

@decorator
def logging_error_handler(func, args, kwargs):
    r"""
    Documentation here
    """
    try:
                
        result = func(*args, **kwargs)
        return result

    except Exception as ex:

        trace = []
        tb = ex.__traceback__
        while tb is not None:
            trace.append({
                "filename": tb.tb_frame.f_code.co_filename,
                "name": tb.tb_frame.f_code.co_name,
                "lineno": tb.tb_lineno
            })
            tb = tb.tb_next
        msg = str({
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        })
        logging.error(msg=msg)
