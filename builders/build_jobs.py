import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import shared as S
from elementor_lib import section

# ---- Sample job listings (PLACEHOLDER data — replace with real postings /
#      wire to a data source before publishing). company `slug` maps to a
#      partner logo in assets/partners. ----
JOBS = [
 dict(id=1, title="Graduate Software Engineer", company="Stripe", slug="stripe",
   location="Dublin", type="Graduate", category="Payments", posted="Posted 2 days ago",
   summary="Join a team building the reliable payments infrastructure used by millions of businesses worldwide.",
   description="<p>As a graduate engineer at Stripe you'll ship production code from your first weeks, working across the payments stack.</p><ul><li>Strong fundamentals in one modern language</li><li>Curiosity and a bias to build</li><li>ISE residency experience a plus</li></ul>",
   apply="#"),
 dict(id=2, title="Machine Learning Intern", company="Provizio", slug="provizio",
   location="Limerick", type="Internship", category="Data & ML", posted="Posted 5 days ago",
   summary="Work on perception and sensor-fusion models that help prevent road collisions before they happen.",
   description="<p>Help build and evaluate ML models on real automotive sensor data.</p><ul><li>Python, NumPy, PyTorch or TensorFlow</li><li>Interest in computer vision / sensor fusion</li></ul>",
   apply="#"),
 dict(id=3, title="Platform Engineer", company="Intercom", slug="intercom",
   location="Dublin", type="Full-time", category="Platform", posted="Posted 1 week ago",
   summary="Build and scale the platform that powers customer communication for thousands of companies.",
   description="<p>Own services at scale, improve reliability and developer experience across the platform.</p>",
   apply="#"),
 dict(id=4, title="Backend Engineer (Residency)", company="Tines", slug="tines",
   location="Remote", type="Residency", category="Security", posted="Posted 3 days ago",
   summary="A paid ISE residency building the automation engine behind modern security operations.",
   description="<p>Contribute to the core workflow engine as a paid resident, with mentoring throughout.</p>",
   apply="#"),
 dict(id=5, title="Data Engineer", company="Fiserv", slug="fiserv",
   location="Dublin", type="Full-time", category="Data & ML", posted="Posted 1 week ago",
   summary="Design robust data pipelines that move and transform financial data at massive scale.",
   description="<p>Build reliable, well-tested pipelines and data models for fintech workloads.</p>",
   apply="#"),
 dict(id=6, title="Frontend Engineer", company="Wayflyer", slug="wayflyer",
   location="Dublin", type="Full-time", category="Product", posted="Posted 4 days ago",
   summary="Craft the product experience that helps e-commerce businesses access growth funding.",
   description="<p>Build accessible, performant interfaces in a modern frontend stack.</p>",
   apply="#"),
 dict(id=7, title="Software Engineering Intern", company="Workday", slug="workday",
   location="Dublin", type="Internship", category="Software", posted="Posted 6 days ago",
   summary="A summer internship working alongside engineers on enterprise-scale software.",
   description="<p>Learn modern engineering practices while shipping real features.</p>",
   apply="#"),
 dict(id=8, title="Validation Software Engineer", company="Kneat", slug="kneat",
   location="Limerick", type="Full-time", category="Software", posted="Posted 2 weeks ago",
   summary="Build the platform digitising validation for the world's most regulated industries.",
   description="<p>Work on a mission-critical SaaS platform used by global life-sciences companies.</p>",
   apply="#"),
 dict(id=9, title="Network Software Engineer", company="Ericsson", slug="ericsson",
   location="Athlone", type="Full-time", category="Networks", posted="Posted 1 week ago",
   summary="Develop the software behind next-generation mobile networks.",
   description="<p>Contribute to large-scale telecoms software in a global engineering team.</p>",
   apply="#"),
 dict(id=10, title="Full-Stack Engineer (Residency)", company="Jentic", slug="jentic",
   location="Remote", type="Residency", category="AI", posted="Posted 3 days ago",
   summary="Paid residency building tools that connect AI agents to real-world systems.",
   description="<p>Ship across the stack on an early-stage AI product, with real ownership.</p>",
   apply="#"),
 dict(id=11, title="QA Automation Engineer", company="Teckro", slug="teckro",
   location="Limerick", type="Full-time", category="Software", posted="Posted 2 weeks ago",
   summary="Own automated testing for a platform transforming how clinical trials run.",
   description="<p>Design and maintain automated test suites across web and mobile.</p>",
   apply="#"),
 dict(id=12, title="Graduate Data Scientist", company="Susquehanna", slug="susquehanna",
   location="Dublin", type="Graduate", category="Data & ML", posted="Posted 5 days ago",
   summary="Apply data and modelling to real trading problems in a quantitative environment.",
   description="<p>Join a graduate programme combining software, statistics and markets.</p>",
   apply="#"),
]

ASSET = S.ASSET

# --- HERO ---
hero = S.hero("Jobs Board", "Roles from the ISE partner network",
  "Graduate roles, internships and residencies from the companies students work with. Search, filter and apply.",
  '<a class="ise-btn ise-btn--primary" href="#jb-app">Browse roles</a> '
  '<a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="/become-a-partner">Post a role</a>',
  max_title="20ch")

