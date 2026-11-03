/** Tiny progressive enhancement; native IntersectionObserver; no animation dependency. */
export function revealOnView(selector='[data-hd-reveal]', root=document) {
  if (!root || typeof root.querySelectorAll!=='function') return ()=>{};
  const nodes=[...root.querySelectorAll(selector)];
  if (!nodes.length || typeof IntersectionObserver==='undefined' || (typeof matchMedia==='function' && matchMedia('(prefers-reduced-motion: reduce)').matches)) return ()=>{};
  const observer=new IntersectionObserver(entries=>{
    for(const entry of entries) if(entry.isIntersecting){
      entry.target.classList.add('hd-revealed');
      observer.unobserve(entry.target);
    }
  },{threshold:0.1});
  nodes.forEach(node=>observer.observe(node));
  return ()=>observer.disconnect();
}
