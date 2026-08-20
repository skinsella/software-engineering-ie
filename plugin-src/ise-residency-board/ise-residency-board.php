<?php
/**
 * Plugin Name: ISE Residency Board
 * Description: Residency job board for Immersive Software Engineering — a "Residency Job" post type, a Partner role, a gated front-end submission form (moderated), and shortcodes for the public board and the submit/login/register flow.
 * Version: 0.1.0
 * Author: ISE / University of Limerick
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

const ISE_RB_CPT   = 'residency_job';
const ISE_RB_ROLE  = 'partner';
const ISE_RB_STUDENT = 'student';
const ISE_RB_SKILL = 'rj_skill';
const ISE_RB_APP = 'residency_app';
const ISE_RB_ROUNDS_OPEN   = array( 'Residency 4', 'Residency 5' );
const ISE_RB_ROUNDS_CLOSED = array( 'Residency 1 closed', 'Residency 2 closed', 'Residency 1 + 2 closed', 'Residency 3 closed' );
const ISE_RB_META = array( 'round', 'company', 'salary', 'champion', 'apply' );

/* ---------------------------------------------------------------------------
 * Post type + Partner role + one-time sample seed (idempotent — works even
 * when the plugin is activated by writing active_plugins directly, since we
 * self-initialise on init rather than relying only on activation hooks).
 * ------------------------------------------------------------------------- */
add_action( 'init', function () {
	register_post_type( ISE_RB_CPT, array(
		'labels' => array(
			'name'          => 'Residency Jobs',
			'singular_name' => 'Residency Job',
			'add_new_item'  => 'Add Residency Job',
			'edit_item'     => 'Edit Residency Job',
		),
		'public'             => true,
		'publicly_queryable' => false,
		'show_ui'            => true,
		'show_in_menu'       => true,
		'menu_icon'          => 'dashicons-businessperson',
		'supports'           => array( 'title' ),
		'capability_type'    => 'post',
		'map_meta_cap'       => true,
	) );

	foreach ( ISE_RB_META as $key ) {
		register_post_meta( ISE_RB_CPT, '_rj_' . $key, array(
			'type'         => 'string',
			'single'       => true,
			'show_in_rest' => false,
			'auth_callback'=> function () { return current_user_can( 'edit_posts' ); },
		) );
	}

	// Partner role: can read + submit (pending) but not publish.
	if ( ! get_role( ISE_RB_ROLE ) ) {
		add_role( ISE_RB_ROLE, 'Partner', array( 'read' => true ) );
	}

	// Seed a few published sample jobs once, so the board is not empty.
	if ( ! get_option( 'ise_rb_seeded' ) ) {
		$samples = array(
			array( 'R4 | Stripe-01',  'Residency 4', 'stripe',      '€3,000 / month (indicative)', 'stripe-champion@example.com',   'residencies@stripe.example' ),
			array( 'R4 | Intercom-01','Residency 4', 'intercom',    '€2,800 / month (indicative)', 'intercom-champion@example.com', 'earlycareers@intercom.example' ),
			array( 'R4 | Provizio-01','Residency 4', 'provizio',    '€2,600 / month (indicative)', 'provizio-champion@example.com', 'jobs@provizio.example' ),
			array( 'R4 | Tines-01',   'Residency 4', 'tines',       'Competitive — TBC',           'tines-champion@example.com',    'residency@tines.example' ),
			array( 'R5 | Stripe-01',  'Residency 5', 'stripe',      '€3,200 / month (indicative)', 'stripe-champion@example.com',   'residencies@stripe.example' ),
			array( 'R5 | Kneat-01',   'Residency 5', 'kneat',       '€2,700 / month (indicative)', 'kneat-champion@example.com',    'careers@kneat.example' ),
			array( 'R5 | Wayflyer-01','Residency 5', 'wayflyer',    '€2,800 / month (indicative)', 'wayflyer-champion@example.com', 'talent@wayflyer.example' ),
		);
		foreach ( $samples as $s ) {
			$id = wp_insert_post( array(
				'post_type'   => ISE_RB_CPT,
				'post_title'  => $s[0],
				'post_status' => 'publish',
			) );
			if ( $id && ! is_wp_error( $id ) ) {
				update_post_meta( $id, '_rj_round',    $s[1] );
				update_post_meta( $id, '_rj_company',  $s[2] );
				update_post_meta( $id, '_rj_salary',   $s[3] );
				update_post_meta( $id, '_rj_champion', $s[4] );
				update_post_meta( $id, '_rj_apply',    $s[5] );
			}
		}
		update_option( 'ise_rb_seeded', 1 );
	}
} );

/* Admin list columns for quick moderation. */
add_filter( 'manage_' . ISE_RB_CPT . '_posts_columns', function ( $cols ) {
	$cols['rj_round']   = 'Round';
	$cols['rj_company'] = 'Company';
	$cols['rj_salary']  = 'Salary';
	return $cols;
} );
add_action( 'manage_' . ISE_RB_CPT . '_posts_custom_column', function ( $col, $post_id ) {
	if ( 0 === strpos( $col, 'rj_' ) ) {
		echo esc_html( get_post_meta( $post_id, '_' . $col, true ) );
	}
}, 10, 2 );

/* ---------------------------------------------------------------------------
 * Helpers
 * ------------------------------------------------------------------------- */
function ise_rb_asset() {
	return get_stylesheet_directory_uri() . '/assets';
}

function ise_rb_positions_for( $round ) {
	return get_posts( array(
		'post_type'   => ISE_RB_CPT,
		'post_status' => 'publish',
		'numberposts' => -1,
		'orderby'     => 'title',
		'order'       => 'ASC',
		'meta_key'    => '_rj_round',
		'meta_value'  => $round,
	) );
}

/* ---------------------------------------------------------------------------
 * [ise_residency_board] — public board grouped by round, with per-round search
 * ------------------------------------------------------------------------- */
