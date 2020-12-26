from nonebot import on_command
from nonebot.plugin import get_loaded_plugins
from nonebot.permission import GROUP
from nonebot.typing import Bot, Event
from omega_miya.utils.Omega_plugin_utils import has_command_permission

"""
# Custom plugin usage text
__plugin_name__ = '帮助'
__plugin_usage__ = r'''【帮助】

一个简单的帮助插件'''

# Init plugin export
init_export(export(), __plugin_name__, __plugin_usage__)
"""

# 注册事件响应器
bot_help = on_command('help', rule=has_command_permission(), aliases={'帮助'}, permission=GROUP, priority=1, block=True)


@bot_help.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    # 获取设置了名称的插件列表
    plugins = list(filter(lambda p: set(p.export.keys()).issuperset({'custom_name', 'usage'}), get_loaded_plugins()))
    if not plugins:
        await bot_help.finish('暂时没有可用的插件QAQ')
    state['plugin_list'] = plugins
    # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    args = str(event.plain_text).strip().lower().split()
    if args:
        # 如果用户发送了参数则直接赋值
        state['plugin_name'] = args[0]
    else:
        # 如果用户没有发送参数, 则发送功能列表并结束此命令
        plugins_list = '\n'.join(p.export.custom_name for p in plugins)
        await bot_help.finish(f'我现在支持的插件有: \n\n{plugins_list}\n\n输入"/help [插件]"即可查看对应帮助')


@bot_help.got('plugin_name', prompt='你想查询哪个插件的用法呢？')
async def handle_plugin_name(bot: Bot, event: Event, state: dict):
    plugin_custom_name = state["plugin_name"]
    # 如果发了参数则发送相应命令的使用帮助
    for p in state['plugin_list']:
        if p.export.custom_name.lower() == plugin_custom_name:
            await bot_help.finish(p.export.usage)
    await bot_help.finish('没有这个插件呢QAQ, 请检查输入插件名是否正确~')
