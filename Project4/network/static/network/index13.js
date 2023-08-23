document.addEventListener('DOMContentLoaded', function () {

    document.querySelector('#compose-post').onsubmit = compose_submit;

    document.querySelector('#fol_posts').onclick = function () {load_fol_posts()}

    document.querySelectorAll('.edit_post').forEach(post => {
        post.onclick = function() {            
            edit_post(this.dataset.postId);
        }
    })

    document.querySelectorAll('.heart').forEach(post => {
        post.onclick = function() {
            likes(this.dataset.postId);
        }
    })
});

// -------------------------------------------- edit -------------------
function edit_post(postid) {    
    text = document.querySelector(`.text-${postid}`)
    content = text.innerHTML
    edit_btn = document.querySelector(`.edit_post-${postid}`)
    text.innerHTML = '';
    edit_btn.style.display = 'none';

    text.innerHTML = `
    <form >
        <div class=''>
        <textarea class='' id='edited_text' name='edit-input' placeholder="Write something">${content}</textarea>
        </div>
        <button type='button' class='btn btn-primary' id='edit-post-form-${postid}'>Save btn</button>
    </form>
    `
    document.querySelector(`#edit-post-form-${postid}`).onclick = () => {
        let edited_post = document.querySelector('#edited_text').value
        fetch(`edited_post/${postid}`, {
            method: 'POST',
            body: JSON.stringify({
                new_post_content: edited_post
            })
        })
        .then(
            text.innerHTML = edited_post
        )
        .then(
            edit_btn.style.display = 'block'
        )            

    }
}


// --------------------------------------------- submit new post ----------------------
function compose_submit() {
    const compose_post = document.querySelector('#post-text').value;
    console.log(document.querySelector('#post-text'))
    console.log(compose_post);
    // console.log("test")
    
    fetch('/new_post', {
        method: 'POST',
        body: JSON.stringify({
            subject: compose_post            
        })
    })
    load_posts();
    document.querySelector('#post-text') = ''
    return false;
}


// -------------------------------------------- likes ------------------
function likes(postid) 
{
    console.log(postid)
    // pi = "" + post_id
    let heart = document.querySelector(`#heart-${postid}`);
    let likesNumber = document.querySelector(`#num-${postid}`);
    console.log(heart)
    console.log(likesNumber)

    // console.log(heart.classList.contains('added'))
    if (heart.classList.contains('added')) 
    {
        fetch(`likes/${postid}`, {
            method: 'POST',                            
            body: JSON.stringify({
                like: false
            })
        })
        .then(() => {
            console.log("srabotalo")

            likesNumber.textContent--;
        })
    }
    else 
    {
        fetch(`likes/${postid}`, {
            method: 'POST',                            
            body: JSON.stringify({
                like: true
            })
        })
        .then(() => {
            console.log("tozhe srabotalo")


            likesNumber.textContent++;
        })
    }
    heart.classList.toggle('added');
}