# --- interactive board widget ---
data_json = json.dumps(JOBS, ensure_ascii=False)
board_script = r"""
<script>
(function(){
  var DATA = __DATA__;
  var ASSET = "__ASSET__";
  var root = document.getElementById('jb-app'); if(!root) return;
  var grid = root.querySelector('.jb-grid'),
      countEl = root.querySelector('.jb-count'),
      emptyEl = root.querySelector('.jb-empty'),
      searchEl = root.querySelector('.jb-search'),
      filters = root.querySelectorAll('.jb-filter'),
      modal = root.querySelector('.jb-modal'),
      modalBody = modal.querySelector('.jb-modal__body');
  function uniq(k){ return Array.from(new Set(DATA.map(function(j){return j[k];}))).sort(); }
  filters.forEach(function(sel){ var k=sel.getAttribute('data-key');
    uniq(k).forEach(function(v){ var o=document.createElement('option'); o.value=v; o.textContent=v; sel.appendChild(o); }); });
  function logo(s){ return '<div class="jb-logo"><img src="'+ASSET+'/partners/'+s+'.png" alt=""></div>'; }
  function card(j){ return '<article class="jb-card" data-id="'+j.id+'"><div class="jb-card__top">'+logo(j.slug)
    +'<div><h3 class="jb-title">'+j.title+'</h3><div class="jb-company">'+j.company+' &middot; '+j.location+'</div></div></div>'
    +'<p class="jb-summary">'+j.summary+'</p><div class="jb-tags"><span class="jb-tag">'+j.type+'</span><span class="jb-tag">'+j.category+'</span></div>'
    +'<div class="jb-card__foot"><span class="jb-posted">'+j.posted+'</span><span class="jb-view">View &amp; apply &rarr;</span></div></article>'; }
  function match(){ var q=searchEl.value.trim().toLowerCase(), fv={};
    filters.forEach(function(s){ if(s.value) fv[s.getAttribute('data-key')]=s.value; });
    return DATA.filter(function(j){ for(var k in fv){ if(j[k]!==fv[k]) return false; }
      if(q){ var h=(j.title+' '+j.company+' '+j.summary+' '+j.category).toLowerCase(); if(h.indexOf(q)<0) return false; } return true; }); }
  function render(){ var l=match(); grid.innerHTML=l.map(card).join('');
    countEl.textContent = l.length+(l.length===1?' role':' roles')+' found'; emptyEl.hidden = l.length>0; }
  function open(j){ modalBody.innerHTML='<div class="jb-card__top">'+logo(j.slug)
    +'<div><h3>'+j.title+'</h3><div class="jb-company">'+j.company+' &middot; '+j.location+'</div></div></div>'
    +'<div class="jb-modal__meta"><span class="jb-tag">'+j.type+'</span><span class="jb-tag">'+j.category+'</span><span class="jb-tag">'+j.posted+'</span></div>'
    +'<div class="jb-modal__desc">'+j.description+'</div>'
    +'<div class="jb-modal__apply"><a class="ise-btn ise-btn--primary" href="'+j.apply+'" target="_blank" rel="noopener">Apply now &rarr;</a></div>';
    modal.hidden=false; document.body.style.overflow='hidden'; }
  function close(){ modal.hidden=true; document.body.style.overflow=''; }
  searchEl.addEventListener('input', render);
  filters.forEach(function(s){ s.addEventListener('change', render); });
  grid.addEventListener('click', function(e){ var c=e.target.closest('.jb-card'); if(!c) return;
    var j=DATA.find(function(x){return String(x.id)===c.getAttribute('data-id');}); if(j) open(j); });
  modal.addEventListener('click', function(e){ if(e.target===modal || e.target.closest('.jb-modal__close')) close(); });
  document.addEventListener('keydown', function(e){ if(e.key==='Escape') close(); });
  render();
})();
</script>
""".replace("__DATA__", data_json).replace("__ASSET__", ASSET)

board_html = '''
<div class="ise-container" id="jb-app">
  <div class="jb-toolbar">
    <input class="jb-search" type="search" placeholder="Search jobs, companies, skills…" aria-label="Search jobs">
    <select class="jb-filter" data-key="type" aria-label="Filter by type"><option value="">All types</option></select>
    <select class="jb-filter" data-key="location" aria-label="Filter by location"><option value="">All locations</option></select>
    <select class="jb-filter" data-key="company" aria-label="Filter by company"><option value="">All companies</option></select>
  </div>
  <div class="jb-count"></div>
  <div class="jb-grid"></div>
  <div class="jb-empty" hidden>No roles match your search. Try clearing a filter.</div>
  <div class="jb-modal" hidden role="dialog" aria-modal="true">
    <div class="jb-modal__box"><button class="jb-modal__close" aria-label="Close">&times;</button><div class="jb-modal__body"></div></div>
  </div>
</div>''' + board_script

board = section(S.band(board_html))

cta = section(S.cta("Hiring ISE talent?",
  "Partners can post graduate roles, internships and residencies to the board.",
  '<a class="ise-btn ise-btn--on-dark" href="/become-a-partner">Post a role</a>'))

S.assemble(114, "Jobs", "jobs", [hero, board, cta], menu_order=9)
print("jobs board built (page 114, slug 'jobs',", len(JOBS), "sample roles)")
