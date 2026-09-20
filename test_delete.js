const fs = require('fs');

let id = 123;
let prods = [{id: 123, name: 'a'}, {id: 456, name: 'b'}];

prods = prods.filter(x => x.id !== id);
console.log(prods);
