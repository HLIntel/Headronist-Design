/** Semantic navigation from a validated manifest. No innerHTML or remote dependencies. */
export function renderNavigation(target, config, doc = document) {
  if (!target || !config || !Array.isArray(config.items)) throw new TypeError('Invalid navigation');
  const safe = href => typeof href === 'string' && (/^#[A-Za-z][\w-]*$/.test(href) || /^\.\/[\w./-]+$/.test(href) && !href.includes('..') || /^https:\/\/[^\s]+$/.test(href));
  const makeLink = (label, href) => {
    if (!label || !safe(href)) throw new Error('Invalid navigation destination');
    const a=doc.createElement('a'); a.textContent=label; a.href=href;
    if (href.startsWith('https://')) {a.rel='noopener noreferrer';a.target='_blank';}
    return a;
  };
  const nav=doc.createElement('nav');nav.setAttribute('aria-label','Primary');
  const brand=makeLink(config.brand.label,config.brand.href);brand.className='hd-nav-brand';nav.append(brand);
  const list=doc.createElement('ul');list.className='hd-nav-items';
  for(const item of config.items){const li=doc.createElement('li');li.append(makeLink(item.label,item.href));list.append(li);}
  nav.append(list);
  if(config.action){const a=makeLink(config.action.label,config.action.href);a.className='hd-nav-action';nav.append(a);}
  target.replaceChildren(nav);return nav;
}
