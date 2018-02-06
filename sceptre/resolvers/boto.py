# -*- coding: utf-8 -*-

from sceptre.resolvers import Resolver


class BotoResponseVariable(Resolver):
    """
    Resolver for shell environment variables.

    :param argument: Name of the environment variable to return.
    :type argument: str
    """
    def resolve(self):
        """
        Retrieves the value of a named environment variable.

        :returns: Value of the environment variable.
        :rtype: str
        """
        result_filter = []

        service, cmd = self.argument.split("::",2)

        if "::" in cmd:
            cmd, result_filter = cmd.split("::",1)
            result_filters = result_filter.split(".")

        client = self.stack.connection_manager.client(service)
        result = service.__getattribute__(cmd)

        for result_filter in result_filters:
            result.__getitem__(result_filter)

        return result
