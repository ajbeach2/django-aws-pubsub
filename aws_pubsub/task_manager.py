"""Task Management for aws_pubsub."""
from .exceptions import TaskNotFound, InvalidTaskRegistry, InvalidTaskFunciontDefinition


class TaskManager(object):
    """Class that collects tasks from installed django apps."""

    def __init__(self):
        """Initialize a Task Manager."""
        self._registry = {}

    def _register(self, task, alias=None):

        keys = ["%s.%s" % (task.__module__, task.__name__)]
        if alias:
            keys.append(alias)

        for key in keys:
            if key in self._registry:
                raise InvalidTaskRegistry("%s task already exists!" % key)

            if (
                len(task.__annotations__) != 1
                or task.__annotations__.get("message", object).__name__ != "dict"
            ):
                raise InvalidTaskFunciontDefinition(
                    "%s Task signature must match: def mytask(message: dict)" % (key)
                )

            else:
                self._registry[key] = task

    def _get_task(self, func):
        task = self._registry.get(func, None)
        if not task:
            raise TaskNotFound("Task %s does not exist!" % func)
        return task


manager = TaskManager()


def register(f, alias=None):
    """Register a task to the manager.

    Args:
        f (function): Task function object
        alias (str): Global alias for task    """

    manager._register(f, alias)


def get_task(f):
    """Return a Task from the task manager."""
    return manager._get_task(f)
