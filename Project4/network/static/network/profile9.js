document.addEventListener('DOMContentLoaded', function () {   
    
    followbtn();
    // console.log("hi ffrom profile")
 
    document.querySelector('#fol_posts').onclick = function () {load_fol_posts()}
    
    // console.log("privet")

    document.querySelectorAll('.heart').forEach(post => {

        post.onclick = function() {
            likes(this.dataset.postId);
        }
    })

    document.querySelectorAll('.edit_post').forEach(post => {
        post.onclick = function() {
            
            edit_post(this.dataset.postId);
        }
    })
})

 
function followbtn() {
    let nnn = document.querySelector('.nnn')
    if (!nnn) {
        return
    }
    
    nnn = document.querySelector('.nnn').innerHTML
    console.log(nnn)
    const follow_btn = document.querySelector('#follow_btn');
    const unfollow_btn = document.querySelector('#unfollow_btn');

    if (!follow_btn || !unfollow_btn || !nnn) {
        return
    }
    else {
        unfollow_btn.addEventListener('click', () => 
        {
            console.log('clic unf')
            fetch(`/profile/${nnn}/follow`, {
                method: 'PUT',
                body: JSON.stringify({
                    follow: false
                })
            })
            .then(() => {
                unfollow_btn.style.display = 'none'
                follow_btn.style.display = 'block'
                count()
            })
    });

    follow_btn.addEventListener('click', () => 
        {
            console.log('clic fol')
            fetch(`/profile/${nnn}/follow`, {
                method: 'PUT',                            
                body: JSON.stringify({
                    follow: true
                })
            })
            .then(() => {
                // console.log("srabotalo")
                unfollow_btn.style.display = 'block'
                follow_btn.style.display = 'none'
                count()
    
            })
    });                

    fetch(`is_follow/${nnn}`)
        .then(response => response.json())            
        .then( status => {
            // console.log(status.status)
            const x = status.status
            console.log(x)
            // alert( "Hi, " + x );
            if (x === true) {
                follow_btn.style.display = 'none'
                unfollow_btn.style.display = 'block'                
            } 
            else if (x == false) {
                follow_btn.style.display = 'block'
                unfollow_btn.style.display = 'none'
                console.log("false")
            }
            
        })        
    }    
}

function count() {
    nnn = document.querySelector('.nnn').innerHTML

    fetch(`count/${nnn}`)
    .then(response => response.json())
    .then(data => {
        let followers = data.followers
        let following = data.following
        console.log(document.querySelector('#followers_count'))
        console.log(followers)
        console.log(following)
        
        document.querySelector('#followers_count').innerHTML = `${followers} Followers` 
        document.querySelector('#following_count').innerHTML = `${following} Following` 
    })
}


// ---------------------------- likes ----------------------------------------
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

// -------------------------------- edit -----------------------------------------
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