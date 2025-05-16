const api=" http://127.0.0.1:8000/createPost"
const a=""
fetch(api)
.then(response => response.json())
.then(meassage=>{
   a =meassage
})

console.log(a)