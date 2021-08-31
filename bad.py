# i am not a phoneticist, phonetician, phonologist, or phonographer
# but it's funny that all these words exist
# i'm also not a phononomist

import logging

import enchant
from termcolor import colored

LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)

d = enchant.Dict("en_US")
orders = ["cv", "vc"]
sentences = []  # TODO

# i omit duplicate phonemes like "ph", "wh", "kn", "gh"
consonant_phonemes_i_guess = [
    "b",
    "c",
    "d",
    "f",
    "g",
    "h",
    "j",
    "k",
    "l",
    "m",
    "n",
    "p",
    "q",
    "r",
    "s",
    "t",
    "v",
    "w",
    "x",
    "y",
    "z",
    "ch",
    "th",
    "sh",
    "zh",
    "ng",
]
vowel_phonemes_that_are_okay = [
    "a",  # short a
    "e",  # bruh
    "i",  # short i
    "o",
    "u",
    "y",  # no no no no no no no
    "ay",  # long a, not a-e diphthong
    "eh",  # bruh
    "ih",  #
    "oo",
    "uh",  # oo ambiguity
    "ey",
]


# anything that produces existing-sounding words
# stuff that would constitute well known neo-pronouns
# and anything i don't like subjectively
cblocklist = [
    # "b",
    "c",  # sound/spelling ambiguity
    # "d",
    "f",
    "g",  # gif or gif?
    "h",  # 'he'
    "j",  # harsh, confuses other langs, not aesthetic
    "k",
    # "l",
    # "m",
    # "n",
    # "p",
    "q",  # so bad. weird consonant.
    "r",  # schwa-inducing, gross
    # "s",
    "t",  # same as k g, harsh
    # "v",
    # "w",
    "x",  # neopro
    "y",  # sometimes ambiguous, also if somebody calls me "ye" i'll die
    "z",  # neopro
    "ch",
    "th",  # "thu, uth, the, tha" all gross! only diphthong-able, as in "they"
    "sh",  # 'she'
    "zh",  # superior phoneme for voiced 'sh'
    "ng",  # obviously bad but funny to include at all
]

# these vowels don't create words that 'look' like pronouns to me
vblocklist = [
    # "a",  # short a
    # "e",  # bruh
    # "i",  # short i
    # "o",
    "u",  #
    "y",  # no no no no no no no
    "ay",  # too diphthong-y
    # "eh",  # bruh
    # "ih",  # too many letters to specify...
    # "oo",
    # "uh",  # oo ambiguity
    "ey",  # diphthong
]


def is_already_word(pronoun_forms: dict):
    res = d.check(pronoun_forms["subj"]) or d.check(pronoun_forms["pos"])
    LOG.debug(
        "%s or %s are already words" % (pronoun_forms["subj"], pronoun_forms["pos"])
    ) if res else None
    return res


def make_possessive(pronoun: str):
    if pronoun[-1] == "s":
        return pronoun
    return pronoun + "s"


def construct_pronoun(consonant: str, vowel: str, order: str):
    if order == "cv":
        pronoun = f"{consonant}{vowel}"
    elif order == "vc":
        pronoun = f"{vowel}{consonant}"
    elif order == "cvc":
        # TODO
        pronoun = f""
    elif order == "vcv":
        # TODO:
        pronoun = f""
    else:
        return {}
    return {"subj": pronoun, "pos": make_possessive(pronoun)}


def main():
    bad = []
    good = []
    vblock = False
    cblock = False

    print(
        """
Already existing third person pronouns:
sg = singular
pl = plural
gl = genderless
ml = male
fl = female

           subj    obj     d. pos    i. pos      reflective?
1st sg gl: i     / me    / my      / mine      / myself
1st pl gl: we    / us    / our     / ours      / ourselves
2nd sg gl: you   / you   / your    / yours     / yourself
2nd pl gl: y'all / y'all / y'all's / y'all's   / y'allselves
3rd sg ml: he    / him   / his     / his       / himself
3rd sg fl: she   / her   / hers    / hers      / herself
3rd sg gl: they  / them  / theirs  / theirs    / themself,theirself
3rd pl gl: they  / them  / theirs  / theirs    / themselves,theirselves
3rd sg gl: it    / it    / its     / its       / itself

Taken consonants: ( front / back )
1st: m / n
2nd: y / r
3rd: h sh th / t m r

"Taken" vowels: (thse are okay to reuse)
1st: i ee uh ow
2nd: oo oh ah
3rd: ee ih schwa ey eh ih
    """
    )

    for vowel in vowel_phonemes_that_are_okay:
        vblock = vowel in vblocklist
        for con in consonant_phonemes_i_guess:
            cblock = con in cblocklist
            for order in orders:
                forms = construct_pronoun(con, vowel, order)
                dont = vblock or cblock  # or is_already_word(forms)
                color = "red" if is_already_word(forms) else "magenta"

                if dont:
                    # toprint = colored(forms["subj"] + " ", "red")
                    bad.append(forms)
                    # print(toprint, end="")
                else:
                    toprint = colored(forms["subj"] + " ", color)
                    good.append(forms)
                    print(toprint, end="")
        if vblock:
            continue
        print()

    if len(good) < 20:
        for pronoun in good:
            for sentence in sentences:
                print(sentence % pronoun)
            print()


if __name__ == "__main__":
    main()
