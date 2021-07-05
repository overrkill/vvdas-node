const prompt = require("prompt-sync")({sigint:true})


date = prompt("purchased on(dd-mm-yyyy) --")
console.log(date)
console.log(new Date(date).toISOString())