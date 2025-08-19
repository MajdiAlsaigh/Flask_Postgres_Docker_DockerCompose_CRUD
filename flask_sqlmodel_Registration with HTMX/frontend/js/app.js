import 'htmx.org';
import htmx from "htmx.org";

// Wait for DOM and enhance HTMX dynamically-loaded content
document.addEventListener('DOMContentLoaded', function () {
    if (typeof htmx !== 'undefined') {
        console.log('[HTMX] Loaded ✅ Version:', htmx.version);
    } else {
        console.error('[HTMX] Failed to load!');
    }
});

// Re-process new content after HTMX swaps (critical!)
document.addEventListener('htmx:afterSwap', function (evt) {
    if (evt.detail.target.id === 'main-block') {
        htmx.process(evt.detail.target);
    }
});
