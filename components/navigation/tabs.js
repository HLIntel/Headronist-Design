/** Accessible native tab controller. Returns cleanup; no dependency. */
export function attachTabs(root) {
  const tabs = [...root.querySelectorAll('[role="tab"]')];
  if (!tabs.length) return () => {};
  const select = (tab, focus = false) => {
    for (const item of tabs) {
      const active = item === tab;
      item.setAttribute('aria-selected', String(active));
      item.tabIndex = active ? 0 : -1;
      const id = item.getAttribute('aria-controls');
      const panel = id && root.querySelector('#' + CSS.escape(id));
      if (panel) panel.hidden = !active;
    }
    if (focus) tab.focus();
  };
  const handlers = tabs.map((tab, index) => {
    const click = () => select(tab);
    const keydown = e => {
      const next = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (next) { e.preventDefault(); select(tabs[(index + next + tabs.length) % tabs.length], true); }
      if (e.key === 'Home') { e.preventDefault(); select(tabs[0], true); }
      if (e.key === 'End') { e.preventDefault(); select(tabs[tabs.length - 1], true); }
    };
    tab.addEventListener('click', click);
    tab.addEventListener('keydown', keydown);
    return () => { tab.removeEventListener('click', click); tab.removeEventListener('keydown', keydown); };
  });
  select(tabs.find(t => t.getAttribute('aria-selected') === 'true') || tabs[0]);
  return () => handlers.forEach(fn => fn());
}
