from typing import Literal

default_reactions = ("like", "dislike")

UserReactions = Literal[*default_reactions, "all", "love"]
ReactionsGetParams = Literal[*default_reactions, "all"]
ReactionsSetParams = Literal[*default_reactions, "love"]