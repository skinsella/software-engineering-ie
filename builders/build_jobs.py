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

# ---------------- Student portal pages ----------------
join_hero = S.hero("For students", "Join the ISE student portal",
  "Create your student account to browse residency placements and build your profile.",
  '<a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="/jobs">View the board</a>', max_title="18ch")
join = section_of(shortcode_widget("[ise_student_register]"))
S.assemble(116, "Join", "join", [join_hero, join], menu_order=98)

profile_hero = S.hero("Student portal", "Your profile",
  "Add your photo, skills, website or CV and GitHub so partner companies can find you.",
  '<a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="/students-directory">Student directory</a>', max_title="16ch")
profile = section_of(shortcode_widget("[ise_student_profile]"))
S.assemble(117, "Profile", "profile", [profile_hero, profile], menu_order=97)

dir_hero = S.hero("For partners", "Student directory",
  "Browse ISE student profiles — skills, portfolios and GitHub — when sourcing for a residency.",
  '<a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="/jobs">View the board</a>', max_title="16ch")
directory = section_of(shortcode_widget("[ise_student_directory]"))
S.assemble(118, "Student directory", "students-directory", [dir_hero, directory], menu_order=96)

print("student portal pages built: /join, /profile, /students-directory")

myapps_hero = S.hero("Student portal", "My applications",
  "Track the residencies you have applied to and their status.",
  '<a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="/jobs">View the board</a>', max_title="16ch")
myapps = section_of(shortcode_widget("[ise_my_applications]"))
S.assemble(119, "My applications", "my-applications", [myapps_hero, myapps], menu_order=95)

applicants_hero = S.hero("For partners", "My applicants",
  "Students who have applied to your residency roles — shortlist, reject, or view their profile.",
  '<a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="/post-a-job">Post a role</a>', max_title="16ch")
applicants = section_of(shortcode_widget("[ise_my_applicants]"))
S.assemble(120, "My applicants", "my-applicants", [applicants_hero, applicants], menu_order=94)

print("application pages built: /my-applications, /my-applicants")
