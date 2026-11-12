// Run with: node --test tests/test_inline_editor.js
const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const source = fs.readFileSync('django_json_widget/static/django_json_widget.js', 'utf8');

function setup() {
    const handlers = {};
    const window = {};
    const containers = [];
    const document = {
        addEventListener: (name, handler) => { handlers[name] = handler; },
        querySelectorAll: () => containers,
    };
    function JSONEditor(container, options) {
        this.set = value => { this.text = JSON.stringify(value); };
        this.getText = () => this.text;
        this.edit = text => { this.text = text; options.onChange(); };
    }
    vm.runInNewContext(source, {document, window, JSONEditor});
    function row(id, empty = false, content = 'null') {
        const textarea = {value: '', nextElementSibling: {textContent: content}};
        const container = {
            id, dataset: {jsoneditorOptions: '{"mode":"code"}'},
            closest: () => empty, nextElementSibling: textarea,
        };
        return {container, textarea, querySelectorAll: () => [container]};
    }
    return {handlers, window, containers, row};
}

test('empty inline template is skipped; added rows get distinct editable editors', () => {
    const s = setup();
    const template = s.row('id_detail-__prefix__-data', true);
    const saved = s.row('id_detail-0-data', false, '{"saved":true}');
    s.containers.push(template.container, saved.container);
    s.handlers.DOMContentLoaded();
    assert.equal(template.container.jsonEditor, undefined);
    const added = s.row('id_detail-1-data');
    s.handlers['formset:added']({target: added});
    added.container.jsonEditor.edit('{"new":true}');
    assert.equal(added.textarea.value, '{"new":true}');
    assert.equal(saved.textarea.value, '{"saved":true}');
    assert.equal(s.window['id_detail-1-data_editor'], added.container.jsonEditor);
    const editor = added.container.jsonEditor;
    s.handlers['formset:added']({target: added});
    assert.equal(added.container.jsonEditor, editor);
});

test('clearing and invalid input replace the submitted value instead of keeping stale JSON', () => {
    const s = setup();
    const row = s.row('id_detail-0-data', false, '{"saved":true}');
    s.containers.push(row.container);
    s.handlers.DOMContentLoaded();
    row.container.jsonEditor.edit('');
    assert.equal(row.textarea.value, '');
    row.container.jsonEditor.edit('{');
    assert.equal(row.textarea.value, '{');
});

test('Wagtail inline events initialize saved and added rows only once', () => {
    const s = setup();
    const saved = s.row('id_items-0-data', false, '{"saved":true}');
    s.handlers['w-formset:ready']({target: saved});
    assert.equal(saved.textarea.value, '{"saved":true}');
    const editor = saved.container.jsonEditor;
    s.handlers.DOMContentLoaded();
    s.handlers['w-formset:ready']({target: saved});
    assert.equal(saved.container.jsonEditor, editor);
    const added = s.row('id_items-1-data');
    s.handlers['w-formset:added']({target: added});
    added.container.jsonEditor.edit('{"new":true}');
    assert.equal(added.textarea.value, '{"new":true}');
    assert.equal(saved.textarea.value, '{"saved":true}');
});
