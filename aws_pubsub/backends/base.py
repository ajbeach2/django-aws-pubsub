import json


class BackendWrapperBase(object):
    def prepare_messages(self, messages, task_name, delay=None):
        entries = []
        for _id, message in enumerate(messages):
            message["Type"] = task_name

            msg = {"Id": "{}".format(_id), "MessageBody": json.dumps(message)}

            if delay:
                msg["DelaySeconds"] = delay

            entries.append(msg)
        return entries

    def enqueue(self, messages, task, delay=None):
        self.send_task(messages, "%s.%s" % (task.__module__, task.__name__), delay)
