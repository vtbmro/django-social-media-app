// Firts lets build an API that return the content of a post 

// Load DOM
document.addEventListener("DOMContentLoaded", function(){

// Get all posts 
    let posts = document.getElementsByClassName("container-fluid border p-3 m-0")

    for(let i = 0; i < posts.length; i++){
        let button = posts[i].querySelector("button")
        
        button.addEventListener("click", function(){
// Replace the text_content with a text area prepopulated with
// the original post content 
            let textarea = document.createElement("textarea");
            let original_post = posts[i].querySelector("span")
            let original_content = posts[i].querySelector("span").innerHTML
            textarea.innerHTML = original_content
            
            original_post.replaceWith(textarea)
            let id = posts[i].id

// Change the editpost button with a new button with an eventlistener

// Add event listener to the button so when it is clicked the changes
// go trough the API and without reloading the page the new content
// gets loaded 

            button.addEventListener("click", function(){
                let save_post = textarea.value
                
// In case user tries to enter an empty post altough the backend 
// already rejects this case
                if (save_post == ""){
                    return alert("Cant input empty post")
                }

                fetch("http://127.0.0.1:8000/profile_page/edit_post", 
                {
                    method: "POST",
                    body: JSON.stringify({
                        post_id: id,
                        content: textarea.value
                    })
                })
                .then(response => response.json())
                .then(json => console.log(json));

// Update the content of the post without a need of reload

                original_post.innerHTML = save_post
                textarea.replaceWith(original_post)
            })
        })
    }
})
