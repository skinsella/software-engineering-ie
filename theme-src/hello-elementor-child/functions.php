<?php
/**
 * ISE — Hello Elementor Child: theme bootstrap.
 *
 * Loads the parent (Hello Elementor) stylesheet, then the child brand
 * stylesheet (UL design tokens + utility classes), then the UL fonts.
 *
 * Fonts: brand primaries are Saol / Inter / Formula Condensed. Here we load
 * the licence-clean UL-sanctioned fallbacks (Cormorant Garamond / Inter /
 * Roboto Condensed) from Google Fonts. For production, self-host these (and
 * swap in licensed Saol/Formula Condensed files) to satisfy GDPR + brand.
 *
 * @package hello-elementor-child
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // No direct access.
}

/**
 * Enqueue parent + child styles and UL brand fonts.
 */
function ise_child_enqueue_assets() {
	// Parent Hello Elementor theme stylesheet.
	wp_enqueue_style(
		'hello-elementor-parent',
		get_template_directory_uri() . '/style.css',
		array(),
		wp_get_theme( 'hello-elementor' )->get( 'Version' )
	);

	// UL brand fonts (fallback families). Preconnect improves first paint.
	wp_enqueue_style(
		'ise-ul-fonts',
		'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Roboto+Condensed:wght@400;500;700&display=swap',
		array(),
		null
	);

	// Child brand stylesheet (design tokens + utility classes).
	wp_enqueue_style(
		'hello-elementor-child',
		get_stylesheet_directory_uri() . '/style.css',
		array( 'hello-elementor-parent', 'ise-ul-fonts' ),
		wp_get_theme()->get( 'Version' )
	);
}
add_action( 'wp_enqueue_scripts', 'ise_child_enqueue_assets', 20 );

/**
 * Add font preconnect resource hints for performance.
 */
function ise_child_resource_hints( $hints, $relation ) {
	if ( 'preconnect' === $relation ) {
		$hints[] = 'https://fonts.googleapis.com';
		$hints[] = array( 'href' => 'https://fonts.gstatic.com', 'crossorigin' );
	}
	return $hints;
}
add_filter( 'wp_resource_hints', 'ise_child_resource_hints', 10, 2 );

/**
 * Register brand editor colour palette so the block/Elementor editor exposes
 * UL greens as named swatches (keeps content authors on-brand).
 */
function ise_child_editor_palette() {
	add_theme_support( 'editor-color-palette', array(
		array( 'name' => 'UL Green',          'slug' => 'ul-green',          'color' => '#005335' ),
		array( 'name' => 'UL Modern Green',   'slug' => 'ul-green-modern',   'color' => '#00B140' ),
		array( 'name' => 'UL Heritage Green', 'slug' => 'ul-green-heritage', 'color' => '#003726' ),
		array( 'name' => 'Ink',               'slug' => 'ink',               'color' => '#16211c' ),
		array( 'name' => 'Paper Off-white',   'slug' => 'paper-off',         'color' => '#f6f8f7' ),
		array( 'name' => 'Paper',             'slug' => 'paper',             'color' => '#ffffff' ),
	) );
}
add_action( 'after_setup_theme', 'ise_child_editor_palette' );
