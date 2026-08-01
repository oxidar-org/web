"""Tests for reserving the article URL's length ahead of generation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ai.base import append_url, build_user_prompt, effective_length, text_budget, url_policy

URL = "https://oxidar.org/why-who-where-rust-debconf26/"
POST = {
    "title": "Rust en DebConf 26",
    "description": "Charla de Oxidar",
    "tags": ["rust"],
    "url": URL,
    "body": "Contenido.",
}

CONFIG = {
    "platforms": {
        "bluesky": {"max_chars": 300},
        "twitter": {"max_chars": 280, "url_cost": 23},
        "instagram": {"max_chars": 2200, "include_url": False},
    }
}


class TestUrlPolicy:
    def test_defaults_to_real_url_length(self):
        should_append, cost = url_policy(POST, "bluesky", CONFIG)
        assert should_append
        assert cost == len(URL) + 2  # + separator

    def test_url_cost_override_wins(self):
        # Twitter rewrites links to a fixed width via t.co.
        _, cost = url_policy(POST, "twitter", CONFIG)
        assert cost == 23 + 2

    def test_platform_can_opt_out(self):
        assert url_policy(POST, "instagram", CONFIG) == (False, 0)

    def test_post_without_url_opts_out(self):
        assert url_policy({"url": ""}, "bluesky", CONFIG) == (False, 0)


class TestTextBudget:
    def test_budget_excludes_url(self):
        assert text_budget(POST, "bluesky", CONFIG) == 300 - len(URL) - 2

    def test_budget_uses_override_cost(self):
        assert text_budget(POST, "twitter", CONFIG) == 280 - 23 - 2

    def test_opt_out_platform_keeps_full_budget(self):
        assert text_budget(POST, "instagram", CONFIG) == 2200

    def test_budget_never_goes_negative(self):
        tiny = {"platforms": {"bluesky": {"max_chars": 10}}}
        assert text_budget(POST, "bluesky", tiny) > 0


class TestAppendUrl:
    def test_appends_url(self):
        assert append_url("Mirá esto", POST, "bluesky", CONFIG) == f"Mirá esto\n\n{URL}"

    def test_does_not_double_append(self):
        text = f"Mirá esto {URL}"
        assert append_url(text, POST, "bluesky", CONFIG) == text

    def test_skips_opt_out_platform(self):
        assert append_url("Mirá esto", POST, "instagram", CONFIG) == "Mirá esto"

    def test_result_fits_within_max_chars(self):
        # The whole point: prose at budget + URL must still fit the real limit.
        budget = text_budget(POST, "bluesky", CONFIG)
        result = append_url("x" * budget, POST, "bluesky", CONFIG)
        assert len(result) <= CONFIG["platforms"]["bluesky"]["max_chars"]


class TestEffectiveLength:
    def test_counts_raw_length_without_override(self):
        text = f"hola{URL}"
        assert effective_length(text, POST, "bluesky", CONFIG) == len(text)

    def test_substitutes_url_cost_when_platform_rewrites_links(self):
        # Twitter counts every link as 23 chars regardless of real length.
        text = f"hola {URL}"
        assert effective_length(text, POST, "twitter", CONFIG) == len("hola ") + 23

    def test_ignores_override_when_url_absent(self):
        assert effective_length("hola", POST, "twitter", CONFIG) == 4

    def test_budget_and_length_agree(self):
        # A message written exactly to budget must never be judged over the limit.
        for platform in ("bluesky", "twitter", "instagram"):
            budget = text_budget(POST, platform, CONFIG)
            text = append_url("x" * budget, POST, platform, CONFIG)
            max_chars = CONFIG["platforms"][platform]["max_chars"]
            assert effective_length(text, POST, platform, CONFIG) <= max_chars, platform


class TestPrompt:
    def test_prompt_states_budget_not_raw_limit(self):
        prompt = build_user_prompt(POST, "bluesky", CONFIG)
        assert str(text_budget(POST, "bluesky", CONFIG)) in prompt
        assert "máximo 300 caracteres" not in prompt

    def test_prompt_forbids_urls(self):
        assert "NO incluyas ninguna URL" in build_user_prompt(POST, "bluesky", CONFIG)
        assert "NO incluyas ninguna URL" in build_user_prompt(POST, "instagram", CONFIG)

    def test_prompt_omits_url_from_post_data(self):
        # Leaving the URL in the data invites the model to echo it back.
        assert URL not in build_user_prompt(POST, "bluesky", CONFIG)
