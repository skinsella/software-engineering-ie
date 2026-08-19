import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import shared as S
from elementor_lib import section, shortcode_widget, section_of

PAD = {"padding": {"unit":"px","top":"56","right":"24","bottom":"72","left":"24","isLinked":False}}

# ---------------- /jobs : the public Residency Job Board ----------------
board_hero = S.hero("Members portal", "Residency Job Board",
  "Open residency positions from ISE partner companies. Search each round and apply directly to the ISE champion.",
  '<a class="ise-btn ise-btn--primary" href="#rounds">View open rounds</a> '
  '<a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="/post-a-job">Post a role</a>',
  max_title="18ch")

board = section_of(shortcode_widget("[ise_residency_board]"))

board_cta = section(S.cta("Are you an ISE champion?",
  "Partner companies can post Residency 4 and 5 positions to the board.",
  '<a class="ise-btn ise-btn--on-dark" href="/post-a-job">Post a residency job</a>'))

S.assemble(114, "Jobs", "jobs", [board_hero, board, board_cta], menu_order=9)

# ---------------- /post-a-job : gated submission + registration ----------------
post_hero = S.hero("For partners", "Post a residency job",
  "ISE partner companies can list Residency 4 and 5 positions. Sign in or register your company, then submit a role for review.",
  '<a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="/jobs">View the board</a>',
  max_title="18ch")

submit = section_of(shortcode_widget("[ise_residency_submit]"), settings=dict(PAD))

register_band = section(S.band(
  '<div class="ise-container" style="max-width:760px;"><p class="ise-eyebrow">New here?</p>'
  '<h2>Register your company</h2><p class="ise-lead">Create a partner account to post and manage residency roles.</p></div>',
  "ise-band"))
register = section_of(shortcode_widget("[ise_partner_register]"),
                      settings={"padding": {"unit":"px","top":"24","right":"24","bottom":"72","left":"24","isLinked":False},
                                "background_background":"classic","background_color":"#f6f8f7"})

S.assemble(115, "Post a job", "post-a-job", [post_hero, submit, register_band, register], menu_order=99)

print("built /jobs (board) + /post-a-job (submit + register), shortcode-driven")