add_shortcode( 'ise_residency_board', function () {
	ob_start();
	if ( ! is_user_logged_in() ) {
		echo '<div class="ise-container" style="padding-block:4rem 5rem;max-width:640px;">';
		echo '<div class="ise-card"><h3>Sign in to view residency placements</h3>'
			. '<p style="color:var(--ink-70);">Residency placements are visible to signed-in ISE students and partners.</p>'
			. '<p><a class="ise-btn ise-btn--primary" href="' . esc_url( wp_login_url( home_url( '/jobs/' ) ) ) . '">Sign in</a> '
			. '<a class="ise-btn ise-btn--ghost" href="' . esc_url( home_url( '/join/' ) ) . '">Create a student account</a></p></div>';
		echo '</div>';
		return ob_get_clean();
	}
	$submit_url = home_url( '/post-a-job/' );
	echo '<div class="ise-band--heritage" style="padding-block:2.75rem;"><div class="ise-container" id="rounds"><div class="rb-rounds">';
	foreach ( ISE_RB_ROUNDS_CLOSED as $c ) {
		echo '<span class="rb-round-btn rb-round-btn--closed">' . esc_html( $c ) . '</span>';
	}
	foreach ( ISE_RB_ROUNDS_OPEN as $o ) {
		echo '<a class="rb-round-btn rb-round-btn--post" href="' . esc_url( $submit_url ) . '">Post a ' . esc_html( $o ) . ' Job</a>';
	}
	echo '</div></div></div>';

	echo '<div class="ise-container" style="padding-block:3rem 4rem;">';
	foreach ( ISE_RB_ROUNDS_OPEN as $round ) {
		$posts = ise_rb_positions_for( $round );
		echo '<div class="rb-round"><div class="rb-round__head"><p class="ise-eyebrow">Now open</p><h2>ISE Current Open ' . esc_html( $round ) . ' Positions</h2></div>';
		// gather skills present in this round for the filter
		$round_skills = array();
		foreach ( $posts as $rp ) {
			foreach ( (array) wp_get_object_terms( $rp->ID, ISE_RB_SKILL, array( 'fields' => 'names' ) ) as $t ) { $round_skills[ $t ] = 1; }
		}
		$round_skills = array_keys( $round_skills ); sort( $round_skills );
		echo '<div class="rb-tools"><input class="rb-search" type="search" placeholder="Search ' . esc_attr( $round ) . ' positions…" aria-label="Search ' . esc_attr( $round ) . ' positions">';
		echo '<select class="rb-skill-filter" aria-label="Filter by skill"><option value="">All skills</option>';
		foreach ( $round_skills as $sk ) { echo '<option value="' . esc_attr( strtolower( $sk ) ) . '">' . esc_html( $sk ) . '</option>'; }
		echo '</select></div>';
		echo '<div class="rb-count"></div><div class="rb-list">';
		if ( $posts ) {
			foreach ( $posts as $p ) {
				$title    = get_the_title( $p );
				$salary   = get_post_meta( $p->ID, '_rj_salary', true );
				$champ    = get_post_meta( $p->ID, '_rj_champion', true );
				$apply    = get_post_meta( $p->ID, '_rj_apply', true );
				$company  = get_post_meta( $p->ID, '_rj_company', true );
				$skills   = wp_get_object_terms( $p->ID, ISE_RB_SKILL, array( 'fields' => 'names' ) );
				$skills_attr = esc_attr( strtolower( implode( ',', (array) $skills ) ) );
				$skills_html = '';
				if ( $skills && ! is_wp_error( $skills ) ) {
					$skills_html = '<div class="rb-skills"><span class="rb-skills__label">Skills</span>';
					foreach ( $skills as $sk ) { $skills_html .= '<span class="jb-tag">' . esc_html( $sk ) . '</span>'; }
					$skills_html .= '</div>';
				}
				$logo = '';
				if ( $company ) {
					$file = get_stylesheet_directory() . '/assets/partners/' . sanitize_file_name( $company ) . '.png';
					if ( file_exists( $file ) ) {
						$logo = '<span class="rb-logo"><img src="' . esc_url( ise_rb_asset() . '/partners/' . rawurlencode( $company ) . '.png' ) . '" alt=""></span>';
					}
				}
				$apply_ui = '';
				if ( ise_rb_is_student( wp_get_current_user() ) ) {
					if ( ise_ra_has_applied( get_current_user_id(), $p->ID ) ) {
						$apply_ui = '<div class="rb-apply-row"><span class="rb-applied">&#10003; Applied</span></div>';
					} else {
						$apply_ui = '<div class="rb-apply-row"><button class="ise-btn ise-btn--primary rb-apply" data-job="' . (int) $p->ID . '" data-title="' . esc_attr( $title ) . '">Apply in-app</button></div>';
					}
				}
				echo '<div class="rb-pos" data-skills="' . $skills_attr . '"><div class="rb-pos__head">' . $logo . '<h3 class="rb-pos__title">' . esc_html( $title ) . '</h3></div><div class="rb-pos__grid">'
					. '<div><span class="rb-label">Residency Title</span><span class="rb-val">' . esc_html( $title ) . '</span></div>'
					. '<div><span class="rb-label">Monthly Salary</span><span class="rb-val">' . esc_html( $salary ) . '</span></div>'
					. '<div><span class="rb-label">ISE Champion Email</span><span class="rb-val"><a href="mailto:' . esc_attr( $champ ) . '">' . esc_html( $champ ) . '</a></span></div>'
					. '<div><span class="rb-label">Email Application Address</span><span class="rb-val"><a href="mailto:' . esc_attr( $apply ) . '">' . esc_html( $apply ) . '</a></span></div>'
					. '</div>' . $skills_html . $apply_ui . '</div>';
			}
		}
		echo '</div><div class="rb-empty" hidden>No positions match your search.</div></div>';
	}
	echo '<div class="jb-modal rb-apply-modal" hidden role="dialog" aria-modal="true"><div class="jb-modal__box"><button class="jb-modal__close" aria-label="Close">&times;</button><div class="rb-apply-body"></div></div></div>';
	echo '</div>';
	echo ise_rb_ajax_js();
	?>
	<script>
	(function(){
	  document.querySelectorAll('.rb-round').forEach(function(round){
	    var input=round.querySelector('.rb-search'), skill=round.querySelector('.rb-skill-filter'),
	        cards=round.querySelectorAll('.rb-pos'), count=round.querySelector('.rb-count'), empty=round.querySelector('.rb-empty');
	    function apply(){ var q=input.value.trim().toLowerCase(), sk=skill?skill.value.toLowerCase():'', n=0;
	      cards.forEach(function(c){
	        var okText=c.textContent.toLowerCase().indexOf(q)>=0;
	        var okSkill=!sk || ((c.getAttribute('data-skills')||'').indexOf(sk)>=0);
	        var show=okText&&okSkill; c.style.display=show?'':'none'; if(show)n++;
	      });
	      if(count) count.textContent=n+(n===1?' position':' positions'); if(empty) empty.hidden=n>0; }
	    input.addEventListener('input',apply); if(skill) skill.addEventListener('change',apply); apply();
	  });
	  var modal=document.querySelector('.rb-apply-modal'); if(modal){
	    var body=modal.querySelector('.rb-apply-body'), jobId=null;
	    function openM(id,title){ jobId=id;
	      body.innerHTML='<h3>Apply — '+title+'</h3><p style="color:var(--ink-70);">Send a short note to the ISE champion with your application.</p>'
	        +'<textarea class="rb-apply-msg" rows="4" placeholder="Why you\'re a fit, links to your work…" style="width:100%;padding:.7rem;border:1px solid var(--line);border-radius:8px;"></textarea>'
	        +'<div style="margin-top:1rem;"><button class="ise-btn ise-btn--primary rb-apply-send">Submit application</button></div>';
	      modal.hidden=false; document.body.style.overflow='hidden'; }
	    function closeM(){ modal.hidden=true; document.body.style.overflow=''; }
	    document.addEventListener('click',function(e){
	      var b=e.target.closest('.rb-apply'); if(b){ openM(b.getAttribute('data-job'), b.getAttribute('data-title')); return; }
	      if(e.target.closest('.rb-apply-modal .jb-modal__close') || e.target===modal){ closeM(); return; }
	      var send=e.target.closest('.rb-apply-send'); if(send){
	        var msg=modal.querySelector('.rb-apply-msg').value; send.disabled=true; send.textContent='Sending…';
	        fetch(window.ISE_AJAX.url,{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},
	          body:'action=ise_apply&nonce='+encodeURIComponent(window.ISE_AJAX.nonce)+'&job='+encodeURIComponent(jobId)+'&message='+encodeURIComponent(msg)})
	          .then(function(r){return r.json();}).then(function(d){
	            body.innerHTML = d && d.success ? '<h3>Application sent</h3><p style="color:var(--ink-70);">The ISE champion has been notified. Track it under <a href="/my-applications/">My applications</a>.</p>' : '<h3>Could not send</h3><p>'+((d&&d.data)||'Please try again.')+'</p>';
	          }).catch(function(){ body.innerHTML='<h3>Could not send</h3><p>Please try again.</p>'; });
	      }
	    });
	    document.addEventListener('keydown',function(e){ if(e.key==='Escape') closeM(); });
	  }
	})();
	</script>
	<?php
	return ob_get_clean();
} );

