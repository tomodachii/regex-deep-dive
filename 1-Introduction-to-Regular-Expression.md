# Introduction to regular expression
## egrep
- command-line utility for pattern matching and is commonly used to search for specific patterns or regular expressions within files or streams of text
- will search through lines of text rather than individual words

## Start end end of the line
carret (^) and dollar ($) sign

> '^cat' matches if you have the beginning of a line, followed immediately by c, followed immediately by a, followed immediately by t

> '^cat$' matches if the line has a beginning-of-line (which, of course, all lines have), followed immediately by cat, and then followed immediately by the end of the line.

> '^$' matches if the line has a beginning-of-line, followed immediately by the end of the line Effectively means: an empty line (with nothing in it, not even spaces).

The caret and dollar are special in that they match a position in the line rather than any actual text characters themselves

## Character classes
### Matching any one of several characters
regular expression construct '[]', usually called a character class let you list the characters you want to allow at that point in the match

Let’s say you want to search for "grey" but also want to find it if it were spelled "gray"
the regular expression:
```
gr[ea]y
```
> While '[e]' matches just an e, and '[a]' matches just an a, the regular expression '[ea]' matches
either

> this means to find g, followed by r, followed by either an e or an a, all followed by y

[!] Notice how outside of a class, literal characters (like the 'g' and 'r' of 'gr[ae]y' ) have an implied ```and then``` between them - match 'g' and then match 'r' ... 
It's completely opposite inside a character class. The contents of a class is a list of characters that can match at that point, so the implication is ```or```.

### Range of characters
Within a character class, the character-class metacharacter '-' (dash) indicates a range of characters
> '<H[1-6]>' matches \<H1\>, \<H2\>, etc -> useful when searching for HTML headers
Multiple ranges are fine

> '[0123456789abcdefABCDEF]' can be written as '[0-9a-fA-F]' or '[A-Fa-f0-9] since the order in which
ranges are given doesn't matter'

You can freely combine ranges with literal characters

> '[0-9A-ZR!.?]' matches a digit, uppercase letter, underscor e, exclamation point, period, or a question mark.

[!] Note that a dash is a metacharacter only within a character class — otherwise it matches the normal dash character

### Negated character classes
If you use ```[^...]``` instead of ```[...]```, the class matches any character that isn’t listed
> [^1-6] matches a character that's not 1 through 6
The ```^``` negates the list -> list the character you don't want to include

The ```^``` used here is the same as the start-of-line caret but the meaning is completely different. Just as the English word “wind” can mean differ ent things depending on the context (sometimes a strong breeze, sometimes what you do to a clock), so can a metacharacter.

Example: search that list of English words for odd words that have q followed by something other than u
```
egrep 'q[^u]' wordlist.txt
```
Two notable words not listed are 'Qantas' and 'Iraq'. Although both words are in the wordlist.txt file, neither were displayed by ```egrep``` command
> Qantas didn’t match because the regular expression called for a lowercase q

> The Iraq example is somewhat of a trick question. The regular expression calls for q followed by a character that’s not u, which precludes matching q at the end of the line. Lines generally have newline characters at the very end but egrep strips those before checking with the regular expression -> after a line-ending q, there's no non-u to be matched

-> a character class, even negated, still requires a character to match

### Matching Any Character with Dot
The metacharacter ```.``` (usually called dot or point) is a shorthand for a character class that matches any character. -> an 'any character here' placeholder in your expression

For example if you want to search for a date such as 03/19/76, 03-19-76, or even 03.19.76, you could go
to the trouble to construct a regular expression that uses character classes to explicitly allow '/', '-', or '.'

so the regex could be
```
03[-./]19[-./]76
```
> In '03[-./]19[-./]76', the dots are not metacharacters because they are within a character class.

