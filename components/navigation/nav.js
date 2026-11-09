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
  for(const item of config.items){
    const li=doc.createElement('li');
    const link=makeLink(item.label,item.href);
    if(item.href.startsWith('#')) link.dataset.section=item.href.slice(1);
    li.append(link);list.append(li);
  }
  nav.append(list);
  if(config.action){const a=makeLink(config.action.label,config.action.href);a.className='hd-nav-action';nav.append(a);}
  target.replaceChildren(nav);
  const sectionLinks=[...nav.querySelectorAll('[data-section]')];
  const setCurrent=id=>sectionLinks.forEach(link=>link.setAttribute('aria-current',String(link.dataset.section===id)));
  const initial=doc.querySelector('main > [id]');
  if(initial) setCurrent(initial.id);
  if(doc.defaultView && 'IntersectionObserver' in doc.defaultView && sectionLinks.length){
    const observer=new doc.defaultView.IntersectionObserver(entries=>{
      const visible=entries.filter(entry=>entry.isIntersecting).sort((a,b)=>b.intersectionRatio-a.intersectionRatio)[0];
      if(visible) setCurrent(visible.target.id);
    },{rootMargin:'-25% 0px -60% 0px',threshold:[0,.25,.5]});
    sectionLinks.forEach(link=>{const section=doc.getElementById(link.dataset.section);if(section) observer.observe(section);});
  }
  return nav;
}
