import assert from "node:assert/strict";
import { createHash } from "node:crypto";
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
assert.match(html, /object-fit:contain/, "GIF não deve ser cortado no celular");
assert.match(html, /\.gif\?v=3/, "A prévia deve renovar o cache dos GIFs");
assert.match(html, /GIF animado/, "Indicador visual da animação obrigatório");
const uniqueGifs=new Set();
for (const filename of files) {
  const gif=readFileSync(join("preview/gifs",filename));
  uniqueGifs.add(createHash("sha256").update(gif).digest("hex"));
  const width=gif.readUInt16LE(6), height=gif.readUInt16LE(8);
  assert.ok(width>=300 && height>=200, "Animação muito pequena: "+filename);
  const graphicControlExtensions=gif.toString("latin1").match(/\x21\xf9\x04/g) || [];
  assert.ok(graphicControlExtensions.length>=12, "GIF não possui quadros animados suficientes: "+filename);
}
assert.equal(uniqueGifs.size,24,"Cada exercício deve ter seu próprio GIF");

console.log("✅ HTML e JavaScript válidos; questionário, UX mobile, checkout desativado e 24 GIFs verificados.");