/* ---------------------------------------------------------------------------
 * [ise_residency_submit] — gated submission form (partners/admins only).
 * Creates a PENDING residency_job for ISE to review.
 * ------------------------------------------------------------------------- */
add_shortcode( 'ise_residency_submit', function () {
	ob_start();
	if ( ! is_user_logged_in() ) {
		echo '<div class="ise-card" style="max-width:520px;"><h3>Partner sign-in required</h3>'
			. '<p style="color:var(--ink-70);">Posting a residency job is for ISE partner companies. Please sign in, or register your company.</p>'
			. '<p><a class="ise-btn ise-btn--primary" href="' . esc_url( wp_login_url( home_url( '/post-a-job/' ) ) ) . '">Sign in</a> '
			. '<a class="ise-btn ise-btn--ghost" href="#register">Register your company</a></p></div>';
		return ob_get_clean();
	}

	if ( ! ise_rb_is_approved( wp_get_current_user() ) ) {
		echo '<div class="ise-card" style="max-width:520px;"><h3>Account pending approval</h3><p style="color:var(--ink-70);">Your company account is awaiting approval by the ISE team. We will email you as soon as you can post roles.</p></div>';
		return ob_get_clean();
	}

	$msg = '';
	if ( 'POST' === $_SERVER['REQUEST_METHOD'] && isset( $_POST['ise_rb_submit'] )
		&& check_admin_referer( 'ise_rb_submit', 'ise_rb_nonce' ) ) {
		$title = sanitize_text_field( wp_unslash( $_POST['rj_title'] ?? '' ) );
		if ( $title ) {
			$id = wp_insert_post( array(
				'post_type'   => ISE_RB_CPT,
				'post_title'  => $title,
				'post_status' => 'pending',           // moderated: ISE approves before it shows
				'post_author' => get_current_user_id(),
			) );
			if ( $id && ! is_wp_error( $id ) ) {
				update_post_meta( $id, '_rj_round',    sanitize_text_field( wp_unslash( $_POST['rj_round'] ?? '' ) ) );
				update_post_meta( $id, '_rj_company',  sanitize_text_field( wp_unslash( $_POST['rj_company'] ?? '' ) ) );
				update_post_meta( $id, '_rj_salary',   sanitize_text_field( wp_unslash( $_POST['rj_salary'] ?? '' ) ) );
				update_post_meta( $id, '_rj_champion', sanitize_email( wp_unslash( $_POST['rj_champion'] ?? '' ) ) );
				update_post_meta( $id, '_rj_apply',    sanitize_email( wp_unslash( $_POST['rj_apply'] ?? '' ) ) );
				$skills_in = sanitize_text_field( wp_unslash( $_POST['rj_skills'] ?? '' ) );
				if ( $skills_in !== '' ) {
					$terms = array_filter( array_map( 'trim', explode( ',', $skills_in ) ) );
					wp_set_object_terms( $id, $terms, ISE_RB_SKILL );
				}
				$msg = '<div class="ise-card" style="border-color:var(--ul-green-modern);"><strong>Thanks — your role was submitted.</strong><br>It will appear on the board once the ISE team approves it.</div>';
				ise_rb_notify( 'New residency role pending review', $title . " was submitted and is pending review.\n\nReview: " . admin_url( 'edit.php?post_type=residency_job&post_status=pending' ) );
			}
		}
	}

	echo $msg;
	$rounds = array_merge( ISE_RB_ROUNDS_OPEN );
	?>
	<form method="post" class="ise-form" style="max-width:560px;display:grid;gap:1rem;">
		<?php wp_nonce_field( 'ise_rb_submit', 'ise_rb_nonce' ); ?>
		<label>Residency title<br><input name="rj_title" required placeholder="e.g. R4 | Acme-01" style="width:100%;padding:.7rem;border:1px solid var(--line);border-radius:8px;"></label>
		<label>Round<br><select name="rj_round" style="width:100%;padding:.7rem;border:1px solid var(--line);border-radius:8px;">
			<?php foreach ( $rounds as $r ) echo '<option>' . esc_html( $r ) . '</option>'; ?>
		</select></label>
		<label>Company (logo slug, optional)<br><input name="rj_company" placeholder="e.g. stripe" style="width:100%;padding:.7rem;border:1px solid var(--line);border-radius:8px;"></label>
		<label>Monthly salary<br><input name="rj_salary" placeholder="e.g. €2,800 / month" style="width:100%;padding:.7rem;border:1px solid var(--line);border-radius:8px;"></label>
		<label>ISE champion email<br><input type="email" name="rj_champion" required style="width:100%;padding:.7rem;border:1px solid var(--line);border-radius:8px;"></label>
		<label>Application email<br><input type="email" name="rj_apply" required style="width:100%;padding:.7rem;border:1px solid var(--line);border-radius:8px;"></label>
		<label>Required skills (comma-separated)<br><input name="rj_skills" placeholder="e.g. Python, React, APIs" style="width:100%;padding:.7rem;border:1px solid var(--line);border-radius:8px;"></label>
		<button class="ise-btn ise-btn--primary" name="ise_rb_submit" value="1" type="submit">Submit for review</button>
	</form>
	<?php
	return ob_get_clean();
} );

/* ---------------------------------------------------------------------------
 * [ise_partner_register] — simple company registration -> Partner role.
 * (MVP: creates the account immediately. For production add admin approval.)
 * ------------------------------------------------------------------------- */
