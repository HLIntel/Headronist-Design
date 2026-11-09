/* Optional progressive enhancement: the unfiltered table works without JS. */
document.querySelectorAll('[data-hd-filter]').forEach((control) => {
  const target = document.getElementById(control.dataset.hdFilter);
  const result = document.getElementById(control.dataset.hdResult);
  if (!target) return;
  const label = control.closest("label");
  if (label) label.hidden = false;
  const rows = Array.from(target.querySelectorAll('[data-hd-status]'));
  const update = () => {
    let visible = 0;
    rows.forEach((row) => {
      row.hidden = control.value !== 'all' && row.dataset.hdStatus !== control.value;
      if (!row.hidden) visible += 1;
    });
    if (result) result.textContent = `${visible} of ${rows.length} activities shown.`;
  };
  control.addEventListener('change', update);
  update();
});
