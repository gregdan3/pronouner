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

# NOTE: the approximations are for my benefit. trust the IPA
consonant_phonemes = [
    # TODO: not so sucks but i have a bad feeling
    {"ipa": "m", "aprx": "m"},
    {"ipa": "n", "aprx": "n"},
    {"ipa": "ŋ", "aprx": "ng"},
    {"ipa": "p", "aprx": "p"},
    {"ipa": "t", "aprx": "t"},
    {"ipa": "tʃ", "aprx": "ch"},
    {"ipa": "k", "aprx": "k"},
    {"ipa": "b", "aprx": "b"},
    {"ipa": "d", "aprx": "d"},
    {"ipa": "d", "aprx": "j"},
    {"ipa": "g", "aprx": "g"},
    {"ipa": "f", "aprx": "f"},
    {"ipa": "θ", "aprx": "th"},  # voiceless, "thick"
    {"ipa": "s", "aprx": "s"},
    {"ipa": "ʃ", "aprx": "sh"},
    {"ipa": "x", "aprx": "🟥"},  # not in my dialect?? voiceless velar fricative
    {"ipa": "h", "aprx": "h"},
    {"ipa": "v", "aprx": "v"},
    {"ipa": "ð", "aprx": "th"},  # voiced, "this"
    {"ipa": "z", "aprx": "z"},
    {"ipa": "ʒ", "aprx": "zh"},
    # given approx is common in chinese loan words and names...
    # there are tons of graphemes for it: treasure, division, azure, zsa
    {"ipa": "l", "aprx": "l"},
    {"ipa": "r", "aprx": "r"},
    {"ipa": "j", "aprx": "y"},  # consonant y
    {"ipa": "w", "aprx": "w"},
]
vowel_phonemes = [  # no diphthongs at all
    # TODO: sucks
    {"ipa": "ɪ", "aprx": "ih"},
    {"ipa": "i", "aprx": "ee"},
    {"ipa": "ʊ", "aprx": "uuh"},  # flat mouth
    {"ipa": "u", "aprx": "oo"},
    {"ipa": "o", "aprx": "oh"},
    {"ipa": "e̞", "aprx": "ih"},
    {"ipa": "ɛ", "aprx": "eh"},
    {"ipa": "ə", "aprx": "uh"},
    {"ipa": "ɔ", "aprx": "auh"},  # not diphthong
    {"ipa": "a", "aprx": "aw"},
    {"ipa": "æ", "aprx": "aaa"},
    {"ipa": "ɐ", "aprx": "ah"},
    {"ipa": "ɑ", "aprx": "aw"},
]


# anything that produces existing-sounding words
# stuff that would constitute well known neo-pronouns
# and anything i don't like subjectively
cblocklist = [
    # "m",
    # "n",
    # "ŋ",  #
    # "p",
    # "t",
    # "tʃ",
    # "k",
    # "b",
    # "d",
    # "dʒ",
    # "g",
    # "f",
    # "θ",
    # "s",
    # "ʃ",  #
    # "x",  #
    # "h",  #
    # "v",
    # "ð",
    # "z",
    # "ʒ",  #
    # "l",
    # "r",
    # "j",
    # "w",
]

# these vowels don't create words that 'look' like pronouns to me
vblocklist = [
    # "a",  # short a
    # "e",  # bruh
    # "i",  # short i
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


def permute_pronouns_from_vowel(vowel: str):
    permutations = []
    for con1 in consonant_phonemes:
        cv = f"{con1}{vowel}"
        permutations.append({"subj": cv, "pos": make_possessive(cv)})
        vc = f"{vowel}{con1}"
        permutations.append({"subj": vc, "pos": make_possessive(vc)})
        for con2 in consonant_phonemes:
            cvc1 = f"{con1}{vowel}{con2}"
            permutations.append({"subj": cvc1, "pos": make_possessive(cvc1)})
            cvc2 = f"{con2}{vowel}{con1}"
            permutations.append({"subj": cvc2, "pos": make_possessive(cvc2)})
    return permutations


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

    for vowel in vowel_phonemes:
        vblock = vowel in vblocklist
        for con in consonant_phonemes:
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
