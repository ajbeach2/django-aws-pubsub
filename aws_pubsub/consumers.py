"""Consumers of Messages."""

import logging
import multiprocessing

from django import db

from aws_pubsub.backends import ack_messages, get_messages
from aws_pubsub.dispatcher import dispatch

logger = logging.getLogger("default")


class MultiProcessConsumer(multiprocessing.Process):
    def __init__(self, _id: int, max_tasks_per_child=10000) -> None:
        """Construct a new Process based consumer.

        Args:
            _id (int): Identifier for this processor
            max_tasks_per_child (int): Max number of tasks
            before the process exits

        """
        multiprocessing.Process.__init__(self)
        self.id = _id
        self.max_tasks_per_child = max_tasks_per_child

    def run(self):
        """Starts the process"""
        db.connections.close_all()
        logger.error("Starting Worker %s" % self.id)
        try:
            x = 0
            while x < self.max_tasks_per_child:
                messages = get_messages()
                if messages:
                    recipt_handles, _ = dispatch(messages)
                    ack_messages(recipt_handles)
                db.reset_queries()
                x += 1

            logger.error("Max tasks reached. Process %s will be replaced" % self.id)
            return
        except (KeyboardInterrupt, SystemExit):
            logger.warning("Consumer %s shutting down...", self.id)


class Consumer(object):
    def run(cls):
        """Starts the process"""

        messages = get_messages()
        if messages:
            recipt_handles, _ = dispatch(messages)
            ack_messages(recipt_handles)

        return recipt_handles
