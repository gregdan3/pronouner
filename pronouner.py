#!/usr/bin/env python3
# i am not a phoneticist, phonetician, phonologist, or phonographer
# but it's funny that all these words exist
# i'm also not a phononomist or phonologer

import argparse
import logging

import enchant
from termcolor import colored

LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)

d = enchant.Dict("en_US")
orders = ["cv", "vc"]
sentences = []  # TODO

# this list comes from my other project: gregdan3/common-english-phonemes
# these are present in >=70% of the english dialects documented in phoible
# NOTE: the approximations are for my benefit. trust the IPA
consonant_phonemes = [
    {"ipa": "b", "aprx": "b"},
    {"ipa": "d", "aprx": "d"},
    {"ipa": "d̠ʒ", "aprx": "j"},
    {"ipa": "f", "aprx": "f"},
    {"ipa": "h", "aprx": "h"},
    {"ipa": "j", "aprx": "y"},
    {"ipa": "l", "aprx": "l"},
    {"ipa": "m", "aprx": "m"},
    {"ipa": "n", "aprx": "n"},
    {"ipa": "pʰ", "aprx": "p"},
    {"ipa": "s", "aprx": "s"},
    {"ipa": "tʰ", "aprx": "t"},
    {"ipa": "t̠ʃ", "aprx": "ch"},
    {"ipa": "v", "aprx": "v"},
    {"ipa": "w", "aprx": "w"},
    {"ipa": "z", "aprx": "z"},
    {"ipa": "ð", "aprx": "th"},  # voiced
    {"ipa": "ŋ", "aprx": "ng"},
    {"ipa": "ɡ", "aprx": "g"},
    {"ipa": "ɹ", "aprx": "r"},
    {"ipa": "ʃ", "aprx": "sh"},
    {"ipa": "ʒ", "aprx": "zh"},
    {"ipa": "θ", "aprx": "th"},  # voiceless
]
# this list comes from my other project: gregdan3/common-english-phonemes
# these are present in >=50% of the english dialects documented in phoible
# ... you really gotta stretch with english vowels
vowel_phonemes = [
    {"ipa": "iː", "aprx": "ee"},
    {"ipa": "ɒ", "aprx": "awh"},
    {"ipa": "ə", "aprx": "uh"},
    {"ipa": "ɛ", "aprx": "eh"},
    {"ipa": "ɪ", "aprx": "ih"},
    {"ipa": "ʊ", "aprx": "euh"},
]

# the default blocklist is:
# - weirdly placed (ŋ)
# - inconsistently written (ʒ)
# - indistinguishable in writing (θ/ð, ɡ/d̠ʒ)
# - already used (h, ʃ)
# - r (ɹ)
cblocklist = [
    # "b",
    # "d",
    "d̠ʒ",
    # "f",
    "h",
    "j",
    # "l",
    # "m",
    # "n",
    # "pʰ",
    # "s",
    # "tʰ",
    # "t̠ʃ",
    # "v",
    # "w",
    # "z",
    "ð",
    "ŋ",
    "ɡ",
    "ɹ",
    "ʃ",
    "ʒ",
    "θ",
]
# vowel default blocklist is lazy or dark vowels
vblocklist = [
    # "iː",
    "ɒ",
    "ə",
    # "ɛ",
    # "ɪ",
    "ʊ",
]


def is_word(pronoun_forms: dict):
    # checking ipa is pointless here
    res = d.check(pronoun_forms["subj_aprx"]) or d.check(pronoun_forms["pos_aprx"])
    return res


def make_possessive(pronoun: str):
    # this is silly but making a unique possessive form on the fly is bad
    if pronoun[-1] == "s":
        return pronoun
    return pronoun + "s"


def construct_pronoun(ph1, ph2, ph3=None, bad: bool = False):
    """takes in 2 or 3 phonemes
    returns dict representation of corresponding pronoun, plus metadata"""
    check = [ph1, ph2]
    if ph3 is not None:
        check.append(ph3)
    p_ipa = ""
    p_aprx = ""
    for e in check:
        p_ipa += e["ipa"]
        p_aprx += e["aprx"]
    constructed = {
        "subj_ipa": p_ipa,
        "pos_ipa": make_possessive(p_ipa),
        "subj_aprx": p_aprx,
        "pos_aprx": make_possessive(p_aprx),
        "has_bad": bad,
    }
    constructed["is_word"] = is_word(constructed)
    return constructed


def permute_pronouns_simple(vowel: dict, vowel_bad: bool = False):
    """more realistic variation of pronoun generation
    English's third person pronouns begin with a fricative
    then end with a vowel, or a diphthong in "they"'s case
    so generating pronouns for more cases than con+vowel is asking for trouble
    """
    permutations = []
    for con1 in consonant_phonemes:
        con1bad = (con1["ipa"] in cblocklist) or vowel_bad
        permutations.append(construct_pronoun(con1, vowel, bad=con1bad))
    return permutations


def permute_pronouns_complex(vowel: dict, vowel_bad: bool = False):
    """not recommended for use
    potentially, generate all the pronouns that are even vaguely reasonable!
    but a vast majority of these pronoun candidates are same-y, hard to read or
    difficult to write.
    """
    permutations = []
    for con1 in consonant_phonemes:
        con1bad = (con1["ipa"] in cblocklist) or vowel_bad
        permutations.append(construct_pronoun(con1, vowel, bad=con1bad))
        permutations.append(construct_pronoun(vowel, con1, bad=con1bad))
        for con2 in consonant_phonemes:
            # NOTE: produces TOO MANY pronoun candidates
            con2bad = (con2["ipa"] in cblocklist) or con1bad
            permutations.append(construct_pronoun(con1, vowel, con2, bad=con2bad))
            permutations.append(construct_pronoun(con2, vowel, con1, bad=con2bad))
    return permutations


def main():
    bad = []
    good = []

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
        vblock = vowel["ipa"] in vblocklist
        permutations = permute_pronouns_simple(vowel, vblock)
        for forms in permutations:
            color = "red" if forms["is_word"] else "magenta"

            toprint = colored(forms["subj_ipa"] + " ", color)
            good.append(forms)
            if not forms["has_bad"]:
                print(toprint, end="")
        if not vblock:
            print()

    if len(good) < 30:
        for pronoun in good:
            for sentence in sentences:
                print(sentence % pronoun)
            print()


if __name__ == "__main__":
    main()
