import time
import inspect
import pkgutil

from ab.utils.exceptions import AlgorithmException
from ab.utils.prometheus import func_metrics
from ab.utils.python_util import arguments

api_hub = {}


class ApiClass:
    """
    stateless class for algorithm abstraction
    """

    @classmethod
    def get_instance(cls, name: str, engine: str = 'python'):
        try:
            return api_hub[(name, engine)]
        except KeyError as e:
            raise AlgorithmException(5000, name) from e

    @staticmethod
    def process_signature(func):
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        defaults_map = {key: value.default for key, value in sig.parameters.items() if value.default != sig.empty}
        return sig, params, defaults_map

    def __init__(self, name, engine, func, **kwargs):
        self.name = name
        self.engine = engine
        self.main = func
        self.decorate_params, _ = arguments()
        self.sig, self.params, self.defaults_map = ApiClass.process_signature(func)

    def __str__(self):
        return '{self.name}{self.sig}'.format(self=self)

    def __repr__(self):
        return str(self)

    def run(self, kwargs):
        # args priority: args > defaults
        main_args = []
        for param in self.params:
            if param in kwargs:
                main_args.append(kwargs[param])
            elif param in self.defaults_map:
                main_args.append(self.defaults_map[param])
            else:
                raise AlgorithmException(5001, '{param}'.format(param=param))

        tic = time.time()
        ret = self.main(*main_args)
        toc = time.time()
        from ab.utils import logger
        logger.debug('{self.name}.main run time:'.format(self=self), toc - tic)
        return ret


def api(name=None, engine='python', **kwargs):
    """
    register func as algorithm entry
    same as Java Spring @Service
    :param name: name of the algorithm. use func.__name__ if name is None
    :param engine: the engine that algorithm runs on
    """
    assert engine in ['python', 'spark']

    def register_func(func):
        register_api(name, engine, func, **kwargs)

        return func

    return register_func


def register_api(name: str, engine: str, func, **kwargs):
    name = name or func.__name__
    # wrap algorithm entry
    func = (func_metrics('algorithm_' + name))(func)
    # TODO check duplication
    api_hub[(name, engine)] = ApiClass(name, engine, func, **kwargs)


def retrieve_api_params(name, engine="python"):
    if (name, engine) in api_hub:
        algo_object = api_hub.get((name, engine))

        return algo_object.decorate_params
    else:
        return {}


def register_all_apis(config):
    """
    auto-import all modules under algorithms for registry
    """
    alg_dir = config.get('ALGORITHM_DIR', 'api')
    for _, modname, _ in pkgutil.iter_modules([alg_dir, ]):
        __import__('{alg_dir}.{modname}'.format(alg_dir=alg_dir.replace("/", "."), modname=modname))
    # fixme:
    # __import__("ab.utils.inner_algorithm")
    from ab.utils import logger
    logger.debug('algorithms:', api_hub)
