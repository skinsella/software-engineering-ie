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
				echo '<div class="rb-pos" data-skills="' . $skills_attr . '"><div class="rb-pos__head">' . $logo . '<h3 class="rb-pos__title">' . esc_html( $title ) . '</h3></div><div class="rb-pos__grid">'
					. '<div><span class="rb-label">Residency Title</span><span class="rb-val">' . esc_html( $title ) . '</span></div>'
					. '<div><span class="rb-label">Monthly Salary</span><span class="rb-val">' . esc_html( $salary ) . '</span></div>'
					. '<div><span class="rb-label">ISE Champion Email</span><span class="rb-val"><a href="mailto:' . esc_attr( $champ ) . '">' . esc_html( $champ ) . '</a></span></div>'
					. '<div><span class="rb-label">Email Application Address</span><span class="rb-val"><a href="mailto:' . esc_attr( $apply ) . '">' . esc_html( $apply ) . '</a></span></div>'
					. '</div>' . $skills_html . '</div>';
			}
		}
		echo '</div><div class="rb-empty" hidden>No positions match your search.</div></div>';
	}
	echo '</div>';
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
	$students = get_users( array( 'role' => ISE_RB_STUDENT, 'number' => 100 ) );
	echo '<div class="sp-directory">';
	if ( $students ) {
		foreach ( $students as $st ) { echo ise_rb_render_profile( $st, true ); }
	} else {
		echo '<p style="color:var(--ink-70);">No student profiles yet.</p>';
	}
	echo '</div></div>'; return ob_get_clean();
} );
