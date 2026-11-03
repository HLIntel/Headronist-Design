/** No fake hrefs; external targets opt into a safe rel. */
export function normalizeLink(value, {external = false} = {}) {
  if (typeof value !== 'string' || !value.trim()) throw new TypeError('Link required');
  const href = value.trim();
  if (/^(javascript|data|vbscript):/i.test(href)) throw new Error('Unsafe URL scheme');
  if (!/^(https?:\/\/|\/[^/]|#|mailto:|tel:)/i.test(href)) throw new Error('Unsupported URL');
  return Object.freeze({href, ...(external ? {target:'_blank',rel:'noopener noreferrer'} : {})});
}
export function normalizeSocial(name, url) {
  const link = normalizeLink(url, {external:true});
  if (!/^https:\/\//i.test(link.href)) throw new Error('Social links require HTTPS');
  return Object.freeze({name:String(name).trim(),...link});
}
