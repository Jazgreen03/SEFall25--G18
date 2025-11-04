export function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  console.log(parts)
  if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
  return null;
}