add_shortcode( 'ise_partner_register', function () {
	ob_start();
	echo '<div id="register"></div>';
	if ( is_user_logged_in() ) {
		echo '<p style="color:var(--ink-70);">You are signed in as ' . esc_html( wp_get_current_user()->user_login ) . '.</p>';
		return ob_get_clean();
	}
	if ( 'POST' === $_SERVER['REQUEST_METHOD'] && isset( $_POST['ise_rb_register'] )
		&& check_admin_referer( 'ise_rb_register', 'ise_rb_rnonce' ) ) {
		$email = sanitize_email( wp_unslash( $_POST['reg_email'] ?? '' ) );
		$pass  = (string) ( $_POST['reg_pass'] ?? '' );
		$company = sanitize_text_field( wp_unslash( $_POST['reg_company'] ?? '' ) );
		if ( $email && $pass && ! email_exists( $email ) ) {
			$uid = wp_insert_user( array(
				'user_login'   => $email,
				'user_email'   => $email,
				'user_pass'    => $pass,
				'display_name' => $company,
				'role'         => ISE_RB_ROLE,
			) );
			if ( ! is_wp_error( $uid ) ) {
				update_user_meta( $uid, 'ise_rb_approved', 0 );
				ise_rb_notify( 'New partner account pending approval', $company . ' (' . $email . ") registered and is awaiting approval.\n\nApprove: " . admin_url( 'users.php' ) );
				echo '<div class="ise-card" style="border-color:var(--ul-green-modern);"><strong>Thanks — your company account was created.</strong><br>It is awaiting approval by the ISE team; we will email you when it is active.</div>';
				return ob_get_clean();
			}
		}
		echo '<div class="ise-card" style="border-color:#c0392b;">Could not register — that email may already be in use.</div>';
	}
	?>
	<form method="post" class="ise-form" style="max-width:520px;display:grid;gap:1rem;">
		<?php wp_nonce_field( 'ise_rb_register', 'ise_rb_rnonce' ); ?>
		<label>Company name<br><input name="reg_company" required style="width:100%;padding:.7rem;border:1px solid var(--line);border-radius:8px;"></label>
		<label>Work email<br><input type="email" name="reg_email" required style="width:100%;padding:.7rem;border:1px solid var(--line);border-radius:8px;"></label>
		<label>Password<br><input type="password" name="reg_pass" required minlength="8" style="width:100%;padding:.7rem;border:1px solid var(--line);border-radius:8px;"></label>
		<button class="ise-btn ise-btn--primary" name="ise_rb_register" value="1" type="submit">Register company</button>
	</form>
	<?php
	return ob_get_clean();
} );

/* ---------------------------------------------------------------------------
 * Partner approval + email notifications
 * ------------------------------------------------------------------------- */
function ise_rb_is_approved( $user ) {
	if ( ! $user || ! $user->ID ) { return false; }
	if ( user_can( $user, 'publish_posts' ) ) { return true; } // admins/editors
	return '1' === (string) get_user_meta( $user->ID, 'ise_rb_approved', true );
}

function ise_rb_notify( $subject, $body ) {
	$to = apply_filters( 'ise_rb_notify_email', get_option( 'admin_email' ) );
	if ( $to ) { wp_mail( $to, '[ISE Jobs] ' . $subject, $body ); }
}

/* Users list: Partner status column + one-click approve. */
add_filter( 'manage_users_columns', function ( $cols ) {
	$cols['ise_rb'] = 'Partner status';
	return $cols;
} );
add_filter( 'manage_users_custom_column', function ( $val, $col, $uid ) {
	if ( 'ise_rb' !== $col ) { return $val; }
	$u = get_userdata( $uid );
	if ( ! $u || ! in_array( ISE_RB_ROLE, (array) $u->roles, true ) ) { return '—'; }
	if ( '1' === (string) get_user_meta( $uid, 'ise_rb_approved', true ) ) {
		return '<span style="color:#00842b;font-weight:600;">Approved</span>';
	}
	$link = wp_nonce_url( admin_url( 'admin-post.php?action=ise_rb_approve&user=' . $uid ), 'ise_rb_approve_' . $uid );
	return '<span style="color:#b8860b;font-weight:600;">Pending</span> &middot; <a href="' . esc_url( $link ) . '">Approve</a>';
}, 10, 3 );

add_action( 'admin_post_ise_rb_approve', function () {
	if ( ! current_user_can( 'edit_users' ) ) { wp_die( 'No permission.' ); }
	$uid = (int) ( $_GET['user'] ?? 0 );
	check_admin_referer( 'ise_rb_approve_' . $uid );
	update_user_meta( $uid, 'ise_rb_approved', 1 );
	$u = get_userdata( $uid );
	if ( $u ) {
		wp_mail( $u->user_email, '[ISE Jobs] Your partner account is approved',
			"Your ISE partner account is now active. You can post residency roles at " . home_url( '/post-a-job/' ) );
	}
	wp_safe_redirect( admin_url( 'users.php' ) );
	exit;
} );

/* Skills taxonomy on residencies + Student role + skill seed (idempotent). */
add_action( 'init', function () {
	register_taxonomy( ISE_RB_SKILL, ISE_RB_CPT, array(
		'labels'       => array( 'name' => 'Skills', 'singular_name' => 'Skill' ),
		'public'       => false,
		'show_ui'      => true,
		'show_admin_column' => true,
		'hierarchical' => false,
	) );
	if ( ! get_role( ISE_RB_STUDENT ) ) {
		add_role( ISE_RB_STUDENT, 'Student', array( 'read' => true ) );
	}
	if ( ! get_option( 'ise_rb_skills_seeded' ) ) {
		$by_company = array(
			'stripe'   => array( 'Go', 'Ruby', 'Distributed Systems' ),
			'intercom' => array( 'Ruby', 'React', 'APIs' ),
			'provizio' => array( 'Python', 'C++', 'Computer Vision' ),
			'tines'    => array( 'Python', 'Security', 'APIs' ),
			'kneat'    => array( 'C#', '.NET', 'Cloud' ),
			'wayflyer' => array( 'TypeScript', 'React', 'Data' ),
		);
		$jobs = get_posts( array( 'post_type' => ISE_RB_CPT, 'post_status' => 'publish', 'numberposts' => -1 ) );
		foreach ( $jobs as $j ) {
			$co = get_post_meta( $j->ID, '_rj_company', true );
			if ( isset( $by_company[ $co ] ) ) {
				wp_set_object_terms( $j->ID, $by_company[ $co ], ISE_RB_SKILL );
			}
		}
		update_option( 'ise_rb_skills_seeded', 1 );
	}
} );

/* ===========================================================================
 * STUDENT SIDE: accounts, profiles (photo/skills/CV/website/GitHub), directory
 * ========================================================================= */
function ise_rb_is_student( $user ) {
	return $user && $user->ID && in_array( ISE_RB_STUDENT, (array) $user->roles, true );
}
function ise_sp_get( $uid, $k ) { return get_user_meta( $uid, '_sp_' . $k, true ); }
function ise_sp_skills( $uid ) {
	return array_values( array_filter( array_map( 'trim', explode( ',', (string) ise_sp_get( $uid, 'skills' ) ) ) ) );
}

