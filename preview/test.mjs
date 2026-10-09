import assert from "node:assert/strict";
import { readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import vm from "node:vm";

const html = readFileSync("preview/index.html", "utf8");
const script = html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
assert.ok(script, "JavaScript da página deve existir");
new vm.Script(script, { filename: "preview/index.html" });

for (const id of ["quiz","plan","cards","tabs","weekInfo","location","goal","level","days"]) {
  assert.match(html, new RegExp('id="' + id + '"'), "Elemento ausente: " + id);
}
assert.match(html, /name="viewport"/, "Viewport responsiva obrigatória");
assert.match(html, /@media\(max-width:560px\)/, "Layout mobile obrigatório");
assert.match(html, /src="\/gifs\/ex-/, "GIFs locais devem ser utilizados");
assert.match(html, /disabled aria-label="Pagamento em preparação"/, "Cobrança real deve permanecer bloqueada");
assert.doesNotMatch(html, /ASAAS_API_KEY|sk_live_|access_token/, "Não expor credenciais no cliente");

const files = readdirSync("preview/gifs").filter(name => name.endsWith(".gif")).sort();
assert.equal(files.length, 24, "Biblioteca deve conter 24 GIFs");
files.forEach((filename, i) => {
  assert.equal(filename, 'ex-' + String(i+1).padStart(2,'0') + '.gif');
  const path = join("preview/gifs", filename);
  assert.ok(statSync(path).size > 1000, "GIF vazio: " + filename);
  assert.match(readFileSync(path).subarray(0,6).toString(), /^GIF8[79]a$/, "Cabeçalho GIF inválido");
});
console.log("✅ HTML e JavaScript válidos; questionário, UX mobile, checkout desativado e 24 GIFs verificados.");
