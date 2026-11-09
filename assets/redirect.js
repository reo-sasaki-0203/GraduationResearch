'use strict';
const destination = document.querySelector('meta[name="research-redirect"]');
if (destination) {
  const target = new URL(destination.content, document.baseURI);
  if (location.hash) target.hash = location.hash;
  location.replace(target.href);
}
