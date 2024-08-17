from modules import shared

class Config:
    @property
    def anthropic_api_key(self):
        return shared.opts.anthropic_api_key

    @property
    def anthropic_model(self):
        return shared.opts.anthropic_model

    @property
    def opt_temperature(self):
        return shared.opts.opt_temperature

    @property
    def max_retry(self):
        return shared.opts.max_retry

    @property
    def output_lang(self):
        return shared.opts.output_lang

    @property
    def save_request_log(self):
        return shared.opts.save_request_log

    @property
    def save_response_log(self):
        return shared.opts.save_response_log

config = Config()