class FormMixin(object):
    """
    处理表单错误
    """

    def get_errors(self):
        if hasattr(self, 'error'):
            errors = self.errors.get_json_data()
            new_errors = {}
            for key, msg_dics in errors.items():
                message = []
                for msg in msg_dics:
                    message.append(msg['message'])
                new_errors[key] = message
            return new_errors
        else:
            return {}