/* Seed one demo student profile so the directory/profile pages have content. */
add_action( 'init', function () {
	if ( get_option( 'ise_rb_demo_student' ) ) { return; }
	if ( ! get_role( ISE_RB_STUDENT ) ) { return; }
	if ( ! email_exists( 'demo.student@example.com' ) ) {
		$uid = wp_insert_user( array(
			'user_login'   => 'demo.student@example.com',
			'user_email'   => 'demo.student@example.com',
			'user_pass'    => wp_generate_password( 20 ),
			'display_name' => 'Demo Student',
			'first_name'   => 'Demo', 'last_name' => 'Student',
			'role'         => ISE_RB_STUDENT,
		) );
		if ( ! is_wp_error( $uid ) ) {
			update_user_meta( $uid, '_sp_headline', '2nd-year ISE student · Residency 3' );
			update_user_meta( $uid, '_sp_skills',   'Python, React, Go, APIs' );
			update_user_meta( $uid, '_sp_bio',      'Building web and data projects. Looking for a Residency 4 placement in backend or ML.' );
			update_user_meta( $uid, '_sp_cv',       'https://example.com/demo-cv.pdf' );
			update_user_meta( $uid, '_sp_website',  'https://example.com' );
			update_user_meta( $uid, '_sp_github',   'https://github.com/example' );
		}
	}
	update_option( 'ise_rb_demo_student', 1 );
} );

/* Render one student profile card (photo/initials + details). */
function ise_rb_render_profile( $user, $compact = false ) {
	$uid = $user->ID;
	$photo = ise_sp_get( $uid, 'photo' );
	$img   = $photo ? wp_get_attachment_image_url( $photo, 'medium' ) : '';
	$name  = $user->display_name ? $user->display_name : $user->user_login;
	$initials = strtoupper( mb_substr( $name, 0, 1 ) );
	$head  = ise_sp_get( $uid, 'headline' );
	$bio   = ise_sp_get( $uid, 'bio' );
	$cv    = ise_sp_get( $uid, 'cv' );
	$site  = ise_sp_get( $uid, 'website' );
	$gh    = ise_sp_get( $uid, 'github' );
	$skills= ise_sp_skills( $uid );
	$out  = '<div class="sp-card">';
	$out .= '<div class="sp-card__head">';
	$out .= $img ? '<img class="sp-photo" src="' . esc_url( $img ) . '" alt="">' : '<span class="sp-photo sp-photo--initials">' . esc_html( $initials ) . '</span>';
	$out .= '<div><h3 class="sp-name">' . esc_html( $name ) . '</h3>';
	if ( $head ) { $out .= '<div class="sp-headline">' . esc_html( $head ) . '</div>'; }
	$out .= '</div></div>';
	if ( $bio && ! $compact ) { $out .= '<p class="sp-bio">' . esc_html( $bio ) . '</p>'; }
	if ( $skills ) {
		$out .= '<div class="sp-skills"><span class="rb-skills__label">Skills</span>';
		foreach ( $skills as $sk ) { $out .= '<span class="jb-tag">' . esc_html( $sk ) . '</span>'; }
		$out .= '</div>';
	}
	$links = array();
	if ( $site ) { $links[] = '<a href="' . esc_url( $site ) . '" target="_blank" rel="noopener">Website</a>'; }
	if ( $cv )   { $links[] = '<a href="' . esc_url( $cv ) . '" target="_blank" rel="noopener">CV</a>'; }
	if ( $gh )   { $links[] = '<a href="' . esc_url( $gh ) . '" target="_blank" rel="noopener">GitHub</a>'; }
	if ( $links ) { $out .= '<div class="sp-links">' . implode( '', $links ) . '</div>'; }
	$out .= '</div>';
	return $out;
}

/* [ise_student_register] — student self-registration (immediate). */
add_shortcode( 'ise_student_register', function () {
	ob_start();
	echo '<div class="ise-container" style="max-width:560px;padding-block:3rem 4rem;">';
	if ( is_user_logged_in() ) {
		echo '<div class="ise-card"><p>You are signed in as ' . esc_html( wp_get_current_user()->display_name ) . '. '
			. '<a href="' . esc_url( home_url( '/profile/' ) ) . '">Edit your profile</a> or <a href="' . esc_url( home_url( '/jobs/' ) ) . '">view the board</a>.</p></div>';
		echo '</div>'; return ob_get_clean();
	}
	if ( 'POST' === $_SERVER['REQUEST_METHOD'] && isset( $_POST['ise_sr'] ) && check_admin_referer( 'ise_sr', 'ise_sr_nonce' ) ) {
		$name  = sanitize_text_field( wp_unslash( $_POST['sr_name'] ?? '' ) );
		$email = sanitize_email( wp_unslash( $_POST['sr_email'] ?? '' ) );
		$pass  = (string) ( $_POST['sr_pass'] ?? '' );
		if ( $email && $pass && ! email_exists( $email ) ) {
			$uid = wp_insert_user( array( 'user_login' => $email, 'user_email' => $email, 'user_pass' => $pass, 'display_name' => $name, 'role' => ISE_RB_STUDENT ) );
			if ( ! is_wp_error( $uid ) ) {
				wp_set_current_user( $uid ); wp_set_auth_cookie( $uid );
				echo '<div class="ise-card" style="border-color:var(--ul-green-modern);"><strong>Welcome to ISE.</strong> '
					. '<a href="' . esc_url( home_url( '/profile/' ) ) . '">Set up your profile</a> or <a href="' . esc_url( home_url( '/jobs/' ) ) . '">view residencies</a>.</div>';
				echo '</div>'; return ob_get_clean();
			}
		}
		echo '<div class="ise-card" style="border-color:#c0392b;">Could not register — that email may already be in use.</div>';
	}
	?>
	<form method="post" class="ise-form" style="display:grid;gap:1rem;">
		<?php wp_nonce_field( 'ise_sr', 'ise_sr_nonce' ); ?>
		<label>Full name<br><input name="sr_name" required style="width:100%;padding:.7rem;border:1px solid var(--line);border-radius:8px;"></label>
		<label>Email<br><input type="email" name="sr_email" required style="width:100%;padding:.7rem;border:1px solid var(--line);border-radius:8px;"></label>
		<label>Password<br><input type="password" name="sr_pass" required minlength="8" style="width:100%;padding:.7rem;border:1px solid var(--line);border-radius:8px;"></label>
		<button class="ise-btn ise-btn--primary" name="ise_sr" value="1" type="submit">Create student account</button>
	</form>
	<?php
	echo '</div>'; return ob_get_clean();
} );

