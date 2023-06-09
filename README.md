[![PyPI version](https://img.shields.io/pypi/v/pipe21.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/pipe21/)
[![Coverage Status](https://coveralls.io/repos/github/tandav/pipe21/badge.svg?branch=coveralls-bage)](https://coveralls.io/github/tandav/pipe21?branch=coveralls-bage)

<img src="https://github.com/tandav/pipe21/assets/5549677/40544d91-475b-4c80-be55-c516810966c3" height="100">

# pipe21 - simple functional pipes [[docs]](https://tandav.github.io/pipe21)

## Basic version
just copy-paste it!

Most frequently used operators. It's often easier to copypaste than install and import.

```py
class B:
    def __init__(self, f): self.f = f
class Pipe  (B): __ror__ = lambda self, x: self.f(x)
class Map   (B): __ror__ = lambda self, x: map   (self.f, x)
class Filter(B): __ror__ = lambda self, x: filter(self.f, x)
```

or install using pip:

```py
pip install pipe21
```

## Examples

#### little docs

```py
from pipe21 import *

x | Pipe(f)   == f     (x   )
x | Map(f)    == map   (f, x)
x | Filter(f) == filter(f, x)
x | Reduce(f) == reduce(f, x)
```

---

#### simple pipes

```py
range(5) | Pipe(list) # [0, 1, 2, 3, 4]
range(5) | Map(str) | Pipe(''.join) # '01234'
range(5) | Filter(lambda x: x % 2 == 0) | Pipe(list) # [0, 2, 4]
range(5) | Reduce(lambda a, b: a + b) # 10
```

---

#### print digits

```py
range(1_000_000) | Map(chr) | Filter(str.isdigit) | Pipe(''.join)
```
Output:

```
0123456789²³¹٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹߀߁߂߃߄߅߆߇߈߉०१२३४५६७८९০১২৩৪৫৬৭৮৯੦੧੨੩੪੫੬੭੮੯૦૧૨૩૪૫૬૭૮૯୦୧୨୩୪୫୬୭୮୯௦௧௨௩௪௫௬௭௮௯౦౧౨౩౪౫౬౭౮౯೦೧೨೩೪೫೬೭೮೯൦൧൨൩൪൫൬൭൮൯෦෧෨෩෪෫෬෭෮෯๐๑๒๓๔๕๖๗๘๙໐໑໒໓໔໕໖໗໘໙༠༡༢༣༤༥༦༧༨༩၀၁၂၃၄၅၆၇၈၉႐႑႒႓႔႕႖႗႘႙፩፪፫፬፭፮፯፰፱០១២៣៤៥៦៧៨៩᠐᠑᠒᠓᠔᠕᠖᠗᠘᠙᥆᥇᥈᥉᥊᥋᥌᥍᥎᥏᧐᧑᧒᧓᧔᧕᧖᧗᧘᧙᧚᪀᪁᪂᪃᪄᪅᪆᪇᪈᪉᪐᪑᪒᪓᪔᪕᪖᪗᪘᪙᭐᭑᭒᭓᭔᭕᭖᭗᭘᭙᮰᮱᮲᮳᮴᮵᮶᮷᮸᮹᱀᱁᱂᱃᱄᱅᱆᱇᱈᱉᱐᱑᱒᱓᱔᱕᱖᱗᱘᱙⁰⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉①②③④⑤⑥⑦⑧⑨⑴⑵⑶⑷⑸⑹⑺⑻⑼⒈⒉⒊⒋⒌⒍⒎⒏⒐⓪⓵⓶⓷⓸⓹⓺⓻⓼⓽⓿❶❷❸❹❺❻❼❽❾➀➁➂➃➄➅➆➇➈➊➋➌➍➎➏➐➑➒꘠꘡꘢꘣꘤꘥꘦꘧꘨꘩꣐꣑꣒꣓꣔꣕꣖꣗꣘꣙꤀꤁꤂꤃꤄꤅꤆꤇꤈꤉꧐꧑꧒꧓꧔꧕꧖꧗꧘꧙꧰꧱꧲꧳꧴꧵꧶꧷꧸꧹꩐꩑꩒꩓꩔꩕꩖꩗꩘꩙꯰꯱꯲꯳꯴꯵꯶꯷꯸꯹０１２３４５６７８９𐒠𐒡𐒢𐒣𐒤𐒥𐒦𐒧𐒨𐒩𐩀𐩁𐩂𐩃𐴰𐴱𐴲𐴳𐴴𐴵𐴶𐴷𐴸𐴹𐹠𐹡𐹢𐹣𐹤𐹥𐹦𐹧𐹨𑁒𑁓𑁔𑁕𑁖𑁗𑁘𑁙𑁚𑁦𑁧𑁨𑁩𑁪𑁫𑁬𑁭𑁮𑁯𑃰𑃱𑃲𑃳𑃴𑃵𑃶𑃷𑃸𑃹𑄶𑄷𑄸𑄹𑄺𑄻𑄼𑄽𑄾𑄿𑇐𑇑𑇒𑇓𑇔𑇕𑇖𑇗𑇘𑇙𑋰𑋱𑋲𑋳𑋴𑋵𑋶𑋷𑋸𑋹𑑐𑑑𑑒𑑓𑑔𑑕𑑖𑑗𑑘𑑙𑓐𑓑𑓒𑓓𑓔𑓕𑓖𑓗𑓘𑓙𑙐𑙑𑙒𑙓𑙔𑙕𑙖𑙗𑙘𑙙𑛀𑛁𑛂𑛃𑛄𑛅𑛆𑛇𑛈𑛉𑜰𑜱𑜲𑜳𑜴𑜵𑜶𑜷𑜸𑜹𑣠𑣡𑣢𑣣𑣤𑣥𑣦𑣧𑣨𑣩𑱐𑱑𑱒𑱓𑱔𑱕𑱖𑱗𑱘𑱙𑵐𑵑𑵒𑵓𑵔𑵕𑵖𑵗𑵘𑵙𑶠𑶡𑶢𑶣𑶤𑶥𑶦𑶧𑶨𑶩𖩠𖩡𖩢𖩣𖩤𖩥𖩦𖩧𖩨𖩩𖭐𖭑𖭒𖭓𖭔𖭕𖭖𖭗𖭘𖭙𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿𞅀𞅁𞅂𞅃𞅄𞅅𞅆𞅇𞅈𞅉𞋰𞋱𞋲𞋳𞋴𞋵𞋶𞋷𞋸𞋹𞥐𞥑𞥒𞥓𞥔𞥕𞥖𞥗𞥘𞥙🄀🄁🄂🄃🄄🄅🄆🄇🄈🄉🄊'
```

#### chunked

```py
>>> range(5) | Chunked(2) | Pipe(list)
[(0, 1), (2, 3), (4,)]
```

---

## Extended version
```py
import pipe21 as P
```

#### FizzBuzz

```py
(
    range(1, 100)
    | P.MapSwitch([
        (lambda i: i % 3 == i % 5 == 0, lambda x: 'FizzBuzz'),
        (lambda i: i % 3 == 0, lambda x: 'Fizz'),
        (lambda i: i % 5 == 0, lambda x: 'Buzz'),
    ])
    | P.Pipe(list)
)

[1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz', 11, 'Fizz', 13, 14, 'FizzBuzz', 16, 17, 'Fizz', 19, 'Buzz', 'Fizz', 22, 23, 'Fizz', 'Buzz', 26, 'Fizz', 28, 29, 'FizzBuzz', 31, 32, 'Fizz', 34, 'Buzz', 'Fizz', 37, 38, 'Fizz', 'Buzz', 41, 'Fizz', 43, 44, 'FizzBuzz', 46, 47, 'Fizz', 49, 'Buzz', 'Fizz', 52, 53, 'Fizz', 'Buzz', 56, 'Fizz', 58, 59, 'FizzBuzz', 61, 62, 'Fizz', 64, 'Buzz', 'Fizz', 67, 68, 'Fizz', 'Buzz', 71, 'Fizz', 73, 74, 'FizzBuzz', 76, 77, 'Fizz', 79, 'Buzz', 'Fizz', 82, 83, 'Fizz', 'Buzz', 86, 'Fizz', 88, 89, 'FizzBuzz', 91, 92, 'Fizz', 94, 'Buzz', 'Fizz', 97, 98, 'Fizz']
```

---

#### play random music from youtube links in markdown files:

```py
import pathlib
import random
import itertools
import re
import operator
import webbrowser
import pipe21 as P


(
    pathlib.Path.home() / 'docs/knowledge/music'               # take a directory
    | P.MethodCaller('rglob', '*.md')                          # find all markdown files
    | P.FlatMap(lambda p: p | P.IterLines())                   # read all lines from all files and flatten into a single iterable
    | P.FlatMap(lambda l: re.findall(r'\[(.+)\]\((.+)\)', l))  # keep only lines with a markdown link
    | P.Map(operator.itemgetter(1))                            # extract a link
    | P.Pipe(list)                                             # convert iterable of links into a list
    | P.Pipe(random.choice)                                    # choose random link
    | P.Pipe(webbrowser.open)                                  # open link in browser
)
```

---

- [all available methods reference](reference.md)
- [review of similar tools / alternatives](similar-tools.md)
- written in pure python, no dependencies
