
// For each post in the page add a button to like the post,
// using an API update the number of likes of the post


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

document.addEventListener("DOMContentLoaded", function (){

    let posts = document.getElementsByClassName("container-fluid border p-3 m-0")
    for(let i = 0; i < posts.length; i++){

// Creates a like button for each of the posts

        let like_btn = document.createElement("button");

// Gets the id of each post to make Fetch request

        let id = posts[i].id

// Uses API to add like/unlike text to each button

        fetch(`http://127.0.0.1:8000/check_liked/${id}`)
        .then(response => response.json())
        .then(json => {
            var response = JSON.stringify(json)
            if (response ==  `{"success":"Liked"}`){
                like_btn.innerHTML = "Unlike"
            }else if(response == `{"error":"Not liked"}`){
                like_btn.innerHTML = "Like"
            }
        })

// Add some style and replace on post

        like_btn.classList.add("btn-primary")
        posts[i].append(like_btn)
        
// Likes or unlikes (+1 to like count and add request.user to liked.by)

        like_btn.addEventListener("click", function(){

            fetch("http://127.0.0.1:8000/like", 
                {
                    method: "POST",
                    body: JSON.stringify({
                        post_id: id,
                    })
                })
                .then(response => response.json())
                .then(json => {});

// Update like count
            sleep(100).then(() =>  
            {
                fetch(`http://127.0.0.1:8000/like_count/${id}`)
                .then(response => response.json())
                .then(json => {
                    let number_likes = json.success      
                    let likes = posts[i].getElementsByClassName("like")[0]
                    likes.innerHTML = number_likes
                })
            })
            

// Update like button text
            sleep(100).then(() =>  
            {
                fetch(`http://127.0.0.1:8000/check_liked/${id}`)
                .then(response => response.json())
                .then(json => {
                    var response = JSON.stringify(json)
                    if (response ==  `{"success":"Liked"}`){
                        like_btn.innerHTML = "Unlike"
                    }else if(response == `{"error":"Not liked"}`){
                        like_btn.innerHTML = "Like"
                    }
                }) 
            })


        })       
    }
})