> The dashes are also not class metacharacters in this case because each is the first thing after [ or [^. Had they not been first, as with '[.-/]', they would be the class range metacharacter, which
would be a mistake in this situation

the regex could also simply be
```
03.19.76
```

However with '03.19.76', each dot can match any character at all, so it can match, say, 'lottery numbers: 19 203319 7639'. 
So, '03[-./]19[-./]76' is more precise, but it's more difficult to read and write. '03.19.76' is easy to understand, but vague

## Alternation
### Matching any one of several subexpressions
A very convenient metacharacter is ```|```, which means 'or'. It allows you to combine multiple expressions into a single expression that matches any of the individual ones.
For example, ```Bob``` and ```Robert``` are separate expressions, but ```Bob|Robert``` is
one expression that matches either. When combined this way, the subexpressions are called alternatives.

Looking back to our ```gr[ea]y``` example, it is interesting to realize that it can be written as ```grey|gray```, and even ```gr(a|e)y```

> With 'gr(a|e)y', the parentheses are required because without them, 'gra|ey' means 'gra' or 'ey', which is not what we want here

Note that something like ```gr[a|e]y``` is not what we want — within a class, the '|' character is just a normal character, like 'a' and 'e'.

Another example

> '(first|1st)' and '(fir|1)st' effectively mean the same thing

[!] IMPORTANT: A ```character class``` can match just a single character in the target text. With ```alternation```, since each alternative can be a full-fledged regular expression in and of itself, each alter native can match an arbitrary amount of text. ```Character classes``` are almost like their own special mini-language (with their own ideas about metacharacters, for example), while ```alternation``` is part of the 'main' regular expression language.

Also, take care when using caret or dollar in an expression that has alternation.
Compare ```[^From|Subject|Date: ]``` with ```^(From|Subject|Date): ```

>'[^From|Subject|Date: ]' matches '^From' or 'Subject' or 'Date: '

>'^(From|Subject|Date): ' matches the start of the line then one from 'From', 'Subject' or 'Date' and then match ': '

Effectively, it matches:

>1) start-of-line, followed by F  r  o  m, followed by ': '

>or 2) start-of-line, followed by S  u  b  j  e  c  t, followed by ': '

>or 3) start-of-line, followed by D  a  t  e, followed by ': '

## Ignoring Differences in Capitalization
The email header example provides a good opportunity to introduce the concept of a case-insensitive match. The field types in an email header usually appear with leading capitalization, such as 'Subject' and 'From' but the email standard actually allows mixed capitalization, so things like 'DATE' and 'from' are also allowed.

One approach is to replace 'From' with '[Ff][Rr][Oo][Mm]' but this is quite cumbersome

there is a way to tell egrep to ignore case when doing comparisons, to perform the match in a case insensitive manner in which capitalization differences are simply ignored. It is not a part of the regular-expression language, but is a related useful feature many tools provide.
```
egrep -i '^(From|Subject|Date): ' mailbox
```

## Word Boundaries
A common problem is that a regular expression that matches the word you want can often also match where the 'word' is embedded within a larger word
Some versions of egrep offer limited support for word recognition: namely the ability to match the boundary of a word (where a word begins or ends)

>The captain wore his cap and cape proudly as
>he sat listening to the recap of how his
>crew saved the men from a capsized vessel.

If you want to match all the 'cap' word you might use the pattern ```cap```, however this will also match the word 'captain', 'cape', 'recap', ...
Say if we want to match the cap word specifically (not the captain, cape, recap, ...), the regex should be
```
\bcap\b
```
Test drive
```
egrep '\bcap\b' wordlist.txt
```

## Optional Items
Let's say we want to match 'color' or 'colour'. The regex could be ```colou?r``` to match either of them. 
The metacharacter ```?``` (question mark) means optional. It is placed after the character that is allowed to appear at that point in the expression, but whose existence isn't actually required to still be considered a successful match.
The question mark attaches only to the immediately-preceding item. This item is always considered successful.

> 'colou?r' is interpreted as 'c' then 'o' then 'l' then 'o' then 'u?' then 'r'. The 'u?' part is always successful

For example, consider matching the date that represents July fourth, with the 'July' part being either 'July' or 'Jul', and the 'fourth' path being 'fourth', '4th' or '4'