/* [ise_student_profile] — edit + preview your own profile (gated). */
add_shortcode( 'ise_student_profile', function () {
	ob_start();
	echo '<div class="ise-container" style="max-width:900px;padding-block:3rem 4rem;">';
	if ( ! is_user_logged_in() ) {
		echo '<div class="ise-card"><h3>Sign in required</h3><p style="color:var(--ink-70);">Your profile is private to you. Sign in or create a student account.</p>'
			. '<p><a class="ise-btn ise-btn--primary" href="' . esc_url( wp_login_url( home_url( '/profile/' ) ) ) . '">Sign in</a> '
			. '<a class="ise-btn ise-btn--ghost" href="' . esc_url( home_url( '/join/' ) ) . '">Create account</a></p></div>';
		echo '</div>'; return ob_get_clean();
	}
	$uid = get_current_user_id();
	if ( 'POST' === $_SERVER['REQUEST_METHOD'] && isset( $_POST['ise_sp_save'] ) && check_admin_referer( 'ise_sp_save', 'ise_sp_nonce' ) ) {
		update_user_meta( $uid, '_sp_headline', sanitize_text_field( wp_unslash( $_POST['sp_headline'] ?? '' ) ) );
		update_user_meta( $uid, '_sp_skills',   sanitize_text_field( wp_unslash( $_POST['sp_skills'] ?? '' ) ) );
		update_user_meta( $uid, '_sp_bio',      sanitize_textarea_field( wp_unslash( $_POST['sp_bio'] ?? '' ) ) );
		update_user_meta( $uid, '_sp_cv',       esc_url_raw( wp_unslash( $_POST['sp_cv'] ?? '' ) ) );
		update_user_meta( $uid, '_sp_website',  esc_url_raw( wp_unslash( $_POST['sp_website'] ?? '' ) ) );
		update_user_meta( $uid, '_sp_github',   esc_url_raw( wp_unslash( $_POST['sp_github'] ?? '' ) ) );
		if ( ! empty( $_FILES['sp_photo']['name'] ) && 0 === strpos( (string) $_FILES['sp_photo']['type'], 'image/' ) ) {
			require_once ABSPATH . 'wp-admin/includes/image.php';
			require_once ABSPATH . 'wp-admin/includes/file.php';
			require_once ABSPATH . 'wp-admin/includes/media.php';
			$att = media_handle_upload( 'sp_photo', 0 );
			if ( ! is_wp_error( $att ) ) { update_user_meta( $uid, '_sp_photo', $att ); }
		}
		echo '<div class="ise-card" style="border-color:var(--ul-green-modern);margin-bottom:1.5rem;"><strong>Profile saved.</strong></div>';
	}
	$u = wp_get_current_user();
	echo '<div class="sp-grid"><div>';
	echo '<p class="ise-eyebrow">Preview</p>' . ise_rb_render_profile( $u );
	echo '</div><div>';
	echo '<p class="ise-eyebrow">Edit your profile</p>';
	$val = function ( $k ) use ( $uid ) { return esc_attr( ise_sp_get( $uid, $k ) ); };
	?>
	<form method="post" enctype="multipart/form-data" class="ise-form" style="display:grid;gap:1rem;">
		<?php wp_nonce_field( 'ise_sp_save', 'ise_sp_nonce' ); ?>
		<label>Photo<br><input type="file" name="sp_photo" accept="image/*"></label>
		<label>Headline<br><input name="sp_headline" value="<?php echo $val('headline'); ?>" placeholder="e.g. 2nd-year ISE student" style="width:100%;padding:.7rem;border:1px solid var(--line);border-radius:8px;"></label>
		<label>Skills (comma-separated)<br><input name="sp_skills" value="<?php echo $val('skills'); ?>" placeholder="Python, React, Go" style="width:100%;padding:.7rem;border:1px solid var(--line);border-radius:8px;"></label>
		<label>Short bio<br><textarea name="sp_bio" rows="3" style="width:100%;padding:.7rem;border:1px solid var(--line);border-radius:8px;"><?php echo esc_textarea( ise_sp_get( $uid, 'bio' ) ); ?></textarea></label>
		<label>Website / portfolio URL<br><input type="url" name="sp_website" value="<?php echo $val('website'); ?>" style="width:100%;padding:.7rem;border:1px solid var(--line);border-radius:8px;"></label>
		<label>CV URL<br><input type="url" name="sp_cv" value="<?php echo $val('cv'); ?>" style="width:100%;padding:.7rem;border:1px solid var(--line);border-radius:8px;"></label>
		<label>GitHub URL<br><input type="url" name="sp_github" value="<?php echo $val('github'); ?>" style="width:100%;padding:.7rem;border:1px solid var(--line);border-radius:8px;"></label>
		<button class="ise-btn ise-btn--primary" name="ise_sp_save" value="1" type="submit">Save profile</button>
	</form>
	<?php
	echo '</div></div></div>'; return ob_get_clean();
} );

/* [ise_student_directory] — signed-in partners/students browse student profiles. */
add_shortcode( 'ise_student_directory', function () {
	ob_start();
	echo '<div class="ise-container" style="padding-block:3rem 4rem;">';
	if ( ! is_user_logged_in() ) {
		echo '<div class="ise-card" style="max-width:560px;"><h3>Sign in to browse students</h3>'
			. '<p style="color:var(--ink-70);">The student directory is visible to signed-in ISE partners and students.</p>'
			. '<p><a class="ise-btn ise-btn--primary" href="' . esc_url( wp_login_url( home_url( '/students-directory/' ) ) ) . '">Sign in</a></p></div>';
		echo '</div>'; return ob_get_clean();
	}
	$user = wp_get_current_user();
	$is_partner = in_array( ISE_RB_ROLE, (array) $user->roles, true ) || user_can( $user, 'edit_posts' );
	$favs = ise_partner_favourites( $user->ID );

	// Single profile view (?student=ID), e.g. from an applicant list.
	$single = isset( $_GET['student'] ) ? (int) $_GET['student'] : 0;
	if ( $single ) {
		$st = get_userdata( $single );
		echo '<p><a href="' . esc_url( home_url( '/students-directory/' ) ) . '">&larr; All students</a></p>';
		if ( $st ) { echo '<div style="max-width:560px;">' . ise_rb_render_profile( $st ) . '</div>'; }
		echo '</div>'; return ob_get_clean();
	}

	$students = get_users( array( 'role' => ISE_RB_STUDENT, 'number' => 200 ) );
	$all_skills = array();
	foreach ( $students as $st ) { foreach ( ise_sp_skills( $st->ID ) as $sk ) { $all_skills[ $sk ] = 1; } }
	$all_skills = array_keys( $all_skills ); sort( $all_skills );

	echo ise_rb_ajax_js();
	echo '<div class="rb-tools"' . ( $is_partner ? ' style="grid-template-columns:2fr 1fr auto;"' : '' ) . '>';
	echo '<input class="rb-search sp-search" type="search" placeholder="Search students by name or skill…">';
	echo '<select class="rb-skill-filter sp-skill"><option value="">All skills</option>';
	foreach ( $all_skills as $sk ) { echo '<option value="' . esc_attr( strtolower( $sk ) ) . '">' . esc_html( $sk ) . '</option>'; }
	echo '</select>';
	if ( $is_partner ) { echo '<label class="sp-savedonly"><input type="checkbox" class="sp-saved-toggle"> Saved only</label>'; }
	echo '</div><div class="sp-count"></div>';

	echo '<div class="sp-directory">';
	if ( $students ) {
		foreach ( $students as $st ) {
			$sk = ise_sp_skills( $st->ID );
			$is_fav = in_array( (int) $st->ID, $favs, true );
			$favbtn = $is_partner ? '<button class="sp-fav' . ( $is_fav ? ' is-fav' : '' ) . '" data-student="' . (int) $st->ID . '" title="Save student" aria-label="Save student">&#9829;</button>' : '';
			echo '<div class="sp-dir-item" data-name="' . esc_attr( strtolower( $st->display_name ) ) . '" data-skills="' . esc_attr( strtolower( implode( ',', $sk ) ) ) . '" data-fav="' . ( $is_fav ? '1' : '0' ) . '">'
				. $favbtn . ise_rb_render_profile( $st, true ) . '</div>';
		}
	} else {
		echo '<p style="color:var(--ink-70);">No student profiles yet.</p>';
	}
	echo '</div>';
	?>
	<script>
	(function(){
	  var search=document.querySelector('.sp-search'), skill=document.querySelector('.sp-skill'),
	      saved=document.querySelector('.sp-saved-toggle'), items=document.querySelectorAll('.sp-dir-item'),
	      count=document.querySelector('.sp-count');
	  function apply(){ var q=(search?search.value:'').trim().toLowerCase(), sk=skill?skill.value.toLowerCase():'', so=saved&&saved.checked, n=0;
	    items.forEach(function(it){
	      var okText=(it.getAttribute('data-name')+' '+it.getAttribute('data-skills')).indexOf(q)>=0;
	      var okSkill=!sk||(it.getAttribute('data-skills')||'').indexOf(sk)>=0;
	      var okSaved=!so||it.getAttribute('data-fav')==='1';
	      var show=okText&&okSkill&&okSaved; it.style.display=show?'':'none'; if(show)n++;
	    });
	    if(count) count.textContent=n+(n===1?' student':' students');
	  }
	  if(search) search.addEventListener('input',apply);
	  if(skill) skill.addEventListener('change',apply);
	  if(saved) saved.addEventListener('change',apply);
	  document.addEventListener('click',function(e){
	    var b=e.target.closest('.sp-fav'); if(!b) return;
	    fetch(window.ISE_AJAX.url,{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},
	      body:'action=ise_fav&nonce='+encodeURIComponent(window.ISE_AJAX.nonce)+'&student='+encodeURIComponent(b.getAttribute('data-student'))})
	      .then(function(r){return r.json();}).then(function(d){ if(d&&d.success){ var on=d.data.saved; b.classList.toggle('is-fav',on); b.closest('.sp-dir-item').setAttribute('data-fav',on?'1':'0'); apply(); } });
	  });
	  apply();
	})();
	</script>
	<?php
	echo '</div>'; return ob_get_clean();
} );

