from environ import Env

env = Env()
env.read_env()

OPENAI_API_KEY = env.str("OPENAI_API_KEY")