from pyparsing import *

# --- Define Grammars for the parser (pyparsing)
integer       = Word(nums)            ### '0123456789'
StrangeName   = Word(printables)      ### '0123456789abc...wxyzABC...WXYZ!"#$%&\\' ()*+,-./:;<=>?@[\\]^_`{|}~'
integer       = Word(nums)            ### '0123456789'
number        = Word(alphanums)       ### 'abc...wyzABC...WXYZ0123456789'
decimalNumber = Combine((Optional(Literal("-"))+Optional(integer)+Optional(Literal("."))+integer))
name          = Word(alphas)          ### 'abc...wxyzABC...WXYZ'


endLine       = Literal("\n")
end           = Literal("\n").suppress()  # go to the end of the line, and suppress it, same as EOL?
EOL           = LineEnd().suppress()      # go to the end of the line, and suppress it, same as end?
all           = SkipTo(end)               # go to the end of the line, match the next line
ligneParLigne = ZeroOrMore(SkipTo('\n').setResultsName("ligne")).setResultsName("lignes")

