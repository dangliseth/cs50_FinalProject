// remove flash messages after 3 seconds.
setTimeout(() => {
    $("div.flashes").fadeOut("slow")
}, 3000)

// handle login modal.
$("#loginForm").on("submit", (event) => {
    // stop form action from running.
    event.preventDefault();

    // get form data.
    const $form = $(event.target); // $(this) can be used if the standard function() is used.
    const url = $form.attr("action");
    const formData = $form.serialize();

    // setup AJAX post.
    $.post(url, formData).done((response) => {
        // login success.
        if (response.success) {
            window.location.href = response.redirect_url;
        }
    })
    .fail(() => {
        // login fail.
        const modalBody = $(".modal-body");

        // create and display the login error alert.
        modalBody.prepend(
            `<div id="error" class="alert alert-danger shadow" role="alert">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-square-fill" viewBox="0 0 16 16">
                    <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2zm6 4c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995A.905.905 0 0 1 8 4m.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2"/>
                </svg>
                Invalid credentials
            </div>`
        );

        // remove login error alert after 3 seconds.
        setTimeout(() => {
            $("div#error").fadeOut("slow")
        }, 3000);
    })
})

$("#logout-btn").hover((event) => {
    const $btn = $(event.target);
    const icon = $btn.find("span.material-symbols-rounded");

    icon.stop(true, true).fadeOut(150, function() {
        $(this).text("directions_run").fadeIn(150);
    });
}, (event) => {
    const $btn = $(event.target);
    const icon = $btn.find("span.material-symbols-rounded");

    icon.stop(true, true).fadeOut(150, function() {
        $(this).text("door_open").fadeIn(150);
    });
});

// Use event delegation on the container to handle events for all select elements,
// including ones that are added dynamically.
$(document).on("change", "select", (event) => {
    // Find the placeholder option within the specific select that was changed and disable it.
    $(event.target).find('option[value=""]').prop("disabled", true);
});