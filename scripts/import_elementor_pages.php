<?php
/**
 * Run via: wp eval-file scripts/import_elementor_pages.php
 *
 * Imports exports/elementor-templates/*.json as real WordPress pages carrying
 * Elementor builder data — the same postmeta Elementor itself writes when you
 * "Import Templates" then apply one to a page (docs/HANDOFF.md steps 3-5),
 * just scripted for a repeatable deploy. Idempotent: re-running updates the
 * existing page found by slug instead of creating duplicates.
 */

$repo = dirname(__DIR__);
$manifest = json_decode(file_get_contents("$repo/exports/elementor-templates/manifest.json"), true);
$elementor_version = defined('ELEMENTOR_VERSION') ? ELEMENTOR_VERSION : '3.30.0';

$front_page_id = null;

foreach ($manifest['pages'] as $entry) {
    $file = "$repo/exports/elementor-templates/{$entry['file']}";
    $tpl = json_decode(file_get_contents($file), true);
    if (!$tpl || !isset($tpl['content'])) {
        WP_CLI::warning("Skipping {$entry['file']}: invalid or empty template JSON");
        continue;
    }

    $existing = get_page_by_path($entry['slug'], OBJECT, 'page');
    // wp_insert_post()/update_post_meta() both call wp_unslash() on their input
    // internally (WP's historical convention: they expect data as it would
    // arrive from $_POST, already slashed). Since our content has real
    // backslashes (escaped quotes inside inline HTML/CSS), we must wp_slash()
    // everything going in or those backslashes get silently stripped, which
    // corrupts _elementor_data's JSON. This is exactly what Elementor's own
    // save code does before calling update_post_meta().
    $post_id = wp_insert_post(wp_slash([
        'ID'           => $existing ? $existing->ID : 0,
        'post_title'   => $entry['title'],
        'post_name'    => $entry['slug'],
        'post_type'    => 'page',
        'post_status'  => 'publish',
        'post_content' => '',
    ]), true);

    if (is_wp_error($post_id)) {
        WP_CLI::warning("Failed to save page {$entry['slug']}: " . $post_id->get_error_message());
        continue;
    }

    update_post_meta($post_id, '_elementor_edit_mode', 'builder');
    update_post_meta($post_id, '_elementor_template_type', 'wp-page');
    update_post_meta($post_id, '_elementor_version', $elementor_version);
    update_post_meta($post_id, '_elementor_data', wp_slash(wp_json_encode($tpl['content'])));
    update_post_meta($post_id, '_elementor_page_settings', wp_slash($tpl['page_settings'] ?? []));
    update_post_meta($post_id, '_wp_page_template', 'elementor_canvas');

    if (!empty($entry['front_page'])) {
        $front_page_id = $post_id;
    }

    WP_CLI::log("  {$entry['slug']} -> post #{$post_id}");
}

if ($front_page_id) {
    update_option('show_on_front', 'page');
    update_option('page_on_front', $front_page_id);
    WP_CLI::success("Front page set to post #{$front_page_id}");
} else {
    WP_CLI::warning('No page in manifest.json was marked front_page=true');
}
