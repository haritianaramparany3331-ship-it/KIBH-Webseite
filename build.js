#!/usr/bin/env node
/**
 * KIBH static site build.
 *
 * Zero dependencies. Reads src/pages/*.html, injects shared partials from
 * src/partials/, writes plain static HTML to dist/. No framework, no runtime
 * JS required for the page to render.
 *
 * Page files declare their own metadata in a leading JSON front-matter block:
 *
 *   <!--{ "title": "...", "description": "...", "url": "/e-rechnung/" }-->
 *
 * Placeholders available in partials and pages:
 *   {{title}} {{description}} {{url}} {{content}} {{nav:<slug>}}
 */

const fs = require("fs");
const path = require("path");

const ROOT = __dirname;
const SRC = path.join(ROOT, "src");
const DIST = path.join(ROOT, "dist");

const read = (p) => fs.readFileSync(p, "utf8");

/**
 * Output path for a page. Driven by the page's declared `url` so that nested
 * routes (/ergebnisse/u2care/) work without mirroring the tree in src/pages.
 * 404 is emitted flat because Vercel serves it by filename.
 */
function outputPath(slug, url) {
  if (slug === "404") return "404.html";
  const clean = String(url || "/").replace(/^\/+|\/+$/g, "");
  return clean ? path.join(clean, "index.html") : "index.html";
}

function loadPartials() {
  const dir = path.join(SRC, "partials");
  return Object.fromEntries(
    fs.readdirSync(dir).map((f) => [path.basename(f, ".html"), read(path.join(dir, f))])
  );
}

function parseFrontMatter(raw) {
  const m = raw.match(/^\s*<!--(\{[\s\S]*?\})-->\s*/);
  if (!m) return [{}, raw];
  return [JSON.parse(m[1]), raw.slice(m[0].length)];
}

/**
 * Mark the current page's nav entry so CSS can style it. Each nav link in the
 * header carries data-nav="<slug>"; we add aria-current + a class to the match.
 */
function markActiveNav(html, slug) {
  return html.replace(new RegExp(`<a\\b[^>]*data-nav="${slug}"[^>]*>`, "g"), (tag) => {
    let out = tag;
    // Merge into any existing class attribute — emitting a second `class` here
    // would be silently ignored by the browser, which keeps only the first.
    if (/\bclass="/.test(out)) {
      out = out.replace(/\bclass="([^"]*)"/, (m, c) => `class="${c} is-active"`);
    } else {
      out = out.replace(/^<a\b/, '<a class="is-active"');
    }
    return out.replace(/^<a\b/, '<a aria-current="page"');
  });
}

function render(template, vars) {
  return template.replace(/\{\{(\w+)\}\}/g, (full, key) =>
    key in vars ? vars[key] : full
  );
}

function build() {
  const partials = loadPartials();
  const pagesDir = path.join(SRC, "pages");
  const pages = fs.readdirSync(pagesDir).filter((f) => f.endsWith(".html"));

  fs.rmSync(DIST, { recursive: true, force: true });
  fs.mkdirSync(DIST, { recursive: true });

  // static assets copied verbatim
  fs.cpSync(path.join(ROOT, "assets"), path.join(DIST, "assets"), { recursive: true });

  const built = [];

  for (const file of pages) {
    const slug = path.basename(file, ".html");
    const [meta, body] = parseFrontMatter(read(path.join(pagesDir, file)));

    const vars = {
      title: meta.title || "KI Beratung Hessen",
      description: meta.description || "",
      url: meta.url || "/",
      bodyClass: meta.bodyClass || "",
    };

    let header = markActiveNav(partials.header, meta.nav || slug);

    const content = render(body, vars);
    let html = render(partials.base, {
      ...vars,
      header,
      footer: partials.footer,
      content,
    });

    // second pass so partials can use page vars too
    html = render(html, vars);

    const out = outputPath(slug, meta.url);
    const dest = path.join(DIST, out);
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.writeFileSync(dest, html);
    built.push(out.replace(/\\/g, "/"));
  }

  console.log(`Built ${built.length} pages:`);
  for (const b of built.sort()) console.log(`  dist/${b}`);
}

build();
