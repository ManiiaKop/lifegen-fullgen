"""

 Please do not put this *unittest* in the tests/unittest GitHub action.
HOWEVER,
 Please keep the raw python script and the unittest, so it can be run by the tests/pronoun_test GitHub action.

This test checks that pronoun tags are formated correctly, 

"""

import os
import re
import sys
import unittest

import ujson

from scripts.cat.cats import Cat
from scripts.utility import process_text

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"


def test():
    """Iterate through all files in 'resources'
    and verify that any detected pronoun tags are
    formatted correctly."""
    failed = False
    failed_files = []

    # Note - we are replacing with a singular-conjugated pronoun,
    # to ensure that we are catching cases where only one verb conjugation
    # was provided - since singular-conjugation
    # should be the second provided conjugation.
    _r = ("name", Cat.default_pronouns[1])
    replacement_dict = {
        "m_c": _r,
        "r_c": _r,
        "r_c1": _r,
        "r_c2": _r,
        "n_c": _r,
        "app1": _r,
        "app2": _r,
        "app3": _r,
        "app4": _r,
        "app5": _r,
        "app6": _r,
        "p_l": _r,
        "s_c": _r,
        "(mentor)": _r,
        "l_n": _r,
        "dead_par1": _r,
        "dead_par2": _r,
        "p1": _r,
        "p2": _r,
        "(deadmentor)": _r,
        "(previous_mentor)": _r,
        "mur_c": _r,
        "t_c": _r,
        "y_c": _r,
        "d_c": _r,
        "d_n": _r,
        "r_a": _r, 
        "r_m": _r,
        "y_p": _r,
        "tm_n": _r,
        "t_l": _r, 
        "t_m": _r, 
        "t_p": _r,
        "t_a": _r,
        "parent": _r,
        "parent1": _r,
        "parent2": _r,
        "sibling": _r,
        "t_s": _r,
        "t_k": _r,
        "t_ka": _r,
        "t_kk": _r,
        "y_m": _r,
        "t_p_positive": _r,
        "t_p_pos": _r,
        "t_p_negative": _r,
        "m_n": _r,
        "r_q": _r,
        "r_k": _r,
        "r_e": _r,
        "crush1": _r,
        "their_crush": _r,
        "your_crush": _r,
        "mate1": _r,
        "t_cc": _r,
        "r_w": _r,
        "y_a": _r,
        "r_s": _r,
        "r_i": _r,
        "y_s": _r,
        "y_l": _r,
        "r_d": _r,
        "df_y_a": _r,
        "r_c_sc": _r,
        "a_n": _r,
        "t_q": _r,
        "brooding_t_l": _r,
        "y_k": _r,
        "dislike_r_c": _r,
        "trust_r_c": _r,
        "neutral_r_c": _r,
        "r_c_brooding": _r,
        "r_c_sweet": _r,
        "plike_r_w": _r,
        "r_c_upstanding": _r,
        "r_a_silly": _r,
        "r_c_unabashed": _r,
        "plike_r_a": _r,
        "r_w_upstanding": _r,
        "r_a_cool": _r,
        "r_w_neurotic": _r,
        "dislike_r_w": _r,
        "plove_t_s": _r,
        "r_c_neurotic": _r,
        "y_kk": _r,
        "trust_r_w": _r,
        "rdf_c": _r,
        "plike_r_c": _r,
        "r_c_stable": _r,
        "r_w_assertive": _r,
        "r_c_assertive": _r,
        "fc_c": _r
    }
    
    cluster_addons = [
        "_upstanding",
        "_brooding",
        "_sweet",
        "_cool",
        "_unlawful",
        "_silly",
        "_neurotic",
        "_introspective",
        "_unabashed",
        "_assertive",
        "_stable"
    ]

    rel_addons = [
        "plike_",
        "plove_",
        "rlike_",
        "rlove_",
        "dislike_",
        "hate_",
        "neutral_",
        "trust_",
        "comfort_",
        "respect_",
        "jealous_"
    ]

    # addons = {}
    
    # for abbrev in list(replacement_dict.keys()):
    #     for r in rel_addons:
    #         addons[f"{r}{abbrev}"] = _r
    #     for x in cluster_addons:
    #         addons[f"{abbrev}{x}"] = _r
    #         for r in rel_addons:
    #             addons[f"{r}{abbrev}{x}"] = _r

    # replacement_dict.update(addons)

    for x in range(0, 11):
        replacement_dict[f"n_c:{x}"] = _r

    for root, _, files in os.walk("resources"):
        for file in files:
            if file.endswith(".json") and file != "credits_text.json":
                path = os.path.join(root, file)

                if not test_replacement_failure(path, replacement_dict):
                    failed = True
                    failed_files.append(path)

    if failed:
        # Set the GITHUB_OUTPUT environment variable to the list of failed files
        if "GITHUB_OUTPUT" in os.environ:
            with open(os.environ["GITHUB_OUTPUT"], "a") as handle:
                print(f"files={':'.join(failed_files)}", file=handle)
        else:
            print(f"files={':'.join(failed_files)}")
        sys.exit(1)
    else:
        sys.exit(0)


def test_replacement_failure(path: str, repl_dict: dict) -> bool:
    """Reads in a file, and finds strings, and runs pronoun replacment on those strings.
    Returns False if there were any issues with the pronoun replacement, or if the
    json is incorrectly formatted."""

    success = True

    with open(path, "r") as file:
        try:
            contents = ujson.loads(file.read())
        except ujson.JSONDecodeError as _e:
            print(f"::error file={path}::File {path} is invalid json")
            print(_e)
            return False

    for _str in get_all_strings(contents):
        try:
            processed = process_text(_str, repl_dict, True)
        except (KeyError, IndexError) as _e:
            print(
                f'::error file={path}: "{_str}" contains invalid pronoun or verb tags.'
            )
            print(_e)
            success = False
        else:
            # This test for any pronoun or verb tag fragments that might have
            # sneaked through. This is most likely caused by using the incorrect type of
            # brackets
            if re.search(r"\{PRONOUN|\(PRONOUN|\{VERB|\(VERB", processed):
                print(
                    f'::error file={path}: "{_str}" contains pronoun tag fragments after replacment'
                )
                success = False

    return success


def get_all_strings(data):
    """Will take any combination of list and dicts,
    and extract all strings, including dictionary keys.
    Recursive."""

    all_strings = []

    if isinstance(data, list):
        for _x in data:
            all_strings.extend(get_all_strings(_x))
    elif isinstance(data, dict):
        for _x in data:
            all_strings.extend(get_all_strings(data[_x]))
            all_strings.extend(get_all_strings(_x))

    elif isinstance(data, str):
        all_strings.append(data)

    return all_strings


class TestPronouns(unittest.TestCase):
    """Test for some common pronoun tagging errors in resources"""

    def test_pronouns(self):
        """Test that all files are ascii decodable."""
        with self.assertRaises(SystemExit) as cm:
            test()
        self.assertEqual(cm.exception.code, 0)