/* ===========================================================================
 * APPLICATIONS (in-app apply) + FAVOURITES (partners saving students)
 * ========================================================================= */
add_action( 'init', function () {
	register_post_type( ISE_RB_APP, array(
		'labels'          => array( 'name' => 'Applications', 'singular_name' => 'Application' ),
		'public'          => false,
		'show_ui'         => true,
		'show_in_menu'    => true,
		'menu_icon'       => 'dashicons-email',
		'supports'        => array( 'title' ),
		'capability_type' => 'post',
		'map_meta_cap'    => true,
	) );
} );

function ise_rb_ajax_js() {
	return '<script>window.ISE_AJAX={url:' . wp_json_encode( admin_url( 'admin-ajax.php' ) )
		. ',nonce:' . wp_json_encode( wp_create_nonce( 'ise_ajax' ) ) . '};</script>';
}

/* --- applications --- */
function ise_ra_has_applied( $student_id, $job_id ) {
	$q = get_posts( array(
		'post_type'   => ISE_RB_APP, 'post_status' => 'any', 'numberposts' => 1, 'fields' => 'ids',
		'meta_query'  => array( 'relation' => 'AND',
			array( 'key' => '_ra_student', 'value' => (int) $student_id ),
			array( 'key' => '_ra_job',     'value' => (int) $job_id ),
		),
	) );
	return ! empty( $q );
}

add_action( 'wp_ajax_ise_apply', function () {
	check_ajax_referer( 'ise_ajax', 'nonce' );
	$user = wp_get_current_user();
	if ( ! ise_rb_is_student( $user ) ) { wp_send_json_error( 'Students only.', 403 ); }
	$job = (int) ( $_POST['job'] ?? 0 );
	$job_post = get_post( $job );
	if ( ! $job_post || ISE_RB_CPT !== $job_post->post_type ) { wp_send_json_error( 'Unknown role.', 400 ); }
	if ( ise_ra_has_applied( $user->ID, $job ) ) { wp_send_json_error( 'You have already applied.', 409 ); }
	$msg = sanitize_textarea_field( wp_unslash( $_POST['message'] ?? '' ) );
	$id = wp_insert_post( array(
		'post_type'   => ISE_RB_APP,
		'post_status' => 'publish',
		'post_author' => $user->ID,
		'post_title'  => $user->display_name . ' → ' . get_the_title( $job ),
	) );
	if ( is_wp_error( $id ) || ! $id ) { wp_send_json_error( 'Could not submit.', 500 ); }
	update_post_meta( $id, '_ra_student', $user->ID );
	update_post_meta( $id, '_ra_job', $job );
	update_post_meta( $id, '_ra_message', $msg );
	update_post_meta( $id, '_ra_status', 'pending' );
	$champ = get_post_meta( $job, '_rj_champion', true );
	if ( $champ ) {
		wp_mail( $champ, '[ISE Jobs] New application: ' . get_the_title( $job ),
			$user->display_name . " applied for " . get_the_title( $job ) . ".\n\n" . $msg );
	}
	ise_rb_notify( 'New residency application', $user->display_name . ' applied for ' . get_the_title( $job ) );
	wp_send_json_success( 'applied' );
} );

/* --- favourites (partner saves a student) --- */
function ise_partner_favourites( $uid ) {
	$f = get_user_meta( $uid, '_sp_favourites', true );
	return is_array( $f ) ? array_map( 'intval', $f ) : array();
}

add_action( 'wp_ajax_ise_fav', function () {
	check_ajax_referer( 'ise_ajax', 'nonce' );
	$user = wp_get_current_user();
	$is_partner = in_array( ISE_RB_ROLE, (array) $user->roles, true ) || user_can( $user, 'edit_posts' );
	if ( ! $is_partner ) { wp_send_json_error( 'Partners only.', 403 ); }
	$sid = (int) ( $_POST['student'] ?? 0 );
	$favs = ise_partner_favourites( $user->ID );
	if ( in_array( $sid, $favs, true ) ) {
		$favs = array_values( array_diff( $favs, array( $sid ) ) ); $saved = false;
	} else {
		$favs[] = $sid; $saved = true;
	}
	update_user_meta( $user->ID, '_sp_favourites', $favs );
	wp_send_json_success( array( 'saved' => $saved ) );
} );

