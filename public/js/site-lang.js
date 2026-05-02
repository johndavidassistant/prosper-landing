// Site-wide language toggle helper.
// Pages that already have their own setLanguage() function should NOT load this.
// For static pages (obrigado*) without their own toggle, this binds the
// EN | PT | ES buttons in the unified header.

(function () {
  function readLang() {
    var q = (window.location.search || '').replace(/^\?/, '');
    var pairs = q.split('&');
    for (var i = 0; i < pairs.length; i++) {
      var kv = pairs[i].split('=');
      if (kv[0] === 'lang') return decodeURIComponent(kv[1] || '');
    }
    return '';
  }

  function applyTranslations(lang) {
    document.documentElement.lang = lang === 'pt' ? 'pt-BR' : (lang === 'es' ? 'es' : 'en');
    document.querySelectorAll('[data-' + lang + ']').forEach(function (el) {
      el.innerHTML = el.getAttribute('data-' + lang);
    });
    document.querySelectorAll('.site-lang-toggle .lang-btn').forEach(function (btn) {
      btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
    });
  }

  function applyPlaceholders(lang) {
    document.querySelectorAll('[data-placeholder-' + lang + ']').forEach(function (el) {
      el.setAttribute('placeholder', el.getAttribute('data-placeholder-' + lang));
    });
  }

  // Allow the page to opt out by setting window.__siteLangManaged = true before this script runs.
  if (window.__siteLangManaged) return;

  var defaultLang = ['en', 'pt', 'es'].indexOf(readLang()) !== -1 ? readLang() : 'pt';
  var current = defaultLang;

  applyTranslations(defaultLang);
  applyPlaceholders(defaultLang);
  document.documentElement.classList.add('lang-ready');

  document.querySelectorAll('.site-lang-toggle .lang-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var lang = this.getAttribute('data-lang');
      if (lang && lang !== current) {
        current = lang;
        applyTranslations(lang);
        applyPlaceholders(lang);
      }
    });
  });

  // Expose a tiny API in case page-specific code wants to react to lang changes.
  window.SiteLang = {
    set: function (lang) {
      if (lang && lang !== current) {
        current = lang;
        applyTranslations(lang);
        applyPlaceholders(lang);
      }
    },
    get: function () { return current; }
  };
})();