> We could just use '(July|Jul) (fourth|4th|4)' but there's a better way
```
July? (fourth|4(th)?)
```
Test drive
```
egrep 'July? (fourth|4(th)?)' wordlist.txt
```

## Other Quantifiers: Repetition
[!] question mark, plus, and star, are called quantifiers because they influence the quantity of what they govern.

The metacharacter ```+``` (plus) means one or more of the immediately-preceding item. Try to match as many times as possible, but fails if it can't match at least once.
The metacharacter ```*``` (star|asterisk) means 'any number, including none, of the immediately-preceding item. Try to match it as many times as possible, but it's OK to settle for nothing if need be.

> ' ?' allows a single optional space

> ' +' one space is required although more are allowed

> ' *' allows any number of optional spaces

html valid tag matching test drive
```
egrep '<HR( +SIZE += +[0-9]+)? +>' wordlist.txt
```

## Parentheses and Backreferences
So far, we have seen two uses for parentheses: 
- to limit the scope of alternation, '|'.
- to group multiple characters into larger units to which you can apply quantifiers like question mark and star.
> For example: ( +SIZE += +[0-9]+)?

Backreferencing is a regular-expression feature that allows you to match new text that is the same as some text matched earlier in the expression (match one generic word, and then say "now match the same thing again").

Backreferences are typically denoted by a backslash followed by a number (\1, \2, \3, and so on) or a name (\k\<name\>) corresponding to the captured group.

For example, say you want to match a repeated word in a string, such as 'hello hello' or 'foo foo foo'. You can use a backreference to ensure that the repeated word occurs multiple times:
```
\b(\w+)\s+\1\b
```
> '\b' matches a word boundary.
> '(\w+)' captures one or more word characters (letters, digits, or underscores).
> '\s+' matches one or more whitespace characters.
> '\1' is a backreference that matches the exact text captured by the first group.

## The Greate Escape
How to actually match a character that a regular expression would normally interpret as a metacharacter ? If I searched for the Internet hostname 'ega.att.com' using ```ega.att.com```, it
could end up matching something like 'megawatt computing'

The metasequence to match an actual period is a period preceded by a backslash: ```ega\.att\.com```

The sequence ```\.``` is described as an escaped period or escaped dot, and you can do this with all the normal metacharacters, except in a characterclass.

A backslash ```\``` used in this way is called an “escape” — when a metacharacter is escaped, it loses its special meaning and becomes a literal character.

> You could use '\([a-zA-Z]+\)' to match a word within parentheses, such as '(very)'

When used before a non-metacharacter, a backslash can have different meanings depending upon the version of the program. 

> For example we have already seen the backreference '\1'

## Important points to be remember
The rules about which characters are and aren’t metacharacters (and exactly what they mean) are different inside a character class.
- dot ```.``` is a metacharacter outside of a class, but not within one. Conversely, a dash ```-``` is a metacharacter within a class (usually, to be specific: it's a metacharacter when used to indicates a range of characters), but not outside. 
- a caret ```^``` has one meaning outside (matches the beginning of a line), another if specified inside a class immediately after the opening ```[``` (matches any character that isn't listed), and a third if given elsewhere in the class (just a normal character).

Don't confuse alternation with a character class! The class ```[abc]``` and the alternation ```(a|b|c)``` effectively mean the same thing, but the similarity in this example does not extend to the general case. 
- A character class can match exactly one character, and that's true no matter how long or short the specified list of acceptable characters might be.
- Alternation, on the other hand, can have arbitrarily long alternatives, each textually unrelated to the other: ```\b(1,000,000|million|thousand thou)\b```. However, alternation can't be negated like a character class.

A negated character class is simply a notational convenience for a normal character class that matches everything not listed. Thus, ```[^x]``` doesn't mean "match unless there is an x" but rather "match if there is something that is not x "The difference is subtle, but important. The first concept matches a blank line, for example, while ```[^x]``` does not

Your eye has always been trained to treat spaces specially. That's a habit you'll have to break when reading regular expressions, because the space character is a normal character, no different from, say, j or 4.