/* --- application status update (partner shortlists/rejects) --- */
add_action( 'wp_ajax_ise_appstatus', function () {
	check_ajax_referer( 'ise_ajax', 'nonce' );
	$user = wp_get_current_user();
	$app = (int) ( $_POST['app'] ?? 0 );
	$status = sanitize_key( $_POST['status'] ?? '' );
	if ( ! in_array( $status, array( 'pending', 'shortlisted', 'rejected' ), true ) ) { wp_send_json_error( 'Bad status.', 400 ); }
	$job = (int) get_post_meta( $app, '_ra_job', true );
	$job_post = get_post( $job );
	$owner = $job_post ? (int) $job_post->post_author : 0;
	if ( $owner !== $user->ID && ! current_user_can( 'edit_others_posts' ) ) { wp_send_json_error( 'Not your role.', 403 ); }
	update_post_meta( $app, '_ra_status', $status );
	wp_send_json_success( array( 'status' => $status ) );
} );

function ise_ra_badge( $status ) {
	$map = array( 'pending' => '#b8860b', 'shortlisted' => '#00842b', 'rejected' => '#c0392b' );
	$c = $map[ $status ] ?? '#6b746f';
	return '<span class="jb-tag" style="color:' . $c . ';background:rgba(0,0,0,.04);">' . esc_html( ucfirst( $status ) ) . '</span>';
}

/* [ise_my_applications] — a student's own applications. */
add_shortcode( 'ise_my_applications', function () {
	ob_start();
	echo '<div class="ise-container" style="max-width:820px;padding-block:3rem 4rem;">';
	if ( ! is_user_logged_in() ) {
		echo '<div class="ise-card"><p>Sign in to view your applications. <a href="' . esc_url( wp_login_url( home_url( '/my-applications/' ) ) ) . '">Sign in</a></p></div></div>';
		return ob_get_clean();
	}
	$apps = get_posts( array( 'post_type' => ISE_RB_APP, 'post_status' => 'any', 'numberposts' => -1,
		'author' => get_current_user_id(), 'orderby' => 'date', 'order' => 'DESC' ) );
	if ( ! $apps ) { echo '<div class="ise-card"><p style="color:var(--ink-70);">You have not applied to any residencies yet. <a href="' . esc_url( home_url( '/jobs/' ) ) . '">Browse the board</a>.</p></div>'; }
	foreach ( $apps as $a ) {
		$job = (int) get_post_meta( $a->ID, '_ra_job', true );
		$status = get_post_meta( $a->ID, '_ra_status', true ) ?: 'pending';
		echo '<div class="ise-card" style="margin-bottom:1rem;display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap;">'
			. '<div><strong>' . esc_html( get_the_title( $job ) ) . '</strong><br><span style="color:var(--ink-50);font-size:.85rem;">Applied ' . esc_html( get_the_date( '', $a ) ) . '</span></div>'
			. ise_ra_badge( $status ) . '</div>';
	}
	echo '</div>';
	return ob_get_clean();
} );

/* [ise_my_applicants] — applications to the current partner's residencies. */
add_shortcode( 'ise_my_applicants', function () {
	ob_start();
	echo '<div class="ise-container" style="max-width:900px;padding-block:3rem 4rem;">';
	$user = wp_get_current_user();
	$is_partner = is_user_logged_in() && ( in_array( ISE_RB_ROLE, (array) $user->roles, true ) || user_can( $user, 'edit_posts' ) );
	if ( ! $is_partner ) {
		echo '<div class="ise-card"><p>Sign in as a partner to view applicants. <a href="' . esc_url( wp_login_url( home_url( '/my-applicants/' ) ) ) . '">Sign in</a></p></div></div>';
		return ob_get_clean();
	}
	$my_jobs = get_posts( array( 'post_type' => ISE_RB_CPT, 'post_status' => 'any', 'numberposts' => -1,
		'author' => ( current_user_can( 'edit_others_posts' ) ? '' : get_current_user_id() ), 'fields' => 'ids' ) );
	$apps = $my_jobs ? get_posts( array( 'post_type' => ISE_RB_APP, 'post_status' => 'any', 'numberposts' => -1,
		'meta_query' => array( array( 'key' => '_ra_job', 'value' => $my_jobs, 'compare' => 'IN' ) ), 'orderby' => 'date', 'order' => 'DESC' ) ) : array();
	if ( ! $apps ) { echo '<div class="ise-card"><p style="color:var(--ink-70);">No applications yet.</p></div>'; }
	echo ise_rb_ajax_js();
	foreach ( $apps as $a ) {
		$job = (int) get_post_meta( $a->ID, '_ra_job', true );
		$sid = (int) get_post_meta( $a->ID, '_ra_student', true );
		$st  = get_userdata( $sid );
		$status = get_post_meta( $a->ID, '_ra_status', true ) ?: 'pending';
		$msg = get_post_meta( $a->ID, '_ra_message', true );
		echo '<div class="ise-card" style="margin-bottom:1.25rem;">'
			. '<div style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;align-items:center;">'
			. '<div><strong>' . esc_html( $st ? $st->display_name : 'Student' ) . '</strong> · <span style="color:var(--ink-70);">' . esc_html( get_the_title( $job ) ) . '</span></div>'
			. '<span class="ra-badge">' . ise_ra_badge( $status ) . '</span></div>'
			. ( $msg ? '<p style="color:var(--ink-70);margin:.75rem 0 0;">' . esc_html( $msg ) . '</p>' : '' )
			. '<div class="ra-actions" data-app="' . (int) $a->ID . '" style="margin-top:1rem;display:flex;gap:.75rem;flex-wrap:wrap;">'
			. ( $sid ? '<a class="ise-btn ise-btn--ghost" href="' . esc_url( add_query_arg( 'student', $sid, home_url( '/students-directory/' ) ) ) . '">View profile</a>' : '' )
			. '<button class="ise-btn ise-btn--primary ra-set" data-status="shortlisted">Shortlist</button>'
			. '<button class="ise-btn ise-btn--ghost ra-set" data-status="rejected">Reject</button>'
			. '</div></div>';
	}
	?>
	<script>
	document.addEventListener('click',function(e){
	  var b=e.target.closest('.ra-set'); if(!b) return;
	  var row=b.closest('.ise-card'), app=row.querySelector('.ra-actions').getAttribute('data-app'), status=b.getAttribute('data-status');
	  b.disabled=true;
	  fetch(window.ISE_AJAX.url,{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},
	    body:'action=ise_appstatus&nonce='+encodeURIComponent(window.ISE_AJAX.nonce)+'&app='+encodeURIComponent(app)+'&status='+encodeURIComponent(status)})
	    .then(function(r){return r.json();}).then(function(d){ b.disabled=false;
	      if(d&&d.success){ var badge=row.querySelector('.ra-badge'); if(badge){ badge.innerHTML='<span class="jb-tag">'+status.charAt(0).toUpperCase()+status.slice(1)+'</span>'; } }
	    }).catch(function(){ b.disabled=false; });
	});
	</script>
	<?php
	echo '</div>';
	return ob_get_clean();
} );
