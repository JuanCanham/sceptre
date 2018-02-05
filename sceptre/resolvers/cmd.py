# -*- coding: utf-8 -*-

import subprocess

from sceptre.resolvers import Resolver


class CmdOutputVariable(Resolver):
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
        result = subprocess.check_output(self.argument ,shell=True)
        result = result.replace("\n","")
        return result
