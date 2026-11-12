(function () {
    function initialize(root) {
        root.querySelectorAll('[data-jsoneditor-options]').forEach(function (container) {
            // The empty form is cloned by Django. Keep it free of editor DOM and handlers.
            if (container.closest('.empty-form') || container.jsonEditor) return;
            var textarea = container.nextElementSibling;
            var data = textarea.nextElementSibling;
            var options = JSON.parse(container.dataset.jsoneditorOptions);
            var editor;
            options.onChange = function () {
                // Preserve empty and invalid text so Django can validate the actual input.
                textarea.value = editor.getText();
            };
            editor = new JSONEditor(container, options);
            textarea.value = data.textContent;
            if (container.dataset.jsoneditorInvalid) {
                textarea.value = JSON.parse(data.textContent);
                editor.setText(textarea.value);
            } else {
                editor.set(JSON.parse(data.textContent));
            }
            container.jsonEditor = editor;
            window[container.id + '_editor'] = editor;
        });
    }

    document.addEventListener('DOMContentLoaded', function () { initialize(document); });
    document.addEventListener('formset:added', function (event) { initialize(event.target); });
    // Wagtail InlinePanel uses its own formset lifecycle events.
    document.addEventListener('w-formset:ready', function (event) { initialize(event.target); });
    document.addEventListener('w-formset:added', function (event) { initialize(event.target); });
    // Django < 4.1 dispatches the formset event through jQuery.
    if (window.django && window.django.jQuery) {
        window.django.jQuery(document).on('formset:added', function (event, row) {
            if (row) initialize(row[0]);
        });
    }
})();
