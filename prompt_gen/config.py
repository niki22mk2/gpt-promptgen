from modules import shared

class Config:
    @property
    def anthropic_api_key(self):
        return shared.opts.anthropic_api_key

    @property
    def openai_api_key(self):
        return shared.opts.openai_api_key

    @property
    def openrouter_api_key(self):
        return shared.opts.openrouter_api_key

    @property
    def deepseek_api_key(self):
        return shared.opts.deepseek_api_key

    @property
    def google_api_key(self):
        return shared.opts.google_api_key

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
    def anthropic_cache_enabled(self):
        return shared.opts.anthropic_cache_enabled

config = Config()