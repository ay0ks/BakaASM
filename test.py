from bakaasm import *

import bakamath

snippet = BakaASM(autoimport=True)

bakamath.openlib(snippet)

(snippet
  .use("libreq -> lq")
  .let("url", "https://discord.com/api/v9/guilds/%lu/messages")
  .let("guild_id", 646393082430095383)
  .let("res", Func("lq:get", (), (Func("url:fmt!", (), (Var("guild_id"),)),)),)
)

print(snippet.build())