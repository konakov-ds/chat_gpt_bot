import logging
import os

import openai
import yaml
from aiogram import Bot, Dispatcher, executor, types

# import config
with open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# set api keys
openai.api_key = config['tokens']['open_ai']
tg_token = config['tokens']['telegram']

# configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=tg_token)
dp = Dispatcher(bot)


# get answer from open ai
@dp.message_handler()
async def echo(message: types.Message):
    response = openai.Completion.create(
        model=config['openai']['model'],
        prompt=message.text,
        temperature=config['openai']['temperature'],
        max_tokens=config['openai']['max_tokens'],
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.5
    )
    await message.answer(response['choices'][0]['text'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

