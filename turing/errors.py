"""Errors of this turing machine"""

class JSONDecodeError(ValueError):
    """Error on decode json, unexpected format"""

class UnexpectedState(ValueError):
    """Unexpected state, state out of states"""

class UnexpectedDirection(ValueError):
    """Unexpected direction, instruction with some direction error"""

class UnexpectedType(ValueError):
    """Unexpected type in configuration of machine"""
