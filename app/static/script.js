// remove flash messages after 3 seconds.
setTimeout(() => {
    $("div.flashes").fadeOut("slow")
}, 3000)

// handle login modal.
$("#loginForm").on("submit", (event) => {
    // stop form action from running.
    event.preventDefault();

    // get form data.
    const $form = $(event.target);
    const url = $form.attr("action");
    const formData = $form.serialize();

    // setup AJAX post.
    $.post(url, formData).done((response) => {
        if (response.success) {
            window.location.href = response.redirect_url;
        }
    })
    .fail(() => {
        modalBody = $(".modal-body");

        modalBody.prepend('<div id="loginError" class="alert alert-warning shadow" role="alert">Invalid credentials</div>')

        setTimeout(() => {
            $("div#loginError").fadeOut("slow")
        }, 3000)
    })
})